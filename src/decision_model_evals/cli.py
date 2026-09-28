from __future__ import annotations

from pathlib import Path
import argparse
import json
import os
import sys

from decision_model_evals.comparison import compare_runs
from decision_model_evals.config import load_models
from decision_model_evals.reporting import write_report
from decision_model_evals.runner import load_suite_ids, run_benchmark, select_cases
from decision_model_evals.schema import load_corpus


def _root() -> Path:
    return Path(__file__).resolve().parents[2]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="decision-evals")
    parser.add_argument("--root", type=Path, default=_root())
    sub = parser.add_subparsers(dest="command", required=True)

    validate = sub.add_parser("validate", help="validate corpus and suites")
    validate.add_argument("--corpus", default="datasets/corpus.jsonl")

    info = sub.add_parser("suite-info", help="show suite composition")
    info.add_argument("suite")

    models = sub.add_parser("list-models", help="show configured models")
    models.add_argument("--config", default="configs/models.yaml")

    run = sub.add_parser("run", help="run a benchmark suite")
    run.add_argument("--model", required=True)
    run.add_argument("--suite", default="smoke")
    run.add_argument("--config", default="configs/models.yaml")
    run.add_argument("--corpus", default="datasets/corpus.jsonl")
    run.add_argument("--output", default="results")
    run.add_argument("--concurrency", type=int, default=1)
    run.add_argument("--retries", type=int, default=2)
    run.add_argument("--retry-backoff", type=float, default=1.0)
    run.add_argument("--timeout", type=float, default=120.0)
    run.add_argument("--local-usd-per-hour", type=float)
    run.add_argument(
        "--allow-errors",
        action="store_true",
        help="return success even when one or more benchmark cases fail at the provider/transport layer",
    )

    report = sub.add_parser("report", help="regenerate report.md from a run")
    report.add_argument("run_dir", type=Path)

    compare = sub.add_parser("compare", help="compare two or more compatible run directories")
    compare.add_argument("run_dirs", type=Path, nargs="+")
    compare.add_argument("--output", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = args.root.resolve()
    if args.command == "validate":
        return _validate(root, args.corpus)
    if args.command == "suite-info":
        return _suite_info(root, args.suite)
    if args.command == "list-models":
        return _list_models(root, args.config)
    if args.command == "run":
        return _run(root, args)
    if args.command == "report":
        print(write_report(args.run_dir.resolve()))
        return 0
    if args.command == "compare":
        text = compare_runs([p.resolve() for p in args.run_dirs])
        if args.output:
            args.output.write_text(text, encoding="utf-8")
            print(args.output)
        else:
            print(text)
        return 0
    raise AssertionError(args.command)


def _validate(root: Path, corpus_rel: str) -> int:
    corpus_path = root / corpus_rel
    cases = load_corpus(corpus_path)
    by_id = {c.id for c in cases}
    domains = sorted({c.domain for c in cases})
    primitive_counts = {p: sum(c.primitive == p for c in cases) for p in ("choice", "noul", "score")}
    print(f"corpus: {len(cases)} cases; domains={len(domains)}; primitives={primitive_counts}")
    for suite_path in sorted((root / "datasets" / "suites").glob("*.yaml")):
        ids = load_suite_ids(suite_path)
        missing = [x for x in ids if x not in by_id]
        if missing:
            raise ValueError(f"{suite_path}: missing cases {missing[:5]}")
        print(f"suite {suite_path.stem}: {len(ids)} cases")
    return 0


def _suite_info(root: Path, suite: str) -> int:
    cases = load_corpus(root / "datasets" / "corpus.jsonl")
    suite_path = _suite_path(root, suite)
    selected = select_cases(cases, load_suite_ids(suite_path))
    counts: dict[str, dict[str, int]] = {}
    for case in selected:
        counts.setdefault(case.domain, {}).setdefault(case.primitive, 0)
        counts[case.domain][case.primitive] += 1
    print(json.dumps({"suite": suite_path.stem, "n": len(selected), "domains": counts}, indent=2, sort_keys=True))
    return 0


def _list_models(root: Path, config_rel: str) -> int:
    models = load_models(root / config_rel)
    for name, model in models.items():
        print(f"{name:12} {model.deployment:7} {model.provider:22} {model.description}")
    return 0


def _run(root: Path, args) -> int:
    _load_dotenv(root / ".env")
    corpus_path = root / args.corpus
    suite_path = _suite_path(root, args.suite)
    models = load_models(root / args.config)
    if args.model not in models:
        raise SystemExit(f"unknown model {args.model!r}; choose from: {', '.join(models)}")
    cases = select_cases(load_corpus(corpus_path), load_suite_ids(suite_path))
    local_rate = args.local_usd_per_hour
    if local_rate is None and os.getenv("LOCAL_COMPUTE_USD_PER_HOUR"):
        local_rate = float(os.environ["LOCAL_COMPUTE_USD_PER_HOUR"])
    run_dir = run_benchmark(
        repo_root=root,
        model_config=models[args.model],
        cases=cases,
        corpus_path=corpus_path,
        suite_path=suite_path,
        output_root=root / args.output,
        concurrency=args.concurrency,
        retries=args.retries,
        retry_backoff_s=args.retry_backoff,
        timeout_s=args.timeout,
        local_usd_per_hour=local_rate,
    )
    report = write_report(run_dir)
    print(report)
    summary = json.loads((run_dir / "summary.json").read_text(encoding="utf-8"))
    errors = int(summary.get("counts", {}).get("errors", 0))
    if errors and not args.allow_errors:
        print(
            f"error: benchmark completed with {errors} provider/transport error(s); see {report}",
            file=sys.stderr,
        )
        return 1
    return 0


def _suite_path(root: Path, suite: str) -> Path:
    candidate = Path(suite)
    if candidate.suffix:
        return candidate if candidate.is_absolute() else root / candidate
    return root / "datasets" / "suites" / f"{suite}.yaml"


def _load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


if __name__ == "__main__":
    sys.exit(main())

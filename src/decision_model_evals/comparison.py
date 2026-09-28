from __future__ import annotations

from itertools import combinations
from math import comb
from pathlib import Path
from typing import Any
import json


def compare_runs(run_dirs: list[Path]) -> str:
    if len(run_dirs) < 2:
        raise ValueError("compare requires at least two run directories")
    loaded = [_load_run(path) for path in run_dirs]
    _assert_comparable(loaded)

    lines = [
        "# Decision model comparison",
        "",
        f"Suite: `{loaded[0]['summary'].get('suite')}`",
        f"Corpus SHA-256: `{loaded[0]['manifest']['corpus']['sha256']}`",
        "",
        "## Overall",
        "",
        "| Model | Valid / total | Accuracy | 95% CI | p50 ms | p95 ms | Provider $/1M decisions | Errors |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for item in loaded:
        summary = item["summary"]
        overall = summary["groups"]["overall"]
        counts = summary["counts"]
        ci = overall.get("accuracy_ci95") or [None, None]
        lines.append(
            "| {model} | {valid}/{total} | {acc} | {ci} | {p50} | {p95} | {cost} | {errors} |".format(
                model=summary.get("model"),
                valid=counts["valid"],
                total=counts["total"],
                acc=_pct(overall.get("accuracy")),
                ci=f"{_pct(ci[0])}–{_pct(ci[1])}",
                p50=_num(_nested(overall, "latency_ms", "p50")),
                p95=_num(_nested(overall, "latency_ms", "p95")),
                cost=_usd(overall.get("provider_cost_per_1m_usd")),
                errors=counts["errors"],
            )
        )

    lines.extend([
        "",
        "## Primitive quality",
        "",
        "| Model | Choice acc | Choice Brier | Noul acc | Noul Brier | Score exact | Score MAE |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ])
    for item in loaded:
        summary = item["summary"]
        c = summary["groups"].get("primitive:choice", {})
        n = summary["groups"].get("primitive:noul", {})
        s = summary["groups"].get("primitive:score", {})
        lines.append(
            f"| {summary.get('model')} | {_pct(c.get('accuracy'))} | {_num(c.get('brier'))} | "
            f"{_pct(n.get('accuracy'))} | {_num(n.get('brier'))} | "
            f"{_pct(s.get('exact_accuracy'))} | {_num(s.get('mae_expected_score'))} |"
        )

    lines.extend([
        "",
        "## Paired correctness comparisons",
        "",
        "McNemar's exact two-sided test is calculated only on cases where both runs returned a valid result. It tests whether the two models have symmetric win/loss disagreements; it is not a measure of effect size.",
        "",
        "| Model A | Model B | Paired n | A-only correct | B-only correct | Accuracy delta A−B | Exact p |",
        "|---|---|---:|---:|---:|---:|---:|",
    ])
    for a, b in combinations(loaded, 2):
        pair = _paired(a, b)
        lines.append(
            f"| {a['summary'].get('model')} | {b['summary'].get('model')} | {pair['n']} | "
            f"{pair['a_only']} | {pair['b_only']} | {pair['delta'] * 100:+.2f} pp | {pair['p']:.6f} |"
        )

    lines.extend([
        "",
        "## Notes",
        "",
        "Do not infer a universal winner from this table. The comparison is conditional on the frozen suite, hardware/runtime configuration, and provider conditions recorded in each run manifest. Quality, calibration, latency, and cost remain separate axes.",
        "",
    ])
    return "\n".join(lines)


def _load_run(path: Path) -> dict[str, Any]:
    path = path.resolve()
    summary = json.loads((path / "summary.json").read_text(encoding="utf-8"))
    manifest = json.loads((path / "manifest.json").read_text(encoding="utf-8"))
    rows: dict[str, dict[str, Any]] = {}
    with (path / "results.jsonl").open("r", encoding="utf-8") as handle:
        for line in handle:
            row = json.loads(line)
            rows[row["case_id"]] = row
    return {"path": path, "summary": summary, "manifest": manifest, "rows": rows}


def _assert_comparable(items: list[dict[str, Any]]) -> None:
    corpus = {item["manifest"]["corpus"]["sha256"] for item in items}
    suite = {item["manifest"]["suite"]["sha256"] for item in items}
    if len(corpus) != 1 or len(suite) != 1:
        raise ValueError("runs are not directly comparable: corpus or suite hashes differ")


def _paired(a: dict[str, Any], b: dict[str, Any]) -> dict[str, Any]:
    common = sorted(set(a["rows"]) & set(b["rows"]))
    valid = [
        case_id
        for case_id in common
        if a["rows"][case_id].get("status") == "ok" and b["rows"][case_id].get("status") == "ok"
    ]
    a_only = sum(bool(a["rows"][i]["correct"]) and not bool(b["rows"][i]["correct"]) for i in valid)
    b_only = sum(bool(b["rows"][i]["correct"]) and not bool(a["rows"][i]["correct"]) for i in valid)
    a_acc = sum(bool(a["rows"][i]["correct"]) for i in valid) / len(valid) if valid else 0.0
    b_acc = sum(bool(b["rows"][i]["correct"]) for i in valid) / len(valid) if valid else 0.0
    return {
        "n": len(valid),
        "a_only": a_only,
        "b_only": b_only,
        "delta": a_acc - b_acc,
        "p": _mcnemar_exact(a_only, b_only),
    }


def _mcnemar_exact(a_only: int, b_only: int) -> float:
    n = a_only + b_only
    if n == 0:
        return 1.0
    k = min(a_only, b_only)
    tail = sum(comb(n, i) for i in range(k + 1)) / (2**n)
    return min(1.0, 2.0 * tail)


def _nested(value: dict[str, Any], *keys: str):
    current: Any = value
    for key in keys:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


def _pct(value: Any) -> str:
    return "—" if value is None else f"{float(value) * 100:.2f}%"


def _num(value: Any) -> str:
    return "—" if value is None else f"{float(value):.3f}"


def _usd(value: Any) -> str:
    return "—" if value is None else f"${float(value):.4f}"

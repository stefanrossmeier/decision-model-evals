from types import SimpleNamespace
import json

from decision_model_evals import cli


def test_run_returns_nonzero_when_provider_cases_failed(tmp_path, monkeypatch) -> None:
    root = tmp_path
    (root / "datasets" / "suites").mkdir(parents=True)
    (root / "datasets" / "corpus.jsonl").write_text(
        '{"id":"c","primitive":"noul","domain":"d","task":"t","state":"s","instructions":"q","criteria":{"true":"yes","false":"no"},"gold":{"noul":true}}\n',
        encoding="utf-8",
    )
    (root / "datasets" / "suites" / "probe.yaml").write_text("case_ids:\n  - c\n", encoding="utf-8")
    (root / "configs").mkdir()
    (root / "configs" / "models.yaml").write_text(
        "models:\n  m:\n    provider: systemone_http\n    endpoint: http://127.0.0.1:1/v1/systemone\n    deployment: local\n    description: test\n",
        encoding="utf-8",
    )

    run_dir = root / "results" / "r"
    run_dir.mkdir(parents=True)
    (run_dir / "summary.json").write_text(json.dumps({"counts": {"errors": 1}}), encoding="utf-8")

    monkeypatch.setattr(cli, "run_benchmark", lambda **kwargs: run_dir)
    monkeypatch.setattr(cli, "write_report", lambda path: path / "report.md")

    args = SimpleNamespace(
        corpus="datasets/corpus.jsonl",
        suite="probe",
        config="configs/models.yaml",
        model="m",
        local_usd_per_hour=None,
        output="results",
        concurrency=1,
        retries=0,
        retry_backoff=0.0,
        timeout=1.0,
        allow_errors=False,
    )
    assert cli._run(root, args) == 1
    args.allow_errors = True
    assert cli._run(root, args) == 0

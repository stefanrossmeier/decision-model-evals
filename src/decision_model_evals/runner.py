from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter, sleep
from typing import Any
import hashlib
import json
import platform
import subprocess
import uuid
import yaml

from decision_model_evals.config import ModelConfig
from decision_model_evals.metrics import summarize
from decision_model_evals.providers import create_provider
from decision_model_evals.schema import Case


def load_suite_ids(path: Path) -> list[str]:
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    ids = raw.get("case_ids") or []
    if not isinstance(ids, list) or not ids:
        raise ValueError(f"suite has no case_ids: {path}")
    if len(ids) != len(set(ids)):
        raise ValueError(f"suite has duplicate case ids: {path}")
    return [str(x) for x in ids]


def select_cases(cases: list[Case], suite_ids: list[str]) -> list[Case]:
    by_id = {c.id: c for c in cases}
    missing = [case_id for case_id in suite_ids if case_id not in by_id]
    if missing:
        raise ValueError(f"suite references missing cases: {missing[:10]}")
    return [by_id[case_id] for case_id in suite_ids]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_revision(root: Path) -> str | None:
    try:
        return subprocess.check_output(
            ["git", "-C", str(root), "rev-parse", "HEAD"],
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def hardware_snapshot() -> dict[str, Any]:
    out: dict[str, Any] = {
        "platform": platform.platform(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "python": platform.python_version(),
    }
    try:
        result = subprocess.check_output(
            [
                "nvidia-smi",
                "--query-gpu=name,memory.total,driver_version",
                "--format=csv,noheader",
            ],
            stderr=subprocess.DEVNULL,
            text=True,
            timeout=5,
        ).strip()
        if result:
            out["nvidia_smi"] = result.splitlines()
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
        pass
    return out


def run_benchmark(
    *,
    repo_root: Path,
    model_config: ModelConfig,
    cases: list[Case],
    corpus_path: Path,
    suite_path: Path,
    output_root: Path,
    concurrency: int = 1,
    retries: int = 2,
    retry_backoff_s: float = 1.0,
    timeout_s: float = 120.0,
    local_usd_per_hour: float | None = None,
) -> Path:
    if concurrency < 1:
        raise ValueError("concurrency must be >= 1")
    run_id = f"{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-{model_config.name}-{uuid.uuid4().hex[:8]}"
    out_dir = output_root / run_id
    out_dir.mkdir(parents=True, exist_ok=False)

    started = datetime.now(timezone.utc)
    suite_perf_started = perf_counter()
    manifest = {
        "run_id": run_id,
        "started_at": started.isoformat(),
        "benchmark_revision": git_revision(repo_root),
        "corpus": {
            "path": str(corpus_path.relative_to(repo_root)),
            "sha256": sha256_file(corpus_path),
            "case_count": len(cases),
        },
        "suite": {
            "path": str(suite_path.relative_to(repo_root)),
            "sha256": sha256_file(suite_path),
        },
        "model_config": asdict(model_config),
        "execution": {
            "concurrency": concurrency,
            "retries": retries,
            "retry_backoff_s": retry_backoff_s,
            "timeout_s": timeout_s,
            "local_usd_per_hour": local_usd_per_hour,
        },
        "hardware": hardware_snapshot(),
    }
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    provider = create_provider(model_config, timeout_s=timeout_s)
    try:
        if concurrency == 1:
            rows = [
                _run_one(provider, model_config, case, retries, retry_backoff_s, local_usd_per_hour)
                for case in cases
            ]
        else:
            rows_by_index: dict[int, dict[str, Any]] = {}
            with ThreadPoolExecutor(max_workers=concurrency) as pool:
                futures = {
                    pool.submit(
                        _run_one,
                        provider,
                        model_config,
                        case,
                        retries,
                        retry_backoff_s,
                        local_usd_per_hour,
                    ): idx
                    for idx, case in enumerate(cases)
                }
                for future in as_completed(futures):
                    rows_by_index[futures[future]] = future.result()
            rows = [rows_by_index[i] for i in range(len(cases))]
    finally:
        provider.close()

    suite_wall_seconds = perf_counter() - suite_perf_started
    _write_jsonl(out_dir / "results.jsonl", rows)
    summary = summarize(rows)
    summary["run_id"] = run_id
    summary["model"] = model_config.name
    summary["suite"] = suite_path.stem
    summary["wall_clock_started_at"] = started.isoformat()
    summary["wall_clock_finished_at"] = datetime.now(timezone.utc).isoformat()
    summary["wall_clock_seconds"] = suite_wall_seconds
    summary["throughput_requests_per_second"] = len(cases) / suite_wall_seconds if suite_wall_seconds else None
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return out_dir


def _run_one(
    provider,
    model_config: ModelConfig,
    case: Case,
    retries: int,
    retry_backoff_s: float,
    local_usd_per_hour: float | None,
) -> dict[str, Any]:
    started = perf_counter()
    last_error: Exception | None = None
    attempts = 0
    request_elapsed_ms_total = 0.0
    for attempt in range(retries + 1):
        attempts = attempt + 1
        call_started = perf_counter()
        try:
            result = provider.decide(case)
            timing_ms = (perf_counter() - call_started) * 1000.0
            request_elapsed_ms_total += timing_ms
            row = _success_row(case, result, timing_ms, attempts)
            row["request_elapsed_ms_total"] = request_elapsed_ms_total
            if model_config.deployment == "local" and local_usd_per_hour is not None:
                row["estimated_local_cost_usd"] = local_usd_per_hour * request_elapsed_ms_total / 3_600_000.0
            else:
                row["estimated_local_cost_usd"] = None
            row["total_elapsed_ms"] = (perf_counter() - started) * 1000.0
            return row
        except Exception as exc:  # noqa: BLE001 - benchmark must record provider failures
            request_elapsed_ms_total += (perf_counter() - call_started) * 1000.0
            last_error = exc
            if attempt < retries:
                sleep(retry_backoff_s * (2**attempt))

    return {
        "case_id": case.id,
        "primitive": case.primitive,
        "domain": case.domain,
        "task": case.task,
        "status": "error",
        "error": f"{type(last_error).__name__}: {last_error}",
        "attempts": attempts,
        "timing_ms": None,
        "total_elapsed_ms": (perf_counter() - started) * 1000.0,
        "request_elapsed_ms_total": request_elapsed_ms_total,
        "provider_cost_usd": None,
        "estimated_local_cost_usd": None,
    }


def _success_row(case: Case, result, timing_ms: float, attempts: int) -> dict[str, Any]:
    gold: str | bool | int
    correct: bool | None
    if case.primitive == "choice":
        gold = str(case.gold.choice)
        correct = str(result.prediction) == gold
    elif case.primitive == "noul":
        gold = bool(case.gold.noul)
        correct = bool(result.prediction) == gold
    else:
        gold = int(case.gold.score)
        if result.probabilities:
            pred_class = int(max(result.probabilities, key=result.probabilities.get))
        else:
            pred_class = int(round(float(result.prediction)))
        correct = pred_class == gold

    return {
        "case_id": case.id,
        "primitive": case.primitive,
        "domain": case.domain,
        "task": case.task,
        "status": "ok",
        "gold": gold,
        "prediction": result.prediction,
        "correct": correct,
        "probabilities": result.probabilities,
        "probability_yes": result.probability_yes,
        "score_levels": len(case.criteria) if case.primitive == "score" and isinstance(case.criteria, list) else None,
        "timing_ms": timing_ms,
        "attempts": attempts,
        "resolved_model": result.model,
        "resolved_provider": result.provider,
        "input_tokens": result.input_tokens,
        "output_tokens": result.output_tokens,
        "provider_cost_usd": result.provider_cost_usd or 0.0,
        "provider_latency_ms": result.provider_latency_ms,
        "raw_response": result.raw,
    }


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True, ensure_ascii=False) + "\n")

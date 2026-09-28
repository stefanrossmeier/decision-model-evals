from __future__ import annotations

from pathlib import Path
from typing import Any
import json


def render_report(summary: dict[str, Any]) -> str:
    overall = summary["groups"].get("overall", {})
    counts = summary["counts"]
    lines = [
        f"# Benchmark report: {summary.get('model', 'unknown')}",
        "",
        f"- Run: `{summary.get('run_id', '')}`",
        f"- Suite: `{summary.get('suite', '')}`",
        f"- Cases: {counts['total']} ({counts['valid']} valid, {counts['errors']} errors)",
        f"- Accuracy: {_pct(overall.get('accuracy'))}",
        f"- Provider cost: {_usd(overall.get('provider_cost_usd'))}",
        f"- Provider cost / 1M decisions at this case mix: {_usd(overall.get('provider_cost_per_1m_usd'))}",
        f"- Estimated local compute cost: {_usd(overall.get('estimated_local_cost_usd'))}",
        f"- p50 / p95 latency: {_num(_nested(overall, 'latency_ms', 'p50'))} / {_num(_nested(overall, 'latency_ms', 'p95'))} ms",
        f"- Suite throughput: {_num(summary.get('throughput_requests_per_second'))} requests/s",
        "",
        "## Primitive results",
        "",
        "| Primitive | n | Accuracy | Macro F1 | Brier | NLL | ECE-10 | p50 ms | p95 ms | Provider cost |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for primitive in ("choice", "noul", "score"):
        group = summary["groups"].get(f"primitive:{primitive}", {})
        lines.append(
            "| {p} | {n} | {acc} | {f1} | {brier} | {nll} | {ece} | {p50} | {p95} | {cost} |".format(
                p=primitive,
                n=group.get("n", 0),
                acc=_pct(group.get("accuracy")),
                f1=_num(group.get("macro_f1")),
                brier=_num(group.get("brier")),
                nll=_num(group.get("nll")),
                ece=_num(group.get("ece_10")),
                p50=_num(_nested(group, "latency_ms", "p50")),
                p95=_num(_nested(group, "latency_ms", "p95")),
                cost=_usd(group.get("provider_cost_usd")),
            )
        )
    lines.extend([
        "",
        "## Domains",
        "",
        "| Domain | n | Accuracy | p50 ms | Provider cost |",
        "|---|---:|---:|---:|---:|",
    ])
    for name, group in sorted(summary["groups"].items()):
        if not name.startswith("domain:"):
            continue
        lines.append(
            f"| {name.split(':', 1)[1]} | {group.get('n', 0)} | {_pct(group.get('accuracy'))} | "
            f"{_num(_nested(group, 'latency_ms', 'p50'))} | {_usd(group.get('provider_cost_usd'))} |"
        )
    score = summary["groups"].get("primitive:score", {})
    if score:
        lines.extend([
            "",
            "## Score-specific metrics",
            "",
            f"- Exact accuracy: {_pct(score.get('exact_accuracy'))}",
            f"- Within ±1 accuracy: {_pct(score.get('within_1_accuracy'))}",
            f"- MAE of expected score: {_num(score.get('mae_expected_score'))}",
            f"- Quadratic weighted kappa: {_num(score.get('quadratic_weighted_kappa'))}",
        ])
    lines.extend([
        "",
        "## Interpretation notes",
        "",
        "Accuracy and calibration are reported separately from latency and cost. The project intentionally does not collapse them into a single winner score. Provider cost is the billed/request-reported amount when available; local models have zero provider cost. Estimated local compute cost is only populated when a machine-hour price was explicitly supplied for the run.",
        "",
    ])
    return "\n".join(lines)


def write_report(run_dir: Path) -> Path:
    summary = json.loads((run_dir / "summary.json").read_text(encoding="utf-8"))
    path = run_dir / "report.md"
    path.write_text(render_report(summary), encoding="utf-8")
    return path


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
    return "—" if value is None else f"{float(value):.4f}"


def _usd(value: Any) -> str:
    return "—" if value is None else f"${float(value):.6f}"

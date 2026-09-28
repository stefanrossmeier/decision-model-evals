from __future__ import annotations

from collections import Counter, defaultdict
from math import log, sqrt
from statistics import mean, median
from typing import Any

EPS = 1e-12


def _quantile(values: list[float], q: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    pos = (len(ordered) - 1) * q
    lo = int(pos)
    hi = min(lo + 1, len(ordered) - 1)
    frac = pos - lo
    return ordered[lo] * (1 - frac) + ordered[hi] * frac


def _ece(conf_correct: list[tuple[float, bool]], bins: int = 10) -> float | None:
    if not conf_correct:
        return None
    total = len(conf_correct)
    error = 0.0
    for idx in range(bins):
        low, high = idx / bins, (idx + 1) / bins
        members = [x for x in conf_correct if low <= x[0] < high or (idx == bins - 1 and x[0] == 1.0)]
        if not members:
            continue
        avg_conf = mean(x[0] for x in members)
        avg_acc = mean(1.0 if x[1] else 0.0 for x in members)
        error += len(members) / total * abs(avg_conf - avg_acc)
    return error


def _wilson(successes: int, total: int, z: float = 1.959963984540054) -> list[float] | None:
    if total <= 0:
        return None
    phat = successes / total
    denom = 1.0 + z * z / total
    center = (phat + z * z / (2.0 * total)) / denom
    half = z * sqrt(phat * (1.0 - phat) / total + z * z / (4.0 * total * total)) / denom
    return [max(0.0, center - half), min(1.0, center + half)]


def _macro_f1(golds: list[str], preds: list[str]) -> float | None:
    labels = sorted(set(golds) | set(preds))
    if not labels:
        return None
    f1s = []
    for label in labels:
        tp = sum(g == label and p == label for g, p in zip(golds, preds, strict=True))
        fp = sum(g != label and p == label for g, p in zip(golds, preds, strict=True))
        fn = sum(g == label and p != label for g, p in zip(golds, preds, strict=True))
        precision = tp / (tp + fp) if tp + fp else 0.0
        recall = tp / (tp + fn) if tp + fn else 0.0
        f1s.append(2 * precision * recall / (precision + recall) if precision + recall else 0.0)
    return mean(f1s)


def _quadratic_weighted_kappa(golds: list[int], preds: list[int], levels: int) -> float | None:
    if not golds or len(golds) != len(preds) or levels < 2:
        return None
    n = len(golds)
    observed = [[0.0] * levels for _ in range(levels)]
    g_hist = Counter(golds)
    p_hist = Counter(preds)
    for g, p in zip(golds, preds, strict=True):
        observed[g][p] += 1.0
    expected = [[g_hist[i] * p_hist[j] / n for j in range(levels)] for i in range(levels)]
    denom_scale = float((levels - 1) ** 2)
    obs_w = exp_w = 0.0
    for i in range(levels):
        for j in range(levels):
            weight = ((i - j) ** 2) / denom_scale
            obs_w += weight * observed[i][j]
            exp_w += weight * expected[i][j]
    return 1.0 - obs_w / exp_w if exp_w > 0 else None


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    valid = [r for r in rows if r.get("status") == "ok"]
    errors = [r for r in rows if r.get("status") != "ok"]
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    groups["overall"] = valid
    for row in valid:
        groups[f"primitive:{row['primitive']}"] .append(row)
        groups[f"domain:{row['domain']}"] .append(row)

    return {
        "counts": {
            "total": len(rows),
            "valid": len(valid),
            "errors": len(errors),
            "error_rate": len(errors) / len(rows) if rows else 0.0,
        },
        "groups": {name: summarize_group(items) for name, items in sorted(groups.items())},
        "errors": [
            {"case_id": r.get("case_id"), "error": r.get("error"), "attempts": r.get("attempts")}
            for r in errors[:100]
        ],
    }


def summarize_group(rows: list[dict[str, Any]]) -> dict[str, Any]:
    if not rows:
        return {"n": 0}
    correctness = [bool(r.get("correct")) for r in rows if r.get("correct") is not None]
    timing = [float(r["timing_ms"]) for r in rows if r.get("timing_ms") is not None]
    costs = [float(r.get("provider_cost_usd") or 0.0) for r in rows]
    cost_bases = sorted({str(r["provider_cost_basis"]) for r in rows if r.get("provider_cost_basis")})
    local_costs = [float(r.get("estimated_local_cost_usd") or 0.0) for r in rows]
    input_tokens = [int(r["input_tokens"]) for r in rows if r.get("input_tokens") is not None]
    output_tokens = [int(r["output_tokens"]) for r in rows if r.get("output_tokens") is not None]
    cached_input_tokens = [
        int(r["cached_input_tokens"]) for r in rows if r.get("cached_input_tokens") is not None
    ]
    cache_write_tokens = [
        int(r["cache_write_tokens"]) for r in rows if r.get("cache_write_tokens") is not None
    ]
    reasoning_tokens = [
        int(r["reasoning_tokens"]) for r in rows if r.get("reasoning_tokens") is not None
    ]

    total_provider_cost = sum(costs)
    out: dict[str, Any] = {
        "n": len(rows),
        "accuracy": mean(correctness) if correctness else None,
        "accuracy_ci95": _wilson(sum(correctness), len(correctness)) if correctness else None,
        "provider_cost_usd": total_provider_cost,
        "provider_cost_basis": cost_bases[0] if len(cost_bases) == 1 else (cost_bases or None),
        "estimated_local_cost_usd": sum(local_costs),
        "mean_provider_cost_usd": mean(costs) if costs else None,
        "provider_cost_per_1000_usd": total_provider_cost * 1000.0 / len(rows),
        "provider_cost_per_1m_usd": total_provider_cost * 1_000_000.0 / len(rows),
        "input_tokens": sum(input_tokens) if input_tokens else None,
        "output_tokens": sum(output_tokens) if output_tokens else None,
        "cached_input_tokens": sum(cached_input_tokens) if cached_input_tokens else None,
        "cache_write_tokens": sum(cache_write_tokens) if cache_write_tokens else None,
        "reasoning_tokens": sum(reasoning_tokens) if reasoning_tokens else None,
        "latency_ms": {
            "mean": mean(timing) if timing else None,
            "p50": median(timing) if timing else None,
            "p90": _quantile(timing, 0.90),
            "p95": _quantile(timing, 0.95),
            "p99": _quantile(timing, 0.99),
        },
    }

    primitives = {r["primitive"] for r in rows}
    if primitives == {"choice"}:
        _choice_metrics(rows, out)
    elif primitives == {"noul"}:
        _noul_metrics(rows, out)
    elif primitives == {"score"}:
        _score_metrics(rows, out)
    return out


def _choice_metrics(rows: list[dict[str, Any]], out: dict[str, Any]) -> None:
    golds, preds, nlls, briers, cal = [], [], [], [], []
    probability_rows = 0
    for row in rows:
        gold = str(row["gold"])
        pred = str(row["prediction"])
        probs = {str(k): float(v) for k, v in (row.get("probabilities") or {}).items()}
        golds.append(gold)
        preds.append(pred)
        if not probs:
            continue
        probability_rows += 1
        p_gold = min(1.0, max(EPS, probs.get(gold, EPS)))
        nlls.append(-log(p_gold))
        labels = set(probs) | {gold}
        briers.append(sum((probs.get(label, 0.0) - (1.0 if label == gold else 0.0)) ** 2 for label in labels))
        if probs:
            conf = max(probs.values())
            cal.append((conf, pred == gold))
    out.update({
        "macro_f1": _macro_f1(golds, preds),
        "nll": mean(nlls) if nlls else None,
        "brier": mean(briers) if briers else None,
        "ece_10": _ece(cal),
        "probability_rows": probability_rows,
        "probability_coverage": probability_rows / len(rows),
    })


def _noul_metrics(rows: list[dict[str, Any]], out: dict[str, Any]) -> None:
    nlls, briers, cal = [], [], []
    golds, preds = [], []
    probability_rows = 0
    for row in rows:
        y = 1.0 if bool(row["gold"]) else 0.0
        pred = bool(row["prediction"])
        golds.append("yes" if y else "no")
        preds.append("yes" if pred else "no")
        if row.get("probability_yes") is None:
            continue
        probability_rows += 1
        p = min(1.0 - EPS, max(EPS, float(row["probability_yes"])))
        briers.append((p - y) ** 2)
        nlls.append(-(y * log(p) + (1.0 - y) * log(1.0 - p)))
        conf = p if pred else 1.0 - p
        cal.append((conf, pred == bool(y)))
    out.update({
        "macro_f1": _macro_f1(golds, preds),
        "nll": mean(nlls) if nlls else None,
        "brier": mean(briers) if briers else None,
        "ece_10": _ece(cal),
        "probability_rows": probability_rows,
        "probability_coverage": probability_rows / len(rows),
    })


def _score_metrics(rows: list[dict[str, Any]], out: dict[str, Any]) -> None:
    exact, within1, selected_abs_err, expected_abs_err, nlls, briers, cal = [], [], [], [], [], [], []
    golds: list[int] = []
    preds: list[int] = []
    max_levels = 0
    probability_rows = 0
    for row in rows:
        gold = int(row["gold"])
        probs = {int(k): float(v) for k, v in (row.get("probabilities") or {}).items()}
        value = float(row["prediction"])
        pred = int(max(probs, key=probs.get)) if probs else int(round(value))
        levels = int(row.get("score_levels") or (max(probs) + 1 if probs else max(gold, pred) + 1))
        max_levels = max(max_levels, levels)
        golds.append(gold)
        preds.append(max(0, min(levels - 1, pred)))
        exact.append(pred == gold)
        within1.append(abs(pred - gold) <= 1)
        selected_abs_err.append(abs(pred - gold))
        if probs:
            probability_rows += 1
            expected_abs_err.append(abs(value - gold))
            p_gold = min(1.0, max(EPS, probs.get(gold, EPS)))
            nlls.append(-log(p_gold))
            briers.append(sum((probs.get(i, 0.0) - (1.0 if i == gold else 0.0)) ** 2 for i in range(levels)))
            cal.append((max(probs.values()), pred == gold))
    out.update({
        "exact_accuracy": mean(exact) if exact else None,
        "within_1_accuracy": mean(within1) if within1 else None,
        "mae_selected_score": mean(selected_abs_err) if selected_abs_err else None,
        "mae_expected_score": mean(expected_abs_err) if expected_abs_err else None,
        "quadratic_weighted_kappa": _quadratic_weighted_kappa(golds, preds, max_levels),
        "nll": mean(nlls) if nlls else None,
        "brier": mean(briers) if briers else None,
        "ece_10": _ece(cal),
        "probability_rows": probability_rows,
        "probability_coverage": probability_rows / len(rows),
    })

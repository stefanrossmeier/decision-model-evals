import pytest

from decision_model_evals.metrics import summarize


def test_choice_metrics_perfect() -> None:
    rows = [
        {
            "status": "ok",
            "case_id": "1",
            "primitive": "choice",
            "domain": "d",
            "gold": "a",
            "prediction": "a",
            "correct": True,
            "probabilities": {"a": 1.0, "b": 0.0},
            "timing_ms": 10.0,
            "provider_cost_usd": 0.01,
            "estimated_local_cost_usd": None,
            "input_tokens": 100,
        },
        {
            "status": "ok",
            "case_id": "2",
            "primitive": "choice",
            "domain": "d",
            "gold": "b",
            "prediction": "b",
            "correct": True,
            "probabilities": {"a": 0.0, "b": 1.0},
            "timing_ms": 20.0,
            "provider_cost_usd": 0.02,
            "estimated_local_cost_usd": None,
            "input_tokens": 200,
        },
    ]
    out = summarize(rows)
    g = out["groups"]["primitive:choice"]
    assert g["accuracy"] == 1.0
    assert g["macro_f1"] == 1.0
    assert g["brier"] == 0.0
    assert g["provider_cost_usd"] == pytest.approx(0.03)
    assert g["latency_ms"]["p50"] == pytest.approx(15.0)


def test_noul_and_score_metrics_exist() -> None:
    rows = [
        {
            "status": "ok",
            "case_id": "n",
            "primitive": "noul",
            "domain": "d1",
            "gold": True,
            "prediction": True,
            "correct": True,
            "probability_yes": 0.9,
            "probabilities": None,
            "timing_ms": 3.0,
            "provider_cost_usd": 0.0,
            "estimated_local_cost_usd": 0.001,
            "input_tokens": 10,
        },
        {
            "status": "ok",
            "case_id": "s",
            "primitive": "score",
            "domain": "d2",
            "gold": 2,
            "prediction": 1.8,
            "correct": True,
            "probabilities": {"0": 0.0, "1": 0.2, "2": 0.8},
            "score_levels": 3,
            "timing_ms": 4.0,
            "provider_cost_usd": 0.0,
            "estimated_local_cost_usd": 0.001,
            "input_tokens": 10,
        },
    ]
    out = summarize(rows)
    assert out["groups"]["primitive:noul"]["brier"] == pytest.approx(0.01)
    assert out["groups"]["primitive:score"]["mae_expected_score"] == pytest.approx(0.2)

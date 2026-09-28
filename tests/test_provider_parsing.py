import pytest

from decision_model_evals.providers.http_systemone import parse_systemone_response
from decision_model_evals.schema import Case


def case(primitive: str, criteria):
    gold = {"choice": "b"} if primitive == "choice" else ({"noul": True} if primitive == "noul" else {"score": 1})
    return Case.from_dict(
        {
            "id": "c",
            "primitive": primitive,
            "domain": "d",
            "task": "t",
            "state": "state",
            "instructions": "q",
            "criteria": criteria,
            "gold": gold,
        }
    )


def test_parse_choice() -> None:
    result = parse_systemone_response(
        {
            "model": "m-snapshot",
            "provider": "p",
            "answers": {"q": {"type": "choice", "choice": "b", "probabilities": {"a": 0.2, "b": 0.8}}},
            "usage": {"input_tokens": 10, "output_tokens": 2, "cost": 0.0001},
        },
        case("choice", {"a": "A", "b": "B"}),
    )
    assert result.prediction == "b"
    assert result.probabilities == {"a": 0.2, "b": 0.8}
    assert result.input_tokens == 10
    assert result.provider_cost_usd == pytest.approx(0.0001)


def test_parse_noul() -> None:
    result = parse_systemone_response(
        {"answers": {"q": {"type": "noul", "noul": 0.72}}},
        case("noul", {"true": "yes", "false": "no"}),
    )
    assert result.probability_yes == pytest.approx(0.72)
    assert result.prediction is True


def test_parse_score() -> None:
    result = parse_systemone_response(
        {"answers": {"q": {"type": "score", "score": 1.25, "probabilities": {"0": 0.0, "1": 0.75, "2": 0.25}}}},
        case("score", ["low", "medium", "high"]),
    )
    assert result.prediction == pytest.approx(1.25)
    assert result.probabilities == {"0": 0.0, "1": 0.75, "2": 0.25}

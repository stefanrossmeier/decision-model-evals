from __future__ import annotations

from typing import Any
import httpx

from decision_model_evals.providers.base import DecisionProvider, DecisionResult
from decision_model_evals.schema import Case


class SystemOneHTTPProvider(DecisionProvider):
    """Adapter for Jev-compatible local /v1/systemone servers."""

    def __init__(self, endpoint: str, model: str | None = None, timeout_s: float = 120.0):
        self.endpoint = endpoint
        self.model = model
        self.client = httpx.Client(timeout=timeout_s)

    def close(self) -> None:
        self.client.close()

    def decide(self, case: Case) -> DecisionResult:
        payload: dict[str, Any] = {
            "state": case.state,
            "questions": {"q": case.question_payload()},
        }
        if self.model:
            payload["model"] = self.model
        response = self.client.post(self.endpoint, json=payload)
        response.raise_for_status()
        raw = response.json()
        return parse_systemone_response(raw, case)


def parse_systemone_response(raw: dict[str, Any], case: Case) -> DecisionResult:
    answers = raw.get("answers") or {}
    answer = answers.get("q")
    if answer is None and len(answers) == 1:
        answer = next(iter(answers.values()))
    if not isinstance(answer, dict):
        raise ValueError(f"missing answer for q: {raw!r}")

    usage = raw.get("usage") or {}
    probabilities = _probabilities(answer)
    prediction: str | float | bool | None = None
    probability_yes: float | None = None

    if case.primitive == "choice":
        prediction = answer.get("choice")
        if prediction is None and probabilities:
            prediction = max(probabilities, key=probabilities.get)
    elif case.primitive == "noul":
        value = answer.get("noul")
        if value is None:
            value = answer.get("probability")
        if value is None and probabilities:
            value = probabilities.get("true", probabilities.get("yes"))
        if value is None:
            raise ValueError(f"noul response has no probability: {answer!r}")
        probability_yes = float(value)
        prediction = probability_yes >= 0.5
    else:
        score = answer.get("score")
        if score is None and probabilities:
            score = sum(int(k) * float(v) for k, v in probabilities.items())
        if score is None:
            raise ValueError(f"score response has no score: {answer!r}")
        prediction = float(score)

    return DecisionResult(
        raw=raw,
        model=_string_or_none(raw.get("model")),
        provider=_string_or_none(raw.get("provider")),
        prediction=prediction,
        probabilities=probabilities,
        probability_yes=probability_yes,
        input_tokens=_int_or_none(usage.get("input_tokens", answer.get("input_tokens"))),
        output_tokens=_int_or_none(usage.get("output_tokens")),
        provider_cost_usd=_float_or_none(usage.get("cost", usage.get("cost_usd"))),
        provider_latency_ms=_first_float(
            raw.get("elapsedMs"), raw.get("elapsed_ms"), raw.get("latency_ms"), usage.get("elapsed_ms")
        ),
    )


def _probabilities(answer: dict[str, Any]) -> dict[str, float] | None:
    raw = answer.get("probabilities")
    if not isinstance(raw, dict):
        return None
    return {str(k): float(v) for k, v in raw.items()}


def _int_or_none(value: Any) -> int | None:
    return int(value) if value is not None else None


def _float_or_none(value: Any) -> float | None:
    return float(value) if value is not None else None


def _string_or_none(value: Any) -> str | None:
    return str(value) if value is not None else None


def _first_float(*values: Any) -> float | None:
    for value in values:
        if value is not None:
            return float(value)
    return None

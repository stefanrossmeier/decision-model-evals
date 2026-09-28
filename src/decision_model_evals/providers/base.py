from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from decision_model_evals.schema import Case


@dataclass
class DecisionResult:
    raw: dict[str, Any]
    model: str | None
    provider: str | None
    prediction: str | float | bool | None
    probabilities: dict[str, float] | None
    probability_yes: float | None
    input_tokens: int | None
    output_tokens: int | None
    provider_cost_usd: float | None
    provider_latency_ms: float | None = None


class DecisionProvider:
    def decide(self, case: Case) -> DecisionResult:
        raise NotImplementedError

    def close(self) -> None:
        pass

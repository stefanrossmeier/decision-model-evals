from __future__ import annotations

from typing import Any
import os
import httpx

from decision_model_evals.providers.base import DecisionProvider
from decision_model_evals.providers.http_systemone import parse_systemone_response
from decision_model_evals.schema import Case


class OpenRouterDecisionsProvider(DecisionProvider):
    """OpenRouter Decisions API adapter used for TypeSafe Jev."""

    def __init__(self, endpoint: str, model: str, api_key_env: str, timeout_s: float = 120.0):
        api_key = os.getenv(api_key_env)
        if not api_key:
            raise RuntimeError(f"{api_key_env} is required for OpenRouter")
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        if os.getenv("OPENROUTER_HTTP_REFERER"):
            headers["HTTP-Referer"] = os.environ["OPENROUTER_HTTP_REFERER"]
        if os.getenv("OPENROUTER_APP_TITLE"):
            headers["X-Title"] = os.environ["OPENROUTER_APP_TITLE"]
        self.endpoint = endpoint
        self.model = model
        self.client = httpx.Client(headers=headers, timeout=timeout_s)

    def close(self) -> None:
        self.client.close()

    def decide(self, case: Case):
        payload: dict[str, Any] = {
            "model": self.model,
            "state": case.state,
            "questions": {"q": case.question_payload()},
        }
        response = self.client.post(self.endpoint, json=payload)
        response.raise_for_status()
        return parse_systemone_response(response.json(), case)

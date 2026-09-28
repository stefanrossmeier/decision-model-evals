from __future__ import annotations

from decision_model_evals.config import ModelConfig
from decision_model_evals.providers.base import DecisionProvider
from decision_model_evals.providers.http_systemone import SystemOneHTTPProvider
from decision_model_evals.providers.openrouter import OpenRouterDecisionsProvider


def create_provider(config: ModelConfig, timeout_s: float) -> DecisionProvider:
    if config.provider == "openrouter_decisions":
        if not config.model or not config.api_key_env:
            raise ValueError(f"{config.name}: OpenRouter requires model and api_key_env")
        return OpenRouterDecisionsProvider(
            endpoint=config.endpoint,
            model=config.model,
            api_key_env=config.api_key_env,
            timeout_s=timeout_s,
        )
    if config.provider == "systemone_http":
        return SystemOneHTTPProvider(
            endpoint=config.endpoint,
            model=config.model,
            timeout_s=timeout_s,
        )
    raise ValueError(f"unsupported provider type: {config.provider}")

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os
import yaml


@dataclass(frozen=True)
class ModelConfig:
    name: str
    provider: str
    model: str | None
    endpoint: str
    api_key_env: str | None
    deployment: str
    description: str


def _resolve_env(raw: dict, key: str, default_key: str | None = None) -> str:
    env_name = raw.get(key)
    if env_name:
        value = os.getenv(str(env_name))
        if value:
            return value
    if default_key:
        value = raw.get(default_key)
        if value:
            return str(value)
    return ""


def load_models(path: Path) -> dict[str, ModelConfig]:
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    result: dict[str, ModelConfig] = {}
    for name, item in (raw.get("models") or {}).items():
        endpoint = _resolve_env(item, "endpoint_env", "endpoint")
        if not endpoint:
            raise ValueError(f"model {name}: endpoint is required")
        result[name] = ModelConfig(
            name=name,
            provider=str(item["provider"]),
            model=item.get("model"),
            endpoint=endpoint,
            api_key_env=item.get("api_key_env"),
            deployment=str(item.get("deployment", "unknown")),
            description=str(item.get("description", "")),
        )
    return result

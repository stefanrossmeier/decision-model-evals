from pathlib import Path

from decision_model_evals.config import load_models

ROOT = Path(__file__).resolve().parents[1]


def test_model_matrix() -> None:
    models = load_models(ROOT / "configs" / "models.yaml")
    assert set(models) == {
        "jev",
        "bosun",
        "decider",
        "semif",
        "luna-structured",
        "luna-classifier",
    }
    assert models["jev"].provider == "openrouter_decisions"
    assert models["jev"].model == "typesafe/jev-1.13"
    assert models["bosun"].deployment == "local"
    assert models["bosun"].endpoint == "http://127.0.0.1:8000/v1/systemone"
    assert models["luna-structured"].model == "openai/gpt-6-luna"
    assert models["luna-structured"].provider == "openrouter_structured_classifier"
    assert models["luna-classifier"].provider == "openrouter_verbalizer_classifier"
    assert models["luna-structured"].api_key_env == "OPENROUTER_API_KEY"
    assert models["luna-structured"].parameters["reasoning_effort"] == "none"
    assert models["luna-structured"].parameters["seed"] == 0
    assert models["luna-structured"].parameters["provider_only"] == ["OpenAI"]
    assert models["luna-classifier"].parameters["require_parameters"] is True


def test_bosun_endpoint_is_fixed_to_server_default(monkeypatch) -> None:
    monkeypatch.setenv("BOSUN_URL", "http://127.0.0.1:8010/v1/systemone")
    models = load_models(ROOT / "configs" / "models.yaml")
    assert models["bosun"].endpoint == "http://127.0.0.1:8000/v1/systemone"

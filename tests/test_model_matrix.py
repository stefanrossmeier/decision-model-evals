from pathlib import Path
import importlib.util

from decision_model_evals.config import load_models

ROOT = Path(__file__).resolve().parents[1]


def test_primary_model_matrix_has_only_active_models() -> None:
    models = load_models(ROOT / "configs/models.yaml")
    assert {"jev", "bosun", "decider", "semif"} <= set(models)
    assert {"luna-structured", "luna-classifier"} <= set(models)
    assert "jevk5" not in models
    assert "autojev" not in models


def _semif_server_module():
    path = ROOT / "scripts/semif-server.py"
    spec = importlib.util.spec_from_file_location("semif_server", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_semif_choice_adapter_preserves_option_ids() -> None:
    m = _semif_server_module()
    row, kind, opts = m._question_to_row("state", "q", {"type":"choice", "instructions":"route", "criteria":{"a":"A", "b":"B"}})
    assert row["question"] == "route"
    assert [o["id"] for o in opts] == ["a", "b"]
    answer = m._answer(kind, opts, {"probabilities":[0.2, 0.8]})
    assert answer["choice"] == "b"
    assert answer["probabilities"] == {"a":0.2, "b":0.8}


def test_semif_noul_and_score_adapter() -> None:
    m = _semif_server_module()
    row, kind, opts = m._question_to_row("state", "q", {"type":"noul", "instructions":"true?", "criteria":{"false":"no", "true":"yes"}})
    answer = m._answer(kind, opts, {"probabilities":[0.25, 0.75]})
    assert answer["noul"] == 0.75
    row, kind, opts = m._question_to_row("state", "q", {"type":"score", "instructions":"rate", "criteria":["low","mid","high"]})
    answer = m._answer(kind, opts, {"probabilities":[0.1,0.2,0.7]})
    assert abs(answer["score"] - 1.6) < 1e-12


def test_semif_runtime_callback_is_not_method_bound() -> None:
    m = _semif_server_module()
    seen = []

    def decide(row):
        seen.append(row)
        return {"probabilities": [0.4, 0.6]}

    m.configure_handler(decide, {"runtime": "test"})
    handler = object.__new__(m.Handler)
    row = {"id": "q"}

    assert handler.decide(row) == {"probabilities": [0.4, 0.6]}
    assert seen == [row]
    assert handler.metadata == {"runtime": "test"}

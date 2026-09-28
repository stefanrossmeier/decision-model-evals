from pathlib import Path

from decision_model_evals.schema import Case, load_corpus

ROOT = Path(__file__).resolve().parents[1]


def test_full_corpus_shape() -> None:
    cases = load_corpus(ROOT / "datasets" / "corpus.jsonl")
    assert len(cases) == 5760
    assert len({case.id for case in cases}) == 5760
    assert {case.primitive for case in cases} == {"choice", "noul", "score"}
    assert len({case.domain for case in cases}) == 16
    for primitive in ("choice", "noul", "score"):
        assert sum(case.primitive == primitive for case in cases) == 1920


def test_case_payload_does_not_include_gold() -> None:
    case = Case.from_dict(
        {
            "id": "x",
            "primitive": "choice",
            "domain": "test",
            "task": "route",
            "state": "hello",
            "instructions": "choose",
            "criteria": {"a": "A", "b": "B"},
            "gold": {"choice": "a", "rationale": "because"},
        }
    )
    payload = case.question_payload()
    assert payload == {"type": "choice", "instructions": "choose", "criteria": {"a": "A", "b": "B"}}
    assert "gold" not in payload

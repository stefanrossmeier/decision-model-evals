from collections import Counter
from pathlib import Path

from decision_model_evals.runner import load_suite_ids, select_cases
from decision_model_evals.schema import load_corpus

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    "probe": 3,
    "smoke": 18,
    "quick": 300,
    "core": 1500,
    "perf": 180,
    "full": 5760,
    "routing": 360,
    "agent-security": 360,
}


def test_frozen_suite_sizes_and_references() -> None:
    corpus = load_corpus(ROOT / "datasets" / "corpus.jsonl")
    for name, count in EXPECTED.items():
        ids = load_suite_ids(ROOT / "datasets" / "suites" / f"{name}.yaml")
        assert len(ids) == count
        assert len(select_cases(corpus, ids)) == count


def test_full_suite_is_balanced() -> None:
    corpus = load_corpus(ROOT / "datasets" / "corpus.jsonl")
    counts = Counter((c.domain, c.primitive) for c in corpus)
    assert set(counts.values()) == {120}


def test_smoke_has_six_per_primitive() -> None:
    corpus = load_corpus(ROOT / "datasets" / "corpus.jsonl")
    selected = select_cases(corpus, load_suite_ids(ROOT / "datasets" / "suites" / "smoke.yaml"))
    counts = Counter(c.primitive for c in selected)
    assert counts == {"choice": 6, "noul": 6, "score": 6}

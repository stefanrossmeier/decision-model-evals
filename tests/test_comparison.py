from decision_model_evals.comparison import _mcnemar_exact


def test_mcnemar_exact_symmetric() -> None:
    assert _mcnemar_exact(3, 3) == 1.0


def test_mcnemar_exact_strong_imbalance() -> None:
    assert _mcnemar_exact(10, 0) < 0.01

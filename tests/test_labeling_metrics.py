from finance_sentiment.labeling import LABELED, labeled_pairs
from finance_sentiment.metrics import (
    cohen_kappa, macro_precision_recall, precision_recall, wilson_ci,
)
from finance_sentiment.scorer import score_text


def test_labeled_set_is_balanced_12_items():
    assert len(LABELED) == 12
    assert {item["label"] for item in LABELED} == {"positive", "negative", "neutral"}
    for label in ("positive", "negative", "neutral"):
        assert sum(1 for i in LABELED if i["label"] == label) == 4


def test_labeled_set_uses_synthetic_data_only():
    for item in LABELED:
        assert item["company"] in {
            "Acme Widgets", "Harborline Foods", "Northgate Tools", "Ficton Retail"}


def test_precision_recall_perfect_case():
    y = ["positive", "positive", "negative"]
    assert precision_recall(y, y, "positive")["precision"] == 1.0
    assert precision_recall(y, y, "positive")["recall"] == 1.0


def test_precision_recall_counts_fp_and_fn():
    result = precision_recall(["positive", "negative"], ["positive", "positive"], "positive")
    assert result["tp"] == 1 and result["fp"] == 1 and result["fn"] == 0


def test_macro_report_includes_accuracy():
    texts, human = labeled_pairs()
    predicted = [score_text(t).label for t in texts]
    report = macro_precision_recall(human, predicted)
    assert 0.0 <= report["accuracy"] <= 1.0
    assert report["macro_precision"] >= 0.0
    assert len(report["per_label"]) == 3


def test_scorer_beats_chance_on_labeled_set():
    texts, human = labeled_pairs()
    predicted = [score_text(t).label for t in texts]
    accuracy = sum(1 for t, p in zip(human, predicted) if t == p) / len(human)
    assert accuracy >= 0.75  # regression check on n=12, not a quality claim


def test_cohen_kappa_perfect_agreement_is_one():
    y = ["positive", "negative", "neutral"]
    assert cohen_kappa(y, y) == 1.0


def test_cohen_kappa_is_bounded():
    kappa = cohen_kappa(["positive", "negative"], ["negative", "positive"])
    assert -1.0 <= kappa <= 1.0


def test_wilson_interval_contains_proportion_and_is_ordered():
    low, high = wilson_ci(9, 12)
    assert 0.0 <= low <= 9 / 12 <= high <= 1.0


def test_wilson_interval_empty_trials_is_zero():
    assert wilson_ci(0, 0) == (0.0, 0.0)

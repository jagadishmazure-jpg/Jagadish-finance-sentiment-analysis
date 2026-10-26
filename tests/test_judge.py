import pytest

from finance_sentiment.judge import (
    JudgeNotConfigured, LiveJudgeHook, StubJudge, length_bias_rate,
    order_flip_rate, self_preference_rate,
)
from finance_sentiment.labeling import labeled_pairs
from finance_sentiment.metrics import cohen_kappa


def test_stub_judge_labels_positive_text():
    assert StubJudge().judge("Revenue grew strongly, demand robust.").label == "positive"


def test_stub_judge_is_deterministic():
    judge = StubJudge()
    text = "Revenue declined and losses widened."
    assert judge.judge(text) == judge.judge(text)


def test_stub_judge_rationale_names_its_limitation():
    verdict = StubJudge().judge("Revenue grew.")
    assert "stub" in verdict.rationale.lower()
    assert "not a live model" in verdict.rationale


def test_live_hook_without_callable_raises_not_configured():
    with pytest.raises(JudgeNotConfigured):
        LiveJudgeHook().judge("Revenue grew.")


def test_live_hook_with_callable_uses_it():
    hook = LiveJudgeHook(judge_callable=lambda t: "called")
    assert hook.judge("anything") == "called"


def test_order_flip_rate_excludes_ties_from_denominator():
    # Identical scores -> tie -> excluded, so considered == 0.
    result = order_flip_rate([("Revenue grew.", "Revenue grew.")])
    assert result["considered"] == 0 and result["rate"] == 0.0


def test_order_flip_rate_counts_are_visible():
    pairs = [("Revenue grew strongly.", "Revenue declined sharply.")]
    result = order_flip_rate(pairs)
    assert result["considered"] == 1 and "flips" in result and "rate" in result


def test_length_bias_rate_reports_counts():
    texts, _ = labeled_pairs()
    result = length_bias_rate(texts)
    assert result["considered"] == len(texts)
    assert 0.0 <= result["rate"] <= 1.0


def test_self_preference_rate_is_zero_for_tag_blind_stub():
    pairs = [("Revenue grew.", "Revenue declined sharply and losses widened.")]
    result = self_preference_rate(pairs)
    assert result["rate"] == 0.0


def test_judge_kappa_vs_human_is_computed():
    texts, human = labeled_pairs()
    judge_labels = [StubJudge().judge(t).label for t in texts]
    kappa = cohen_kappa(human, judge_labels)
    assert -1.0 <= kappa <= 1.0

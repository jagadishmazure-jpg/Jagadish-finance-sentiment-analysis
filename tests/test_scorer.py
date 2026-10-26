from finance_sentiment.scorer import score_text


def test_positive_text_scores_positive():
    r = score_text("Revenue grew strongly and demand remained robust.")
    assert r.label == "positive" and r.score > 0


def test_negative_text_scores_negative():
    r = score_text("Revenue declined and losses widened amid headwinds.")
    assert r.label == "negative" and r.score < 0


def test_neutral_text_scores_neutral():
    r = score_text("The document lists dates, sections, and page numbers.")
    assert r.label == "neutral" and r.score == 0.0


def test_negation_flips_sign():
    assert score_text("results were strong").label == "positive"
    assert score_text("results were not strong").label == "negative"


def test_intensifier_increases_magnitude():
    plain = score_text("growth was strong")
    intense = score_text("growth was very strong")
    assert abs(intense.score) > abs(plain.score)


def test_score_is_deterministic():
    text = "Revenue grew strongly, margins expanded, demand robust."
    assert score_text(text) == score_text(text)


def test_score_is_clipped_to_unit_range():
    r = score_text("growth growth growth growth growth growth strong robust record beat")
    assert -1.0 <= r.score <= 1.0


def test_empty_text_is_neutral_with_zero_confidence():
    r = score_text("")
    assert r.label == "neutral" and r.hits == 0 and r.confidence == 0.0


def test_confidence_grows_with_hits():
    one = score_text("growth")
    many = score_text("growth strong robust record momentum")
    assert many.confidence > one.confidence

"""Deterministic financial-sentiment lexicon.

Words were chosen by the author for this synthetic demo, not copied from
any published lexicon. Weights are small integers so scores are easy to
audit by hand: a human can recompute any score from this file alone.
"""

POSITIVE = {
    "growth": 2,
    "grew": 2,
    "strong": 2,
    "robust": 2,
    "expand": 2,
    "expanded": 2,
    "expansion": 2,
    "beat": 2,
    "exceeded": 2,
    "momentum": 2,
    "confident": 2,
    "confidence": 2,
    "optimistic": 2,
    "resilient": 2,
    "improved": 2,
    "improvement": 2,
    "record": 2,
    "profitable": 2,
    "profit": 1,
    "gains": 2,
    "gain": 1,
    "upside": 2,
    "healthy": 2,
    "solid": 1,
    "accelerating": 2,
    "demand": 1,
    "outperform": 2,
    "recovery": 2,
    "stable": 1,
    "strength": 2,
}

NEGATIVE = {
    "decline": -2,
    "declined": -2,
    "weak": -2,
    "weakness": -2,
    "loss": -2,
    "losses": -2,
    "risk": -1,
    "risks": -1,
    "pressure": -1,
    "pressured": -2,
    "pressures": -1,
    "downturn": -2,
    "miss": -2,
    "missed": -2,
    "shortfall": -2,
    "contraction": -2,
    "shrinking": -2,
    "uncertain": -2,
    "uncertainty": -2,
    "headwind": -2,
    "headwinds": -2,
    "deteriorating": -2,
    "challenging": -1,
    "widened": -2,
    "slowed": -1,
    "slowing": -1,
    "volatility": -1,
    "default": -2,
}

NEGATORS = {"not", "no", "never", "without"}
INTENSIFIERS = {"very": 1.5, "significantly": 1.5, "sharply": 1.5, "strongly": 1.5}
HEDGES = {"may", "might", "could", "possibly", "potentially"}


def weight(word):
    """Return the lexicon weight for a word, or 0 if it is not listed."""
    if word in POSITIVE:
        return POSITIVE[word]
    if word in NEGATIVE:
        return NEGATIVE[word]
    return 0

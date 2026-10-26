"""Deterministic lexicon-based sentiment scorer.

Rules, in order:
1. Tokenise to lowercase alphabetic words.
2. A lexicon word contributes its weight.
3. A negator in the previous 3 tokens flips the sign of the next
   lexicon word.
4. An intensifier immediately before a lexicon word multiplies it by 1.5.
5. Score is the weighted sum clipped to [-1, 1] by dividing by 5.
   Labels: score >= 0.15 positive, <= -0.15 negative, else neutral.
6. Confidence grows with the number of sentiment hits: hits / (hits + 2).

No model, no network, no randomness. The same text always gives the
same score, which is the whole point: the scorer is the auditable
baseline that the judge path is measured against.
"""

import re
from dataclasses import dataclass

from .lexicon import INTENSIFIERS, NEGATORS, weight

_TOKEN = re.compile(r"[a-z]+")


@dataclass(frozen=True)
class SentimentResult:
    text: str
    score: float
    label: str
    positive_hits: int
    negative_hits: int
    hits: int
    word_count: int
    coverage: float
    confidence: float


def tokenize(text):
    return _TOKEN.findall(text.lower())


def score_text(text):
    tokens = tokenize(text)
    weighted_sum = 0.0
    positive_hits = 0
    negative_hits = 0
    for i, token in enumerate(tokens):
        w = weight(token)
        if w == 0:
            continue
        window = tokens[max(0, i - 3):i]
        if any(t in NEGATORS for t in window):
            w = -w
        if i > 0 and tokens[i - 1] in INTENSIFIERS:
            w = w * INTENSIFIERS[tokens[i - 1]]
        weighted_sum += w
        if w > 0:
            positive_hits += 1
        elif w < 0:
            negative_hits += 1
    hits = positive_hits + negative_hits
    score = max(-1.0, min(1.0, weighted_sum / 5.0))
    if score >= 0.15:
        label = "positive"
    elif score <= -0.15:
        label = "negative"
    else:
        label = "neutral"
    word_count = len(tokens)
    coverage = hits / word_count if word_count else 0.0
    confidence = hits / (hits + 2.0) if hits else 0.0
    return SentimentResult(
        text=text,
        score=round(score, 4),
        label=label,
        positive_hits=positive_hits,
        negative_hits=negative_hits,
        hits=hits,
        word_count=word_count,
        coverage=round(coverage, 4),
        confidence=round(confidence, 4),
    )

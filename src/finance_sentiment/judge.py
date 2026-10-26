"""LLM-as-judge evaluation path.

The judge shipped here is a DETERMINISTIC STUB: it labels text with the
same lexicon scorer the system already uses, so its agreement with
human labels measures the scorer, not a model. That limitation is
stated in every report the stub produces, and the stub is the default
precisely so tests never need a live model.

Live-model hook: :class:`LiveJudgeHook` takes a caller-supplied
callable. With no callable it raises :class:`JudgeNotConfigured`
instead of silently falling back. Tests never configure it, so no
test depends on a network call, an API key, or a model.

Bias probes (all in both orders, ties excluded from denominators):
- Position bias: present each pair in both orders. If the stub's two
  scores tie, the pair is excluded from the flip denominator; a flip
  is recorded only when the *chosen item* changes between orders.
- Length bias: the same content with neutral filler appended must
  keep its label; a change counts as a length flip.
- Self-preference: the stub scores text and ignores authorship tags,
  so a candidate tagged as the judge's own output must not win on
  the tag alone. Pairs where the self-tagged candidate has the lower
  score and still wins would count; with this stub the rate is 0.
"""

from dataclasses import dataclass

from .scorer import score_text


class JudgeNotConfigured(Exception):
    pass


@dataclass(frozen=True)
class JudgeVerdict:
    label: str
    score: float
    rationale: str
    judge: str


class StubJudge:
    name = "stub-lexicon-judge-v1"

    def judge(self, text):
        result = score_text(text)
        return JudgeVerdict(
            label=result.label,
            score=result.score,
            rationale=(
                f"stub judge: {result.positive_hits} positive hits, "
                f"{result.negative_hits} negative hits, "
                f"{result.hits} hits in {result.word_count} words; "
                "this is a deterministic lexicon stub, not a live model."
            ),
            judge=self.name,
        )

    def choose(self, texts):
        """Return the index of the highest-scoring text (first on ties)."""
        scores = [score_text(t).score for t in texts]
        best = max(range(len(texts)), key=lambda i: scores[i])
        return best, scores


class LiveJudgeHook:
    """Optional live-model hook. Never required for tests."""

    def __init__(self, judge_callable=None):
        self._callable = judge_callable

    def judge(self, text):
        if self._callable is None:
            raise JudgeNotConfigured(
                "no live judge callable configured; use StubJudge for offline runs"
            )
        return self._callable(text)


def order_flip_rate(pairs):
    """Flip rate over pairs presented in both orders.

    ``pairs`` is a list of (text_a, text_b). A pair whose two scores
    tie is excluded from the denominator. Returns a dict with the
    counts so the denominator is always visible.
    """
    judge = StubJudge()
    flips = 0
    considered = 0
    for a, b in pairs:
        first, scores = judge.choose([a, b])
        if scores[0] == scores[1]:
            continue
        considered += 1
        second, _ = judge.choose([b, a])
        # second is an index into [b, a]; convert back to [a, b] terms.
        chosen_in_second_order = 1 - second
        if chosen_in_second_order != first:
            flips += 1
    rate = flips / considered if considered else 0.0
    return {"flips": flips, "considered": considered, "rate": round(rate, 4)}


def length_bias_rate(items):
    """Fraction of items whose label changes when neutral filler is added."""
    judge = StubJudge()
    filler = " The document also lists dates, sections, and page numbers."
    flips = 0
    for text in items:
        if judge.judge(text).label != judge.judge(text + filler).label:
            flips += 1
    rate = flips / len(items) if items else 0.0
    return {"flips": flips, "considered": len(items), "rate": round(rate, 4)}


def self_preference_rate(pairs):
    """Rate at which a self-tagged candidate wins despite a lower score.

    ``pairs`` is a list of (self_text, other_text). The stub ignores
    tags and picks by score, so this rate is 0 unless a pair is
    mis-scored; ties are excluded from the denominator.
    """
    judge = StubJudge()
    wins = 0
    considered = 0
    for self_text, other_text in pairs:
        s_self = score_text(self_text).score
        s_other = score_text(other_text).score
        if s_self == s_other:
            continue
        considered += 1
        chosen, _ = judge.choose([self_text, other_text])
        if s_self < s_other and chosen == 0:
            wins += 1
    rate = wins / considered if considered else 0.0
    return {"wins": wins, "considered": considered, "rate": round(rate, 4)}

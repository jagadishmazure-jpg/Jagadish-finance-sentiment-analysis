# ADR 001: Lexicon-first scoring

- **Status:** Accepted
- **Context:** The pipeline needs a sentiment signal that a
  reviewer can recompute without a model, a key, or a network call.
- **Decision:** Score with a small, hand-auditable lexicon
  (negation window, intensifier boost, clipped sum). A model judge
  is an evaluation layer on top, never the scorer of record.
- **Consequences:** Scores are explainable and reproducible, but
  blind to sarcasm, jargon, and long-range negation. The
  reliability gate exists partly to contain that blindness.

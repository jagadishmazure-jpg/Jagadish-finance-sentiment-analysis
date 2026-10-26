# Use-case patterns (distilled)

These are working notes on the patterns this repo implements, in
the author's own words. They are not a summary of any source
document, and they contain no copied sentences.

## Pattern: tone as a research signal

- **Input:** invented call transcripts and filing excerpts.
- **Transform:** lexicon scoring with negation and intensifier
  handling.
- **Output:** a score, a label, hit counts, coverage, and
  confidence — all five, never the label alone.
- **Use:** a researcher's notebook, a credit file's qualitative
  section, or a monitoring dashboard, always behind the gate.

## Pattern: reliability before action

- **Check:** magnitude against a threshold, support against a
  hit minimum, length against a word minimum.
- **Fail mode:** route to a named human with scope and expiry,
  not to a queue nobody owns.
- **Anti-pattern:** a "force" flag, a silent default to ACT, or a
  threshold tuned on the same items used to report accuracy.

## Pattern: evaluating a judge

- Run each comparison in both orders.
- Exclude ties from flip denominators, and print denominators.
- Measure agreement with human labels (kappa), not just with the
  scorer.
- Report a Wilson interval with every proportion on a small set.
- Probe length and self-preference separately; a judge can be
  clean on one bias and dirty on another.

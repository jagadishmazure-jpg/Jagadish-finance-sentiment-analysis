# Recruiter summary

- **Problem:** Earnings calls and filing excerpts are long, and a
  sentiment number on its own hides whether it deserves to be acted on.
- **Approach:** A deterministic lexicon scorer over synthetic text,
  checked against a hand-labeled set, evaluated with a stub judge
  (bias probes, kappa, Wilson intervals), and passed through a
  reliability gate that sends weak scores to a human.
- **Proof (real run, n=12 synthetic items):** scorer accuracy 12/12,
  macro precision/recall/F1 1.0, judge agreement with human labels
  kappa 1.0 (Wilson 95% interval 0.7575–1.0), gate acted on 8 and sent
  4 to review, order-flip / length-bias / self-preference rates all
  0.0 on the probe sets used. These are regression-check numbers on
  a tiny invented set, not claims about real markets.
- **Guardrails:** view-only SQLite reads, tested confirmation gates,
  PII redaction including card numbers and emails, fetch-time row
  caps, negative-cost rejection, dry-run email by default.

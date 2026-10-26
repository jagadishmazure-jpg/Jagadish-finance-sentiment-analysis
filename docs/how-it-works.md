# How it works, step by step

1. **Ingest (synthetic only).** A document is an invented
   earnings-call snippet or filing excerpt about an invented company
   (Acme Widgets, Harborline Foods, Northgate Tools, Ficton Retail).
   Nothing is fetched from any real source.
2. **Redact.** `redaction.redact` removes card numbers, email
   addresses, phone numbers, and SSNs, replacing each with a typed
   placeholder. Redacted text is what gets scored.
3. **Score.** `scorer.score_text` tokenises, looks up lexicon
   weights, flips signs after negators, boosts after intensifiers,
   and clips the sum to [-1, 1]. Label thresholds are +0.15 / -0.15.
4. **Evaluate against labels.** The 12-item hand-labeled set gives
   per-label precision/recall/F1, macro averages, and accuracy.
   Sample size is always stated with the numbers.
5. **Judge evaluation.** The stub judge labels the same texts. Its
   agreement with human labels is reported as Cohen's kappa with a
   Wilson interval. Bias probes run every pair in both orders;
   tied pairs are excluded from the flip denominator.
6. **Gate.** `ReliabilityGate` (threshold 0.30, at least 2 hits, at
   least 8 words) decides ACT or HUMAN_REVIEW. A blocked decision
   can only proceed with a confirmed human approval from
   `ConfirmationGate`, which checks the named approver, scope,
   expiry, single use, consent text, and confidence.
7. **Store.** Scores and documents are read back through views
   under the strict authorizer, with a fetch-time row cap.
8. **Notify (optional, dry-run).** The email channel defaults to
   dry-run and refuses to send in CI. No credentials are involved.

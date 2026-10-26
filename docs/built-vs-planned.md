# Built vs planned

| Item | Status |
|---|---|
| Deterministic lexicon scorer (negation, intensifiers) | Built, tested |
| Hand-labeled synthetic set (12 items, 4 per label) | Built, tested |
| Precision/recall/F1 + macro averages | Built, tested |
| Stub judge + live-model hook (never required) | Built, tested |
| Position / length / self-preference bias probes, both orders, ties excluded | Built, tested |
| Cohen's kappa vs human labels, Wilson intervals | Built, tested |
| Reliability gate (threshold, hits, length) + human-review routing | Built, tested |
| Confirmation gate (named, single-use, scoped, expiring; bypass/reject/absent/low-confidence/contradicting tests) | Built, tested |
| View-aware SQLite authorizer | Built, tested |
| PII redaction (cards, emails, phones, SSNs) | Built, tested |
| Fetch-time row cap, negative-cost rejection, hashed brand blocklist, dry-run email | Built, tested |
| Offline demo printing real numbers | Built, run |
| Live-model judge evaluation on a real model | Written-not-run: hook exists, no model configured, no test depends on it |
| Real-transcript validation | Planned: not in scope for a synthetic-only repo; would need a separate, properly licensed dataset and a new evaluation |
| Deployment, package release, hosted demo | Planned: none claimed, none built |

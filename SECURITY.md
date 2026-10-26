# Security policy

## Scope

This repo is a synthetic-data research demo. It holds no real market
data, no real company disclosures, no customer data, and no
credentials. Do not add any of those things.

## Controls enforced by tests

- **View-only reads.** The SQLite authorizer allows base-table reads
  only through the views `v_documents` / `v_scores` (or SQLite's
  empty-column view-expansion probe, which names no column and
  returns no value). Direct base-table reads, `sqlite_master` reads,
  writes, PRAGMA, ATTACH, and `load_extension` are denied.
  Proof: `tests/test_authorizer.py`.
- **Reliability gate.** Scores below the calibrated threshold, with
  too few hits, or from too-short text route to human review, and
  acting on a blocked decision without a confirmed approval raises.
  Proof: `tests/test_gate.py`.
- **Confirmation gate.** Approvals are named-person, single-use,
  scoped, and expiring. Bypass, reject, absent, low-confidence, and
  self-contradicting-consent paths are all tested.
- **PII redaction.** Card numbers, email addresses, phone numbers,
  and SSNs are redacted before scoring. Proof: `tests/test_redaction.py`.
- **Row cap.** Fetches use `fetchmany(MAX + 1)`; no `fetchall`, no
  LIMIT rewriting. Proof: `tests/test_store_cap_budget_email_brand.py`.
- **Negative costs rejected**, never clamped to zero.
- **Email dry-run by default**; sending is refused in CI and no
  credentials exist in this repo.

## Reporting a vulnerability

If you find a security issue in this demo, please open an issue
describing it without including any real personal or financial data.
Do not use this repo's email channel to send sensitive information:
it is a simulation, not a secure reporting channel.

## Not investment advice

Sentiment scores produced here are research signals over synthetic
text. They are not investment, credit, or trading advice, and they
must not be used to make real financial decisions.

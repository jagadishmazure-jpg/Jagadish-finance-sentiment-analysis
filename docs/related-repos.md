# Related repos

Cross-links instead of duplication. These are sibling portfolio
repos in the same series; each covers its own slice, and this repo
does not re-implement them.

- **finance-compliance-rag** — retrieval over compliance material
  and auditable policy answers; this repo's redaction and gating
  patterns are the shared hygiene, not a copy of that pipeline.
- **finance-kyc-aml-pipeline** — customer due-diligence and
  screening workflows; where sentiment here is a research signal,
  that repo's outputs are compliance decisions with their own
  audit trail.
- **finance-credit-memo** — credit underwriting memos from
  borrower data; sentiment signals from this repo could feed a
  memo's qualitative section, but the memo repo owns the credit
  decision and its explainability.
- **finance-portfolio-risk-agent** — continuous portfolio risk
  monitoring and threshold alerts; a gated sentiment signal could
  be one input to its risk summaries, not a replacement for them.
- **finance-bank-in-a-box** — multi-agent orchestration across
  investment, risk, and compliance; this repo is one capability
  such an orchestrator could call, behind its own gate.
- **finance-governance-poc** — governance, explainability, and
  auditability for finance AI; the threat model and ADRs here are
  written to be consistent with that repo's governance view.
- **finance-data-validation** — data contracts and validation for
  finance inputs; an adopter should validate transcripts and
  filings there before scoring them here.
- **fraud-detection-agents** (existing portfolio repo) — fraud
  flagging and triage; sentiment is a different signal family and
  is deliberately not mixed into fraud scoring here.
- **llm-evals-observability** — general LLM evaluation and
  observability; the judge probes here are the finance-sentiment
  instance of that discipline, scoped to this repo's labeled set.

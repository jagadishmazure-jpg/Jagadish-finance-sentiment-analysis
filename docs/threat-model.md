# Threat model

## Assets

- Synthetic documents and scores (low sensitivity, but treated as
  if they matter: the controls are the demo).
- Human approvals and review decisions (integrity-critical: a
  forged approval turns a blocked signal into an action).
- Judge evaluations (integrity-critical: a biased judge that looks
  clean misleads calibration).

## STRIDE sketch

- **Spoofing:** a different person confirming someone else's
  approval. Mitigation: approver name must match the approval;
  mismatch raises. Residual: names are strings, not identities;
  a production system needs real authentication.
- **Tampering:** editing a score or bypassing the gate by reading
  the base table directly. Mitigation: authorizer denies direct
  reads and writes on guarded connections; gate `act()` has no
  bypass flag. Residual: the unguarded seeding connection must
  never be exposed to application code.
- **Repudiation:** "I never approved that." Mitigation:
  single-use approvals with scope and expiry; an adopter must
  persist the approval record (this scaffold keeps it in memory).
- **Information disclosure:** PII in source text leaking into
  scores, logs, or outputs. Mitigation: redaction before scoring,
  covering cards and emails as well as phones and SSNs. Residual:
  redaction is pattern-based; unusual formats can slip through,
  so review queues should still treat outputs as sensitive.
- **Denial of service:** unbounded result sets. Mitigation:
  fetch-time row cap. Residual: the cap must be set per call site.
- **Elevation of privilege:** a judge or agent marking its own
  output as approved. Mitigation: approvals require a named human
  approver distinct from the requester path, and the stub judge
  cannot create approvals at all.

## LLM-specific notes

- **Prompt injection via document text:** documents are scored by
  a lexicon, not by a model, so injected instructions in text
  cannot change the scorer's behaviour. If a live judge is added,
  its prompt must treat document text as data, and injection
  tests must be added before that judge touches decisions.
- **Judge bias:** position, length, and self-preference probes
  exist for exactly this risk; a live judge must pass them on a
  fresh set, not just on the stub's probe sets.
- **Over-reliance:** the reliability gate is the control against
  treating a fluent or confident-looking score as a decision.

## ADRs

See `docs/adr/`: 001 lexicon-first scoring, 002 view-only reads,
003 stub judge by default.

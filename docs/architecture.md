# Architecture

```mermaid
flowchart LR
    A[Synthetic transcripts<br/>and filing excerpts] --> B[PII redaction<br/>cards, emails, phones, SSNs]
    B --> C[Lexicon scorer<br/>deterministic, auditable]
    C --> D[Labeled-set evaluation<br/>precision / recall / F1]
    C --> E[Stub judge + bias probes<br/>both orders, ties excluded]
    C --> F[Reliability gate<br/>threshold, hits, length]
    F -->|ACT| G[Signal output]
    F -->|HUMAN_REVIEW| H[Confirmation gate<br/>named, single-use, expiring]
    H -->|confirmed| G
    D --> I[SQLite store<br/>views only, authorizer]
    E --> I
```

Reading rule: application code reads `v_documents` and `v_scores`
only. The authorizer enforces that at the database layer, not by
convention. Seeding happens before the authorizer is installed.

See also `knowledge/architecture.md` for the same diagram with
notes on each component.

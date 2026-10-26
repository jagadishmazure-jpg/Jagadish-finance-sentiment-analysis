# Architecture notes (Mermaid)

## Pipeline

```mermaid
flowchart LR
    A[Synthetic transcripts<br/>and filing excerpts] --> B[PII redaction]
    B --> C[Lexicon scorer]
    C --> D[Labeled-set evaluation]
    C --> E[Stub judge + bias probes]
    C --> F[Reliability gate]
    F -->|ACT| G[Signal output]
    F -->|HUMAN_REVIEW| H[Confirmation gate]
    H -->|confirmed| G
```

## Store access

```mermaid
flowchart TD
    App[Application code] -->|SELECT| V1[v_documents]
    App -->|SELECT| V2[v_scores]
    V1 -->|source = view| T1[documents base table]
    V2 -->|source = view| T2[scores base table]
    App -.->|denied| T1
    App -.->|denied| T2
    App -.->|denied| SM[sqlite_master]
```

Notes:

- The scorer is deterministic: same text, same score, always.
  That is a feature for audit, and a limitation for language
  understanding (see `docs/limitations.md`).
- The gate sits between scoring and any consumer. There is no
  code path from scorer to output that skips it.
- The judge never writes scores and never creates approvals. It
  only labels, so a compromised or biased judge cannot by itself
  move a signal to action.
- The fictional firm used in examples is Hollowbrook Capital, an
  invented investment research firm. It is not a real business,
  and no example in this repo describes a real company.

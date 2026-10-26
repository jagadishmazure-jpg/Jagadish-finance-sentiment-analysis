# Finance Sentiment Analysis

> **Synthetic data only, always.** Every transcript and filing
> excerpt in this repo is invented, about invented companies, for
> an invented firm — Hollowbrook Capital, a fictional investment
> research firm used in examples. Nothing here is real market data,
> real disclosure, or investment advice. No affiliation with any
> university, programme, or institution is claimed.

A system that reads synthetic earnings-call transcripts and
SEC-filing-style excerpts, turns them into sentiment signals for
investment and credit research, and then asks the question that
matters before anyone acts: can this score be trusted enough to
use? Weak scores do not slip through — they go to a human.

## Recruiter summary

- **Problem:** A sentiment number on its own hides whether it
  deserves to be acted on.
- **Approach:** Deterministic lexicon scorer, hand-labeled
  synthetic set, stub-judge evaluation with bias probes, and a
  reliability gate that routes weak scores to human review.
- **Proof (real run, n=12 synthetic items):** accuracy 12/12,
  macro precision/recall/F1 1.0, judge-vs-human kappa 1.0 with a
  Wilson 95% interval of 0.7575–1.0, gate acted on 8 and sent 4 to
  review, order-flip / length-bias / self-preference rates 0.0 on
  the probe sets used. Regression-check numbers on a tiny invented
  set — not claims about real markets.
- **Guardrails:** view-only SQLite reads, tested confirmation
  gates, PII redaction (cards, emails, phones, SSNs), fetch-time
  row caps, negative-cost rejection, dry-run email by default.

## How it works

```text
synthetic text → PII redaction → lexicon scorer → labeled-set evaluation
                                          → stub judge + bias probes
                                          → reliability gate → ACT or HUMAN_REVIEW
```

Full walkthrough: [docs/how-it-works.md](docs/how-it-works.md) ·
Architecture: [docs/architecture.md](docs/architecture.md) ·
Real code and output: [docs/code-and-output.md](docs/code-and-output.md)

## Run it (offline, standard library only)

```bash
python3 -m pytest tests/ -q
PYTHONPATH=src python3 -m finance_sentiment.demo
```

No dependencies, no network, no API keys. The live-model judge
hook exists but is never required for tests; without a callable
it raises instead of silently substituting anything.
See [docs/how-to-run.md](docs/how-to-run.md).

## What is in here

- **(1) Deterministic lexicon scorer** — negation window,
  intensifier boost, clipped score, auditable by hand.
- **(2) Ground-truth labeling harness** — 12 hand-labeled
  synthetic items (4 positive, 4 negative, 4 neutral).
- **(3) LLM-as-judge evaluation** — deterministic stub judge plus
  an optional live-model hook; position, length, and
  self-preference bias probes in both orders, ties excluded from
  denominators, order-flip rate, Cohen's kappa vs human labels,
  Wilson confidence intervals.
- **(4) Reliability decision gate** — blocks acting on scores
  below a calibrated threshold (0.30, min 2 hits, min 8 words)
  and routes them to human review.
- **(5) Precision/recall reporting** — per-label and macro, with
  counts, on the labeled set.

## Guardrails (each proved by a named test)

See [docs/guardrails.md](docs/guardrails.md) for the full table,
including the SQLite view-aware authorizer, the confirmation
gate's bypass/reject/absent/low-confidence/contradicting-consent
tests, card-and-email PII redaction, the fetch-time row cap, and
negative-cost rejection. If this README says something is
enforced, a test proves it.

## Docs

- [docs/recruiter-summary.md](docs/recruiter-summary.md) — recruiter summary
- [docs/purpose.md](docs/purpose.md) — purpose and audience
- [docs/architecture.md](docs/architecture.md) — architecture (Mermaid)
- [docs/how-it-works.md](docs/how-it-works.md) — step by step
- [docs/code-and-output.md](docs/code-and-output.md) — real excerpts, real output
- [docs/how-to-run.md](docs/how-to-run.md) — offline first, optional live judge
- [docs/guardrails.md](docs/guardrails.md) — guardrails and proof tests
- [docs/limitations.md](docs/limitations.md) — limitations and known failures
- [docs/built-vs-planned.md](docs/built-vs-planned.md) — built vs planned
- [docs/implementation-guide.md](docs/implementation-guide.md) — adopter guide
- [docs/interview-points.md](docs/interview-points.md) — interview points
- [docs/threat-model.md](docs/threat-model.md) — threat model + ADRs
  ([001](docs/adr/001-lexicon-first.md), [002](docs/adr/002-view-only-reads.md), [003](docs/adr/003-stub-judge-by-default.md))
- [docs/related-repos.md](docs/related-repos.md) — related repos, cross-links
- [knowledge/notes.md](knowledge/notes.md) — distilled notes
- [knowledge/architecture.md](knowledge/architecture.md) — Mermaid architecture notes
- [knowledge/use-case-patterns.md](knowledge/use-case-patterns.md) — distilled patterns

## Built / Written-not-run / Planned

| Item | Status |
|---|---|
| Lexicon scorer, labeled set, precision/recall, stub judge + probes, kappa + Wilson, reliability + confirmation gates, authorizer, redaction, row cap, budget, email dry-run, offline demo | Built, tested, suite green (72 tests) |
| Live-model judge evaluation | Written-not-run: hook exists, no model configured, no test depends on it |
| Real-transcript validation, deployment, package release | Planned: none claimed, none built |

## Limitations, honestly

The 12-item set is a regression check, not validation; the stub
judge's kappa measures the scorer, not a model; text without
lexicon words defaults to neutral. Read
[docs/limitations.md](docs/limitations.md) before quoting any
number from this repo.

## License and security

MIT — see [LICENSE](LICENSE). Security policy and reporting:
[SECURITY.md](SECURITY.md).

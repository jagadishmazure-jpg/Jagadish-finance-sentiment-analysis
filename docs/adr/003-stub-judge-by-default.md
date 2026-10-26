# ADR 003: Stub judge by default, live judge opt-in

- **Status:** Accepted
- **Context:** Tests must pass offline with no keys and no network,
  and a judge result must never silently be a model result when
  the reader expects a stub (or vice versa).
- **Decision:** The default judge is a deterministic lexicon stub
  that names itself as a stub in every rationale. A live judge is
  available only through an explicitly supplied callable; with none,
  it raises instead of falling back.
- **Consequences:** Judge kappa in this repo measures the scorer,
  not a model, and is reported as such. Adopters must re-run all
  probes when they plug in a real model.

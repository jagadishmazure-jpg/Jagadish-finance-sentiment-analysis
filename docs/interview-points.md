# Interview points

- **"Why a lexicon first?"** Because it is auditable and
  reproducible. A model score that cannot be recomputed by hand is
  a poor baseline for a regulated workflow; the lexicon gives the
  team something to argue with before any model is introduced.
- **"What is the gate actually protecting?"** Acting on a weak
  signal. The gate combines magnitude, support (hit count), and
  length, and its blocked path has no bypass: only a confirmed
  human approval proceeds, and that approval is named, scoped,
  single-use, and expiring.
- **"Why both orders for the judge?"** A judge that prefers the
  first-presented candidate will look accurate in one order and
  wrong in the other. Running both orders and excluding ties from
  the denominator separates real preference from presentation
  artefacts.
- **"Why Wilson, not just accuracy?"** With n=12, accuracy alone
  is misleading: 12/12 still leaves a wide interval (0.7575–1.0).
  Reporting the interval is the difference between a demo and a
  claim.
- **"How does the authorizer work?"** SQLite passes the view name
  as the source argument for base-table reads that happen through
  a view, and no source for direct reads. The authorizer keys on
  that argument, so enforcement lives in the database layer, not
  in query-writing discipline. The one exception, the empty-column
  view-expansion probe, is documented and bounded.
- **"What would you do next with real data?"** Grow the labeled
  set with proper licensing, calibrate the threshold on it, add a
  real judge behind the hook, and re-run every probe before any
  score reaches a decision-maker.
- **"What is the known failure you are proudest of keeping?"**
  The neutral-default problem: text without lexicon words scores
  neutral even when the meaning is not neutral. It stays visible
  in limitations, and the gate's routing to review is the honest
  mitigation.

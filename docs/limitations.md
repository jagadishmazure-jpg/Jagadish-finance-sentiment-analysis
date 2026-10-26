# Limitations and known failures

Kept visible on purpose. These are not footnotes; they bound every
number in this repo.

1. **Tiny, invented labeled set (n=12).** Accuracy 12/12 is a
   regression check, not evidence about real calls. One item is
   ~8 points. The Wilson interval (0.7575–1.0) is the honest
   headline, not the 1.0.
2. **Lexicon blindness.** Sarcasm, negation beyond 3 tokens,
   sector jargon, and multi-sentence hedging are missed or
   mis-scored. Example kept as a known miss: "results were not
   strong" is handled (negation window), but "we would not describe
   the quarter as strong in any sense" may escape the window
   depending on wording. The scorer has no parser and no context.
3. **Stub judge, not a model.** Judge kappa 1.0 measures the
   scorer against itself through the stub. It says nothing about
   any live model's judgement. Bias rates of 0.0 on the probes are
   the expected result for a deterministic, tag-blind stub, not
   evidence that real judges are unbiased.
4. **Neutral is the default, not a finding.** Text with no lexicon
   hits scores neutral, even if the real meaning is negative but
   expressed without listed words. Absence of signal is routed to
   review by the gate, which is the mitigation, not a fix.
5. **No real-data validation.** Nothing here has been run on real
   transcripts or filings, and nothing should be: this repo is
   synthetic-only by design.
6. **Email "send" is a simulation.** The opted-in path records a
   result; it does not connect to any mail server. An adopter must
   replace `_deliver` and re-prove delivery before relying on it.
7. **Authorizer probe exception.** SQLite's empty-column
   view-expansion probe is allowed for known tables/views because
   it names no column and returns no value. It is documented in
   `store.py` and bounded to those tables; it is not a general
   bypass, and direct column reads are still denied.

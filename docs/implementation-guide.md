# Implementation guide (for adopters)

## Adopt the scorer

1. Copy `lexicon.py` and `scorer.py`. Keep the lexicon in one
   file so a reviewer can audit every weight.
2. Add your domain words with tests that pin each word's sign and
   a negation case. Do not tune weights on the evaluation set and
   then report that set as validation.
3. Keep scoring deterministic and offline. If you add a model,
   keep the lexicon as the fallback and report both.

## Adopt the gate

1. Calibrate the threshold on a labeled set larger than this
   repo's 12 items, and report the calibration set size with the
   threshold. A threshold chosen on n=12 is a placeholder.
2. Wire `HUMAN_REVIEW` to a real review queue, not a log file.
   The confirmation gate's approval object is the audit record:
   keep approver, scope, timestamp, and expiry with the decision.
3. Never add a "force act" path. If an emergency override is ever
   needed, it should be a new, separately approved decision type
   with its own tests, not a flag on `act()`.

## Adopt the store

1. Seed before installing the authorizer; the guarded connection
   cannot write by design.
2. Read through views only. If you add a view, add it to
   `ALLOWED_VIEWS` and add a test that the view reads and the
   underlying table does not.
3. Keep the fetch cap at the call site (`fetchmany`), and size it
   from the consumer's real need, not from the table's size.

## Adopt the judge evaluation

1. Replace the stub with a real judge behind `LiveJudgeHook`, then
   re-run kappa, Wilson, and all three bias probes on a fresh set.
2. Keep ties out of flip denominators and always print the
   denominator with the rate. A rate without a denominator is not
   a result.
3. Monitor drift: re-run the probes on a schedule and alert when
   kappa falls or flip rates rise, rather than trusting one run.

## What not to adopt blindly

- The 12-item set is a smoke test, not training or validation data.
- The email simulation is not a mailer.
- The lexicon is not a financial model and its output is not advice.

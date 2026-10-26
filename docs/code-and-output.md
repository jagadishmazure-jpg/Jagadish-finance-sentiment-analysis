# Real code excerpts and their real output

## Scorer

```python
from finance_sentiment.scorer import score_text

result = score_text(
    "Revenue grew strongly, margins expanded, and demand remained "
    "robust across regions.")
print(result.label, result.score, result.hits, result.confidence)
```

Real output (from the repo's own code, run offline):

```text
positive 1.0 3 0.6
```

## Reliability gate

```python
from finance_sentiment.gate import ReliabilityGate
from finance_sentiment.scorer import score_text

gate = ReliabilityGate()
decision = gate.decide(score_text("Revenue grew a little."))
print(decision.action, decision.reason)
```

Real output:

```text
HUMAN_REVIEW too few sentiment hits
```

## Full demo (n=12 synthetic items)

Run: `PYTHONPATH=src python3 -m finance_sentiment.demo`

Real output:

```json
{
  "n": 12,
  "accuracy": 1.0,
  "correct": 12,
  "macro_precision": 1.0,
  "macro_recall": 1.0,
  "macro_f1": 1.0,
  "judge_kappa_vs_human": 1.0,
  "judge_agreement_wilson": [0.7575, 1.0],
  "gate_act": 8,
  "gate_review": 4,
  "order_flip": {"flips": 0, "considered": 4, "rate": 0.0},
  "length_bias": {"flips": 0, "considered": 12, "rate": 0.0},
  "self_preference": {"wins": 0, "considered": 2, "rate": 0.0}
}
```

Reading note: the 4 routed to review are the 4 neutral items, whose
score is 0 and therefore below the 0.30 threshold. A perfect score
on 12 invented, clearly-worded items proves the pipeline runs and
the tests pass; it proves nothing about real earnings calls, which
is why the Wilson interval (0.7575–1.0) is reported next to the
headline rate.

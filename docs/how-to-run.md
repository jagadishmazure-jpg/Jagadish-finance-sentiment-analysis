# How to run (offline first)

Prerequisites: Python 3.12+ and pytest. Standard library only; no
dependencies to install, no network, no API keys, no accounts.

```bash
# Tests (from the repo root)
python3 -m pytest tests/ -q

# Demo report (real numbers from the labeled set)
PYTHONPATH=src python3 -m finance_sentiment.demo
```

## Optional: live-model judge hook (never required)

```python
from finance_sentiment.judge import LiveJudgeHook

# With no callable this raises JudgeNotConfigured by design.
# Pass your own callable to use a real model; tests never do this.
hook = LiveJudgeHook(judge_callable=my_model_function)
```

There is no cloud step, no deployment, and no package release in
this repo. If an adopter adds a live model, cost inputs go through
`budget.validate_cost`, which rejects negative amounts, and judge
drift should be monitored by re-running the kappa and bias probes
on a fresh labeled set.

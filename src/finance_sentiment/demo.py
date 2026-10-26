"""Offline demo: score the labeled set, evaluate, gate, and report.

Run:  PYTHONPATH=src python3 -m finance_sentiment.demo
All numbers printed come from this run; copy them, with their sample
size (n=12), into the README and docs/code-and-output.md.
"""

from .gate import ReliabilityGate
from .judge import StubJudge, length_bias_rate, order_flip_rate, self_preference_rate
from .labeling import LABELED, labeled_pairs
from .metrics import cohen_kappa, macro_precision_recall, wilson_ci
from .scorer import score_text


def run_demo():
    texts, human = labeled_pairs()
    predicted = [score_text(t).label for t in texts]
    judge = StubJudge()
    judge_labels = [judge.judge(t).label for t in texts]
    gate = ReliabilityGate()
    decisions = [gate.decide(score_text(t)).action for t in texts]
    metrics = macro_precision_recall(human, predicted)
    kappa = cohen_kappa(human, judge_labels)
    correct = sum(1 for t, p in zip(human, predicted) if t == p)
    pairs = [(LABELED[i]["text"], LABELED[j]["text"])
             for i, j in [(0, 1), (3, 4), (6, 7), (9, 10)]]
    self_pairs = [(LABELED[i]["text"], LABELED[j]["text"])
                  for i, j in [(0, 1), (3, 4)]]
    report = {
        "n": len(texts),
        "accuracy": metrics["accuracy"],
        "correct": correct,
        "macro_precision": metrics["macro_precision"],
        "macro_recall": metrics["macro_recall"],
        "macro_f1": metrics["macro_f1"],
        "per_label": metrics["per_label"],
        "judge_kappa_vs_human": kappa,
        "judge_agreement_wilson": wilson_ci(
            sum(1 for t, p in zip(human, judge_labels) if t == p), len(human)),
        "gate_act": decisions.count("ACT"),
        "gate_review": decisions.count("HUMAN_REVIEW"),
        "order_flip": order_flip_rate(pairs),
        "length_bias": length_bias_rate(texts),
        "self_preference": self_preference_rate(self_pairs),
    }
    return report


def main():
    import json
    print(json.dumps(run_demo(), indent=2))


if __name__ == "__main__":
    main()

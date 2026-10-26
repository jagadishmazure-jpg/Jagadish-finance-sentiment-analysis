"""Precision/recall, Cohen's kappa, and Wilson intervals.

All functions work on plain label lists. Ties are never a concept here;
they matter in the judge module, where tied pairs are excluded from
the order-flip denominator (see judge.py).
"""

import math

LABELS = ("positive", "negative", "neutral")


def confusion(y_true, y_pred, positive_label):
    tp = sum(1 for t, p in zip(y_true, y_pred) if t == positive_label and p == positive_label)
    fp = sum(1 for t, p in zip(y_true, y_pred) if t != positive_label and p == positive_label)
    fn = sum(1 for t, p in zip(y_true, y_pred) if t == positive_label and p != positive_label)
    tn = sum(1 for t, p in zip(y_true, y_pred) if t != positive_label and p != positive_label)
    return {"tp": tp, "fp": fp, "fn": fn, "tn": tn}


def precision_recall(y_true, y_pred, positive_label):
    c = confusion(y_true, y_pred, positive_label)
    precision = c["tp"] / (c["tp"] + c["fp"]) if (c["tp"] + c["fp"]) else 0.0
    recall = c["tp"] / (c["tp"] + c["fn"]) if (c["tp"] + c["fn"]) else 0.0
    f1 = (
        2 * precision * recall / (precision + recall)
        if (precision + recall)
        else 0.0
    )
    return {"label": positive_label, **c, "precision": round(precision, 4),
            "recall": round(recall, 4), "f1": round(f1, 4)}


def macro_precision_recall(y_true, y_pred):
    per_label = [precision_recall(y_true, y_pred, label) for label in LABELS]
    n = len(per_label)
    return {
        "per_label": per_label,
        "macro_precision": round(sum(d["precision"] for d in per_label) / n, 4),
        "macro_recall": round(sum(d["recall"] for d in per_label) / n, 4),
        "macro_f1": round(sum(d["f1"] for d in per_label) / n, 4),
        "accuracy": round(sum(1 for t, p in zip(y_true, y_pred) if t == p) / len(y_true), 4)
        if y_true else 0.0,
    }


def cohen_kappa(y_true, y_pred):
    """Cohen's kappa between two label sequences."""
    n = len(y_true)
    if n == 0:
        return 0.0
    observed = sum(1 for t, p in zip(y_true, y_pred) if t == p) / n
    expected = 0.0
    for label in set(y_true) | set(y_pred):
        p_true = sum(1 for t in y_true if t == label) / n
        p_pred = sum(1 for p in y_pred if p == label) / n
        expected += p_true * p_pred
    if expected == 1.0:
        return 1.0
    return round((observed - expected) / (1.0 - expected), 4)


def wilson_ci(successes, trials, z=1.96):
    """Wilson score interval for a proportion. Returns (low, high)."""
    if trials <= 0:
        return (0.0, 0.0)
    p = successes / trials
    denom = 1 + z * z / trials
    centre = (p + z * z / (2 * trials)) / denom
    half = (z / denom) * math.sqrt(p * (1 - p) / trials + z * z / (4 * trials * trials))
    return (round(max(0.0, centre - half), 4), round(min(1.0, centre + half), 4))

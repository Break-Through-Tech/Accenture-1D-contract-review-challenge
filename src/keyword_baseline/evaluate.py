"""Evaluation step: join labels to the (label-free) predictions, pick one threshold per category.

Run from the repo root:
  .venv/bin/python -m src.keyword_baseline.evaluate
Masked pairs (mask == 1) are dropped. Threshold = integer in 1..max possible score
(2 x anchor groups + 1 x support groups); detection = score >= threshold. Pick the highest
F1; tie -> higher recall; tie -> lower threshold.
"""
import hashlib
import json
from fractions import Fraction
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RULES = ROOT / "configs" / "keyword_rules_v1.json"
PRED = ROOT / "reports" / "keyword_baseline" / "validation_predictions.csv"
LABELS = ROOT / "data" / "gate3" / "validation_chunk_labels_768_512.csv"
OUT = ROOT / "reports" / "keyword_baseline"
THRESHOLDS = ROOT / "configs" / "keyword_thresholds_v1.json"
LOW_SUPPORT = 20


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def counts(g, th):
    pred = g.score >= th
    pos = g.target == 1
    return int((pred & pos).sum()), int((pred & ~pos).sum()), int((~pred & pos).sum()), int((~pred & ~pos).sum())


def metrics(tp, fp, fn, tn):
    p = tp / (tp + fp) if tp + fp else 0.0
    r = tp / (tp + fn) if tp + fn else 0.0
    f = 2 * tp / (2 * tp + fp + fn) if 2 * tp + fp + fn else 0.0
    return p, r, f


def main():
    rules = json.load(open(RULES))
    pred = pd.read_csv(PRED)
    lab = pd.read_csv(LABELS, usecols=["chunk_id", "category", "target", "mask"])
    m = pred.merge(lab, on=["chunk_id", "category"], how="left", validate="one_to_one")
    assert m.target.notna().all() and len(m) == 24810
    unmasked = m[m["mask"] == 0]
    print("pairs:", len(m), "unmasked:", len(unmasked), "masked:", len(m) - len(unmasked))

    search, final, chosen = [], [], {}
    for cat, c in rules["categories"].items():
        max_score = sum(2 if g["role"] == "anchor" else 1 if g["role"] == "support" else 0 for g in c["groups"])
        g = unmasked[unmasked.category == cat]
        best = None
        for th in range(1, max_score + 1):
            tp, fp, fn, tn = counts(g, th)
            p, r, f = metrics(tp, fp, fn, tn)
            search.append({"category": cat, "threshold": th, "tp": tp, "fp": fp, "fn": fn, "tn": tn,
                           "precision": p, "recall": r, "f1": f})
            key = (Fraction(2 * tp, 2 * tp + fp + fn) if 2 * tp + fp + fn else Fraction(0), Fraction(tp, tp + fn) if tp + fn else Fraction(0), -th)
            if best is None or key > best[0]:
                best = (key, th, tp, fp, fn, tn)
        _, th, tp, fp, fn, tn = best
        p, r, f = metrics(tp, fp, fn, tn)
        n_pos = tp + fn
        contracts = int(g[g.target == 1].title.nunique())
        chosen[cat] = th
        final.append({"category": cat, "threshold": th, "max_possible_score": max_score, "tp": tp, "fp": fp, "fn": fn,
                      "tn": tn, "support": n_pos, "positive_contracts": contracts, "predicted_positive": tp + fp,
                      "precision": round(p, 4), "recall": round(r, 4), "f1": round(f, 4),
                      "low_support_warning": n_pos < LOW_SUPPORT})
    res = pd.DataFrame(final)
    macro = float(res.f1.mean())
    TP, FP, FN = res.tp.sum(), res.fp.sum(), res.fn.sum()
    micro = 2 * TP / (2 * TP + FP + FN)
    pd.DataFrame(search).to_csv(OUT / "validation_threshold_search.csv", index=False)
    res.to_csv(OUT / "validation_metrics.csv", index=False)
    json.dump({
        "rule_set_version": rules["rule_set_version"],
        "rules_sha256": sha256(RULES),
        "predictions_sha256": sha256(PRED),
        "threshold_rule": "integers 1..max possible score; highest F1, tie higher recall, tie lower threshold; unmasked pairs only",
        "thresholds": chosen,
        "validation_macro_f1": round(macro, 4),
        "validation_micro_f1": round(float(micro), 4),
    }, open(THRESHOLDS, "w"), indent=2)
    print(res.to_string(index=False))
    print(f"macro-F1 {macro:.4f}  micro-F1 {micro:.4f}")


if __name__ == "__main__":
    main()

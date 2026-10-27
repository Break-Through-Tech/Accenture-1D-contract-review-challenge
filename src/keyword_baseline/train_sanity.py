"""Train sanity check: score the train chunks, pick thresholds on train, report F1 (bug check only, optimistic).

Run from the repo root:
  .venv/bin/python -m src.keyword_baseline.score_chunks --chunks data/gate3/train_chunks_768_512.csv \
      --out-prefix <dir>/train
  .venv/bin/python -m src.keyword_baseline.train_sanity --pred <dir>/train_predictions.csv
Uses the same masking and threshold rule as evaluate.py. Not a result: thresholds are tuned on the same data.
"""
import argparse
import json

import pandas as pd

from .evaluate import OUT, ROOT, RULES, max_possible_score, metrics, search_thresholds

LABELS = ROOT / "data" / "gate3" / "train_chunk_labels_768_512.csv"
NOTE = "train; optimistic; bug check only"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pred", required=True, help="train predictions CSV from score_chunks")
    ap.add_argument("--out", default=str(OUT / "train_sanity_metrics.csv"))
    args = ap.parse_args()
    rules = json.load(open(RULES))
    pred = pd.read_csv(args.pred)
    lab = pd.read_csv(LABELS, usecols=["chunk_id", "category", "target", "mask"])
    m = pred.merge(lab, on=["chunk_id", "category"], how="left", validate="one_to_one")
    assert m.target.notna().all() and len(m) == len(lab)
    unmasked = m[m["mask"] == 0]
    print("pairs:", len(m), "unmasked:", len(unmasked), "masked:", len(m) - len(unmasked))

    out = []
    for cat, c in rules["categories"].items():
        _, (_, th, tp, fp, fn, tn) = search_thresholds(unmasked[unmasked.category == cat], max_possible_score(c))
        out.append({"category": cat, "best_threshold": th, "tp": tp, "fp": fp, "fn": fn,
                    "f1": round(metrics(tp, fp, fn, tn)[2], 4), "note": NOTE})
    res = pd.DataFrame(out).sort_values("category")
    res.to_csv(args.out, index=False)
    print(res.to_string(index=False))


if __name__ == "__main__":
    main()

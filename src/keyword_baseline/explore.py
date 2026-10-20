"""Phase 2: print train spans and Gate 2 hard negatives for one or more categories.

Run from repo root: .venv/bin/python -m src.keyword_baseline.explore "Anti-Assignment" ...
"""
import sys

import pandas as pd

from src.keyword_baseline.data import REVIEW_CSV, load_train_spans

SEED = 20260904  # error-selection seed from CLAUDE.md
MAXCHARS = 420


def clip(text):
    text = " ".join(str(text).split())
    return text if len(text) <= MAXCHARS else text[:MAXCHARS] + " ..."


spans = load_train_spans(verbose=False)
review = pd.read_csv(REVIEW_CSV)
for cat in sys.argv[1:]:
    print(f"\n{'=' * 20} {cat} {'=' * 20}")
    sub = spans[spans["category"] == cat]
    print(f"--- {min(5, len(sub))} random TRAIN spans (of {len(sub)}) ---")
    for i, t in enumerate(sub.sample(5, random_state=SEED)["text"], 1):
        print(f"[P{i}] {clip(t)}")
    hn = review[(review["target_category"] == cat) & (review["example_type"] == "HARD NEGATIVE")]
    print("--- 5 hard negatives (gate2_excerpt_review.csv) ---")
    for i, (src, t) in enumerate(zip(hn["source_category"], hn["answer_text"]), 1):
        print(f"[N{i}] (is really: {src}) {clip(t)}")

"""Phase 2 helper: load the 10-category train spans, with leakage and manifest checks."""
import json
import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
SPLITS = ROOT / "data" / "splits"
REVIEW_CSV = ROOT / "data" / "cuad" / "gate2_excerpt_review.csv"


def load_train_spans(verbose=True):
    """Return a DataFrame of train spans (title, category, text, start) for the 10 core categories."""
    # Checks for leakage and confirms the train.json matches the manifest
    manifest = pd.read_csv(f"{SPLITS}/split_manifest.csv")
    train_titles = set(manifest.loc[manifest["split"] == "train", "title"])
    val_titles = set(manifest.loc[manifest["split"] == "validation", "title"])
    assert len(train_titles) == 326 and len(val_titles) == 82
    assert train_titles.isdisjoint(val_titles)

    d = json.load(open(f"{SPLITS}/train.json"))["data"]
    assert {c["title"] for c in d} == train_titles
    if verbose:
        print("train.json titles match manifest train titles: True")

    # Pulls 10 categories from excerpt
    categories = sorted(pd.read_csv(REVIEW_CSV)["target_category"].unique())
    assert len(categories) == 10

    rows = []
    for contract in d:
        for qa in contract["paragraphs"][0]["qas"]:
            category = re.search(r'related to "(.+?)"', qa["question"]).group(1)
            if category not in categories:
                continue
            for a in qa["answers"]:
                rows.append({"title": contract["title"], "category": category,
                             "text": a["text"], "start": a["answer_start"]})
    spans = pd.DataFrame(rows)

    if verbose:
        print(spans.groupby("category").agg(spans=("text", "size"), contracts=("title", "nunique")))

    assert set(spans["title"]) <= train_titles
    if verbose:
        print("leakage guard passed:", spans["title"].nunique(), "contracts, all in train")
    return spans


if __name__ == "__main__":
    load_train_spans()

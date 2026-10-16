import json
import pandas as pd
import re

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

## Checks for leakage and confirms the train.json matches the manifest
SPLITS = ROOT / "data" / "splits"

manifest = pd.read_csv(f"{SPLITS}/split_manifest.csv")
train_titles = set(manifest.loc[manifest["split"] == "train", "title"])
val_titles = set(manifest.loc[manifest["split"] == "validation", "title"])

assert len(train_titles) == 326 and len(val_titles) == 82
assert train_titles.isdisjoint(val_titles)

d = json.load(open(f"{SPLITS}/train.json"))["data"]
print("train.json titles match manifest train titles:", {c["title"] for c in d} == train_titles)


## Pulls 10 categories from excerpt
REVIEW_CSV = ROOT / "data" / "cuad" / "gate2_excerpt_review.csv"

CATEGORIES = sorted(pd.read_csv(REVIEW_CSV)["target_category"].unique())

assert len(CATEGORIES) == 10

rows = []
for contract in d:
    for qa in contract["paragraphs"][0]["qas"]:
        category = re.search(r'related to "(.+?)"', qa["question"]).group(1)
        if category not in CATEGORIES:
            continue
        for a in qa["answers"]:
            rows.append({"title": contract["title"], "category": category,
                         "text": a["text"], "start": a["answer_start"]})

spans = pd.DataFrame(rows)

print(spans.groupby("category").agg(spans=("text", "size"), contracts=("title", "nunique")))

assert set(spans["title"]) <= train_titles
print("leakage guard passed:", spans["title"].nunique(), "contracts, all in train")


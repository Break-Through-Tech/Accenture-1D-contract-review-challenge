"""Score a chunk file with the keyword rules. Writes predictions (no labels) and match evidence.

Run from the repo root, e.g.
  .venv/bin/python -m src.keyword_baseline.score_chunks --chunks data/gate3/validation_chunks_768_512.csv \
      --out-prefix reports/keyword_baseline/validation
Labels are never read here; they are joined later in a separate evaluation step.
"""
import argparse
import json
from pathlib import Path

import pandas as pd

from .normalize import normalize_with_map
from .scorer import prepare_category, score_text

ROOT = Path(__file__).resolve().parents[2]
RULES = ROOT / "configs" / "keyword_rules_v1.json"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chunks", required=True)
    ap.add_argument("--out-prefix", required=True)
    ap.add_argument("--rules", default=str(RULES))
    ap.add_argument("--check-offsets", action="store_true", help="assert source slice matches the phrase")
    args = ap.parse_args()

    rules = json.load(open(args.rules))
    version = rules["rule_set_version"]
    prepared = {cat: prepare_category(c) for cat, c in rules["categories"].items()}
    cats = sorted(prepared)
    chunks = pd.read_csv(args.chunks, usecols=["chunk_id", "title", "text"])

    pred_rows, ev_rows = [], []
    for chunk_id, title, text in zip(chunks.chunk_id, chunks.title, chunks.text):
        normalized = normalize_with_map(text)
        for cat in cats:
            score, matches = score_text(text, prepared[cat], args.check_offsets, normalized)
            live = [m for m in matches if not m["vetoed"]]
            pred_rows.append({
                "chunk_id": chunk_id, "title": title, "category": cat, "rule_set_version": version,
                "score": score, "matched_groups": ";".join(sorted({m["group_id"] for m in live})),
                "n_vetoed_matches": len(matches) - len(live),
            })
            for m in matches:
                ev_rows.append({"chunk_id": chunk_id, "category": cat, **{k: m[k] for k in
                                ("rule_id", "group_id", "role", "src_start", "src_end", "vetoed")}})
    prefix = Path(args.out_prefix)
    prefix.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(pred_rows).to_csv(f"{prefix}_predictions.csv", index=False)
    pd.DataFrame(ev_rows).to_csv(f"{prefix}_match_evidence.csv", index=False)
    print(f"{len(pred_rows)} prediction rows, {len(ev_rows)} match rows -> {prefix}_*.csv")


if __name__ == "__main__":
    main()

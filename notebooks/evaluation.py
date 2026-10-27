'''Locked evaluation rules shared by the validation evaluation (gate3_evaluation.ipynb) and the
official-test evaluation, so both use the same code. Its SHA-256 goes in the run receipt.

Implements the Glossary's Metric Calculation Rules, Low-Support Warnings, Paired Uncertainty
Intervals, Repeatable Error Selection and Error-Review Categories. Every function works on
"rows": one row per (baseline, chunk_id, category) with target, mask, detected, title and
context_group_id.
'''
import hashlib
import re
from pathlib import Path

import numpy as np
import pandas as pd

BOOTSTRAP_REPS = 10_000
BOOTSTRAP_SEED = 20260903
ERROR_SEED = 20260904
REVIEWER_SEED = 20260905
ERRORS_PER_GROUP = 5
LOW_SUPPORT_GROUPS = 20
SAMPLING_PROTOCOL_VERSION = "error_selection_v1"
ERROR_TYPES = ["false_positive", "false_negative"]

PRIMARY_CAUSES = ["gold_data", "chunking", "language_context", "baseline", "pipeline", "unresolved"]
SECONDARY_CAUSES = [
    "lexical_or_drafting_variation", "neighboring_category_confusion", "negation_exception_polarity_scope",
    "party_entity_coreference", "long_range_dependency_or_cross_reference", "generic_boilerplate",
    "keyword_coverage_proximity_veto_aggregation", "tfidf_vocabulary_weighting_linear_ranking",
    "threshold_tradeoff", "overlap_or_duplicate_concentration", "annotation_ambiguity_or_inconsistency",
    "other",  # needs a written explanation
]
REVIEW_FIELDS = ["primary_cause", "secondary_causes", "evidence_note", "confidence", "workflow_stage"]

AUTHORIZATION_FIELDS = ["approved_commit", "approver", "executor", "authorization_id", "workflow_sha256",
                        "chunking_config_sha256", "artifact_bundle_ids", "official_source_sha256",
                        "authorization_time", "permitted_action"]


def prf(tp, fp, fn):
    '''Precision, recall and F1, returning 0 wherever a denominator is 0. Works on scalars and arrays.'''
    tp, fp, fn = (np.asarray(x, dtype=float) for x in (tp, fp, fn))
    div = lambda a, b: np.divide(a, b, out=np.zeros_like(a), where=b > 0)
    return div(tp, tp + fp), div(tp, tp + fn), div(2 * tp, 2 * tp + fp + fn)


def check_predictions(pred, chunks, categories):
    '''Asserts one baseline's prediction contract: unique (chunk_id, category) keys, exactly 10 rows for
    every approved chunk and no others, finite scores, one threshold per category, and
    detected == (score >= threshold).'''
    assert not pred.duplicated(["chunk_id", "category"]).any(), "duplicate (chunk_id, category) keys"
    assert set(pred["chunk_id"]) == set(chunks["chunk_id"]), "chunk ids differ from the approved chunks"
    assert sorted(pred["category"].unique()) == sorted(categories)
    assert (pred.groupby("chunk_id").size() == len(categories)).all()
    assert np.isfinite(pred["score"]).all() and np.isfinite(pred["threshold"]).all(), "non-finite score"
    assert (pred.groupby("category")["threshold"].nunique() == 1).all(), "more than one threshold per category"
    assert pred["detected"].dtype == bool and (pred["detected"] == (pred["score"] >= pred["threshold"])).all()


def join_labels(pred, labels):
    '''Joins predictions to labels one-to-one on (chunk_id, category) and checks targets and masks are binary.'''
    m = pred.merge(labels[["chunk_id", "category", "target", "mask"]], on=["chunk_id", "category"],
                   how="outer", validate="one_to_one", indicator=True)
    assert (m["_merge"] == "both").all(), "predictions and labels don't match one-to-one"
    assert m["target"].isin([0, 1]).all() and m["mask"].isin([0, 1]).all(), "non-binary target or mask"
    return m.drop(columns="_merge")


def unmasked(rows):
    '''The evaluation units: masked pairs stay in the row-level file but never enter metrics or error lists.'''
    return rows[rows["mask"] == 0]


def with_outcomes(rows):
    pos, det = rows["target"] == 1, rows["detected"]
    return rows.assign(tp=det & pos, fp=det & ~pos, fn=~det & pos, tn=~det & ~pos)


def category_table(rows):
    '''Per-category counts, supports, metrics and low-support warnings for one baseline's unmasked rows.'''
    assert (rows["mask"] == 0).all()
    r = with_outcomes(rows)
    t = r.groupby("category")[["tp", "fp", "fn", "tn"]].sum()
    t["positive_support"] = t["tp"] + t["fn"]
    t["negative_support"] = t["fp"] + t["tn"]
    t["predicted_positive"] = t["tp"] + t["fp"]
    t["precision"], t["recall"], t["f1"] = prf(t["tp"], t["fp"], t["fn"])
    positives, detections = r[r["target"] == 1].groupby("category"), r[r["detected"]].groupby("category")
    t["positive_contracts"] = positives["title"].nunique().reindex(t.index, fill_value=0)
    t["positive_context_groups"] = positives["context_group_id"].nunique().reindex(t.index, fill_value=0)
    t["predicted_context_groups"] = detections["context_group_id"].nunique().reindex(t.index, fill_value=0)
    t["low_gold_support"] = t["positive_context_groups"] < LOW_SUPPORT_GROUPS
    t["low_predicted_support"] = t["predicted_context_groups"] < LOW_SUPPORT_GROUPS
    t["zero_support"] = (t["positive_support"] == 0) | (t["negative_support"] == 0)
    return t.reset_index()


def summary(table):
    '''Macro-F1 (plain mean of the 10 category F1s) and micro metrics from counts pooled over categories.'''
    assert len(table) == 10
    tp, fp, fn, tn = (int(table[k].sum()) for k in ["tp", "fp", "fn", "tn"])
    p, r, f = prf(tp, fp, fn)
    return {"macro_f1": float(table["f1"].mean()), "micro_precision": float(p), "micro_recall": float(r),
            "micro_f1": float(f), "tp": tp, "fp": fp, "fn": fn, "tn": tn}


def bootstrap_intervals(rows, baselines, reps=BOOTSTRAP_REPS, seed=BOOTSTRAP_SEED):
    '''Paired bootstrap over context groups: every repetition resamples context_group_id values with
    replacement and applies the same sample to every baseline, keeping predictions and thresholds fixed.
    Returns 95% percentile intervals for each baseline's macro-F1, micro-F1 and category F1, and for
    baselines[1] - baselines[0]. A category is unstable if any repetition has no positive support.'''
    assert (rows["mask"] == 0).all() and len(baselines) == 2
    groups = np.sort(rows["context_group_id"].unique())
    categories = sorted(rows["category"].unique())
    # tp/fp/fn per (baseline, context group, category); resampling a group keeps all its chunks and rows
    counts = (with_outcomes(rows).groupby(["baseline", "context_group_id", "category"])[["tp", "fp", "fn"]].sum()
              .reindex(pd.MultiIndex.from_product([baselines, groups, categories]), fill_value=0)
              .to_numpy().reshape(len(baselines), len(groups), len(categories), 3))
    rng = np.random.default_rng(seed)
    draws = rng.integers(0, len(groups), size=(reps, len(groups)))
    weights = np.apply_along_axis(np.bincount, 1, draws, minlength=len(groups))  # times each group was drawn
    tp, fp, fn = np.moveaxis(np.einsum("rg,bgkx->rbkx", weights, counts), -1, 0)  # each (reps, baselines, categories)

    category_f1 = prf(tp, fp, fn)[2]
    stats = {"macro_f1": category_f1.mean(axis=2), "micro_f1": prf(tp.sum(2), fp.sum(2), fn.sum(2))[2]}
    stats.update({f"f1:{c}": category_f1[:, :, k] for k, c in enumerate(categories)})
    no_positives = (tp + fn)[:, 0, :] == 0  # (reps, categories); labels are the same for both baselines
    zero_positive = dict(zip(categories, no_positives.sum(axis=0)))
    zero_positive[""] = no_positives.any(axis=1).sum()  # macro/micro: any category without positives

    out = []
    for name, values in stats.items():
        category = name.split(":", 1)[1] if name.startswith("f1:") else ""
        series = {b: values[:, i] for i, b in enumerate(baselines)}
        series[f"{baselines[1]}_minus_{baselines[0]}"] = values[:, 1] - values[:, 0]
        for scope, v in series.items():
            lo, hi = np.percentile(v, [2.5, 97.5])
            n_zero = int(zero_positive[category])
            out.append({"scope": scope, "metric": name.split(":")[0], "category": category,
                        "lower_95": lo, "upper_95": hi, "width": hi - lo,
                        "reps_without_positive_support": n_zero, "unstable": n_zero > 0})
    return pd.DataFrame(out)


def error_population(rows):
    '''Every unmasked false positive and false negative.'''
    assert (rows["mask"] == 0).all()
    fp = rows[rows["detected"] & (rows["target"] == 0)].assign(error_type="false_positive")
    fn = rows[~rows["detected"] & (rows["target"] == 1)].assign(error_type="false_negative")
    return pd.concat([fp, fn], ignore_index=True)


def ranking_key(seed, eval_set_id, baseline, category, error_type, context_group_id, chunk_id):
    # no run id in the key, so reruns select the same cases
    return hashlib.sha256(
        "|".join(map(str, [seed, eval_set_id, baseline, category, error_type, context_group_id, chunk_id])).encode()
    ).hexdigest()


def select_errors(errors, eval_set_id, baselines, categories, seed=ERROR_SEED):
    '''Repeatable error selection: per (baseline, category, error type) group, rank cases by SHA-256 key,
    take the top case of each context group first, then fill up to five from the remaining ranked cases.
    Returns (selected cases, one row per group including groups with no errors).'''
    e = errors.assign(ranking_key=[
        ranking_key(seed, eval_set_id, *k) for k in
        errors[["baseline", "category", "error_type", "context_group_id", "chunk_id"]].itertuples(index=False)
    ]).sort_values("ranking_key")
    selected, groups = [], []
    for b in baselines:
        for c in categories:
            for t in ERROR_TYPES:
                g = e[(e["baseline"] == b) & (e["category"] == c) & (e["error_type"] == t)]
                first = g.drop_duplicates("context_group_id").head(ERRORS_PER_GROUP)
                chosen = pd.concat([first, g.drop(first.index)]).head(ERRORS_PER_GROUP)
                selected.append(chosen.assign(selection_order=range(1, len(chosen) + 1)))
                groups.append({"baseline": b, "category": c, "error_type": t,
                               "n_errors": len(g), "n_selected": len(chosen), "no_errors": len(g) == 0})
    return pd.concat(selected, ignore_index=True), pd.DataFrame(groups)


def assign_reviewers(selected, reviewers, seed=REVIEWER_SEED):
    '''Seeded review order with two different reviewers per selected case.'''
    assert len(set(reviewers)) >= 2
    rng = np.random.default_rng(seed)
    out = selected.iloc[rng.permutation(len(selected))].reset_index(drop=True)
    pairs = np.array([rng.choice(reviewers, 2, replace=False) for _ in range(len(out))]).reshape(-1, 2)
    return out.assign(review_order=range(1, len(out) + 1), reviewer_1=pairs[:, 0], reviewer_2=pairs[:, 1])


def review_sheet(assigned):
    '''One blank assessment row per (case, reviewer), so the two reviews stay independent.'''
    sheets = [assigned.assign(reviewer_slot=i, reviewer=assigned[f"reviewer_{i}"]) for i in (1, 2)]
    sheet = pd.concat(sheets).drop(columns=["reviewer_1", "reviewer_2"]).sort_values(["review_order", "reviewer_slot"])
    return sheet.assign(**{f: "" for f in REVIEW_FIELDS}).reset_index(drop=True)


def read_markdown_fields(path):
    '''Reads "- field: value" lines from the Markdown approval.'''
    return dict(re.findall(r"^- (\w+): *(.*?) *$", Path(path).read_text(encoding="utf-8"), flags=re.M))


def check_authorization(md_path, json_record):
    '''Confirms the Markdown approval and the JSON authorization record the same value for every required
    field, and that none is blank. List values (bundle ids) are comma-separated in the Markdown.'''
    md = read_markdown_fields(md_path)
    for field in AUTHORIZATION_FIELDS:
        value = json_record.get(field)
        value = ", ".join(value) if isinstance(value, list) else value
        assert value not in (None, ""), f"authorization JSON has no {field}"
        assert md.get(field) == value, f"{field} differs: Markdown {md.get(field)!r} vs JSON {value!r}"

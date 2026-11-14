# AGENTS.md

Guide for AI coding agents (and new teammates) working in this repo.

## What this project is

Break Through Tech AI Studio × Accenture **Contract Review Challenge**. Using the CUAD v1 dataset (510 commercial contracts, 41 annotated clause categories), the team is building a pipeline that:

1. detects 10 core clause categories in contract chunks (multi-label classification),
2. scores them Low/Medium/High risk with an explainable rule-based layer, and
3. rolls them up into a contract-level triage score.

Milestones: **September** – data understanding + keyword/TF-IDF baselines (Gates 1–4); **October** – fine-tune a lightweight transformer (done: ModernBERT-base); **November** – risk scoring + end-to-end pipeline.

Background and rules:
- [README.md](README.md) – project summary, pipeline order and validation results.
- [Challenge-Project-Overview.md](Challenge-Project-Overview.md) – scope and success criteria.
- [docs/coach/september-execution/Accenture-Sept-Milestone.md](docs/coach/september-execution/Accenture-Sept-Milestone.md) – the Gate checklists. **Treat these as the spec.** October gates are also under [docs/coach/](docs/coach/).
- [docs/coach/september-execution/Glossary.md](docs/coach/september-execution/Glossary.md) – exact definitions (fixed TF-IDF settings, keyword baseline rules, threshold selection, metric rules, reproducibility tolerance, etc.).
- [data/cuad/README.md](data/cuad/README.md) – CUAD JSON format.
- [data/risk/README.md](data/risk/README.md) – buyer-side risk-label data for the November work.

## Environment

- Notebooks are run **locally** (VS Code / Jupyter), not in Google Colab, even though the milestone docs say Colab. Don't add Colab-specific code (`/content` paths, Drive mounts, `!git clone`). The Colab cell at the top of `01_EDA.ipynb` is a leftover. **Exception:** `october_transformer_colab.ipynb` was run in Colab for the GPU and uses `/content` uploads and a Drive mount; it can't be run locally as-is.
- Python 3.12, virtualenv in `.venv` (gitignored). Install with `pip install -r requirements.txt` (pinned: pandas, numpy, scikit-learn, iterative-stratification, torch, transformers, jupyter).
- Notebooks find the repo root with `PROJECT_ROOT = Path.cwd().parent if Path.cwd().name == "notebooks" else Path.cwd()`. The kernel's working directory is the notebook's folder, so `from text_normalization import normalize_text` and `import evaluation` work from `notebooks/` without `sys.path` changes.
- The keyword baseline is a package in `src/keyword_baseline/`, run as modules from the repo root (`python -m src.keyword_baseline.<module>`).
- No test suite, linter or build step. To verify a change, run the notebook top to bottom; notebooks use `assert` statements as their checks.

## Repository layout

```
anomaly_log.csv              Gate 1 anomaly log (severity, owner, status, decision)
notebooks/
  01_EDA.ipynb               Gate 1 EDA on train_separate_questions.json -> data/cuad/cleaned_train_df.csv, anomaly_log.csv
  create_split.ipynb         Gate 1: data validation + frozen 80/20 train/validation split -> data/splits/, reports/
  review_bundles.ipynb       Gate 2: picks the 10 core categories / 5 review bundles, positive + hard-negative excerpts
  gate3_chunking.ipynb       Gate 3: chunking comparison, approved 768/512 chunks + chunk labels -> data/gate3/
  keyword_baseline.ipynb     Gate 3: overview of the keyword baseline; can re-run src/keyword_baseline
  tf_idf_baseline.ipynb      Gate 3: TF-IDF + LinearSVC baseline -> reports/tf_idf_baseline/
  gate3_evaluation.ipynb     Gate 3: rescores both frozen baselines on validation, metrics, bootstrap intervals,
                             error review sheet, run receipt, official-test authorization draft -> reports/gate3_evaluation/
  gate3_independent_metric_check.ipynb   Independent recomputation of metrics from validation_rows.csv
  october_transformer_colab.ipynb        October: ModernBERT-base candidates A/B, thresholds, frozen package (Colab)
  text_normalization.py      normalize_text(): the shared 4-step normalization (see below)
  evaluation.py              Locked evaluation rules (metrics, bootstrap, error selection, authorization check)
src/keyword_baseline/
  normalize.py               normalize_with_map(): same output as normalize_text, plus offsets back to source text
  scorer.py                  prepare_category / score_text: evidence-group scoring
  score_chunks.py            Scores a chunk file -> predictions + match evidence (never reads labels)
  evaluate.py                Joins validation labels, picks thresholds -> reports/keyword_baseline/, configs/keyword_thresholds_v1.json
  train_sanity.py            Train-set bug check (optimistic, not a result)
  data.py, explore.py        Rule-writing helpers: load/print train spans and Gate 2 hard negatives
configs/
  keyword_rules_v1.json      FROZEN keyword rules (184 IDs); hash + freeze record in keyword_freeze_v1.md
  keyword_thresholds_v1.json Per-category keyword thresholds chosen on validation
  Accenture_October_Transformer/selected_transformer_candidate_a/
                             Frozen transformer package: config, tokenizer, thresholds, category order, metadata, hashes
                             (weights are *.safetensors, gitignored; they live on the team's Google Drive)
data/
  cuad/                      Original CUAD files (CUADv1.json, train_separate_questions.json, test.json, category_descriptions.csv)
                             plus derived cleaned_train_df.csv, cleaned_df.csv, gate2_excerpt_review.csv
  splits/                    FROZEN split: train.json, validation.json, split_manifest.csv, split_verification.json
  gate3/                     Approved chunks + labels: {train,validation}_chunks_768_512.csv, {train,validation}_chunk_labels_768_512.csv
  risk/                      Coach-supplied buyer-side risk labels (weak labels, not legal judgments); see its README, SCHEMA, METHODOLOGY
reports/
  final_category_support.csv, figures/   Gate 1 training profile
  keyword_baseline/          validation predictions, match evidence, threshold search, metrics, decision_tables/, weak_behavior.md
  tf_idf_baseline/           config_summary, category_results, threshold_searches, validation_margins, failures (CSV)
                             selected_model.npz + selected_model.json (saved model, no pickle)
  gate3_evaluation/          validation_* results, artifact_manifest.json, run_receipt.json, official_test_authorization_draft.{md,json}
docs/coach/                  Coach/milestone docs (read-only reference)
```

## Pipeline (run in this order)

1. **`create_split.ipynb`** – loads `data/cuad/train_separate_questions.json` (408 contracts), asserts Gate 1 totals (408 contracts, 41 categories, 16,728 annotation sets, 11,180 spans), checks span integrity, hashes contract text into `context_group_id`, and splits by context group with `MultilabelStratifiedShuffleSplit` (80/20, seed `20260901`).
2. **`review_bundles.ipynb`** – training split only. Selects the 10 core categories in 5 bundles:
   - Assignment and Control: Anti-Assignment, Change Of Control
   - Contract Term and Renewal: Expiration Date, Renewal Term
   - Licensing: License Grant, Non-Transferable License
   - Trade Restraint: Exclusivity, Non-Compete
   - Liability: Cap On Liability, Uncapped Liability
3. **`gate3_chunking.ipynb`** – a "token" is a contiguous non-whitespace run, so chunks keep exact character offsets into the source. The approved config is **768-token chunks with 512-token overlap (step 256)**, `config_version = gate3_chunking_v1`. It was the only candidate with zero lost positive annotations; 512/128 lost 20. Each chunk has exactly 10 label rows (one per core category): `target=1` if a span is fully inside the chunk, `mask=1` if a span only partly overlaps it (masked rows are excluded from training and evaluation).
4. **Keyword baseline** (`src/keyword_baseline/`, overview in `keyword_baseline.ipynb`) – evidence groups per category (anchor +2, support +1, counterevidence −1, group max, floor 0). `score_chunks` writes label-free predictions; `evaluate` then joins labels and picks an integer threshold per category (best F1, ties: higher recall, then lower threshold). Validation macro-F1 ≈ 0.673.
5. **`tf_idf_baseline.ipynb`** – one TF-IDF vectorizer fitted on training chunks only, with the fixed Glossary settings (`ngram_range=(1,2)`, `token_pattern=(?u)\b\w+\b`, sublinear tf, L2). Grid of `min_df ∈ {2,5}` × `C ∈ {0.1,1,10}`, one `LinearSVC(class_weight="balanced")` per category, per-category threshold = the validation margin with the best F1 (same tie rule). The selected config is `min_df=2, C=10.0` (macro-F1 ≈ 0.712). The model is saved as plain arrays in NPZ + a JSON with SHA-256 hashes, then reloaded and re-scored to check reproducibility (`atol=1e-10, rtol=1e-8`).
6. **`gate3_evaluation.ipynb`** – rebuilds both baselines from committed files only, rescores validation, reproduces thresholds and metrics with `evaluation.py`, writes bootstrap intervals and the error-review sheet, a run receipt (commit, clean tree, dependency versions, hashes) and the official-test authorization draft. `gate3_independent_metric_check.ipynb` recomputes the metrics separately.
7. **`october_transformer_colab.ipynb`** – `answerdotai/ModernBERT-base`, 10 outputs, mask-aware BCE, max length 4,096, batch 2 × 4 accumulation, lr 3e-5, 3 epochs, seed 42. Pre-registered candidates: A (unweighted) and B (positive-class weights). **A was selected** (validation macro-F1 ≈ 0.764, micro-F1 ≈ 0.808) and frozen to `configs/Accenture_October_Transformer/selected_transformer_candidate_a/`.

**Status / not built yet:** the official-test evaluation of the keyword and TF-IDF baselines is authorized (`AUTH-TEST-001`, one run via `notebooks/evaluation.py`) but its results aren't committed. Risk scoring and the contract-level rollup (November) haven't been started in code.

## Rules you must follow

These come from the milestone spec. Breaking them invalidates the team's Gate evidence.

- **Don't use the official test set in development.** Don't load `data/cuad/test.json` or `CUADv1.json` test contracts, and don't compute or print labels, span counts, prevalence or examples from them, except in the explicitly authorized official-test evaluation. All model selection uses `data/splits/train.json` / `validation.json` only. The same applies to `split=official_test` rows in `data/risk/`.
- **The official-test run is authorized once.** It must match the authorization record (approved commit, workflow and file hashes, the two baselines). Don't run it again or widen it (e.g. adding the transformer) without a new authorization.
- **The split is frozen.** Don't regenerate `data/splits/` or change seed `20260901`. Don't try other splits.
- **The chunking method is frozen** (768/512, `gate3_chunking_v1`). Changing it requires a new recorded team comparison and decision.
- **Fit only on training chunks.** Vocabularies, IDF weights and classifiers are fitted on training chunks; validation and test data are only transformed.
- **Don't hand-edit generated outputs.** Every file in `reports/`, `data/splits/`, `data/gate3/` and `configs/keyword_thresholds_v1.json` must come from a notebook or script run. Change the code and rerun it.
- **Leave keyword rules alone once frozen.** `configs/keyword_rules_v1.json` is frozen (SHA-256 in `configs/keyword_freeze_v1.md`). Don't tune it on validation results. Record weak behavior in `reports/keyword_baseline/weak_behavior.md` instead.
- **The transformer candidate is frozen.** Don't change files in `selected_transformer_candidate_a/`; `file_hashes.json` must still match.
- **Use the shared normalization.** Keyword and TF-IDF text must go through `notebooks/text_normalization.py::normalize_text` (NFKC → casefold → curly quotes/dashes to ASCII → collapse whitespace). Import it; don't copy it. `src/keyword_baseline/normalize.py::normalize_with_map` gives identical output plus offsets; keep the two in sync. (`review_bundles.ipynb` has an older local `normalize_text` used only for excerpt de-duplication.)
- **Use the locked evaluation code.** Metrics, bootstrap intervals and error selection come from `notebooks/evaluation.py`. Its hash is in the run receipt and authorization, so changing it invalidates them.
- **Keep fixed seeds.** Split `20260901`; `LinearSVC` `random_state=20260902`; `evaluation.py` bootstrap `20260903`, error selection `20260904`, reviewer assignment `20260905`; transformer `42`.

## Gotchas

- **Line endings in data CSVs.** Chunk text has newlines inside quoted fields, and `text_hash` = SHA-256 of the exact UTF-8 text. `.gitattributes` marks `data/**/*.csv -text` so Git stores them byte-for-byte. Older checkouts may have CRLF-converted copies. `load_chunks()` in `tf_idf_baseline.ipynb` replaces `\r\n` → `\n` and then asserts every hash (there's a TODO to remove the replace). Always verify `text_hash` when you load chunk files.
- **Label files are long format** (one row per chunk × category). Pivot them and reorder to the chunk file's row order before aligning with a feature matrix (see `load_label_matrices`).
- **Category names**: CUAD questions are long strings like `Highlight the parts (if any) of this contract related to "X" ...`. Notebooks pull out the quoted name `X`.
- **Annotation set ≠ QA record.** An annotation set is a unique (contract, category) pair; some pairs have more than one QA record.
- One pair of training contracts has identical text. Both are kept, share a `context_group_id`, and always land in the same split.
- `selected_model.npz`'s file hash changes on every save (zip timestamps). Compare the per-array hashes in `selected_model.json` instead.
- Load the NPZ with `allow_pickle=False`. Don't save models with pickle or joblib.
- `gate3_evaluation.ipynb` records whether the working tree was clean in `run_receipt.json`. Commit before a run you mean to keep.
- `data/risk/` uses its own `split` column and `contract_id`; `source_partition=train` means the original CUAD file, not this repo's training split.

## Conventions

- Work happens in notebooks. Move code into a `.py` module under `notebooks/` only once more than one notebook needs it (as with `text_normalization.py` and `evaluation.py`). The keyword baseline is the exception: it was written as a script package in `src/`.
- Each notebook step gets a markdown cell explaining what it does and why, followed by the code. Docstrings use `'''...'''`. Comments are short and explain why.
- Put output paths in constants at the top of the save cell, and create directories with `mkdir(parents=True, exist_ok=True)`.
- Git: work on a feature branch (e.g. `annabel-tf-idf-baseline`) and open a PR to `main` on `Break-Through-Tech/Accenture-1D-contract-review-challenge`. Commit regenerated outputs together with the notebook that produced them.

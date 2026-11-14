# Contract Review Challenge: Clause Detection and Risk Triage on CUAD

Break Through Tech AI Studio × Accenture. We built a pipeline that reads commercial contracts, classifies excerpts into one of ten legal clause categories, and assigns a Low / Medium / High risk score for each contract.

---

### 👥 **Team Members**

| Name              | Contribution                                                                                                                                                              |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Adriana Soldat    | EDA, data validation, finalizing 10 core categories, chunking methods, independent metric check, official-test authorization, testing and implementing transformer models |
| Annabel Wang      | EDA, initial review bundles, finding representative spans, text normalization, TF-IDF baseline, keyword and TF-IDF validation evaluation                                  |
| Mary-kate Laibhen | Training data validation, creating train-validation split, normalizing baseline and transformer evaluation models, anomaly analysis                                       |
| Mahir Rana        | Keyword baseline: rules, scorer, decision tables, freeze, evaluation, weak-behavior write-up                                                                              |

---

## 🎯 **Project Highlights**

- Detects 10 core CUAD clause categories in contract chunks as a multi-label classification task.
- Built three detectors on the same frozen split and chunks:

  | Model                                  | Validation macro-F1 |  Micro-F1 | Precision |    Recall |
  | -------------------------------------- | ------------------: | --------: | --------: | --------: |
  | Keyword rules (`keyword_rules_v1`)     |               0.673 |     0.690 |     0.717 |     0.665 |
  | TF-IDF + LinearSVC (`min_df=2, C=10`)  |               0.712 |     0.749 |     0.762 |     0.735 |
  | ModernBERT-base, candidate A (October) |           **0.764** | **0.808** | **0.833** | **0.785** |

- The TF-IDF model is saved as plain NumPy arrays with SHA-256 hashes, and reloading it reproduces the same scores.
- Gate rules prevent data leakage: the official test set is never used during development, and the split, chunking, and keyword rules are frozen and recorded by hash.

---

## 👩🏽‍💻 **Setup and Installation**

The team runs notebooks locally (VS Code or Jupyter). The only exception is the transformer notebook, which needs a GPU.

```bash
git clone https://github.com/Break-Through-Tech/Accenture-1D-contract-review-challenge.git
cd Accenture-1D-contract-review-challenge
python -m venv .venv            # Python 3.12
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

The CUAD v1 data is already in [data/cuad/](data/cuad/). See [data/cuad/README.md](data/cuad/README.md) for its format.

Run the notebooks in [notebooks/](notebooks/) from top to bottom. They check their own results with `assert` statements, and there is no separate test suite. Pipeline order:

| Step                     | Notebook / script                                                                                                                                  | Output                                                                           |
| ------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| 1. EDA                   | [01_EDA.ipynb](notebooks/01_EDA.ipynb)                                                                                                             | `data/cuad/cleaned_train_df.csv`, [anomaly_log.csv](anomaly_log.csv)             |
| 2. Frozen split          | [create_split.ipynb](notebooks/create_split.ipynb)                                                                                                 | [data/splits/](data/splits/)                                                     |
| 3. Core categories       | [review_bundles.ipynb](notebooks/review_bundles.ipynb)                                                                                             | `data/cuad/gate2_excerpt_review.csv`                                             |
| 4. Chunking              | [gate3_chunking.ipynb](notebooks/gate3_chunking.ipynb)                                                                                             | [data/gate3/](data/gate3/)                                                       |
| 5. Keyword baseline      | [keyword_baseline.ipynb](notebooks/keyword_baseline.ipynb) + [src/keyword_baseline/](src/keyword_baseline/)                                        | [reports/keyword_baseline/](reports/keyword_baseline/)                           |
| 6. TF-IDF baseline       | [tf_idf_baseline.ipynb](notebooks/tf_idf_baseline.ipynb)                                                                                           | [reports/tf_idf_baseline/](reports/tf_idf_baseline/)                             |
| 7. Validation evaluation | [gate3_evaluation.ipynb](notebooks/gate3_evaluation.ipynb), [gate3_independent_metric_check.ipynb](notebooks/gate3_independent_metric_check.ipynb) | [reports/gate3_evaluation/](reports/gate3_evaluation/)                           |
| 8. Transformer           | [october_transformer_colab.ipynb](notebooks/october_transformer_colab.ipynb)                                                                       | [configs/Accenture_October_Transformer/](configs/Accenture_October_Transformer/) |

You can also run the keyword scripts from the repo root, for example:

```bash
python -m src.keyword_baseline.score_chunks --chunks data/gate3/validation_chunks_768_512.csv --out-prefix reports/keyword_baseline/validation
python -m src.keyword_baseline.evaluate
```

Rules for contributors (the frozen split, no use of the official test set, no hand-editing of generated files) are in [AGENTS.md](AGENTS.md).

---

## 🏗️ **Project Overview**

Legal and procurement teams spend a lot of time reading contracts to find terms that create risk, such as assignment limits, missing liability caps, or non-compete obligations. Accenture asked us to build an explainable first-pass triage tool: find the clauses that matter, rate their risk, and point reviewers to the contracts that need attention first.

Milestones:

- **September:** data understanding, a frozen split, chunking, and keyword and TF-IDF baselines (Gates 1–4).
- **October:** fine-tune a transformer and compare it with the baselines.
- **November:** risk scoring and the end-to-end pipeline.

The full scope is in [Challenge-Project-Overview.md](Challenge-Project-Overview.md). Gate checklists and definitions are in [docs/coach/](docs/coach/).

---

## 📊 **Data Exploration**

**Dataset:** [CUAD v1](https://www.atticusprojectai.org/cuad) has 510 commercial contracts with expert annotations for 41 clause categories, in SQuAD-style JSON. The training file contains 408 contracts, 16,728 annotation sets, and 11,180 answer spans.

**Split:** we split the 408 training contracts 80/20 into training and validation. The split is grouped by contract text (so duplicate contracts stay together), stratified across labels, and uses seed `20260901`. It is frozen. The 102 official-test contracts are held out.

**Core categories:** we chose 10 categories in 5 review bundles.

| Bundle                    | Categories                              |
| ------------------------- | --------------------------------------- |
| Assignment and Control    | Anti-Assignment, Change Of Control      |
| Contract Term and Renewal | Expiration Date, Renewal Term           |
| Licensing                 | License Grant, Non-Transferable License |
| Trade Restraint           | Exclusivity, Non-Compete                |
| Liability                 | Cap On Liability, Uncapped Liability    |

**Chunking:** contracts are much longer than a model's input limit. We use 768-token chunks with a 512-token overlap. This was the only configuration we compared that lost no positive annotations. Each chunk gets one label per category: `target=1` if an annotated span lies fully inside the chunk, and `mask=1` if a span only partly overlaps the chunk. Masked rows are left out of training and scoring.

**Text normalization:** the keyword and TF-IDF models share one function, [text_normalization.py](notebooks/text_normalization.py), which applies NFKC, casefolding, ASCII quotes and dashes, and whitespace collapsing.

Figures from the training profile are in [reports/figures/](reports/figures/). Data issues we found are logged in [anomaly_log.csv](anomaly_log.csv).

---

## 🧠 **Model Development**

- **Keyword baseline:** 184 hand-written evidence rules ([configs/keyword_rules_v1.json](configs/keyword_rules_v1.json)). A matching anchor adds 2 to a chunk's score, a support term adds 1, and counter-evidence subtracts 1. A per-category threshold is then chosen on validation. The rules were frozen before validation was scored ([configs/keyword_freeze_v1.md](configs/keyword_freeze_v1.md)).
- **TF-IDF baseline:** one vectorizer fitted on training chunks only, using unigrams and bigrams with sublinear TF. It feeds one `LinearSVC(class_weight="balanced")` per category. We searched a grid of `min_df ∈ {2,5}` × `C ∈ {0.1,1,10}`, and each category's threshold maximizes validation F1.
- **Transformer:** `answerdotai/ModernBERT-base` fine-tuned with a multi-label BCE loss. Settings: max length 4,096, effective batch size 8, learning rate 3e-5, 3 epochs, seed 42. Two candidates were pre-registered, unweighted (A) and class-weighted (B) loss, and we selected A for its higher micro-F1, higher precision, and lower validation loss. The repo stores its config, tokenizer, and thresholds. The model weights are not stored here.

---

## 📈 **Results & Key Findings**

The validation results above are scored on 24,810 chunk–category pairs, with masked rows removed. Per-category results and bootstrap intervals are in [reports/gate3_evaluation/](reports/gate3_evaluation/).

- The transformer is better than both baselines on every summary metric, and its precision gain is the largest.
- With keyword rules, the hardest categories are **Change Of Control** (F1 0.45), **Non-Compete** (0.48), and **Exclusivity** (0.57). Their wording overlaps with nearby clause types, and they have few positive contracts. Weak behavior is recorded in [weak_behavior.md](reports/keyword_baseline/weak_behavior.md), and the rules were not tuned after freezing.
- Non-Transferable License is the easiest category (keyword F1 0.91).
- One official-test evaluation of the keyword and TF-IDF baselines has been authorized ([authorization draft](reports/gate3_evaluation/official_test_authorization_draft.md)). Its results are not in this repo yet.

---

## 🚀 **Next Steps**

- Run the authorized official-test evaluation.
- Build risk scoring with the buyer-side risk labels in [data/risk/](data/risk/). These are research-derived weak labels, not legal judgments, and the High class has very few examples.
- Combine clause-level risk into a contract-level triage score and connect the pipeline end to end.

---

## 📝 **License**

Not yet chosen. CUAD v1 is released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

---

## 📄 **References**

- Hendrycks, D., Burns, C., Chen, A., & Ball, S. (2021). _CUAD: An Expert-Annotated NLP Dataset for Legal Contract Review._ NeurIPS Datasets and Benchmarks.
- Warner, B., et al. (2024). _Smarter, Better, Faster, Longer: A Modern Bidirectional Encoder for Fast, Memory Efficient, and Long Context Finetuning and Inference_ (ModernBERT).

---

## 🙏 **Acknowledgements**

Thanks to our Break Through Tech AI Studio coach Beth Parnell, and our Challenge Advisor Tate Arevalo, and to Accenture for hosting the challenge.

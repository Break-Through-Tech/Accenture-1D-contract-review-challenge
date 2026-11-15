# Gate 3.1 — Evaluation Alignment Report

## 1. Objective

Verify that the September keyword baseline, September TF-IDF baseline, and October ModernBERT Candidate A transformer use the same approved validation evaluation units.

The alignment checks compare chunk-category identifiers, ground-truth labels, evaluation masks, category names, validation text, and source metadata.

No model retraining or threshold retuning was performed as part of this alignment work.

## 2. Approved Evaluation Configuration

- Validation chunks: 2,481
- Categories: 10
- Total chunk-category evaluation pairs: 24,810
- Unmasked evaluation pairs: 24,646
- Masked evaluation pairs: 164
- Chunk size: 768
- Chunk overlap: 512
- Chunk step: 256

## 3. September Baseline Verification

**Keyword baseline — PASS**

The September keyword baseline reproduced all 24,810 validation scores exactly.

**TF-IDF baseline — PASS**

The September TF-IDF baseline reproduced all 24,646 unmasked validation margins within the required numerical tolerance, with identical detection decisions.

**Evaluation alignment — PASS**

The keyword and TF-IDF baselines used identical `(chunk_id, category)` evaluation keys and matching targets, masks, document titles, and context-group identifiers.

## 4. October Transformer Alignment

**Previously verified in the October notebook session:**

- Full validation coverage: 2,481 chunks across 10 categories
- Exact evaluation-key alignment with approved validation labels
- Matching ground-truth targets and evaluation masks
- Matching source metadata and validation text
- Consistent category names despite differences in category ordering

These checks passed in the earlier notebook session. However, the complete transformer prediction CSV was not preserved.

## 5. Reproducibility Limitation

The October Candidate A transformer was trained by another team member.

The selected checkpoint configuration, tokenizer, thresholds, and category-order files are available, but the fine-tuned `model.safetensors` weights are not currently available in the local checkout.

A ModernBERT checkpoint found in the local Hugging Face cache did not match the expected Candidate A SHA-256 hash.

Therefore, independent reproduction of the frozen transformer predictions remains pending.

## 6. Artifact Manifest

The artifact manifest is stored at:

`reports/gate3_alignment/artifact_manifest.json`

The manifest records available evaluation artifacts and identifies the missing transformer validation prediction CSV.

The manifest must be updated when the original checkpoint or prediction CSV becomes available.

## 7. Conclusion

The completed checks support alignment between the September baselines and the October transformer evaluation units.

The September baseline results have been independently verified. October alignment checks passed in the earlier notebook session, but full independent transformer reproduction remains blocked by the missing fine-tuned checkpoint or saved predictions.

**Outstanding action:** Obtain the original Candidate A checkpoint or full-validation prediction CSV from the teammate responsible for training, verify its provenance, and complete the reproducibility artifacts before final approval.
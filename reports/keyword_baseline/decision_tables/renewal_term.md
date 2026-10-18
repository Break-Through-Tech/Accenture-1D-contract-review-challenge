# Decision table: Renewal Term

Rule set: `configs/keyword_rules_v1.json` (DRAFT, not frozen). Evidence: the 326 train contracts only (`data/splits/train.json`, `data/gate3/train_*_768_512.csv`, `data/cuad/gate2_excerpt_review.csv`). No validation or test data was used.
Status: **APPROVED by Mahir 2026-10-16; R1-R5 (section 9) APPLIED to the JSON** (RT-G4-01 retired, RT-G1-07..10 added). Rule set remains an unfrozen draft.
Claim labels: **VERIFIED** = seen in a cited source or scratch run on train; **INFERRED** = hypothesis, not checked.

## 1. Inclusion meaning

A chunk is a Renewal Term positive when it contains text saying that, after the first term ends, the agreement continues or can be continued for a further period: automatic renewal, successive renewal periods, or an option or right to renew or extend. The CUAD category description is "what is the renewal term after the initial term expires? This includes automatic extensions and unilateral extensions with prior notice."

What it is *not*: the length of the first term (Expiration Date), or the notice a party must give to stop a renewal (CUAD category "Notice Period To Terminate Renewal").

Train support: 141 spans in 119 of 326 contracts. **VERIFIED** (Phase 1 span table in plan.md section 3b).

## 2. Evidence groups (how the score is built)

Each group contributes at most once per chunk (strongest hit only). Anchor = +2, support = +1, counter = -1, total floored at 0. Match is a plain substring on normalized text (casefolded, quotes/dashes unified, whitespace collapsed).

| Group | Role | Phrases (rule IDs) | Train spans containing it | Train occurrences (all text) |
|---|---|---|---|---|
| RT-G1 automatic renewal wording | anchor | automatically renew (01), automatic extension (02), automatic renewal (03), renew for (04), shall renew (05), automatically extended (06) | 47, 2, 5, 28, 3, 3 | 48, 2, 7, 28, 3, 3 |
| RT-G2 successive renewal terms | anchor | successive terms (02), successive one (03), successive renewal (04) | 5, 14, 2 | 5, 16, 3 |
| RT-G3 named renewal period | support | renewal term (01), extension term (02) | 36, 2 | 134, 3 |
| RT-G5 notice-to-stop wording | support | unless either party (01) | 26 | 28 |
| RT-G4 non-renewal notice | counter | not to renew (01), non-renewal (02) | 16, 6 | 25, 32 |
| RT-V1 veto (cancels RT-G1) | veto | not automatically renew | 0 | 0 |

All counts **VERIFIED** (scratch run on the 326 train contracts; "spans containing" = normalized span text contains the phrase; "occurrences" = substring count over full contract text, so it includes unlabeled mentions). Group IDs and rule IDs: see `RT-G*-**` in the JSON; the `RT-G4`/`RT-G5` numbering is out of order for historical reasons.

Maximum possible score: 2 anchor groups x 2 + 2 support groups x 1 = **6**. Threshold candidates therefore run 1-6.

## 3. Counterevidence and vetoes

- **RT-G4 (counter, -1)** was added from hard negative N2 (a "notice of election not to renew" labeled Notice Period To Terminate Renewal). **Problem (VERIFIED):** 16 of 141 positive spans contain "not to renew" and 6 contain "non-renewal", because the most typical renewal clause is "automatically renews ... unless a party gives notice of non-renewal". So the counter punishes real positives. See examples E2, E3. Train-only simulation (section 8): dropping RT-G4-01 raises train F1 from .655 to .686; dropping both counters gives .691 but dropping only RT-G4-02 makes things worse, so RT-G4-02 earns its place (it pushes down "non-renewal" notice text). Proposed edit R1 removes RT-G4-01 only.
- **RT-V1 (veto, cancels RT-G1 matches that overlap "not automatically renew")**. **VERIFIED: 0 train hits**, so it has never been exercised on real data. Its justification is logical (a clause saying the contract does *not* auto-renew is the opposite of a renewal term), i.e. **INFERRED** from drafting practice. Kept, labeled as untested. The only real "not renew" phrases in train are notices or unrelated text (E8), none of which overlap an RT-G1 phrase.

## 4. Context / proximity limits

None. All matching is chunk-wide (a chunk is up to 768 words with 512 overlap). Consequence (**VERIFIED** on train chunks): a chunk that holds both a renewal clause and an unrelated "Renewal Term" definition scores the same as one with only the clause; nothing is gained or lost by distance. The only locality rule is the veto's overlap with the anchor match.

## 5. Required confusion case: Renewal Term vs initial term (Expiration Date)

Rule of thumb in the rules: **the words "initial term" never score for Renewal Term.** There is no RT rule for "initial term". "Initial term" appears 258 times in train text, only 65 inside Renewal Term spans (**VERIFIED**), so it would be a poor signal. Initial-term-only text therefore scores 0 here and belongs to Expiration Date (ED-G3 "initial term", support).

Where the two categories overlap is the defined-term sentence "(the 'Initial Term' and any 'Renewal Terms' collectively the 'Term')". That scores +1 for RT-G3 ("renewal term" matches inside "renewal terms") and stays below a threshold of 2. **If the threshold search picks 1, this class of text fires** (see section 7, item 2).

## 6. Known near-misses and exclusions

| Pattern | What happens | Evidence |
|---|---|---|
| Defined-term mentions of "Renewal Term" in unrelated clauses (fees, rent, termination fees) | +1 only (RT-G3); fires only if threshold = 1 | 133 occurrences of "renewal term" in train, 54 inside RT spans (**VERIFIED**) |
| "Successive" meaning contract-year months ("twelve (12) successive months") | Fixed by P1: bare "successive" removed, replaced by RT-G2 phrases | plan.md audit findings (**VERIFIED**) |
| Renewal of licenses/permits/IP ("withdrawn, cancelled, suspended or not renewed") | "not renew" is not an RT rule; "renew for" does not match this wording; scores 0 | E8 (**VERIFIED**) |
| Notice of non-renewal (Notice Period To Terminate Renewal) | Mostly caught by RT-G4-02 "non-renewal"; leaks as +1 for "renewal term" | hard negatives N2, N4 (**VERIFIED**) |
| Auto-renewal clause that is *not* labeled Renewal Term in train | One case: Ipass "Every Business Entity Term automatically renews for a period of no less than 12 months" scores 2 (false positive) | **VERIFIED** (only 1 such occurrence of "automatically renew" outside RT spans) |
| Exclusion: clauses saying the contract does NOT renew | Intended to score 0 via RT-V1 | **INFERRED** (0 train hits) |

## 7. Known weak spots (be honest in the write-up)

1. **Recall ceiling.** Only 66 of 141 spans (47%) contain a current anchor phrase (**VERIFIED**); 54 of the 119 contracts with a Renewal Term span have no anchored span. Missed wordings: "may be extended for one year upon mutual agreement", "option to extend", "renewable for 1 year", "continue automatically for successive annual periods", month-to-month continuation, "Successor Franchise" rights. Many of these are option or unilateral-extension wordings that the CUAD description includes but the anchors do not cover.
2. **Threshold-1 risk.** At threshold 1 every chunk with any support phrase fires, and "renewal term" alone appears 133 times. The train simulation chose threshold 2 in every variant tried (best F1), but the real threshold is chosen on validation later.
3. **Chunk overlap inflates counts.** Train chunk counts are ~3x contract counts because of the 512-word overlap. Chunk-level numbers in section 8 are therefore for bug-checking only (also optimistic: the threshold is tuned on the same train data).

## 8. Train-only simulation (bug check, optimistic)

Approximate scorer (substring match on normalized chunk text, group-max, floor 0, no veto offset map), train chunks only, unmasked pairs, best threshold by F1. **VERIFIED** by scratch run; the "current" row reproduces the .655 in plan.md.

| Variant | Best F1 | Threshold | TP | FP | FN |
|---|---|---|---|---|---|
| current rules | .655 | 2 | 156 | 9 | 155 |
| R1: drop RT-G4-01 | .686 | 2 | 167 | 9 | 144 |
| R1 + drop RT-G4-02 too (not proposed) | .691 | 2 | 169 | 9 | 142 |
| R1 + R2 (add "renewed for") | .713 | 2 | 183 | 19 | 128 |
| R1-R3 (+ "automatically extend") | .726 | 2 | 189 | 21 | 122 |
| R1-R4 (+ "right to renew") | .745 | 2 | 199 | 24 | 112 |
| R1-R5 (+ "additional one") | .762 | 2 | 206 | 24 | 105 |

Anchor coverage of the 141 spans: 66 (47%) now, 83 (59%) with R2-R5 (**VERIFIED**).

## 9. Proposed rule edits (NOT applied; need Mahir's OK)

| ID | Change | Train evidence (spans containing / total occurrences) | Why |
|---|---|---|---|
| R1 | Remove RT-G4-01 "not to renew" (retire the ID; do not reuse) | 16 positive spans contain it of 25 total occurrences | It subtracts from typical positive clauses (E2, E3) |
| R2 | Add RT-G1-07 "renewed for" (anchor, train_span) | 22 / 28 (precision ~0.79) | Passive form of "renew for" ("will be automatically renewed for one additional period") |
| R3 | Add RT-G1-08 "automatically extend" (anchor, train_span) | 5 / 6 (~0.83) | Variant not covered by RT-G1-06 "automatically extended" |
| R4 | Add RT-G1-09 "right to renew" (anchor, train_span) | 6 / 9 (~0.67) | Option wording ("Publishers exercise their right to renew") |
| R5 | Add RT-G1-10 "additional one" (anchor, train_span) | 8 / 10 (~0.80) | "for additional one (1) year periods" |

R4 and R5 have small support (6 and 8 spans). R1 is the one that fixes a logical flaw; R2-R5 are recall gains. "Precision" here is spans-containing over total occurrences, a rough contract-text estimate, not chunk-level precision. Candidates I rejected on this evidence: "may be extended" (4/34), "additional term" (4/48), "renewal"/"renew" alone (precision ~0.14-0.17), "automatically" alone (74/240).

## 10. Examples that exercise each branch

All from the 326 train contracts. Scores use the current rules unless noted. "+2 RT-G1" means anchor group matched.

| ID | Branch | Source | Text (shortened) | Score now |
|---|---|---|---|---|
| E1 | Anchor + support, no counter (clean positive) | Renewal Term span, ENERGOUSCORP_03_16_2017-EX-10.24 | "...will automatically renew for one or more annual periods after the Initial Term (each a "Renewal Term") unless either party gives notice of non-renewal..." | +2 RT-G1 (automatically renew) +1 RT-G3 (renewal term) +1 RT-G5 (unless either party) -1 RT-G4 (non-renewal) = **3** |
| E2 | Counter hurting a real positive (the R1 case) | Renewal Term span, SIBANNAC,INC_12_04_2017-EX-2.1 | "The term of this Agreement is twelve (12) months from the date hereof, and will be automatically renewed for one (1) additional twelve month period unless either party shall notify the other in writing of its intention not to renew." | +2 +1 (unless either party) -1 (not to renew) = **2** now; 3 after R1 |
| E3 | Counter (RT-G4-02, kept) subtracting from a real positive | Renewal Term span, NANOPHASETECHNOLOGIESCORP_11_01_2005 | "...shall thereafter automatically renew for additional two (2) year terms unless a party provides the other party with notice of non-renewal no less than 6 months prior to the expiration of the initial term or any renewal term..." | +2 RT-G1 +1 RT-G3 (renewal term) -1 RT-G4-02 (non-renewal) = **2**. Still detected at threshold 2, but would be lost at 3; R1 does not change it |
| E4 | Support only, option wording (miss) | Renewal Term span, LeadersonlineInc_20000427 | "LeadersOnline shall have the option ... to extend the Term of this Agreement for an additional 12 months (a "Renewal Term")..." | +1 RT-G3 = **1**: below threshold 2 (a miss; no anchor for "option to extend") |
| E5 | No anchor at all (miss) | Renewal Term span, BravatekSolutionsInc_20170418 | "Contract is renewable for 1 year extension by amendment to this agreement." | **0** (miss; "renewable" not a rule) |
| E6 | Initial term, no renewal (correct 0) | Hard negative, labeled Expiration Date, Magenta Therapeutics | "This Agreement shall commence on the Effective Date and shall extend for a period of Five (5) years thereafter ("Initial Term"), unless ... extended by mutual written agreement..." | **0**: no RT rule fires |
| E7 | Initial term + "any renewal terms" (support leak) | Hard negative, labeled Expiration Date, BellringBrandsInc_20190920 | "...shall terminate automatically without notice on December 31, 2022, unless the Parties agree in writing to extend the term ... (the initial term and any renewal terms are referred to collectively herein as the "Term")." | +1 RT-G3 (renewal terms) = **1**: not detected at threshold 2, detected at threshold 1 (false positive) |
| E8 | Notice of non-renewal (correct, fixed by counter) | Hard negative, labeled Notice Period To Terminate Renewal, BUFFALOWILDWINGSINC_06_05_1998-EX-10.3 | "We shall give you written notice of our election not to renew the franchise at least three (3) months prior to the expiration of the initial or first renewal term..." | +1 RT-G3 (renewal term) -1 RT-G4-01 = **0**. Without R1 this is the only job RT-G4-01 does; after R1 it scores 1 (below threshold 2) |
| E9 | Notice of non-renewal, support leak | Hard negative, labeled Notice Period To Terminate Renewal, CybergyHoldingsInc_20140520 | "This Agreement may be terminated by either party at the expiration of its term or any renewal term upon thirty (30) days written notice..." | +1 RT-G3 = **1** |
| E10 | Anchor outside a positive span (false positive) | Not a labeled span; IpassInc_20181203 | "Every Business Entity Term automatically renews for a period of no less than 12 months, unless otherwise agreed to in writing between the parties." | +2 RT-G1 = **2**: fires, but not labeled Renewal Term in train. Rare (1 occurrence) |
| E11 | Unrelated "not renew" (license renewal) | Not a labeled span; OLDAPIWIND-DOWNLTD_01_08_2016 | "...any such license, certificate, approval or permit to be withdrawn, cancelled, suspended or not renewed." | **0** |
| E12 | Veto | Synthetic, **INFERRED** (0 train hits) | "This Agreement shall not automatically renew." | RT-G1-01 matches inside "not automatically renew"; RT-V1 cancels it: **0**. Without the veto it would score 2 |

## 11. Sources

- CUAD category name and description: `data/cuad/category_descriptions.csv` (train-independent).
- Train spans: `data/splits/train.json` via `src/keyword_baseline/data.py` (Renewal Term: 141 spans, 119 contracts).
- Hard negatives: `data/cuad/gate2_excerpt_review.csv` rows with `target_category == "Renewal Term"`, `example_type` negative. N2 and N4 above (E8, E9) and N1, N3, N5 (E6, E7, plus Solutions Vending, an Expiration Date "Initial Term" sentence that scores 1 from "unless either party" (RT-G5) alone).
- All example scores in section 10 were re-checked with the approximate scratch scorer (not yet the real Phase 4 scorer); E12 is a synthetic sentence.
- Chunks: `data/gate3/train_chunks_768_512.csv` and `train_chunk_labels_768_512.csv` (`gate3_chunking_v1`).
- Rule-level provenance and rationale: `configs/keyword_rules_v1.json`.
- Reviewer: not yet assigned (Issue #8 requires a teammate other than the author).

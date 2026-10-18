# Decision table: Cap On Liability

Rule set: `configs/keyword_rules_v1.json` (DRAFT, not frozen). Evidence: the 326 train contracts only (`data/splits/train.json`, `data/gate3/train_*_768_512.csv`, `data/cuad/gate2_excerpt_review.csv`). No validation or test data used.
Status: **APPROVED by Mahir 2026-10-16; C1-C4 (section 9) APPLIED to the JSON** (CL-G4 retired, CL-G7/G8/G9 added). Rule set remains an unfrozen draft.
Claim labels: **VERIFIED** = seen in a cited source or scratch run on train; **INFERRED** = hypothesis.

## 1. Inclusion meaning

CUAD asks: "Does the contract include a cap on liability upon the breach of a party's obligations? This includes time limitation for the counterparty to bring claims or maximum amount for recovery." In the labeled data this covers more than a dollar cap (**VERIFIED**, train spans):
- an amount ceiling ("total liability ... shall not exceed the fees paid");
- exclusions of damage types ("neither party shall be liable for special, consequential, incidental, punitive damages"), which is by far the most common form;
- claim time bars ("all claims ... shall be brought within [***] year"), exclusive-remedy and limited-recourse wording.

Not included: the carve-out that removes a cap (Uncapped Liability); but see section 5, the two labels are **not mutually exclusive on a chunk**.

Train support: 432 spans in 181 of 326 contracts (**VERIFIED**, Phase 1 table).

## 2. Evidence groups

Each group counts at most once per chunk. Anchor +2, support +1, counter -1, floor 0. Plain substring match on normalized text.

| Group | Role | Phrases (rule IDs) | Spans containing | All-train occurrences |
|---|---|---|---|---|
| CL-G1 ceiling on the amount | anchor | aggregate liability (04), total liability (05), exceed the total (06), liability shall not exceed (07), maximum liability (08) | 12, 14, 4, 2, 7 | 17, 14, 4, 2, 11 |
| CL-G5 exceed wording | support | shall not exceed (CL-G1-01), will not exceed (CL-G1-02) | 28, 10 | 86, 28 |
| CL-G2 damages-exclusion wording | support | consequential (01), punitive (02) | 171, 90 | 221, 127 |
| CL-G3 no-liability wording | support | in no event (01), neither party shall be liable (02) | 114, 30 | 411, 62 |
| CL-G6 limitation heading | support | limitation of liability (01) | 9 | 162 |
| CL-G4 "limitation does not apply" | counter | shall not apply (01), inapplicable (02), nothing in this section (03) | 7, 0, 1 | 168, 14, 45 |

All counts **VERIFIED** (scratch run on 326 train contracts; "spans containing" = normalized span text contains the phrase, "all-train occurrences" = substring count over whole contracts). The "spans" counts for CL-G6 show why it is only support: "limitation of liability" is mostly a heading, outside the labeled span (9 of 162).

Maximum score now: 1 anchor group x 2 + 4 support groups = **6**. The only anchor group is CL-G1, so a chunk without an amount-cap phrase can reach 4 at most.

## 3. Counterevidence and vetoes

- **CL-G4 (counter, -1)** exists to push down carve-out text ("this limitation shall not apply to ..."), the five Uncapped hard negatives. **Problem (VERIFIED):** at chunk level the carve-out almost always sits in the same chunk as the cap. Of 234 unmasked train chunks labeled Uncapped Liability, **227 are also labeled Cap On Liability** (only 7 are Uncapped-only); 515 chunks are Cap-only. So CL-G4 penalizes real Cap positives. Train simulation: drop all three CL-G4 rules, F1 .670 to .698 (dropping only CL-G4-01 gives .695). Proposed edit C1.
- **Vetoes:** none. A veto would need a window (e.g. "shall not apply" within N characters of a cap phrase), which is not part of the spec's chunk-wide design; and see above: the two labels coexist, so there is nothing to cancel.

## 4. Context / proximity limits

None. All matching is chunk-wide (768 words, 512-word overlap). Consequence (**VERIFIED**): fee-cap sentences and a real liability cap in the same chunk are indistinguishable; see near-misses.

## 5. Required confusion cases

**Cap vs Uncapped carve-outs.** The five gate-2 hard negatives are carve-out sentences labeled Uncapped Liability ("THESE LIMITATIONS SHALL NOT APPLY TO ... GROSS NEGLIGENCE", "THE LIMITATIONS ... SHALL BE INAPPLICABLE TO ... INDEMNIFY", "Nothing in this Section 8.7 shall operate to limit ... any liability under Section 8.5"). As bare sentences all five score 0 on Cap (E8), because they contain no cap phrase. That is the correct answer *for the excerpt*. But a real chunk holds the cap sentence and the carve-out together, so it is positive for both categories (227 of 234 Uncapped chunks, **VERIFIED**). The decision for this baseline: **do not try to separate them with Cap counters; the Uncapped category is judged by its own anchors (see its table).** The cost is that a carve-out-only chunk (e.g. a section that starts with "Notwithstanding the foregoing, the limitations shall not apply...") can score on Cap if it also holds damages-exclusion wording. Only 7 such Uncapped-only chunks exist in train.

**Cap vs "not liable" (Uncapped).** Handled in the Uncapped table. For Cap: "shall not be liable for consequential damages" is a Cap positive in CUAD labeling (E2, E3), not a negative.

## 6. Known near-misses and exclusions

| Pattern | What happens | Evidence |
|---|---|---|
| Payment/fee caps: "annual fee shall not exceed $300", "aggregate fees payable ... shall not exceed 6.0%", milestone totals | +1 from CL-G5 only; fires only if threshold = 1 | E9, E10 (**VERIFIED**: 53 of 86 "shall not exceed" occurrences are outside labeled Cap spans) |
| "maximum liability" in a non-cap sentence | +2, fires at threshold 2 (false positive) | E11 (Sonos, "subject to the maximum liability parameters set forth in Exhibit C") (**VERIFIED**) |
| Boilerplate damages exclusion | Counts as a Cap positive per CUAD labeling; scores 1-2 now | E2, E3 |
| Carve-out only (no cap phrase) | 0-1 | E8 |
| Cap written without any anchor phrase ("liability ... whether in contract or tort, exceed the price paid") | Scores only the support phrases it contains (1 here) | E5 (Scansource) |
| Claim time bar, limited recourse, warranty limitation | 0; no rule | E6, E7 |

## 7. Known weak spots (be honest in the write-up)

1. **Anchor recall is very low.** Only 36 of 432 spans (8%) contain an anchor phrase (**VERIFIED**); 147 of 181 contracts have no anchored span. Span-level score distribution with the current rules (**VERIFIED**): 0 for 169 spans, 1 for 123, 2 for 115, 3+ for 25. Detection depends on stacking support groups, so the threshold will sit at 2 and the category stays recall-limited.
2. **Heterogeneous positives.** Time bars, limited recourse, warranty limits and exclusive-remedy clauses have nothing in common with amount caps. Keyword rules cannot cover them without large false-positive costs. They are documented as misses.
3. **"Limitation of liability" is mostly a heading.** 150 occurrences sit outside the labeled span, but in the same chunk, so it still helps at chunk level.
4. **Chunk overlap inflates chunk counts about 3x**; sim F1 is optimistic (threshold tuned on train) and is a bug check only.

## 8. Train-only simulation (bug check, optimistic)

Approximate scorer, train chunks, unmasked pairs, best threshold by F1. **VERIFIED** by scratch run; "current" reproduces the .670 in plan.md.

| Variant | Best F1 | Th | TP | FP | FN |
|---|---|---|---|---|---|
| current | .670 | 2 | 413 | 71 | 336 |
| C1: drop CL-G4-01 only | .695 | 2 | 437 | 71 | 312 |
| C1: drop all CL-G4 | .698 | 2 | 441 | 74 | 308 |
| C1 + C2 (lost profits group) | .717 | 2 | 468 | 89 | 281 |
| C1 + C2 + C3 (incidental/exemplary/whether in contract) | .736 | 2 | 512 | 130 | 237 |
| C1-C4 (+ sole and exclusive remedy) | .745 | 2 | 522 | 130 | 227 |

Each added group raises recall and false positives (FP 74 to 130); precision falls from ~.86 to ~.80. That is the trade being proposed.

## 9. Proposed rule edits (NOT applied; need Mahir's OK)

| ID | Change | Train evidence (spans containing / all-train occurrences) | Why |
|---|---|---|---|
| C1 | Remove CL-G4 entirely (CL-G4-01, -02, -03 retired; IDs not reused) | 227 of 234 Uncapped chunks are also Cap chunks; F1 +.028 | Counter penalizes real Cap positives (E4, E5) |
| C2 | New support group CL-G7 "lost-profit wording": lost profits (01), loss of profit (02), lost revenue (03), loss of data (04) | 54/60, 36/40, 12/13, 12/16 (precision ~0.75-0.92) | Standard damages-exclusion terms that CUAD labels as Cap |
| C3 | New support group CL-G8 "other damages terms": incidental (01), exemplary (02), whether in contract (03) | 130/189, 55/70, 28/38 (~0.69-0.79) | Same, broader list. Group-max means three phrases add only +1 |
| C4 | New support group CL-G9 "exclusive remedy": sole and exclusive remedy (01) | 18/20 (0.90) | Exclusive-remedy limits are labeled Cap |

C3 costs the most precision (FP 89 to 130 in the table above). Candidates rejected: "indirect" (127 spans / 872 occ, 0.15), "special" (0.32), "liable for" (0.24), "limited to" (0.06), bare "liability" (0.09), "exclusive remedy" without "sole and" (32/47, 0.68; left out to keep C4 narrow). "limit of liability" and "limitation on liability" did not appear in labeled spans (0/11 and 1/12).

## 10. Examples that exercise each branch

All from the 326 train contracts. "Now" = current rules, "proposed" = after C1-C4. Scores from the approximate scratch scorer (not yet the Phase 4 scorer).

| ID | Branch | Source | Text (shortened) | Now | Proposed |
|---|---|---|---|---|---|
| E1 | Anchor + support (clean amount cap) | Cap span, NETGEAR distribution agreement | "EXCEPT FOR DAMAGES ARISING UNDER SECTIONS 14.A AND 16.A, IN NO EVENT WILL NETGEAR's OR BAY NETWORKS' TOTAL LIABILITY FOR ANY DAMAGES ... EXCEED THE [*] TO NETGEAR PURSUANT TO THE AGREEMENT." | 3 (+2 total liability, +1 in no event) | 3 |
| E2 | Damages exclusion, no anchor (the common positive) | Cap span, MACROGENICSINC_08_02_2013 | "NEITHER PARTY SHALL BE LIABLE TO THE OTHER FOR ANY SPECIAL, CONSEQUENTIAL, INCIDENTAL, PUNITIVE, OR INDIRECT DAMAGES OR FOR LOST PROFITS ..." | 2 (+1 neither party shall be liable, +1 consequential) | 4 |
| E3 | Anchor + support, counter trims it | Cap span, BERKELEYLIGHTS_06_26_2020 | "TO THE GREATEST EXTENT PERMITTED UNDER APPLICABLE LAW, IN NO EVENT WILL A PARTY'S AGGREGATE LIABILITY (ABOVE AMOUNTS ACTUALLY PAID ...) ..." (full span also contains "shall not apply") | 2 (+2 aggregate liability, +1 in no event, -1 shall not apply) | 3 |
| E4 | Counter hurting a real positive (cap + carve-out in one span) | Cap span, IPAYMENT,INC_05_14_2007 | "...shall not exceed [***] times the amount of clearing/sponsorship fees paid ...; provided, however, that this limitation shall not apply to either party's obligation to indemnify the other for credit/fraud losses ..." | **0** (+1 shall not exceed, -1 shall not apply) | 1 |
| E5 | Counter hurting a real positive (damages exclusion + carve-out) | Cap span, CardlyticsInc_20180112 | "Neither Party shall be liable to the other for any special, indirect, incidental, consequential, punitive or exemplary damages ...; provided, however, that the limitations set forth in this Section shall not apply to ... 'Indemnity' ..." | **1** | 4 |
| E5b | Cap with no anchor phrase (a miss) | Cap span, Scansource Cisco | "In no event shall Cisco's or its suppliers' or licensors' liability to Customer, whether in contract, tort ..., exceed the price paid by Customer for the Software ..." | 1 | 2 |
| E6 | Zero-score positive: time bar | Cap span, ADMA BioManufacturing | "All claims by Sanofi Pasteur for breach or default under this Agreement shall be brought within [***] year after the cause of action comes into existence or otherwise shall be waived." | 0 | 0 |
| E7 | Zero-score positive: limited recourse | Cap span, WELLSFARGOMORTGAGEBACKEDSECURITIES | "...the obligations of Counterparty hereunder are limited recourse obligations of Counterparty, payable solely from the Trust Estate ..." | 0 | 0 |
| E8 | Carve-out sentence only (Uncapped hard negatives N1-N5, gate-2 review) | Magenta ("THESE LIMITATIONS SHALL NOT APPLY TO DAMAGES ARISING FROM ... GROSS NEGLIGENCE"); Edietsco ("SHALL BE INAPPLICABLE TO ..."); Kitov ("Nothing in this Section 8.7 shall operate to limit or exclude any liability ...") | as shown | 0 for all 5 | 0 for 4; 1 for Pareteum ("Limitation of liability ... shall not apply: a) ... willful misconduct") from "limitation of liability" |
| E9 | Fee cap (CL-G5 false positive) | Not a Cap span; AtnInternationalInc_20191108 | "annual fee shall not exceed three hundred dollars ($300.00)" | 1 | 1 |
| E10 | Fee cap in an offering | Not a Cap span; ALLIANCEBANCORPINC | "the aggregate fees payable to Sandler O'Neill and Selected Dealers shall not exceed 6.0% of the aggregate dollar amount of the Securities sold" | 1 | 1 |
| E11 | Anchor false positive | Not a Cap span; Sonos manufacturing | "(and subject to the maximum liability parameters set forth in Exhibit C), IAC will use commercially reasonable efforts to reduce its inventory of Excess Components" | **2** | 2 |
| E12 | Two labels on one span | Cap span, Aimmune 8-K | "NEITHER PARTY SHALL BE LIABLE ... FOR ANY LOST PROFITS, OR ANY SPECIAL, CONSEQUENTIAL ... NOTWITHSTANDING THE FOREGOING, NOTHING IN THIS SECTION 11.4 IS INTENDED TO OR SHALL LIMIT ... THE INDEMNIFICATION RIGHTS ..." | 1 (nothing in this section subtracts) | 4 |

Scoring note: excerpts are shortened; scores were computed on the complete span text (E9-E11: a ~400-character window around the phrase), so the shortened text may not show every phrase that fired.

## 11. Sources

- CUAD category description: `data/cuad/category_descriptions.csv`.
- Train spans: `data/splits/train.json` via `src/keyword_baseline/data.py`.
- Hard negatives: `data/cuad/gate2_excerpt_review.csv`, `target_category == "Cap On Liability"`, five rows, all labeled Uncapped Liability.
- Chunks and labels: `data/gate3/train_chunks_768_512.csv`, `train_chunk_labels_768_512.csv` (the 227/234 and 515/7 co-occurrence counts come from unmasked rows of the labels file).
- Rule-level provenance: `configs/keyword_rules_v1.json`.
- Reviewer: not yet assigned.

# Decision table: Anti-Assignment

Rule set: `configs/keyword_rules_v1.json` (DRAFT, not frozen). Evidence: the 326 train contracts only (`data/splits/train.json`, `data/gate3/train_*_768_512.csv`, `data/cuad/gate2_excerpt_review.csv`; all 10 gate-2 titles checked to be in train). No validation or test data used; `train_separate_questions.json` not opened.
Status: **APPROVED by Mahir 2026-10-16; A1-A4 (section 9) APPLIED to the JSON** (AA-G7/G8/G9 added, AA-G3-01 retired). Rule set remains an unfrozen draft.
Claim labels: **VERIFIED** = seen in a cited source or scratch run on train; **INFERRED** = hypothesis.

## 1. Inclusion meaning

CUAD asks whether consent is required from a counterparty to assign the contract to a third party. In the labeled data (**VERIFIED**, train spans) positives are not only "Neither party may assign this Agreement without consent". They also include:
- the consequence sentence on its own ("Any purported assignment without such consent shall be void");
- permitted-assignment exceptions that sit in the same clause (to affiliates, on merger, "either party may assign ... without consent");
- "delegate" or "sub-contract" restrictions ("Neither Party shall delegate the performance of its duties ... without the prior written consent");
- one-line fragments ("transferable or assignable.", "Any assignment in violation of this Section 14.1 shall be null and void.").

Not included: IP ownership transfer ("Each Party will assign, and does hereby assign, ... rights with respect to the Inventions"), change-of-control termination rights, and license non-transferability. These are other categories, but see section 5: text of these categories often shares a chunk with a real Anti-Assignment clause.

Train support: 404 spans in 235 of 326 contracts (**VERIFIED**, Phase 1 table).

## 2. Evidence groups

Each group counts at most once per chunk. Anchor +2, support +1, counter -1, floor 0. Plain substring match on normalized text. Groups marked NEW are proposed in section 9.

"Spans containing" = how many of the 404 Anti-Assignment spans contain the phrase; "all-train occ." = substring count over all 326 contracts; "chunk TP / FP" = unmasked train chunks (9,660; 782 positive) that contain the phrase and are labeled positive / negative for Anti-Assignment. All **VERIFIED** (scratch runs `cat.py`, `cand2.py` and a chunk-level phrase counter).

| Group | Role | Phrase (rule ID) | Spans containing | All-train occ. | Chunk TP / FP |
|---|---|---|---|---|---|
| AA-G1 prohibition on assigning | anchor | may not assign (01) | 23 | 23 | 60 / 0 |
| | | shall not assign (02) | 12 | 12 | 29 / 0 |
| | | may not be assigned (03) | 31 | 34 | 77 / 5 |
| | | shall not be assigned (04) | 5 | 5 | 12 / 0 |
| | | not assign (05) | 47 | 50 | 117 / 9 |
| | | not be assigned (06) | 37 | 43 | 92 / 11 |
| AA-G6 unconsented assignment is void | anchor | without such consent (01) | 14 | 18 | 49 / 0 |
| | | purported assignment (02) | 11 | 12 | 34 / 0 |
| | | shall be void (03) | 27 | 35 | 79 / 15 |
| AA-G7 assigning "this Agreement" (NEW) | anchor | assign this agreement (01) | 80 | 129 | 232 / 13 |
| | | assign its rights (02) | 26 | 37 | 67 / 8 |
| | | assign any (03) | 24 | 33 | 70 / 11 |
| | | (union of the three) | | | 338 / 32 |
| AA-G2 generic consent | support | without the prior written consent (01) | 141 | 346 | 387 / 449 |
| | | without prior written consent (02) | 9 | 32 | 33 / 44 |
| AA-G8 bare "assignment" (NEW) | support | assignment (01) | 119 | 1,093 | 609 / 965 |
| AA-G9 permitted assignment (NEW) | support | may assign (01) | 86 | 147 | 270 / 20 |
| AA-G3 other ways of moving the contract | support | transfer (01) | 148 | 2,809 | 426 / 2,384 |
| | | delegate (02) | 46 | 103 | 129 / 106 |
| AA-G4 IP assignment | counter | right, title and interest (01) | 0 | 207 | 10 / 390 |

Maximum score now: anchors G1, G6 (2 each) + supports G2, G3 (1 each) = **6**. After A1-A3: anchors G1, G6, G7 + supports G2, G3, G8, G9 = **10** (A4 does not change the maximum; AA-G3 keeps "delegate").

Why AA-G2 is only support (**VERIFIED**): it fires on 836 unmasked chunks, 449 of them negative (precision .46); "without the prior written consent" is standard wording in confidentiality, license and assignment-of-IP clauses alike.

## 3. Counterevidence and vetoes

- **AA-G4-01 "right, title and interest" (counter, -1).** The spec lists this as a confusion case and the rule had "not verified on train". It is now checked (**VERIFIED**):
  - 0 of 404 Anti-Assignment spans contain it; it occurs 207 times in the 326 contracts.
  - 403 unmasked chunks contain it: 393 negative, 10 positive (2.5%, below the 8% base rate). 156 of the 403 also contain an IP Ownership Assignment span.
  - It subtracts 1 from those 10 real positives, which are chunks that hold an Anti-Assignment clause elsewhere plus a definition or ownership sentence (Wells Fargo "cap collateral" definition, Buffalo Wild Wings sign ownership, Ehave ownership, Garrett Motion). Only 1 of the 10 crosses threshold 2 without the counter (Garrett Motion, 2 to 1).
  - Under current rules at threshold 2, negatives scoring 2 or more among those 393: 16 without the counter, 4 with it. Net effect: it removes about 12 false positives and loses 1 true positive. Sim F1 with the counter .635, without .630; after A1-A3 .790 with, .787 without.
  - Decision: **keep, no edit.** It is the one counter that pays for itself; this is the Cap On Liability lesson applied (check against positives and co-occurrence before keeping), and here it passes. Promotes the provenance from "not verified" to "verified on train" in the revision note.
- **Change-of-control counters: tested and rejected** (section 5).
- **Vetoes:** none. Chunk-wide design, no windows (see section 4).

## 4. Context / proximity limits

None. All matching is chunk-wide (768 words, 512-word overlap). Consequence (**VERIFIED**): an assignment sentence in one section and a "transfer" or "consent" in a different section of the same chunk combine into one score. This is why the noisy phrases "transfer" and "assignment" are limited to support (+1, once per chunk).

## 5. Required confusion cases

**Anti-Assignment vs IP assignment (AA-G4-01).** Gate-2 hard negative N1 (Anixa: "Each Party will assign, and does hereby assign, to the other Party rights with respect to the applicable Inventions ...") scores 0 now and 0 after A1-A3 as a bare sentence. In its 600-character source excerpt it scores 0 now and 1 after A1-A3 (only "assignment" in "such assignment"), below any threshold in the sim. At chunk level (**VERIFIED**): 348 train chunks fully contain an IP Ownership Assignment span; 13 of them (3.7%) are also Anti-Assignment positives, so IP chunks are mostly clean negatives. "hereby assign" (7 positive chunks vs 111 negative) was tested as an extra counter: F1 .738 to .738, no gain, not proposed. The counter AA-G4-01 is the only IP guard needed (section 3).

**Anti-Assignment vs Change of Control.** Unmasked chunks labeled for both categories (**VERIFIED**, label file):

| | CoC = 0 | CoC = 1 |
|---|---|---|
| AA = 0 | 8,681 | 165 |
| AA = 1 | 655 | 112 |

112 of the 277 Change Of Control chunks (40%) are also Anti-Assignment positives, because "assignment, including by merger or change of control, requires consent" is one clause. Tested as AA features, on top of A1 (**VERIFIED**, sim):

| Test | F1 | Verdict |
|---|---|---|
| baseline for the test (A1 only) | .738 | |
| "change of control" + "change in control" as counter | .735 | rejected: removes real positives |
| same two phrases as support | .694 | rejected: "change of control" 60 positive vs 180 negative chunks, "change in control" 26 vs 102 |
| "merger" as counter | .695 | rejected: 228 positive vs 214 negative chunks |

Decision: **Anti-Assignment contains no change-of-control wording.** The two labels coexist on one chunk and separating them is the Change Of Control table's job (next). Gate-2 CoC hard negatives: N3 Dynamex ("In the event of a change in control of a Party, the other Party shall have the right ... to terminate") scores 0 on Anti-Assignment under every variant (correct). N2 Verticalnet ("No transfer of this Agreement by operation of law or change in Control of a party ... shall be considered an assignment for purposes of this Section") is the cross-reference case: as a bare sentence it scores 1 now, 2 after A1-A3, 1 after A4. Its 600-character excerpt also contains the clause "neither party may assign this Agreement without the other party's prior written consent", so the excerpt scores 1 now and 5 after A1-A3: INFERRED that this chunk is a legitimate Anti-Assignment positive and the label belongs to a different span in it.

**Change of Control vs assignment-only (cross-reference for the next table).** Anti-Assignment text that says only "assign" scores on this category and not on Change Of Control. The reverse (CoC text mentioning "assignment") is a CoC-table question; do not add "assignment" wording to CoC as an anchor. 165 CoC-only chunks and 112 shared chunks are the counts to carry over.

## 6. Known near-misses and exclusions

| Pattern | What happens | Evidence |
|---|---|---|
| Permitted-assignment sentence without any restriction ("BKC may assign this Agreement to any person which acquires its business") | fires A1 (+2) and A3 (+1), false positive in chunks where the annotator labeled no Anti-Assignment | F1; 13 negative chunks for "assign this agreement", 20 for "may assign" (**VERIFIED**) |
| "assignment for the benefit of creditors" (insolvency termination events) | "assignment" +1 only, never alone enough at threshold 3 | F2; 965 negative chunks contain "assignment" |
| "transfer" in confidentiality, forum and share-issuance wording | +1 from AA-G3-01; with "without the prior written consent" in the same chunk it reaches 2 | F3; 2,384 negative chunks (**VERIFIED**); the reason for A4 |
| IP assignment sentences | 0-1 | E-IP |
| License "nontransferable (except to permitted assigns)" | +1 from "transfer" | E12 |
| Genuine anti-assignment text whose labeled span belongs to another category (franchise "Transfer by You", CoC clause plus its neighbor) | scores 2-5, looks like a false positive but is arguably correct; unavoidable | N2, N4 (**INFERRED** that annotators labeled only the other category) |
| Restriction written without any anchor phrase ("may be assigned or transferred", "shall not be assignable", "shall not subcontract, assign, license") | scores only what support phrases it contains (0-1) | E6, E7, E8 |

## 7. Known weak spots (be honest in the write-up)

1. **Anchor recall is still low.** Only 122 of 404 spans (30%) contain an anchor phrase now; 128 of 235 contracts have no anchored span (**VERIFIED**). After A1: 205 of 404 spans, 70 of 235 contracts without an anchored span. Span score distribution now: 0 for 126, 1 for 108, 2 for 78, 3 or more for 92. After A1-A3: 0 for 56, 1 for 88, 2 for 66, 3 or more for 194. After A1-A4: 0 for 91 (dropping "transfer" costs low-score spans their only point).
2. **Many positives say only "assignment", "assignable" or "assigned".** "shall not be assignable", "may be assigned or transferred", "transferable or assignable" have no rule that credits them as an anchor. "assignable" was tested as support (F1 .738 to .734) and as anchor (.720): rejected.
3. **AA-G3-01 "transfer" is noisy**: 148 spans but 2,809 occurrences and 2,384 negative chunks. Before A1-A3 it is load-bearing: dropping it takes F1 .635 to .607 (it combines with AA-G2 to reach 2). After A1-A3 it is not (A4).
4. **AA-G2 generic consent is support only** (449 negative chunks; precision .46). Dropping it entirely: F1 .790 to .743 (A1-A3 basis), so it stays.
5. **Bare "assignment" (A2) is a weak support** (609 vs 965 chunks). It raises the best threshold from 2 to 3. Group-max means it adds at most +1.
6. **Annotation noise**: genuine anti-assignment wording inside chunks labeled only for another category (franchise "Transfer by You", CoC neighbors); a keyword baseline cannot beat this.
7. **Chunk overlap inflates counts about 3x**; sim F1 is optimistic (threshold tuned on train) and is a bug check only.

## 8. Train-only simulation (bug check, optimistic)

Approximate scorer, 9,660 unmasked train chunks (782 positive), best threshold by F1. **VERIFIED** by scratch run; "current" reproduces the .635 in the hand-off.

| Variant | Best F1 | Th | TP | FP | FN |
|---|---|---|---|---|---|
| current | .635 | 2 | 432 | 147 | 350 |
| A1: anchor AA-G7 (3 phrases) | .738 | 2 | 558 | 172 | 224 |
| A1 + A2 (support "assignment") | .763 | 3 | 522 | 64 | 260 |
| A1 + A2 + A3 ("may assign") | .790 | 3 | 552 | 64 | 230 |
| A1-A4 (+ retire "transfer") | .802 | 2 | 600 | 115 | 182 |

Single-edit checks used to choose among candidates (all against the baseline stated):
- Drop AA-G4-01 only: .635 to .630 (current), .790 to .787 (A1-A3). Counter kept.
- Drop "transfer" only, current rules: .607. Drop "transfer" and "delegate": .567 (best threshold falls to 1). Neither is proposed without A1-A3.
- G7 with 2 phrases only: .721; with 3: .738; with 5 (adds "assign or transfer", "assignment of this agreement"): .742, and the best A1-A3 variant with 5 was .766 vs .763, no useful gain, so 3 phrases.
- Extra AA-G6 phrases ("attempted assignment", "null and void", "shall be null") on the A1-A4 basis: .802 to .804, +.002, not proposed.
- Extra supports on top of A1-A3 + A4: "neither party may" .800, "written consent of the other" .799, "operation of law" .786, "merger" .786. None beats .802.

A1-A3 trade-off: precision at the best threshold is .90 (552 / 616); A4 raises recall .71 to .77 and drops precision to .84 (600 / 715) because the best threshold moves from 3 to 2.

Because the final threshold is chosen later on validation, these are not the thresholds that will be used. Max score is 10, so thresholds 1-10 will be tried.

## 9. Proposed rule edits (NOT applied; need Mahir's OK)

| ID | Change | Train evidence | Why | Sim F1 |
|---|---|---|---|---|
| A1 | New anchor group **AA-G7** "assigning this Agreement": AA-G7-01 "assign this agreement", AA-G7-02 "assign its rights", AA-G7-03 "assign any" | spans 80 / 26 / 24; all-train occ. 129 / 37 / 33; chunk precision .95 / .89 / .86, union 338 TP vs 32 FP | The current anchors need "may not" / "shall not" / "not be assigned"; the most common drafting "Neither party may assign this Agreement" (E1) never fires them. Anchor spans 122 to 205 of 404 | .635 to .738 |
| A2 | New support group **AA-G8**: AA-G8-01 "assignment" | 119 spans / 1,093 occ.; chunks 609 TP vs 965 FP (precision .39, recall .78) | Credits one-line fragments ("Any assignment in violation of this Section ... null and void", E4). Weak: one point only | .738 to .763 (th 3) |
| A3 | New support group **AA-G9**: AA-G9-01 "may assign" | 86 spans / 147 occ.; chunks 270 TP vs 20 FP (precision .93) | Permitted-assignment exceptions sit inside the labeled clause | .763 to .790 (th 3) |
| A4 | **Retire AA-G3-01 "transfer"** (ID never reused; AA-G3-02 "delegate" stays) | 148 spans, 2,809 occ., chunks 426 TP vs 2,384 FP (precision .15) | Noisiest rule in the category; load-bearing only before A1-A3. Recall gain, precision loss. **Optional: Mahir's call** (F1 gain is only +.012) | .790 to .802 (th 3 to 2) |
| no edit | Keep AA-G4-01 (counter), AA-G2 (support), AA-G6, AA-G1 as they are | section 3 | AA-G4-01 now verified on train | |

Candidates rejected: "assignable" / "not assignable" (support .734, anchor .720), "neither party may" as anchor (.721), "operation of law" (.701 as anchor), "successors and assigns" (.680 as anchor, 168 occ. but 8 spans), "binding upon" / "inure" (boilerplate), "hereby assign" as counter (no gain), change-of-control wording in any role (section 5), "void" alone (309 vs 1,128 chunks), "consent" alone (682 vs 2,615), "prohibited" (.11).

If A4 is declined, threshold is expected to sit at 3, F1 .790. If A2-A3 are declined, A1 alone reaches .738 at threshold 2.

## 10. Examples that exercise each branch

All from the 326 train contracts. Scores are from the approximate scratch scorer (`sim.score`, **VERIFIED** by running it, not by reading the text). "Now" = current rules; "A1-3" = after A1-A3; "A1-4" = after A1-A4. Spans are scored on the full span text; the F and E-IP rows use a ~460-character window around the phrase, so the scorer sees a chunk-level slice, not the whole 768-word chunk.

| ID | Branch | Source | Text (shortened) | Now | A1-3 | A1-4 |
|---|---|---|---|---|---|---|
| E1 | Standard clause, no G1 phrase (the main miss) | AA span, CORIO license and hosting agreement; also gate-2 positive P1 | "Neither party may assign this Agreement or any rights or obligations hereunder, whether by operation of law or otherwise, without the prior written consent of the other party." | 1 (+1 G2) | 4 (+1 G2, +2 G7, +1 G9) | 4 |
| E2 | Anchor + consequence | AA span, Manufacturers Services | "MSL may not assign this Agreement without IBM's prior written consent. Any attempted assignment without such consent is void." | 4 (+2 G1, +2 G6) | 7 (+2 G7, +1 G8) | 7 |
| E3 | Consequence-only | AA span, Cerence | "Any purported assignment without such consent shall be void." | 2 (+2 G6) | 3 (+1 G8) | 3 |
| E4 | One-line fragment, no anchor | AA span, CORIO | "Any assignment in violation of this Section 14.1 shall be null and void." | **0** | 1 (+1 G8) | 1 |
| E5 | Delegate-driven support | AA span, Global Technologies | "Neither Party shall delegate the performance of its duties under this Agreement without the prior written consent of the other Party." | 2 (+1 G2, +1 G3) | 2 | 2 |
| E6 | Miss: "assignable" | AA span, Aduro | "This Agreement shall not be assignable by Consultant." | **0** | **0** | **0** |
| E7 | Miss: "may be assigned or transferred" | AA span, Kiromic | "Neither this Agreement nor any right hereunder or interest herein may be assigned or transferred by Consultant without the express written consent of Company." | 1 (+1 "transfer") | 1 | **0** |
| E8 | Miss: "shall not subcontract, assign, license" | AA span, iPayment | "Except as expressly set forth herein, ISO shall not subcontract, assign, license or in any other manner extend or transfer to any third party any right or obligation ISO has with respect to SERVICERS' Program." | 1 | 1 | **0** |
| E9 | AA clause also describing change of control | AA span, Reynolds Consumer Products | "A change of control shall be deemed an assignment requiring consent hereunder provided that any transfer or assignment that results in ... shall not require ..." | 1 | 2 (+1 "transfer", +1 G8) | 1 |
| N1 | IP assignment hard negative | gate-2 N1, Anixa ("Each Party will assign, and does hereby assign, to the other Party rights ... Inventions ...") | as shown | 0 | 0 | 0 |
| N2 | CoC / assignment-only cross-reference | gate-2 N2, Verticalnet ("No transfer of this Agreement by operation of law or change in Control ... shall be considered an assignment ...") | as shown | 1 | 2 | 1 |
| N3 | CoC termination hard negative | gate-2 N3, Dynamex ("In the event of a change in control of a Party, the other Party shall have the right ... to terminate") | as shown | 0 | 0 | 0 |
| N4 | Franchise transfer restriction, labeled Non-Transferable License | gate-2 N4, Airtech ("You shall not sell, assign, transfer, convey ... without the prior written consent of AIRSOPURE") | as shown | 2 | 2 | 1 |
| N5 | License non-transferability hard negative | gate-2 N5, OFG Bancorp ("nonexclusive, nontransferable (except to permitted assigns of this Agreement) limited license ...") | as shown | 1 | 1 | 0 |
| F1 | Permitted-assignment false positive | not an AA positive; International Fast Food (Burger King) ("15.9 Assignment by BKC. BKC may assign this Agreement to any person or company which acquires its Burger King business ...") | window | 1 | **5** (+2 G7, +1 G8, +1 G9, +1 "transfer") | 4 |
| F2 | "assignment" in insolvency | not an AA positive; Deltathree ("the making of a general assignment for the benefit of creditors") | window | 0 | 1 | 1 |
| F3 | "transfer" in a confidentiality clause | not an AA positive; Cytodyn ("unauthorized disclosure, use or transfer of its confidential information") | window | 1 | 1 | 0 |
| C1 | Counter fires on a negative (works) | not an AA positive; Aimmune 8-K ("assign to Xencor ... all of Aimmune's right, title and interest in and to any agreements") | window | n/a | 3 with the counter, 4 without | |

Notes: E1 and N1-N5 are gate-2 rows (`independent_review_decision` is empty for all ten; the 5 positives and 5 hard negatives were taken from the excerpt file as given). N2 and N4 excerpts (600 characters of context) score 1 and 4 now, 5 and 5 after A1-A3, because they contain real anti-assignment sentences beside the labeled span (section 5, section 6). F1 is the clearest cost of A1/A3: a one-sided right to assign counts as evidence. C1 shows the counter lowers a score but, at threshold 3, a 3 still fires; the counter pays through the 12 negatives it removes at threshold 2 (section 3), not through this example.

## 11. Sources

- CUAD category description: `data/cuad/category_descriptions.csv`.
- Train spans: `data/splits/train.json` via `.agent/scratch/lib.py`.
- Gate-2 excerpts: `data/cuad/gate2_excerpt_review.csv`, `target_category == "Anti-Assignment"` (5 positive, 5 hard negative; Ip Ownership Assignment, Change Of Control x2, Non-Transferable License, License Grant sources).
- Chunks and labels: `data/gate3/train_chunks_768_512.csv`, `train_chunk_labels_768_512.csv` (unmasked rows; AA x CoC table; IP overlap = IP Ownership Assignment span fully inside chunk `char_start`..`char_end`).
- Rule-level provenance: `configs/keyword_rules_v1.json` (categories["Anti-Assignment"]).
- Scratch: `.agent/scratch/{lib,cat,cand2,sim}.py`; one-off experiment scripts in the session scratchpad (not part of the repo).
- Reviewer: not yet assigned.

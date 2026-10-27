# Decision table: Change Of Control

Rule set: `configs/keyword_rules_v1.json` (FROZEN 2026-10-18 as `keyword_rules_v1`, 184 IDs, SHA-256 `07602f34...7ba7e3`). Evidence: the 326 train contracts only (`data/splits/train.json`, `data/gate3/train_*_768_512.csv`, `data/cuad/gate2_excerpt_review.csv`; no validation or test data used; `train_separate_questions.json` and `test.json` not opened).
Status: **APPROVED by Mahir 2026-10-16; CC1-CC4 (section 9) APPLIED to the JSON** (CC-G1-02 retired; CC-G4/G5/G6/G7 added; sim reproduces F1 .559).
Claim labels: **VERIFIED** = seen in a cited source or scratch run on train; **INFERRED** = hypothesis.

## 1. Inclusion meaning

CUAD asks whether one party has a right (usually to terminate, or to demand consent) when the other party changes ownership or control: a merger, an acquisition, or a sale of most of its shares or assets. In the labeled train data (**VERIFIED**, 152 spans in 76 contracts) the positives are mixed:
- Explicit wording: "This Agreement may be terminated by either Party ... following a Change of Control of Exact". 64 of 152 spans (42%) contain "change of control" or "change in control"; 88 spans (58%) do not.
- Ownership-change termination without the word "control": "In the event of the merger or consolidation of Company with any other entity, Licensor shall have the right to terminate" (Mossimo), "If ENERGOUS is acquired by a third party, ENERGOUS' acquirer will have the right ... to terminate" (Energous), "Ownership Change Event" (theglobe).
- Change of control treated as an assignment ("any change of control, merger, consolidation, or acquisition ... shall be deemed an assignment", DigitalCinema), and permitted-assignment exceptions tied to a merger or sale of the business (CORIO, Exact Sciences, Tom Online).
- Franchise "Transfer" definitions that include a merger, consolidation or ownership change (Buffalo Wild Wings, Mrs. Fields, JOINTCORP, Hospitality Investors Trust).
- Bare list headers that the annotator labeled together with the real clause ("A Termination Event shall have occurred if:", "This Agreement may be terminated:"). No keyword rule can find these.

Not included: plain assignment restrictions (Anti-Assignment), IP ownership transfer, and employment severance triggered by a change in control. The first is the hard one: see section 5.

Train support: 152 spans in 76 of 326 contracts, the fewest of the 10 categories (**VERIFIED**, Phase 1 table).

## 2. Evidence groups

Each group counts at most once per chunk. Anchor +2, support +1, counter -1, floor 0. Plain substring match on normalized text. NEW = proposed in section 9.

"Spans containing" = how many of the 152 Change Of Control spans contain the phrase; "all-train occ." = substring count over all 326 contracts; "chunk TP / FP" = unmasked train chunks that contain the phrase and are labeled positive / negative for Change Of Control. All **VERIFIED** (scratch runs `cat.py`, `cand2.py`, `cc.py`). Chunk universe: 9,714 unmasked chunks, **282 positive** (277 of them are also unmasked for Anti-Assignment, which is where the 112 / 165 split comes from; the other 5 have Anti-Assignment masked).

| Group | Role | Phrase (rule ID) | Spans containing | All-train occ. | Chunk TP / FP |
|---|---|---|---|---|---|
| CC-G1 explicit wording | anchor | change of control (01) | 52 | 179 | 111 / 121 |
| | | change in control (02) | 14 | 88 | 33 / 93 |
| | | change-of-control (03) | 0 | 0 | 0 / 0 |
| CC-G2 ownership-change wording | support | voting securities (01) | 5 | 103 | 18 / 143 |
| | | controlling interest (02) | 1 | 21 | 15 / 25 |
| | | merges with (03) | 3 | 4 | 8 / 3 |
| | | change in ownership (04) | 1 | 2 | 3 / 0 |
| CC-G3 triggering transaction | support | merger (01) | 36 | 269 | 118 / 334 |
| | | consolidation (02) | 21 | 105 | 70 / 136 |
| | | substantially all (03) | 20 | 178 | 91 / 330 |
| CC-G4 "change in control" (NEW, replaces CC-G1-02) | support | change in control (01) | 14 | 88 | 33 / 93 |
| CC-G5 termination right (NEW) | support | may terminate (01) | 16 | 354 | 83 / 613 |
| | | right to terminate (02) | 7 | 222 | 55 / 427 |
| | | terminate this agreement (03) | 30 | 691 | 120 / 1,031 |
| | | immediately terminate (04) | 2 | 71 | 21 / 161 |
| | | automatically terminate (05) | 3 | 45 | 16 / 96 |
| | | (union of the five) | | | 142 / 1,348 |
| | | (union, only in chunks that contain an anchor phrase) | | | 79 / 25 |
| CC-G6 merger or consolidation (NEW) | anchor | merger or consolidation (01) | 9 | 38 | 38 / 29 |
| | | consolidation or merger (02) | 4 | 6 | 12 / 5 |
| | | (union of the two) | | | 50 / 34 |
| CC-G7 ownership-change wording (NEW) | anchor | ownership change (01) | 3 | 3 | 6 / 0 |
| | | change in the control (02) | 1 | 2 | 3 / 0 |
| | | (union of the two) | | | 9 / 0 |

Maximum score now: anchor CC-G1 (2) + supports CC-G2, CC-G3 (1 each) = **4**. After CC1-CC4: anchors CC-G1, CC-G6, CC-G7 (6) + supports CC-G2, CC-G3, CC-G4, CC-G5 (4) = **10**.

Why the anchors are weak (**VERIFIED**): "change of control" has chunk precision .48 and recall .39; "change in control" .26 and .12. 103 of the 121 false-positive chunks for "change of control" sit in contracts that do contain a labeled Change Of Control span elsewhere. They are definitions ("1.6 'change in control' means ..."), permitted-assignment exceptions ("may assign ... in connection with a change of control", ON2, Accuray, Magenta), employment severance ("outside the change in control period", Bicycle) and assignment headings ("31. Assignment and Change of Control", Adams Golf). A keyword cannot tell the clause the annotator labeled from these; the only chunk-level signal found is the termination wording next to the anchor (CC1-CC2 below).

## 3. Counterevidence and vetoes

Every candidate counter was checked against positive chunks and against Anti-Assignment co-occurrence (the lesson from Cap On Liability and Anti-Assignment). **VERIFIED** (sim, current rules as baseline .476; each row = add that one counter):

| Counter tried | Chunk TP / FP | Sim F1 | Verdict |
|---|---|---|---|
| severance | 0 / 75 | .482 | zero positives lost, but +.006 alone and +.001 on top of CC1-CC4; not proposed (CC5, rejected as noise) |
| good reason | 0 / 19 | .480 | same |
| means | 48 / 1,894 | .459 | rejected: removes 20 TP |
| as defined | 37 / 1,364 | .466 | rejected |
| right, title and interest (the IP counter used in Anti-Assignment) | 17 / 382 | .468 | rejected: loses 5 TP, gains 5 FP-removals |
| hereby assign | 3 / 115 | .477 | no gain |
| assign this agreement | 50 / 210 | .467 | rejected: 45 of the 50 TP chunks are also Anti-Assignment positives |
| without the prior written consent | 72 / 785 | .461 | rejected |
| may not assign | 12 / 50 | .480 | no usable gain (+.004), and all 12 TP chunks are Anti-Assignment positives; assignment wording is not a safe counter (section 5) |
| employment / executive / stock option | 19 / 616, 21 / 697, 6 / 26 | .464 / .468 / .471 | rejected |

**Vetoes:** none (chunk-wide design, no windows). No counter is proposed.

## 4. Context / proximity limits

None. All matching is chunk-wide (768 words, 512-word overlap). Consequence (**VERIFIED**): "change of control" in one section and "may terminate" in a different section of the same chunk combine into one score. This is why CC-G5 (termination) is support only: alone it is almost noise (142 TP vs 1,348 FP, precision .10; the number of chunks is huge because termination clauses are everywhere), but next to an anchor it separates clause from definition (79 TP vs 25 FP, precision .76, against .48 for the anchor alone).

## 5. Required confusion cases

### 5a. Change of Control vs assignment-only (Anti-Assignment cross-reference)

Unmasked chunks labeled for both categories (**VERIFIED**, label file; same table as the Anti-Assignment table):

| | CoC = 0 | CoC = 1 |
|---|---|---|
| AA = 0 | 8,681 | 165 |
| AA = 1 | 655 | 112 |

112 of the 277 Change Of Control chunks (40%) are also Anti-Assignment positives. P(CoC) is 1.9% when AA = 0 but 14.6% when AA = 1, so **assignment wording is mild positive evidence for Change Of Control, not a counter** (**VERIFIED**):

| Assignment phrase | CoC chunk TP / FP | precision (base rate .029) | TP chunks that are also AA |
|---|---|---|---|
| may not assign | 12 / 50 | .19 | 12 of 12 |
| shall not assign | 6 / 22 | .21 | 6 of 6 |
| not be assigned | 14 / 91 | .13 | 14 of 14 |
| assign this agreement | 50 / 210 | .19 | 45 of 50 |
| may assign | 42 / 267 | .14 | 41 of 42 |
| without such consent | 14 / 38 | .27 | 14 of 14 |
| without the prior written consent | 72 / 785 | .08 | 63 of 72 |

Decision: **no assignment wording on Change Of Control**, neither as counter (section 3) nor as support (precision .08 to .27 is far below "change of control" at .48, and the same chunks would then score on both categories). Following the Anti-Assignment note, "assignment" is not added as an anchor either. The separation has to come from what Change Of Control has and Anti-Assignment does not: change-of-control wording (AA has none), merger/consolidation pairs, and termination wording next to them (CC2, CC3).

What the proposed rules do to the two groups of chunks (**VERIFIED**, sim, fire = score at or above the threshold):

| Chunk group | Count | current, th 2 | current, th 3 | proposed, th 2 | proposed, th 3 |
|---|---|---|---|---|---|
| neither label | 8,681 | 180 | 77 | 218 | 68 |
| AA positive, CoC negative ("assignment-only") | 655 | 37 | 18 | 81 | 35 |
| CoC positive, AA negative ("CoC-only") | 165 | 101 | 22 | 117 | 88 |
| both | 112 | 56 | 33 | 80 | 60 |

Honest reading: the proposed rules fire on **more** assignment-only chunks (18 to 35 at th 3, 2.7% to 5.3%) because permitted-assignment exceptions are written with "merger or consolidation" ("may assign ... in the event of a merger or consolidation", Anixa, Fibrogen). At th 3 they also find far more CoC-only chunks (22 to 88 of 165) so the net trade is positive, but this is a leak of Anti-Assignment text into Change Of Control that CC3 makes slightly larger. It is unavoidable without a context rule (a labeled CoC span and the AA exception often sit in one clause: gate-2 hard negatives below).

Gate-2 hard negatives for this category (`target_category == "Change Of Control"`, `example_type == HARD NEGATIVE`, all five have source category Anti-Assignment; **VERIFIED**, scored in section 10): Energous (permitted assignment "to any successor in the event of a Change of Control") scores 2 as a span and 3 with its 600-character excerpt, Euromedia ("A change of control of Rogers shall not be considered an assignment") scores 3, Bellring ("undergoes a 'change in control'") scores 2 now and 1 after CC1, Anixa and Fibrogen (merger/transfer-of-assets exceptions) score 1. **INFERRED**: the Energous and Euromedia excerpts look like real Change Of Control wording and are negatives only because the annotator labeled the chunk's other clause for Anti-Assignment; unavoidable.

### 5b. Anti-Assignment vs Change of Control vs IP assignment (Change Of Control side)

IP ownership sentence ("Each Party will assign, and does hereby assign, ... Inventions", shortened as in the Anti-Assignment table): scores 0 on Change Of Control now and after CC1-CC4 (**VERIFIED**, E-IP). At chunk level (**VERIFIED**): 348 unmasked train chunks fully contain an IP Ownership Assignment span; 12 of them (3.4%) are Change Of Control positives. How often the IP chunks fire:

| Rules | th 2 | th 3 |
|---|---|---|
| current | 8 of 348 (4 are CoC-negative) | 0 |
| proposed (CC1-CC4) | 8 of 348 (3 CoC-negative) | 4 (1 CoC-negative) |

At th 3 the 3 extra firings are IP chunks that really are Change Of Control positives. So IP assignment is a clean negative here, and no IP counter is needed ("right, title and interest" rejected in section 3). Triangle summary: Anti-Assignment text shares chunks with Change Of Control (112 of 277); IP assignment text mostly does not (12 of 348); the Change Of Control side separates them only through its own anchors.

## 6. Known near-misses and exclusions

| Pattern | What happens | Evidence |
|---|---|---|
| Definition of "change in control" or "change of control" | anchor fires, labeled negative unless the annotator tagged it | F1 Array; 121 + 93 FP chunks for the two anchors |
| Permitted assignment "in connection with a change of control" | anchor fires, labeled Anti-Assignment only | F5 ON2; 103 of 121 FP chunks are in contracts that have a CoC span elsewhere (**VERIFIED**) |
| Employment severance "change in control period" | anchor fires; CC1 cuts it from 2 to 1 | F2 Bicycle |
| Assignment clause that mentions "change of control transaction" in passing | scores 2 | F3 Staar, F4 Adams Golf |
| Merger in entire-agreement boilerplate ("merger clause") | "merger" +1 only | CC-G3-01 rationale; 334 FP chunks (**VERIFIED**) |
| Franchise "Transfer" definitions (merger, consolidation, ownership interest) | score 0-4; some positives, some labeled Non-Transferable License or Anti-Assignment | E11, E12 |
| Annotator-labeled list headers ("This Agreement may be terminated:") | no phrase to match | E-header; unavoidable |
| "may be terminated" (passive) | not in CC-G5; tested as extra phrase, F1 .559 to .560, +.001, not added | cc11 (**VERIFIED**) |

## 7. Known weak spots (be honest in the write-up)

1. **Anchor recall is low.** Only 64 of 152 spans (42%) contain an anchor phrase; 36 of 76 contracts have a labeled span but none with an anchor (**VERIFIED**, cat.py). The 88 anchorless spans can reach at most 2 today (two supports), and many score 0 or 1 (E6, E9, E10).
2. **Both anchors are noisy** (.48 and .26 chunk precision, section 2). The best score is a combination of anchor + termination wording, not an anchor alone.
3. **This category is the hardest of the three tables done so far.** Sim F1 starts at .476 (Anti-Assignment started at .635). Even the best variant tested stays near .56. Expect a weak validation F1; it is kept and explained, never fixed by editing rules after validation.
4. **Ownership-change vocabulary is long-tail**: "merges with", "ownership change", "change in ownership", "Ownership Change Event", "substantial change in ownership of its stock", "sells a controlling interest", "is acquired by a third party" each cover one to three contracts. CC4 adds only phrases with zero train false positives, but on 3 contracts of evidence (low support).
5. **Positives with no usable phrase** exist (E11 Hospitality "Change of Ownership Transfer" scores 0; E14 Hertz "Licensee is acquired by a third party" scores 0; E15 Dynamex "the Party whose control has changed" scores 0). "is acquired" tested as anchor: F1 .476 to .485 alone, but 17 FP chunks vs 15 TP (.47), not proposed.
6. **Annotation noise**: genuine change-of-control wording inside chunks labeled only Anti-Assignment (section 5a); a keyword baseline cannot beat this.
7. **Chunk overlap inflates counts about 3x** (CC4: 9 TP chunks come from 3 contracts; "merger or consolidation": 12 TP and 10 FP contracts). Sim F1 is optimistic (threshold tuned on train) and is a bug check only.

## 8. Train-only simulation (bug check, optimistic)

Approximate scorer (`sim.score`), 9,714 unmasked chunks (282 positive), best threshold by F1 over 1-8 (the stock `sim.py` stops at 5; thresholds up to 8 were needed here). **VERIFIED** by scratch runs; "current" reproduces .476 (th 2, 158 TP / 224 FP / 124 FN with the stock `sim.py`).

| Variant | Best F1 | Th | TP | FP | FN |
|---|---|---|---|---|---|
| current | .476 | 2 | 158 | 224 | 124 |
| CC1 alone | .485 | 2 | 148 | 180 | 134 |
| CC2 alone | .474 | 3 | 123 | 114 | 159 |
| CC3 alone | .516 | 2 | 184 | 247 | 98 |
| CC4 alone | .492 | 2 | 165 | 224 | 117 |
| CC1 | .485 | 2 | 148 | 180 | 134 |
| CC1 + CC2 | .481 | 2 | 182 | 292 | 100 |
| CC1 + CC2 + CC3 | .542 | 3 | 144 | 105 | 138 |
| CC1 + CC2 + CC3 + CC4 | **.559** | 3 | 150 | 105 | 132 |

Leave-one-out from CC1-CC4 (.559): without CC1 .555 (3; 161 / 137 / 121), without CC2 .541 (th 2; 180 / 203 / 102), without CC3 .495 (3; 119 / 80 / 163), without CC4 .542 (3; 144 / 105 / 138). So CC3 is the big one, CC2 and CC4 add about .017 each, CC1 adds .004 and mostly shifts balance toward precision (.59 vs .54 precision at th 3: 150 / 255 vs 161 / 298).

Other single checks used to choose the proposals (**VERIFIED**; basis stated):
- Drop CC-G2-01 "voting securities": .476 to .466; drop CC-G2-02 "controlling interest": .455; drop CC-G3-03 "substantially all": .460; drop CC-G3-01/02: .476 (no change). Weak support rules that are not harmful or are load-bearing stay.
- Drop CC-G1-02 outright: .489 (th 2, 138 / 144 / 144); demote to support: .485 (148 / 180 / 134). Demotion keeps more recall, chosen over dropping.
- CC2 phrase set: "may terminate" only .496 to .452 depending on basis, 3 phrases .513, 5 phrases .516, 5 + passive/other variants .518; the 5-phrase set is kept for being simple, not the maximum.
- CC3 variants on the CC1+CC2 basis: "merger, consolidation" as support .537 vs .516 (141 / 102 / 141), but 28 TP vs 68 FP chunks (precision .29) and it fires on enumerations in boilerplate; not proposed. "merger or acquisition" .509 (5 / 20 chunks), "sale of all or substantially all" .530 (24 / 66): not proposed.
- CC4 variants: "change of ownership" 3 / 6 chunks (Hospitality franchise cluster) F1 +.004 vs +.009 for the clean pair; "controlling interest" as anchor .514 (15 / 25).
- Trigger-phrasing support ("in the event of a change of control", "upon a change of control", "following a change of control", "undergoes a change", "other party undergoes", "deemed an assignment") on the CC1-CC3 basis: .537 vs .516 (+.021), but these are all substrings of text the anchor already catches; they would double-count one clause as two groups. Not proposed.

Because the final threshold is chosen later on validation, these thresholds are not the ones that will be used. Max score is 10 after CC1-CC4, so thresholds 1-10 will be tried.

## 9. Proposed rule edits (NOT applied; need Mahir's OK)

IDs follow the existing convention (`CC-Gn-mm`); "CC1..CC4" are edit numbers, not rule IDs. Retired IDs are never reused.

| ID | Change | Train evidence | Why | Sim F1 |
|---|---|---|---|---|
| CC1 | **Demote "change in control"**: retire CC-G1-02; new support group **CC-G4** with CC-G4-01 "change in control". (**Optional: Mahir's call**) | spans 14; all-train occ. 88; chunks 33 TP / 93 FP (precision .26 vs .48 for "change of control") | An anchor is meant to be a high-precision phrase. Precision .26 is below the anchor bar; as support it still adds +1 next to "change of control". Small effect | .476 to .485; .559 vs .555 in the full set |
| CC2 | New support group **CC-G5** "termination right": CC-G5-01 "may terminate", -02 "right to terminate", -03 "terminate this agreement", -04 "immediately terminate", -05 "automatically terminate" | union 142 TP / 1,348 FP chunks overall (precision .10), but 79 TP / 25 FP in chunks that already contain an anchor (precision .76, vs .48 for the anchor alone); spans 16 / 7 / 30 / 2 / 3 | The only chunk-level signal found that separates the labeled clause from definitions and permitted-assignment mentions. Support only: alone it adds 1 and is below any useful threshold. Moves best th from 2 to 3 | on its own .474; adds +.017 on top of CC1+CC3+CC4 |
| CC3 | New anchor group **CC-G6** "merger or consolidation of a party": CC-G6-01 "merger or consolidation", CC-G6-02 "consolidation or merger" | spans 9 / 4; all-train occ. 38 / 6; chunks 38 TP / 29 FP and 12 TP / 5 FP, union 50 / 34 (precision .60, the highest of any phrase tested, above "change of control"); contracts 12 TP / 10 FP and 3 / 2 | Covers the "In the event of the merger or consolidation of Company ... right to terminate" family (Mossimo, Ashworth, Warning Mgmt) that has no "control" wording. Caveat: the same pair appears in permitted-assignment exceptions (Anixa, Fibrogen), so it adds assignment-only firings (section 5a) | .476 to .516 alone; +.064 on top of CC1+CC2+CC4 |
| CC4 | New anchor group **CC-G7** "ownership-change wording": CC-G7-01 "ownership change", CC-G7-02 "change in the control". (**Optional, low support: Mahir's call**) | chunks 6 / 0 and 3 / 0 (union 9 / 0); contracts 2 and 1 (union 3); spans 3 and 1 | Zero false positives, but evidence is 3 contracts. Same standing as CC-G2-03/04, which were already approved with "low support" notes. Covers "Ownership Change Event" and "change in the control of the owner" | .476 to .492 alone; +.017 on top of CC1-CC3 |
| no edit | Keep CC-G1-01, CC-G1-03, CC-G2 (all four), CC-G3 (all three) as they are | section 2, section 8 leave-one-out | None is harmful, several are load-bearing. CC-G1-03 "change-of-control" has 0 train occurrences (the hyphenated form is not in train); kept as a drafting variant. No counters added (section 3) | |

Candidates rejected: severance / good reason counter (CC5, +.001), "is acquired" (.47 precision), "merger, consolidation" (28 / 68), "merger or acquisition", "sale of all or substantially all" as its own group, trigger-phrasing support (double counting), "may be terminated" (+.001), "change of ownership" (franchise "Change of Ownership Transfer" cluster: 3 / 6), "controlling interest" as anchor (15 / 25), "undergoes" (22 / 9 chunks; as anchor .476 to .481 alone, +.005), every assignment-wording counter or support (section 5a), IP counter (section 3).

If CC1 and CC4 are declined, CC2 + CC3 alone reach .540 (th 3; 155 / 137 / 127). CC2 + CC3 + CC4 without CC1 reaches .555. If CC2 is declined (CC1 + CC3 + CC4), F1 is .541. CC3 is the one with real weight: without it the set falls to .495 (CC3 alone on the current rules: .516).

## 10. Examples that exercise each branch

All from the 326 train contracts. Scores are from the approximate scratch scorer (`sim.score`, **VERIFIED** by running it, not by reading the text). Columns: "Now" = current rules; "CC1" = after CC1; "CC1-2" = after CC1+CC2; "CC1-3"; "CC1-4" = all proposed edits. Span rows score the full span text; F rows use a ~460-character window around the phrase; G2 rows give span / 600-character excerpt scores from `gate2_excerpt_review.csv`.

| ID | Branch | Source | Text (shortened) | Now | CC1 | CC1-2 | CC1-3 | CC1-4 |
|---|---|---|---|---|---|---|---|---|
| E1 | Explicit anchor, passive "may be terminated" | CoC span, Zogenix (also gate-2 positive) | "This Agreement may be terminated by either Party upon [***] written notice ... the other Party undergoes a Change of Control" | 2 | 2 | 2 | 2 | 2 |
| E2 | Anchor + automatic termination | CoC span, SFG Financial (gate-2 positive) | "Upon the occurrence of any Change of Control (as defined below) this Agreement and all Licensee's rights and licenses hereunder shall automatically terminate unless ..." | 2 | 2 | 3 (+1 CC-G5) | 3 | 3 |
| E3 | Anchor, passive termination | CoC span, Exact Sciences (gate-2 positive) | "This Agreement may be terminated by either Party upon six (6) months written notice following a Change of Control of Exact" | 2 | 2 | 2 | 2 | 2 |
| E4 | Anchor, reassignment on change of control | CoC span, Rand Worldwide (gate-2 positive) | "In the event there is a change of Control of an Affiliate ... this Agreement must be assigned back to the party" | 2 | 2 | 2 | 2 | 2 |
| E5 | Anchor + several supports | CoC span, Digital Cinema Destinations (gate-2 positive) | "any change of control, merger, consolidation, or acquisition of all or substantially all of the assets of Network Affiliate (collectively, a 'Change of Control') shall be deemed an assignment" | 3 | 3 | 3 | 3 | 3 |
| E6 | No anchor: acquisition-triggered termination | CoC span, Energous | "If ENERGOUS is acquired by a third party, ENERGOUS' acquirer will have the right ... to terminate this Agreement upon written notice to DIALOG." | **0** | 0 | 1 (+1 CC-G5) | 1 | 1 |
| E7 | CC3 target: merger/consolidation termination | CoC span, Mossimo | "In the event of the merger or consolidation of Company with any other entity, Licensor shall have the right to terminate the Contract Period ..." | 1 (+1 "merger") | 1 | 2 (+1 "right to terminate") | **4** (+2 CC-G6) | 4 |
| E8 | CC4 target: Ownership Change Event | CoC span, theglobe.com | "... may terminate this Agreement in its sole discretion if one of the following companies ... does an 'Ownership Change Event'" | 1 | 1 | 2 | 2 | **4** (+2 CC-G7) |
| E9 | Miss: ownership change of stock | CoC span, Kallo | "In the event Agent changes its legal structure or undergoes a substantial change in ownership of its stock ... Kallo shall have the option of immediate termination" | 1 (+1 CC-G2-04) | 1 | 1 | 1 | 1 |
| E10 | Miss: acquired or merges | CoC span, Intersectent | "In the case that either company is acquired by, or merges with, another company ... that company may make a contract buyout payment" | 1 (+1 "merges with") | 1 | 1 | 1 | 1 |
| E11 | Miss: franchise change of ownership | CoC span, Hospitality Investors Trust | "Our consent to the Change of Ownership Transfer is subject to the following conditions ..." | **0** | 0 | 0 | 0 | 0 |
| E12 | Controlling interest, merger | CoC span, Marshall Holdings | "If the COMPANY ceases business or ... sells a controlling interest to a third party, or agrees to a consolidation or merger ..." | 2 (+1 "controlling interest", +1 "merger") | 2 | 2 | 4 (+2 CC-G6) | 4 |
| E13 | Merges with, voting securities | CoC span, Cardlytics | "(c) Supplier either: (i) merges with another entity, (ii) suffers a transfer involving fifty (50%) percent or more of any class of its voting securities ..." | 2 | 2 | 2 | 2 | 2 |
| E14 | Miss: "is acquired by a third party" | CoC span, Hertz Group Realty | "This Agreement and all rights and licenses ... shall terminate ... after: 3.2.1 Licensee is acquired by a third party" | **0** | 0 | 0 | 0 | 0 |
| E15 | Miss: "the Party whose control has changed" | CoC span, Dynamex | "In the event this Agreement is terminated ... then the Party whose control has changed shall not enter into an agreement with any other Party ..." | **0** | 0 | 0 | 0 | 0 |
| E-IP | IP assignment sentence | Anixa wording, shortened from the Anti-Assignment table | "Each Party will assign, and does hereby assign, to the other Party rights with respect to the applicable Inventions ..." | 0 | 0 | 0 | 0 | 0 |
| N1 | Permitted assignment to a CoC successor (gate-2 hard negative) | Energous; labeled Anti-Assignment | "either party may ... assign this Agreement in its entirety to any successor in the event of a Change of Control" | span 2 / excerpt 3 | 2 / 3 | 2 / 3 | 2 / 3 | 2 / 3 |
| N2 | Merger/consolidation assignment exception (gate-2 hard negative) | Anixa; labeled Anti-Assignment | "Neither Party may assign ... except ... to an entity that acquires all or substantially all of the business ... whether by merger, consolidation, sale of assets or otherwise" | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 |
| N3 | "change of control ... not an assignment" (gate-2 hard negative) | Euromedia; labeled Anti-Assignment | "A change of control of Rogers shall not be considered an assignment of this Agreement." | 3 / 3 | 3 / 3 | 3 / 3 | 3 / 3 | 3 / 3 |
| N4 | Merger exception (gate-2 hard negative) | Fibrogen | "... may assign this Agreement without the other party's consent to an entity that acquires substantially all of the business or assets ... whether by merger, transfer of assets, or otherwise" | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 |
| N5 | Quoted "change in control" (gate-2 hard negative) | Bellring | "... Premier may assign this Agreement in the event that Premier is sold, merged into or with another entity, or undergoes a 'change in control'" | 2 / 2 | **1 / 1** | 1 / 1 | 1 / 1 | 1 / 1 |
| F1 | Definition false positive | not a CoC positive; Array BioPharma ("1.6 'Change in Control' means, with respect to a party ...") | window | 2 | **1** | 1 | 1 | 1 |
| F2 | Employment severance | not a CoC positive; Bicycle Therapeutics ("severance pay and benefits ... outside the change in control period") | window | 2 | **1** | 1 | 1 | 1 |
| F3 | Assignment clause mentioning a transaction | not a CoC positive; Staar Surgical ("neither party may, directly or indirectly (including in connection with a change of control transaction), transfer or assign") | window | 2 | 2 | 2 | 2 | 2 |
| F5 | Permitted-assignment exception | not a CoC positive; ON2 Technologies ("either party may assign ... in connection with a change of control") | window | 2 | 2 | 2 | 2 | 2 |

Notes:
- The positives in the table are gate-2 rows where marked; E1 and E3 do not gain from CC2 because "may be terminated" is passive and not in CC-G5 (tested, +.001, section 6). Excerpts for the gate-2 positives score 2 to 3 (SFG, Zogenix, Exact Sciences gain +1 from CC-G5 in the excerpt; DigitalCinema 3; Rand 2).
- N3 and N1 are the cost of an anchor that cannot see the neighboring sentence; they stay at 3 under every variant. F3 and F5 stay at 2 for the same reason; at the final threshold (INFERRED to be about 3 on the proposed scale) F3 and F5 would not fire, while E5, E7 and E12 would.
- CC1 is the only edit that lowers a false-positive window (F1, F2, N5). CC3 is the only edit that moves a real positive across the likely threshold (E7, E12).
- Examples F4 (Adams Golf "31. Assignment and Change of Control") and F6 (Accuray) were attempted: F4 scores 2 under every variant like F3; F6 text was not found in the window search and is omitted.

## 11. Sources

- CUAD category description: `data/cuad/category_descriptions.csv`.
- Train spans: `data/splits/train.json` via `.agent/scratch/lib.py`.
- Gate-2 excerpts: `data/cuad/gate2_excerpt_review.csv`, `target_category == "Change Of Control"` (5 positive, 5 hard negative; all five hard negatives have source category Anti-Assignment).
- Chunks and labels: `data/gate3/train_chunks_768_512.csv`, `train_chunk_labels_768_512.csv` (unmasked rows; 9,714 chunks, 282 positive; AA x CoC table; IP overlap = IP Ownership Assignment span fully inside chunk `char_start`..`char_end`).
- Rule-level provenance: `configs/keyword_rules_v1.json` (categories["Change Of Control"], 10 rule IDs, P6 notes on CC-G2).
- Scratch: `.agent/scratch/{lib,cat,cand2,sim}.py`; session experiment scripts in the session scratchpad (`cc.py` chunk-level phrase counter, `cc5`-`cc14` simulations; not part of the repo).
- Reviewer: not yet assigned.

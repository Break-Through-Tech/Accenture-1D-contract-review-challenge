# Decision table: License Grant

Rule set: `configs/keyword_rules_v1.json` (FROZEN 2026-10-18 as `keyword_rules_v1`, 184 IDs, SHA-256 `07602f34...7ba7e3`). Evidence: the 326 train contracts only (`data/splits/train.json`, `data/gate3/train_*_768_512.csv`, `data/cuad/gate2_excerpt_review.csv`; no validation or test data used; `train_separate_questions.json` and `test.json` not opened).
Status: **APPROVED by Mahir 2026-10-16; L1-L5 (section 9) APPLIED to the JSON.**
Claim labels: **VERIFIED** = seen in a cited source or scratch run on train; **INFERRED** = hypothesis.

## 1. Inclusion meaning

CUAD asks whether the contract contains a license granted by one party to the other. In the labeled train data (**VERIFIED**, 513 spans in 164 contracts, the second most of the 10 categories) positives are the grant sentence and its neighbors:
- the standard grant: "VerticalNet hereby grants to Neoforma a non-exclusive, non-transferable license to use ...";
- grants without "to": "Chase grants Affiliate a non-exclusive, nontransferable, revocable right to ...", "NETGEAR and Bay Networks grant Distributor a non-exclusive, royalty-free, limited right to use the Trademarks";
- grants phrased as authorization or a right: "Emdeon is hereby granted a non-exclusive and worldwide right to use ...", "HDS shall have the right to use the name, image, likeness ...", "each party authorizes the other party to display and use the other's trademarks";
- forward-looking and conditional grants: "Investor hereby agrees to grant to Company a non-exclusive, irrevocable, royalty-free license ...", "In the event of a Supply Failure, Miltenyi shall grant Bellicum's Second-Source Supplier a limited ... license";
- scope fragments that the annotator tagged together with the grant ("to make, have made, use, sell, offer for sale, import ...", "The licenses granted pursuant to", "The use right granted under this Agreement is only valid in the PRC", "and promote the Service.").

Not included: license revocability or perpetuity statements after expiry (Irrevocable Or Perpetual License, the two gate-2 hard negatives from Cytodyn and Vericel), non-transferability wording alone (Non-Transferable License), exclusivity appointment ("appoints and grants Distributor the exclusive right to sell", Gentech, Exclusivity), IP ownership transfer. These other categories **share chunks** with License Grant, see section 5.

Train support: 513 spans in 164 of 326 contracts (**VERIFIED**, Phase 1 table).

## 2. Evidence groups

Each group counts at most once per chunk. Anchor +2, support +1, counter -1, floor 0. Plain substring match on normalized text. NEW = proposed in section 9.

Columns: "spans" = how many of the 513 License Grant spans contain the phrase; "all-train occ." = substring count over all 326 contracts; "chunk TP / FP" = unmasked train chunks (9,655; **807 positive**, base rate 8.4%) that contain the phrase and are labeled positive / negative; "contracts" = distinct train contracts behind those TP / FP chunks (chunk overlap inflates chunk counts about 3x). All **VERIFIED** (scratch runs `cat.py`, `lg1.py`, `lg6.py`).

| Group | Role | Phrase (rule ID) | Spans | All-train occ. | Chunk TP / FP | Contracts TP / FP |
|---|---|---|---|---|---|---|
| LG-G1 grant verb | anchor | hereby grants (01) | 235 | 268 | 461 / 65 | 108 / 24 |
| | | grants to (02) | 214 | 267 | 429 / 85 | 116 / 27 |
| | | grants (03, NEW) | 328 | 513 | 631 / 289 | 144 / 76 |
| LG-G2 license object | anchor | license to (01) | 186 | 394 | 426 / 272 | 113 / 63 |
| | | right and license (02) | 72 | 96 | 117 / 14 | 38 / 6 |
| | | license under (03, NEW) | 26 | 59 | 87 / 42 | 24 / 12 |
| LG-G3 license qualifiers | support | non-exclusive (01) | 198 | 309 | 415 / 196 | 107 / 63 |
| | | royalty-free (02) | 122 | 145 | 244 / 26 | 65 / 10 |
| | | nonexclusive (03, NEW) | 33 | 56 | 77 / 40 | 23 / 12 |
| | | royalty free (04, NEW) | 13 | 15 | 32 / 6 | 11 / 2 |
| LG-G4 irrevocable or perpetual | counter | irrevocable (01) | 55 | 98 | **135 / 92** | 34 / 26 |
| LG-G5 use right and perpetuity (NEW) | support | right to use (01) | 55 | 215 | 204 / 243 | 75 / 61 |
| | | perpetual (02) | 78 | 105 | 165 / 46 | 42 / 16 |
| | | (union) | | | 323 / 286 | |

Maximum score now: anchors LG-G1, LG-G2 (4) + supports LG-G3 (1; LG-G3-01 and -02 share one group) = **5**. After L1-L5: 4 + LG-G3 + LG-G5 = **6** (counter removed).

Why the counter is wrong (**VERIFIED**): the counter LG-G4-01 "irrevocable" sits in 135 positive chunks and 92 negative ones (precision .59, base rate 8.4%). "Irrevocable" is common inside real grants ("a non-exclusive, irrevocable, royalty-free license", Rare Element, Investor) so the counter takes a point from positives. Dropping it: .717 to .753 (L2). The two gate-2 hard negatives from Irrevocable Or Perpetual License do not need the counter (section 10).

## 3. Counterevidence and vetoes

Every candidate counter was checked against positive chunks and co-occurrence (**VERIFIED**, sim on the L1+L2 basis, which is .784; each row adds one counter):

| Counter tried | Chunk TP / FP | Sim F1 | Verdict |
|---|---|---|---|
| no license | 16 / 55 | .782 | no gain |
| does not grant | 14 / 29 | .785 | +.001, not worth it |
| not grant | 34 / 95 | .779 | worse |
| hereby assigns (ownership transfer) | 45 / 49 | .776 | worse: 45 true positives share the wording |
| shall own | 53 / 88 | .774 | worse |
| implied / by implication | 70 / 728; 27 / 60 | .772 / .780 | worse |
| all rights not expressly granted | 9 / 1 | .780 | worse (reserved-rights sentences sit inside real grants) |
| reserves all | 17 / 24 | .782 | no gain |
| revocable | 170 / 95 | .748 | clearly worse |
| no right or license | 5 / 3 | .784 | no change |
| nothing in this | 67 / 527 | .773 | worse |
| covenant not to | 0 / 41 | .786 | +.002; 0 true positives lost but only 41 chunks of boilerplate; not proposed |

Result: **no counter survives.** The existing counter is retired (L2). Vetoes: none (chunk-wide design, no windows).

## 4. Context / proximity limits

None. All matching is chunk-wide (768 words, 512-word overlap). Consequence (**VERIFIED**): "grants" in an unrelated sentence ("if BKC grants its consent", "which grants to any other entity or person a right or license", "licenses granted to BLI") and a "license to" in a different clause of the same chunk combine into one score. This is the main source of false positives (section 6).

## 5. Required confusion cases

### 5a. License Grant vs ownership transfer / IP assignment

Chunks that fully contain an IP Ownership Assignment span (**VERIFIED**, same method as the Anti-Assignment table; 335 unmasked train chunks): 123 of them (37%) are License Grant positives, because IP agreements normally pair an assignment with a back-license. So IP assignment is **not** a clean negative for this category, unlike for Anti-Assignment (3.7%) and Change Of Control (3.4%). Firing at threshold 3 on those 335 chunks (**VERIFIED**, sim):

| Rules | IP chunks that fire | of which License Grant negative |
|---|---|---|
| current | 85 | 7 |
| proposed (L1-L5) | 117 | 12 |

The extra firings are mostly real positives (+32 chunks, +5 false positives). The ownership-transfer sentence itself scores 0: "Ono hereby assigns and shall cause to be assigned to Array all worldwide rights in and to ... Product Trademarks" (a License Grant span in train, tagged because of the neighboring grant) scores 0 under every variant (E4). Counters on "hereby assigns" and "shall own" were tested and rejected (section 3): 45 of the 94 "hereby assigns" chunks are positives. **Decision: no ownership-transfer counter.**

### 5b. License Grant vs incidental "license"

"License" is in 760 positive and 3,212 negative chunks (precision .19, recall .94). It is deliberately **not** a rule. The incidental uses (**VERIFIED**, FP windows in section 10): the table of contents ("Section 3.01 License grants"), warranties ("an agreement which grants to any other entity or person a right or license"), expiry clauses ("the licenses granted to BLI ... shall terminate"), consent ("BKC grants its consent"). The anchors LG-G1/G2 need a grant verb or the phrase "license to / right and license / license under", and a support, to reach threshold 3. The cost of "grants" (L1) is exactly this incidental use: 289 negative chunks contain it, in 76 contracts.

### 5c. Overlap with Non-Transferable License, Exclusivity and Anti-Assignment (INFERRED to matter for the next tables)

Unmasked chunks labeled for License Grant and the other category (**VERIFIED**):

| | LG = 0 | LG = 1 |
|---|---|---|
| Non-Transferable License = 0 | 8,788 | 496 |
| Non-Transferable License = 1 | 54 | 297 |
| Exclusivity = 0 | 8,584 | 597 |
| Exclusivity = 1 | 235 | 198 |
| Anti-Assignment = 0 | 8,032 | 746 |
| Anti-Assignment = 1 | 720 | 53 |

297 of the 351 Non-Transferable License chunks (85%) are also License Grant positives; 198 of the 433 Exclusivity chunks (46%) are; only 53 of 773 Anti-Assignment chunks (7%). So License Grant evidence will also fire on most Non-Transferable License chunks, and Non-Transferable's own table should not count "grants" or "license to" as its anchors without a counter.

False-positive rate of the License Grant rules at threshold 3 (negatives only, **VERIFIED**): outside Non-Transferable chunks 100 of 8,788 (1.1%), inside 9 of 54 (17%); outside Exclusivity 97 of 8,584, inside 11 of 235 (4.7%); outside Anti-Assignment 101 of 8,032, inside 7 of 720. For comparison the current rules fire on 46 / 40 / 46 of the same "outside" groups at threshold 3, so the leak roughly doubles everywhere (it is the cost of "grants", section 6), and it is not concentrated in the overlapping categories.

## 6. Known near-misses and exclusions

| Pattern | What happens | Evidence |
|---|---|---|
| "grants" in non-license sentences ("grants its consent", "grants to any third party any rights to distribute") | +2 (L1); a second group in the same chunk (a "license to" or support) gets it to 4 | F1-F6 in section 10; 289 negative chunks |
| Table of contents / headings ("license grants", "grant of rights") | +2 or less | F-Cerence in section 10 |
| Irrevocable Or Perpetual License post-expiry statement (gate-2 hard negatives) | 1 now, 2 after L5 ("perpetual"); below threshold 3 | N1, N2 |
| Non-Transferable License sentence "right and license to use the Licensed Marks granted hereunder is nonexclusive" | scores 2 now, 3 after L1-L4 | N3 (Airtech); it is also a License Grant-like sentence (**INFERRED**: annotator tagged only the other category) |
| Exclusivity appointment ("appoints and grants Distributor the exclusive right to sell") | 0 now, 2 after L1 ("grants") | N5 (Gentech) |
| License fragments with no phrase ("The licenses granted pursuant to", "and promote the Service.") | 0 | E10, E11 |
| Authorization wording ("authorizes the other party to display and use", "is hereby authorized and licensed") | 0-1 | not a rule; "authorize" is in 255 positive and 2,491 negative chunks |

## 7. Known weak spots (be honest in the write-up)

1. **Recall is the limit, not precision.** Current rules reach precision .91 (478 / 527) at threshold 3 but find only 59% of positive chunks; the proposed set reaches .85 (627 / 736) and 78% recall (**VERIFIED**, sim). 180 positive chunks still score below 3 (section 8).
2. **Anchor coverage is already 67% of spans** (346 of 513; 19 of 164 contracts have no anchored span). L1 and L4 raise it only to 368 spans and 11 contracts without. Most remaining positives are fragments, forward-looking grants ("agrees to grant", "shall grant", tested but only +.002), or authorization wording.
3. **"grants" costs precision.** The new anchor is the largest F1 edit (+.042 alone) and the largest false-positive source (+9 FP at the best threshold; 289 negative chunks overall).
4. **The best threshold stays at 3** both now and after the edits. On the proposed rules 406 negative chunks score exactly 1 and 464 score exactly 2, against 55 at 3 (section 8 distribution); at threshold 2 the plain-cap-style leakage would be large. Threshold selection on validation decides how much of this shows.
5. **Annotation noise**: the Non-Transferable License sentence N3 and the Exclusivity appointment N5 are grant-like text labeled only for another category.
6. **Chunk overlap inflates counts about 3x**; sim F1 is optimistic (threshold tuned on train) and is a bug check only. The five edits were chosen from a sweep of about 60 candidate phrases on train; low-support ones are flagged.

## 8. Train-only simulation (bug check, optimistic)

Approximate scorer (`sim.score`), 9,655 unmasked chunks (807 positive), best threshold by F1 over 1-9. **VERIFIED** by scratch runs; "current" reproduces the stock `sim.py` result .717 (th 3, 478 TP / 49 FP / 329 FN).

| Variant | Best F1 | Th | TP | FP | FN |
|---|---|---|---|---|---|
| current | .717 | 3 | 478 | 49 | 329 |
| L1 ("grants" into LG-G1) | .759 | 3 | 529 | 58 | 278 |
| L1 + L2 (retire counter) | .784 | 3 | 563 | 66 | 244 |
| L1-L3 (+ spelling variants) | .799 | 3 | 583 | 69 | 224 |
| L1-L4 (+ "license under") | .806 | 3 | 596 | 76 | 211 |
| L1-L5 (+ "right to use", "perpetual") | **.813** | 3 | 627 | 109 | 180 |

Single edits on the current rules: L1 .759, L2 .753, L3 .736, L4 .732, L5 .763. Leave-one-out from L1-L5 (.813): without L1 .803 (598 / 84 / 209), without L2 .802 (613 / 109 / 194), without L3 .806 (618 / 109 / 189), without L4 .809 (614 / 96 / 193), without L5 .806 (596 / 76 / 211). The edits are close to additive; no single one dominates, and L3 and L4 are +.004 to +.007 each.

Score distribution on the proposed rules (unmasked chunks): negatives 0: 7,869; 1: 406; 2: 464; 3: 55; 4: 37; 5: 10; 6: 7. Positives 0: 52; 1: 35; 2: 93; 3: 124; 4: 158; 5: 215; 6: 130. Current rules: negatives 0: 8,309; 1: 176; 2: 314; 3: 26; 4: 21; 5: 2. Positives 0: 105; 1: 64; 2: 160; 3: 148; 4: 139; 5: 191.

Other single checks used to choose the proposals (**VERIFIED**; basis stated):
- Drop one existing rule (current rules): LG-G1-01 .678, LG-G1-02 .696, LG-G2-01 .739 (th 2, 548 / 129 / 259), LG-G2-02 .703, LG-G3-01 .722, LG-G3-02 .707. All except LG-G2-01 lose F1, so they stay. LG-G2-01 "license to" is the only rule whose removal raises F1 on the current rules (+.022), but demoting it to support after L1+L2 gives .772 vs .784, and retiring it .733; **no change to it** (it is 426 TP / 272 FP chunks but needed for recall).
- "grants" as a separate anchor group instead of a third rule in LG-G1: .799 vs .759, but it double counts the same meaning ("hereby grants" would add 4) and breaks the rule that synonyms share a group. Rejected on design grounds.
- Anchor candidates on top of L1+L2 (each added in its group): "hereby grant" +.002, "agrees to grant" +.002, "grant of license" +.001, "license grant" -.005 (212 FP chunks). Not proposed.
- Support candidates: "worldwide" +.002 (a 243 FP chunk phrase), "non-transferable|nontransferable" +.009 but this is Non-Transferable License vocabulary and 85% overlap makes it double counting; "limited license|sublicense" -.006 to -.016. Not proposed.
- "right to use" alone as its own support group +.013 (B + right to use .797), "perpetual" alone +.009; the pair +.011 on B2 (.809), so a single group of two. Retained as L5 (optional).

Because the final threshold is chosen later on validation, these thresholds are not the ones that will be used. Max score is 6 after L1-L5, so thresholds 1-6 will be tried.

## 9. Proposed rule edits (NOT applied; need Mahir's OK)

IDs follow the existing convention (`LG-Gn-mm`); "L1..L5" are edit numbers, not rule IDs. Retired IDs are never reused.

| ID | Change | Train evidence | Why | Sim F1 |
|---|---|---|---|---|
| L1 | Add **LG-G1-03** "grants" to the anchor group LG-G1 (same meaning as "hereby grants" / "grants to", so same group and no double count) | spans 328 of 513; all-train occ. 513; chunks 631 TP / 289 FP (precision .69, recall .78); contracts 144 / 76 | The annotator tagged grant sentences without "to" ("Chase grants Affiliate a ...", "NETGEAR ... grant Distributor"). Largest F1 gain, also the largest FP source | .717 to .759 |
| L2 | **Retire LG-G4-01 "irrevocable"** (counter; ID never reused). Leaves LG-G4 empty | 135 TP / 92 FP chunks (precision .59 > base rate .084); contracts 34 / 26 | The counter subtracts a point from real grants that say "irrevocable"; section 3 shows no replacement counter helps | .759 to .784 |
| L3 | Add spelling variants to the existing support group LG-G3: **LG-G3-03 "nonexclusive"**, **LG-G3-04 "royalty free"** | "nonexclusive" 33 spans, 77 / 40 chunks; "royalty free" 13 spans, 32 / 6 chunks | Same meaning as LG-G3-01/02 without the hyphen; ordinary drafting variants (**VERIFIED**: both occur in train) | .784 to .799 |
| L4 | Add **LG-G2-03 "license under"** to the anchor group LG-G2. (**Optional, small: Mahir's call**) | 26 spans, 59 occ.; chunks 87 TP / 42 FP (precision .67); contracts 24 / 12 | "the license granted under / a license under the Licensed Patents" sentences; +.007 | .799 to .806 |
| L5 | New support group **LG-G5** "use right and perpetuity": LG-G5-01 "right to use", LG-G5-02 "perpetual". (**Optional: Mahir's call**) | 55 and 78 spans; chunks 204 / 243 and 165 / 46, union 323 / 286; contracts 75 / 61 and 42 / 16 | Right-to-use grants and perpetual licenses, many without "license to". Weak per phrase ("right to use" precision .46) but only +1, and the two sit in one group | .806 to .813 |
| no edit | Keep LG-G1-01/02, LG-G2-01/02 (anchors) and LG-G3-01/02 (supports) | section 2, section 8 | Each is load-bearing: dropping any lowers F1 except LG-G2-01, whose removal helps only without L1+L2 | |

Candidates rejected: any counter (section 3), "license" and "grant" alone (precision .19 and .26), "hereby grant", "agrees to grant", "shall grant", "grant of license" (+.001 to +.002), "license grant" (-.005), "worldwide", "non-transferable" (double counts Non-Transferable License), "sublicense" and "limited license" (-.006 to -.016), "granted to" (precision .27), "authorize/permit" (precision .10 and .09), "grants" as its own anchor group (double counting).

If L4 and L5 are declined, L1-L3 reach .799. If only L5 is declined, .806. If L2 is declined (counter kept), .802. L1 is the biggest (.803 without it).

## 10. Examples that exercise each branch

All from the 326 train contracts. Scores are from the approximate scratch scorer (`sim.score`, **VERIFIED** by running it, not by reading the text). Columns: "Now" = current rules; "+L1" = after L1; "+L2" = L1-L2; "+L3" = L1-L3; "+L4" = L1-L4; "All" = L1-L5. Span rows score the full span text; the F rows use a ~460-character window around the phrase in a negative chunk that fires at threshold 3 under the proposed rules. G2 rows are gate-2 rows; span and 600-character excerpt scores are identical for every row.

| ID | Branch | Source | Text (shortened) | Now | +L1 | +L2 | +L3 | +L4 | All |
|---|---|---|---|---|---|---|---|---|---|
| E1 | Standard grant, both anchors | gate-2 positive, Neoforma | "VerticalNet hereby grants to Neoforma a non-exclusive, non-transferable license to use ..." | 5 | 5 | 5 | 5 | 5 | 5 |
| E2 | Grant without "to" (L1 target) | License Grant span, Creditcards.com | "Chase grants Affiliate a non-exclusive, nontransferable, revocable right to ..." | 1 | 3 | 3 | 3 | 3 | 3 |
| E3 | Grant without "to", two parties | License Grant span, Netgear | "NETGEAR and Bay Networks grant Distributor a non-exclusive, royalty-free, limited right to use the Trademarks." | 1 | 1 | 1 | 1 | 1 | 2 |
| E4 | Ownership transfer in a grant-tagged span | License Grant span, Array BioPharma | "Ono hereby assigns and shall cause to be assigned to Array all worldwide rights in and to (i) any Product Trademarks ..." | 0 | 0 | 0 | 0 | 0 | 0 |
| E5 | Counter hurt a real grant (L2 target) | License Grant span, Rare Element | "Investor hereby agrees to grant to Company a non-exclusive, irrevocable, royalty-free license under any Joint Improvement ..." | 0 | 0 | 1 | 1 | 3 | 3 |
| E6 | "License under" (L4 target) | License Grant span, Oasys Mobile | "Subject to the terms of this Agreement and Scope of Use ..., E.piphany grants HSNS a nonexclusive, nontransferable, non-sublicensable license ..." | 0 | 2 | 2 | 3 | 3 | 3 |
| E7 | Spelling variants (L3 target) | License Grant span, Jingwei | "The license under this Agreement is a non-exclusive, non-assignable and non-transferable license." | 1 | 1 | 1 | 1 | 3 | 3 |
| E8 | Gate-2 positive, "Each Party grants" | Reynolds Consumer Products | "Each Party grants, and shall cause its Affiliates to grant, to the other Party ... a royalty-free, non-exclusive, non-transferable, worldwide license ..." | 1 | 3 | 3 | 3 | 3 | 3 |
| E9 | Right to use and perpetuity (L5 target) | License Grant span, Iovance | "MD Anderson also grants LBIO a non-exclusive, royalty free, perpetual license (with rights to sub-license) ..." | 1 | 3 | 3 | 3 | 3 | 4 |
| E10 | Fragment, no phrase | License Grant span, Entrust | "The licenses granted pursuant to" | 0 | 0 | 0 | 0 | 0 | 0 |
| E11 | Fragment, no phrase | License Grant span, theglobe.com | "and promote the Service." | 0 | 0 | 0 | 0 | 0 | 0 |
| E12 | Appointment, no phrase | License Grant span, Scansource | "Cisco makes, and Distributor accepts, the appointment of Distributor as an authorized, non-exclusive distributor ..." | 1 | 1 | 1 | 1 | 1 | 1 |
| E13 | Right to use, no verb | License Grant span, Jingwei | "The use right granted under this Agreement is only valid in the PRC." | 0 | 0 | 0 | 0 | 0 | 0 |
| P1 | Gate-2 positive | Armstrong Flooring | "the Company hereby grants to Seller a perpetual, non-exclusive, royalty-free license in, to and under the Company Licensed Patents ..." | 3 | 3 | 3 | 3 | 3 | 4 |
| P2 | Gate-2 positive | Leju Holdings | "Licensor hereby grants to Licensee, and Licensee hereby accepts from Licensor, an exclusive, non-transferable ..." | 4 | 4 | 4 | 4 | 4 | 4 |
| P3 | Gate-2 positive | King Pharmaceuticals | "Depomed hereby grants to King a non-assignable, non-sublicensable, non-exclusive, royalty-free right and license ..." | 5 | 5 | 5 | 5 | 5 | 5 |
| N1 | Gate-2 hard negative: Irrevocable Or Perpetual | Cytodyn | "Following the expiration of the Royalty Term ..., the licenses granted under Section 2.1 ... shall be [perpetual, irrevocable ...]" | 0 | 0 | 1 | 1 | 1 | 2 |
| N2 | Gate-2 hard negative: Irrevocable Or Perpetual | Vericel | "Following expiration of the Royalty Term ..., the license granted to Vericel under Section 9.1 ..." | 0 | 0 | 1 | 1 | 1 | 2 |
| N3 | Gate-2 hard negative: Non-Transferable License | Airtech | "The right and license to use the Licensed Marks granted hereunder to You is nonexclusive ..." | 2 | 2 | 2 | 3 | 3 | 3 |
| N4 | Gate-2 hard negative: Non-Transferable License | Ehave | "Subject to Section 2(e), the grant set out in Clause 2(b)(i) is exclusive such that Ehave shall not license any other Person ..." | 0 | 0 | 0 | 0 | 0 | 0 |
| N5 | Gate-2 hard negative: Exclusivity | Gentech | "Company hereby appoints and grants Distributor the exclusive right to sell and distribute the Products ..." | 0 | 2 | 2 | 2 | 2 | 2 |
| F1 | "grants" a right, not a license | not a License Grant positive; Glu Mobile ("... or grants to any third party any rights to distribute the wireless products ...") | window | 2 | 2 | 2 | 2 | 2 | 2 |
| F2 | License referenced in an expiry clause | not a positive; Berkeley Lights ("the licenses granted to BLI from Ginkgo pursuant to Section 9.2 (Grants to BLI) ...") | window | 3 | 3 | 3 | 3 | 3 | 3 |
| F3 | Right to negotiate, not a grant | not a positive; iBio ("the creating party grants to the other party a time-limited first right to negotiate a commercial license ...") | window | 4 | 4 | 4 | 4 | 4 | 4 |
| F4 | Warranty about another agreement | not a positive; Papa John's ("... any oral or written agreement ... which grants to any other entity or person a right or license ...") | window | 4 | 4 | 4 | 4 | 4 | 4 |
| F5 | Sublicensing by a licensee | not a positive; Bellicum ("... Bellicum grants rights with respect to a Bellicum product under license ...") | window | 0 | 2 | 2 | 2 | 2 | 2 |
| F6 | Consent, not a license | not a positive; International Fast Food ("If BKC grants its consent, franchisee shall effectuate such registration") | window | 0 | 2 | 2 | 2 | 2 | 2 |
| F7 | Table of contents | not a positive; Cerence ("... Section 3.01. License grants 6 ...") | window | 0 | 2 | 2 | 2 | 2 | 2 |

Notes:
- F2-F4 already fire (score 3-4) under the current rules; L1-L5 do not change them. They show the baseline false-positive class (a "grants to" / "license to" in a sentence the annotator did not tag). F5-F7 are the new false positives that L1 adds (score 2, below threshold 3; they only fire in chunks that also hold another support or anchor).
- E2, E6, E7, E8, E9 and the gate-2 positive P-rows show the gain; E10, E11, E13 (fragments, no phrase) are unreachable by keywords.
- N3 rises from 2 to 3 after L3 (it contains "nonexclusive") and N1/N2 from 0 to 2 after L2 and L5; none reaches the expected best threshold 3 except N3. **INFERRED** from section 5c that N3 is a legitimate grant-like sentence tagged only for Non-Transferable License.
- E5 (Rare Element) is the clearest L2 case: the counter "irrevocable" took a point from a real grant; after L2 it scores 1, and 3 once "license under" (L4) and "perpetual" (L5) are added.

## 11. Sources

- CUAD category description: `data/cuad/category_descriptions.csv`.
- Train spans: `data/splits/train.json` via `.agent/scratch/lib.py`.
- Gate-2 excerpts: `data/cuad/gate2_excerpt_review.csv`, `target_category == "License Grant"` (5 positive, 5 hard negative; sources Irrevocable Or Perpetual License x2, Non-Transferable License x2, Exclusivity).
- Chunks and labels: `data/gate3/train_chunks_768_512.csv`, `train_chunk_labels_768_512.csv` (unmasked rows; 9,655 chunks, 807 positive; co-occurrence tables; IP overlap = IP Ownership Assignment span fully inside chunk `char_start`..`char_end`).
- Rule-level provenance: `configs/keyword_rules_v1.json` (categories["License Grant"], 7 rule IDs).
- Scratch: `.agent/scratch/{lib,cat,cand2,sim}.py`; session experiment scripts in the session scratchpad (`gen.py` harness, `lg1`-`lg8` simulations; not part of the repo).
- Reviewer: not yet assigned.

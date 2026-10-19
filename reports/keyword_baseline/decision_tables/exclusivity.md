# Decision table: Exclusivity

Rule set: `configs/keyword_rules_v1.json` (FROZEN 2026-10-18 as `keyword_rules_v1`, 184 IDs, SHA-256 `07602f34...7ba7e3`). Evidence: the 326 train contracts only (`data/splits/train.json`, `data/gate3/train_*_768_512.csv`, `data/cuad/gate2_excerpt_review.csv`; all gate-2 titles checked to be in train). No validation or test data used; `train_separate_questions.json` not opened.
Status: **APPROVED and APPLIED 2026-10-16 (X1-X4 all approved by Mahir).** The scorer reproduces train sim F1 .533.
Claim labels: **VERIFIED** = seen in a cited source or scratch run on train; **INFERRED** = hypothesis.

## 1. Inclusion meaning

CUAD asks whether the contract has an exclusive-dealing commitment (**VERIFIED**, `data/cuad/category_descriptions.csv`): a commitment to buy all "requirements" from one party, a ban on selling or licensing to third parties, or a ban on working with other parties, during or after the contract. In the labeled train spans (**VERIFIED**) positives are:
- distributor or license grants worded "exclusive right", "an exclusive license", "exclusive distributor", "on an exclusive basis";
- the commitment as a noun ("Exclusivity is granted for the region of Nigeria", "violates ENVISION's exclusivity", "Exclusivity Date means ...");
- bans without the word "exclusive" ("Reseller shall not obtain the software ... from any Entity other than ...", "neither Vertex nor any affiliate may sell any Product to ... other than pursuant to this JSA", "Allied shall not endorse ... any other company").

Not included: non-exclusive grants (the opposite meaning), "exclusive remedy" / "exclusive jurisdiction" boilerplate, and plain non-competes (other category, but 63 chunks overlap, section 5).

Train support: 262 spans in 116 of 326 contracts (**VERIFIED**, Phase 1 table). Only 67 of the 262 spans contain a current anchor.

## 2. Evidence groups

Each group counts at most once per chunk. Anchor +2, support +1, counter -1, floor 0. Plain substring match on normalized text. NEW = proposed in section 9.

"Chunk TP / FP" = unmasked train chunks (9,716; 450 positive, 4.6%) that contain the phrase and are labeled positive / negative for Exclusivity. All **VERIFIED** (scratch runs `cat.py`, `cand2.py` and a chunk-level phrase counter).

| Group | Role | Phrase (rule ID) | Spans containing | All-train occ. | Chunk TP / FP |
|---|---|---|---|---|---|
| EX-G1 exclusive right or role | anchor | exclusive right (01) | 38 | 151 | 104 / 211 |
| | | exclusive distributor (02) | 8 | 51 | 21 / 37 |
| | | an exclusive (NEW, 03) | 53 | 90 | 105 / 70 |
| | | exclusivity (NEW, 04) | 14 | 171 | 114 / 174 |
| | | exclusively from (NEW, 05) | 6 | 8 | 18 / 5 |
| EX-G2 exclusively | anchor | exclusively (01) | 24 | 206 | 92 / 361 |
| EX-G3 competitor wording | support | competes with (01) | 1 | 8 | 5 / 16 |
| EX-G5 bare "exclusive" (NEW) | support | exclusive (01) | 181 | 1,533 | 387 / 2,100 |
| EX-V1..V3 vetoes | veto | non-exclusive, nonexclusive, non- exclusive (cancel EX-G1) | 11 / 0 / 2 | 309 / 56 / 32 | 92 / 537 for "non-exclusive" |

Maximum score now: anchors EX-G1, EX-G2 (2 each) + support EX-G3 (1) = 5. After X1-X4: EX-G1 anchor (2) + EX-G4 "exclusively" (1) + EX-G5 "exclusive" (1) + EX-G3 (1) = **5**, but a typical strong clause scores 3-4 ("an exclusive" + "exclusive").

Why the change (**VERIFIED**): "exclusively" as an anchor fires on 453 unmasked chunks, 361 negative (precision .20; "to be used exclusively for ..." is common). A lone "exclusively" reaches threshold 2 and swamps the category (540 FP at the current best threshold 1, precision .25). The strong, unlisted words are "an exclusive" (precision .60) and "exclusivity" (.40; the current rules do not contain it at all).

## 3. Counterevidence and vetoes

- **Vetoes EX-V1..V3 (non-exclusive): kept** (**VERIFIED**). With all three removed from the final rule set sim F1 falls from .533 to .506; with the current rules .306 to .302. "Non-exclusive" occurs in 629 chunks, 92 of them Exclusivity positives (chunks that also contain an exclusive clause), so the veto cancels only the overlapping match, not the whole chunk. The plan's note ("EX non-exclusive vetoes fire on 537 negatives") is true but harmless: a veto firing on a negative chunk costs nothing.
- **New vetoes EX-V4..V6** (same three phrases, cancelling the new group EX-G5): needed because bare "exclusive" is a substring of "non-exclusive". Sim: with them .533, without .529 (small, kept for explainability).
- **Counters for boilerplate "exclusive" (remedy, jurisdiction, venue, property, "exclusive of")**: tested and **rejected**. Chunk precision is 1.4-8% (below the 4.6% base rate, so they are real counterevidence), but the F1 gain is +.002 ("exclusive remedy/remedies") or none, because bare "exclusive" is only +1 and the strong anchors rarely co-occur with them.
- **Counter for "non-exclusive" as -1**: not needed, the veto already handles it.

## 4. Context / proximity limits

None proposed (the rule engine is plain substring + group max). The same limits as other tables: "exclusive license" in a License Grant clause is genuinely also Exclusivity in CUAD labels (section 5), so no attempt is made to separate them.

## 5. Required confusion cases

**5a. Exclusivity vs License Grant (VERIFIED, train).** 198 of the 450 Exclusivity chunks (44%) are also License Grant positives. "An exclusive license" is therefore real Exclusivity evidence, not a License Grant false alarm. Among the false positives at the proposed threshold 3 (272 chunks) 44 are License Grant chunks, 22 Non-Compete, 17 Non-Transferable License, 24 Expiration Date, 13 Anti-Assignment (so most FPs are neither: boilerplate "exclusive" mentions).

**5b. Non-exclusive grants (gate-2 hard negatives, License Grant x4, Irrevocable Or Perpetual License x1).** All five contain "non-exclusive". Scores (600-character excerpt): current 0, 0, 0, 0, 0; after X1-X4 0, 1 (Zogenix), 0, 0, 0. Zogenix's excerpt rises to 1 (INFERRED) because a nearby sentence uses "exclusive"; it stays below the threshold. The veto does its job.

**5c. Exclusivity vs Non-Compete (VERIFIED).** 63 of 450 Exclusivity chunks (14%) are also Non-Compete positives; 63 of the 307 Non-Compete chunks are Exclusivity (21%). Both categories contain "shall not sell / endorse any other ...". No rule tries to separate them. Of the Exclusivity false positives at threshold 3, 22 are Non-Compete chunks.

**5d. Boilerplate "exclusive" (remedy, jurisdiction, venue).** Rejected as counters, see section 3. They do not reach a high score on their own because bare "exclusive" is only +1.

## 6. Known near-misses and exclusions

- Lone "exclusively" (e.g. "used exclusively for") no longer reaches 2.
- "Sole and exclusive" (24 TP / 275 FP) is mostly "sole and exclusive remedy"; rejected as an anchor.
- "Exclusive of" (3 / 218) means "excluding"; irrelevant to the category and below base rate.
- "Right of first ..." (17 / 106, precision .14), "most favored" (2 / 15), "agrees not to" (23 / 292) all fail the anchor bar.

## 7. Known weak spots (be honest in the write-up)

- 151 of the 262 spans (58%) after the edits still contain no anchor: bans without the word "exclusive" ("shall not ... any other ..."), requirements clauses ("purchase all of its requirements from"), and short fragments. They stay unreachable for a keyword baseline. INFERRED recall ceiling at threshold 3 is about .58 on train chunks.
- Precision is moderate: at threshold 3 precision .49 / recall .58; at 4 precision .67 / recall .15 (**VERIFIED**, sim).
- "Exclusive" mentions in License Grant boilerplate ("non-exclusive" handled; "exclusive" in a definitions section is not).

## 8. Train-only simulation (bug check, optimistic)

Scratch scorer: `sim.score` (group max, vetoes cancel an overlapping match). Best threshold over 1-8 on unmasked train chunks. **Optimistic** because the new phrases were found on the same train data; thresholds will be chosen on validation later.

| Rule set | Best F1 | Threshold | TP | FP | FN |
|---|---|---|---|---|---|
| Current | .306 | 1 | 179 | 540 | 271 |
| X1 (demote "exclusively") alone | .306 | 1 | 179 | 540 | 271 |
| X1+X2 | .500 | 2 | 278 | 384 | 172 |
| X1-X3 | .511 | 2 | 288 | 389 | 162 |
| X1-X4 (all) | **.533** | 3 | 262 | 272 | 188 |

Leave-one-out (all minus one / only that one): X1 .432 / .306; X2 .309 / .425; X3 .520 / .306; X4 .511 / .308. X1 and X2 only work together (X2 with "exclusively" still an anchor gives .425, with 718 FP).

Score distribution after X1-X4 (rows: negative / positive chunks; columns: score 0-4): negatives 7,500 / 1,040 / 454 / 239 / 33; positives 46 / 86 / 56 / 195 / 67.

## 9. Proposed rule edits (NOT applied; need Mahir's OK)

IDs follow the existing convention (`EX-Gn-mm`); "X1..X4" are edit numbers. Retired IDs are never reused.

| ID | Change | Train evidence | Why | Sim F1 |
|---|---|---|---|---|
| X1 | **Retire EX-G2-01 "exclusively" (anchor)**; add it as support, new group **EX-G4**, EX-G4-01 "exclusively" | 92 TP / 361 FP chunks (precision .20; 24 of 262 spans) | As an anchor a lone "exclusively" fires 453 chunks. Alone this edit changes nothing; it pays off only with X2 | .306 to .306 |
| X2 | Add anchor rules to **EX-G1**: EX-G1-03 "an exclusive", EX-G1-04 "exclusivity" | "an exclusive" 105 / 70 chunks (precision .60; 53 spans); "exclusivity" 114 / 174 (.40; 14 spans) | The two best unlisted words; "an exclusive" covers "an exclusive license / right / basis / distributor" | .306 to .500 |
| X3 | Add anchor rule EX-G1-05 "exclusively from" (optional, small) | 18 / 5 chunks (precision .78); 6 spans; 8 occurrences in all train | Wording "purchase exclusively from"; small but precise | .500 to .511 |
| X4 | New support group **EX-G5**: EX-G5-01 "exclusive"; new vetoes **EX-V4..V6** ("non-exclusive", "nonexclusive", "non- exclusive") cancelling EX-G5 | 387 / 2,100 chunks (precision .156, 3.4x base rate); 181 of 262 spans contain it | Partial credit for any "exclusive" wording; vetoes stop "non-exclusive" counting | .511 to .533 (threshold 3) |
| no edit | Keep EX-G1-01/02, EX-G3-01, EX-V1..V3 | section 3, section 8 | All load-bearing or harmless | |

Candidates rejected: "even as to" (23 / 0 chunks but all already anchored, +0), "exclusive basis" / "exclusive territory" / "exclusive license" / "exclusive rights" as extra rules (+0 to +.005), "sole and exclusive", "right to market", "hereby appoints" (precision .35), "provider of", bare "sole" / "only" / "solely" (precision .04-.07), "shall not" / "agrees not to" / "other than" (precision .05-.06), boilerplate counters (section 3), and a greedy search's later picks ("as the exclusive", "have the exclusive": +.007 each, overfit to single contracts).

If X3 is declined, .520 at threshold 3. If X4 is declined, .511 at threshold 2. X1 and X2 should be approved together.

## 10. Examples that exercise each branch

Scores from the scratch scorer (**VERIFIED** by running it). "Now" = current rules; "After" = X1-X4. Span rows score the span text; G2 rows score the 600-character gate-2 excerpt.

| ID | Branch | Source | Text (shortened) | Now | After |
|---|---|---|---|---|---|
| E1 | "an exclusive" license | Exclusivity span, ArTara | "University hereby grants to ArTara an exclusive license to use the Program Data solely for the Project ..." | 0 | 3 |
| E2 | "an exclusive and royalty-free right" | Exclusivity span, NLS Pharmaceutics | "Licensor hereby grants to License an exclusive and royaltyfree right to use the Trademark ..." | 0 | 3 |
| E3 | Noun "Exclusivity" | Exclusivity span, Kallo | "Exclusivity is granted for the region of Nigeria," | 0 | 2 |
| E4 | Noun "exclusivity" in a breach consequence | Exclusivity span, Legacy Technology | "SIERRA shall cease making sales to any customer or distributor who ... violates ENVISION's exclusivity." | 0 | 2 |
| E5 | Definition | Exclusivity span, Intricon | "Exclusivity Date means October 1, 2008, the date Intricon makes its first quarterly payment ..." | 0 | 2 |
| E6 | Existing anchor plus "exclusive" | Exclusivity span, Zogenix | "Distributor shall have the exclusive right to market, promote, sell ... the Product in the Field in the Territory" | 2 | 3 |
| E7 | "exclusive right" + "exclusively from" | Exclusivity span, Fibrogen | "FG shall have the exclusive right and obligation to supply the Lead Compounds to Astellas ..." | 4 | 4 |
| E8 | Gate-2 positive, "exclusive distributor" | G2, Lime Energy | "Company hereby appoints Distributor as Company's exclusive distributor within the Market ..." | 2 | 3 |
| E9 | Gate-2 positive, "an exclusive" | G2, Hyperion Software | "Developer hereby grants to Distributor an exclusive ..." | 0 | 3 |
| E10 | Gate-2 positive | G2, Innerscope Hearing | "Erchonia grants Distributor the exclusive, non- transferable ..." | 2 | 3 |
| E11 | Gate-2 positive | G2, Gentech | "Company hereby appoints and grants Distributor ..." | 2 | 3 |
| E12 | Gate-2 positive, license to the other party | G2, Zogenix | "Distributor hereby grants Zogenix an irrevocable, perpetual, royalty-free, fully paid-up, exclusive license ..." | 0 | 1 |
| E13 | Unreachable: ban without "exclusive" | Exclusivity span, Worldwide Strategies | "Reseller shall not obtain the TouchStar Software or Support Services (or any software or services which compete ...) for sale from any Entity other than ..." | 0 | 0 |
| E14 | Unreachable: ban without "exclusive" | Exclusivity span, Vertex Energy | "During the Term, neither Vertex nor any affiliate of Vertex may sell any Product to any customers for their use as bunker fuel other than pursuant to ..." | 0 | 0 |
| E15 | Unreachable: endorsement ban | Exclusivity span, Allied Esports | "Allied shall not endorse, or permit the marketing of any other company whose principal business is as an e-commerce provider ..." | 0 | 0 |
| N1 | Hard negative: non-exclusive grant | G2 (License Grant), Fuse Medical | "The Supplier hereby grants to the Distributor the non-exclusive right, in the Territory, to use the Trade Mark ..." | 0 | 0 |
| N2 | Hard negative: non-exclusive grant | G2 (License Grant), Zogenix | "Zogenix hereby grants to Distributor a non-exclusive, r..." | 0 | 1 |
| N3 | Hard negative: non-exclusive grant | G2 (License Grant), SFG Financial | "Licensor hereby, subject to ... grants ... a non-exclusive ..." | 0 | 0 |
| N4 | Hard negative: non-exclusive grant | G2 (License Grant), SmartRx | "... Company grants Distributor a limited, revocable, non-transferable, non-exclusive ..." | 0 | 0 |
| N5 | Hard negative: non-exclusive grant | G2 (Irrevocable Or Perpetual License), Armstrong Floor | "... the Company hereby grants to Seller a perpetual, non-ex..." | 0 | 0 |
| N6 | Non-exclusive in a labeled-Exclusivity span (veto) | Exclusivity span, Glu Mobile | "Licensee's right and license ... shall become non-exclusive after D..." | 0 | 0 |

Notes:
- E1-E5 are the new reach: no current anchor, now 2-3. At the expected best threshold of 3 (INFERRED from sim) E4 and E5 would still not fire; the noun-only "exclusivity" spans are weak.
- E12 and N2 show the same excerpt-level artifact: a nearby sentence with the word "exclusive" lifts both; neither reaches 3.
- E13-E15 are the unreachable class (INFERRED: a keyword baseline cannot read "shall not ... other than").
- Sim F1 is optimistic and thresholds are chosen on validation only.

## 11. Sources

- CUAD category description: `data/cuad/category_descriptions.csv`.
- Train spans: `data/splits/train.json` via `.agent/scratch/lib.py`.
- Gate-2 excerpts: `data/cuad/gate2_excerpt_review.csv`, `target_category == "Exclusivity"` (5 positive; 5 hard negative: License Grant x4, Irrevocable Or Perpetual License x1).

# Decision table: Non-Compete

Rule set: `configs/keyword_rules_v1.json` (FROZEN 2026-10-18 as `keyword_rules_v1`, 184 IDs, SHA-256 `07602f34...7ba7e3`). Evidence: the 326 train contracts only (`data/splits/train.json`, `data/gate3/train_*_768_512.csv`, `data/cuad/gate2_excerpt_review.csv`; no validation or test data used; `train_separate_questions.json` and `test.json` not opened).
Status: **APPROVED and APPLIED 2026-10-16 (K1-K6 all approved by Mahir).** The scorer reproduces train sim F1 .497.
Claim labels: **VERIFIED** = seen in a cited source or scratch run on train; **INFERRED** = hypothesis.

## 1. Inclusion meaning

CUAD asks whether a party is restricted from competing with the counterparty or from engaging in a competing business, inside or beyond the term. In the labeled train data (**VERIFIED**, 164 spans in 77 contracts) very few positives say "non-compete". They are:
- distributor and agent restrictions: "the Distributor ... shall handle no products that are competitive with the Products", "Agent may not offer or promote competitive products without the consent of Kallo";
- franchise covenants: "Member shall not, either directly or indirectly, own, manage, ... any Competitive Business", "you agree not to engage in a competitive business for a period of two (2) years";
- consultant/employee covenants: "Consultant will not directly or indirectly (i) participate ...", "Maimon agrees not to: (a) compete with the business of the Company";
- sponsor/advertising bans on named competitors: "Application Provider will not serve advertising ... for any 'Excite@Home Named Competitor'", "SRP may not obtain any associate or secondary sponsors whose products or concepts compete with Logan's";
- R&D and territory bans: "Vyera hereby covenants not to Develop, Manufacture, Commercialize or otherwise exploit a Competitive Product in the Territory", "Array shall not conduct Clinical Studies for a Product in the Ono Territory ...";
- bare fragments tagged with the clause ("The Distributor shall not:", "This Agreement may be terminated:" style headers).

Not included: employee non-solicit (No-Solicit Of Employees: three of the five gate-2 hard negatives: Buffalo Wild Wings, Vitalibis, Aduro), exclusive-dealing promises (Exclusivity: Ediets, Performance Sports Brands hard negatives). Both sit in the same sentences and chunks; see section 5.

Train support: 164 spans in 77 of 326 contracts (**VERIFIED**, Phase 1 table).

## 2. Evidence groups

Each group counts at most once per chunk. Anchor +2, support +1, counter -1, floor 0. Plain substring match on normalized text. NEW = proposed in section 9.

Columns: "spans" = how many of the 164 Non-Compete spans contain the phrase; "all-train occ." = substring count over all 326 contracts; "chunk TP / FP" = unmasked train chunks (9,718; **309 positive**, base rate 3.2%) that contain the phrase and are labeled positive / negative; "contracts" = distinct train contracts behind those TP / FP chunks (chunk overlap inflates chunk counts about 3x). All **VERIFIED** (scratch runs `cat.py`, `nc2.py`, `nc5.py`).

| Group | Role | Phrase (rule ID) | Spans | All-train occ. | Chunk TP / FP | Contracts TP / FP |
|---|---|---|---|---|---|---|
| NC-G1 agrees not to compete | anchor | not compete (01) | 0 | 3 | 5 / 3 | 3 / 3 |
| | | not to compete (02) | 1 | 10 | 10 / 11 | 4 / 4 |
| NC-G2 competing business | anchor | competes with (01) | 5 | 8 | 13 / 7 | 5 / 3 |
| | | compete with (03) | 12 | 24 | 32 / 21 | 10 / 10 |
| | | competitive business (04) | 10 | 18 | 19 / 15 | 3 / 2 |
| NC-G3 indirect involvement | support | directly or indirectly (01) | 29 | 570 | 104 / 1,017 | 34 / 172 |
| NC-G5 competition wording | support | competing (rule ID NC-G2-02) | 16 | 85 | 56 / 75 | 20 / 18 |
| | | non-competition (NC-G5-02) | 6 | 40 | 32 / 29 | 11 / 8 |
| NC-G4 employee no-solicit | counter | solicit (01) | 3 | 295 | **52 / 386** | 21 / 88 |
| NC-G6 competitive / competing product (NEW) | support | competitive with (01) | 12 | 31 | 34 / 44 | 13 / 16 |
| | | competitive to (02) | 3 | 7 | 7 / 10 | 3 / 4 |
| | | competitive product (03) | 5 | 24 | 19 / 33 | 6 / 11 |
| | | competitive products (04) | 3 | 13 | 14 / 21 | 4 / 6 |
| | | competing product (05) | 7 | 42 | 21 / 51 | 7 / 10 |
| | | competing products (06) | 1 | 10 | 8 / 18 | 3 / 7 |
| | | competing business (07) | 4 | 18 | 13 / 2 | 4 / 2 |
| | | (union) | | | 87 / 133 | |
| NC-G7 competitor (NEW) | support | competitor (01) | 29 | 190 | 78 / 186 | 21 / 41 |
| | | competitors (02) | 12 | 73 | 31 / 73 | 9 / 22 |
| | | (union) | | | 78 / 186 | |
| NC-G8 named or explicit competition (NEW) | support | in competition (01) | 3 | 4 | 5 / 0 | 2 / 0 |
| | | own, manage (02) | 4 | 4 | 5 / 0 | 2 / 0 |
| | | named competitor (03) | 6 | 20 | 10 / 5 | 1 / 1 |
| | | named competitors (04) | 4 | 10 | 8 / 3 | 1 / 1 |
| | | (union) | | | 20 / 5 | |
| NC-G9 restricted marketing action (NEW) | support | not market (01) | 3 | 6 | 11 / 6 | 4 / 2 |
| | | not promote (02) | 3 | 8 | 10 / 12 | 4 / 4 |
| | | not endorse (03) | 1 | 5 | 6 / 9 | 3 / 4 |
| | | (union) | | | 27 / 27 | |
| NC-G10 any competitor (NEW, optional) | support | any competitor (01) | 5 | 9 | 16 / 4 | 6 / 1 |
| | | a competitor (02) | 5 | 33 | 18 / 53 | 6 / 13 |
| | | (union) | | | 31 / 53 | |

Maximum score now: anchors NC-G1, NC-G2 (4) + supports NC-G3, NC-G5 (2) = **6**. After K1-K6: + five new support groups = **11** (counter removed).

Note on IDs (cosmetic, **VERIFIED**): the rule "competing" has ID `NC-G2-02` but sits in group `NC-G5`; the rule file kept the ID when it was moved. Not changed by this table.

Why it is the weakest category so far (**VERIFIED**): no phrase with real recall has chunk precision above .65 (most are .43 to .60; the cleaner ones, "competing business", "any competitor", "in competition", come from 2-6 contracts), the two anchor groups cover only 28 of 164 spans (17%), and 62 of 77 contracts with a span have no anchored span. Non-compete is expressed in dozens of drafting styles, usually around "compet*" words that also appear in ordinary sentences ("competitive prices", "competitors" in definitions).

## 3. Counterevidence and vetoes

- **NC-G4-01 "solicit" (counter, -1).** It was written to separate employee no-solicit clauses (three gate-2 hard negatives). **Problem (VERIFIED):** it sits in 52 positive chunks (21 contracts) and 386 negative ones (88 contracts). Precision .12 is four times the base rate (.032), so a "solicit" chunk is *more* likely than average to be a positive; the counter subtracts a point from real non-competes (many non-compete covenants are written next to a non-solicit in the same clause, e.g. franchise and consultant covenants). Dropping it: .332 to .360 (K1). On the proposed set: .497 with, .462 without K1.
- **Other counters tested** (**VERIFIED**): none tried beyond "solicit"; the Exclusivity overlap (section 5) suggests "exclusive" as a counter, but it occurs in 133 positive and 2,366 negative chunks (precision .05, recall .43) and would remove many true positives; not run as a counter. The No-Solicit hard negatives score 0-1 on their own span and excerpt (section 10) and do not need one.
- **Vetoes:** none (chunk-wide design, no windows).

## 4. Context / proximity limits

None. All matching is chunk-wide (768 words, 512-word overlap). Consequence (**VERIFIED**): "competitor" in a definitions section and "shall not" in a different clause of the same chunk are added together, which is why plain "competitor" has 186 negative chunks. "directly or indirectly" (1,017 negative chunks) is in many non-solicit and confidentiality clauses; NC-G3-01 is kept (see section 8) only because dropping it lowers the best threshold to 1 and lowers precision.

## 5. Required confusion cases

The spec's confusion list names none for Non-Compete; the gate-2 hard negatives define two (No-Solicit Of Employees, Exclusivity). Both are covered here.

### 5a. Non-Compete vs Exclusivity

Unmasked chunks labeled for both (**VERIFIED**):

| | NC = 0 | NC = 1 |
|---|---|---|
| Exclusivity = 0 | 8,978 | 244 |
| Exclusivity = 1 | 384 | 63 |

63 of the 307 Non-Compete chunks (21%) are also Exclusivity positives; 63 of 447 Exclusivity chunks (14%). "Exclusive" is too common to separate them (133 positive vs 2,366 negative chunks). The two hard negatives (Ediets: "eDiets will not buy, sell, display or distribute advertising from ... Women.com Competitor"; Performance Sports Brands: "North agrees not to enter into an agreement with another company ... products similar to the Endorsed Products") score 0 on their span under every variant; Ediets' 600-character excerpt scores 1 after K3, because it contains "competitor". **INFERRED**: both are real competitive restrictions that the annotator labeled only Exclusivity; the scorer cannot tell them from the sponsor non-competes labeled positive here (Invenda, Logan's). The overlap shows in the fire rates (section 8): at threshold 2 the proposed rules fire on 15 of 384 Exclusivity-only chunks vs 8 now.

### 5b. Non-Compete vs No-Solicit Of Employees

No-solicit wording is the "solicit" counter's target. The three hard negatives (**VERIFIED**, section 10): Vitalibis scores 0, Aduro 0 now and 1 after K1 (the counter was subtracting from a 0, so retiring it only matters when a point is present), Buffalo Wild Wings 1 on its span. Buffalo's 600-character excerpt rises from 1 to 4 under K1-K6, because the surrounding franchise covenant reads as a real non-compete (competitive-business and "directly or indirectly" wording): **INFERRED** that the excerpt includes a genuine non-compete clause next to the no-solicit sentence. At train level, "solicit" has chunk precision .12; a plain no-solicit chunk therefore is not suppressed any more, and that is the cost of K1: 64 false-positive chunks stay almost unchanged (63 to 64 at the best threshold) while true positives rise from 74 to 82 (**VERIFIED**, K1 alone).

### 5c. Non-Compete vs License Grant and Anti-Assignment (carry-over)

Unmasked overlap (**VERIFIED**): 53 of 303 Non-Compete chunks are also License Grant positives (17%), 29 of 303 Anti-Assignment (10%). At threshold 3 the proposed rules fire on 7 of 752 License Grant chunks and 9 of 748 Anti-Assignment chunks that are Non-Compete negatives, no more than their share (section 8).

## 6. Known near-misses and exclusions

| Pattern | What happens | Evidence |
|---|---|---|
| "competitor" in a definition or list ("'Competitors' means online supermarkets ...", "Named Competitors as listed in Exhibit E") | +1 (K3); labeled positive in some sponsor deals, negative in others | "competitor" 78 / 186 chunks; "named competitor(s)" 18 / 8 |
| "competitive" in ordinary commercial wording ("competitive prices", "competitive disadvantage") | not a rule on its own | "competitive" 89 / 273 chunks; tested alone .354 anchor, .378 support, rejected |
| "directly or indirectly" in confidentiality, non-solicit or ownership clauses | +1 from NC-G3-01 | 104 / 1,017 chunks |
| No-solicit of employees | 0-1 | section 5b |
| Exclusive-dealing promise ("will not enter into an agreement with another company ...") | 0 | section 5a |
| Termination right for a competing product ("(c) Vyera breaches its obligations under Section 2.6 (Competitive Products)") | scores 1; labeled positive | E15 |
| Fragments and headers ("The Distributor shall not:", "CytoDyn shall have the right to terminate ... following:") | 0 | E2, E16 |
| Restriction without any "compet*" word ("Excite@Home shall not promote ...", "MKOS will not seek to acquire any technologies") | 1 | E10, E14 |

## 7. Known weak spots (be honest in the write-up)

1. **Expect a weak validation F1.** The current rules reach .332; even the best variant found stays near .50 on train (optimistic), with precision about .45 at threshold 2 (172 TP / 211 FP). This is a "hard category for keywords" result; it is kept and explained, not tuned further after validation.
2. **Anchors cover 28 of 164 spans (17%).** The strongest phrases ("compete with", "competes with", "competitive business") are in 10 to 12 spans and still have 20-40% false positives at chunk level. No anchor-quality phrase (precision > .85 with real recall) exists: the best, "competing business" (13 / 2), has 4 spans and 4 contracts.
3. **Most positives need two or three supports to reach the threshold.** Positives at score 0 or 1 under the proposed rules: 62 and 75 chunks of 309 (44%).
4. **Several edits are low support**: NC-G8's phrases occur in 2 contracts each; "named competitor(s)" comes from 1 contract (the Excite@Home deal), which also supplies several other positives. Flagged as optional.
5. **Annotation noise**: sponsor/exclusivity sentences and the no-solicit excerpt in section 5b look identical to labeled non-competes.
6. **Chunk overlap inflates counts about 3x**; sim F1 is optimistic (threshold tuned on train) and is a bug check only. The sweep tried about 95 candidate phrases on train.

## 8. Train-only simulation (bug check, optimistic)

Approximate scorer (`sim.score`), 9,718 unmasked chunks (309 positive), best threshold by F1 over 1-9. **VERIFIED**; "current" reproduces the stock `sim.py` result .332 (th 2, 74 TP / 63 FP / 235 FN).

| Variant | Best F1 | Th | TP | FP | FN |
|---|---|---|---|---|---|
| current | .332 | 2 | 74 | 63 | 235 |
| K1 (retire counter "solicit") | .360 | 2 | 82 | 64 | 227 |
| K1 + K2 (competitive / competing product) | .444 | 2 | 126 | 132 | 183 |
| K1-K3 (+ competitor) | .465 | 2 | 142 | 160 | 167 |
| K1-K4 (+ named / explicit competition) | .481 | 2 | 150 | 165 | 159 |
| K1-K5 (+ restricted marketing action) | .490 | 2 | 157 | 175 | 152 |
| K1-K6 (+ "any competitor") | **.497** | 2 | 172 | 211 | 137 |

Single edits on the current rules: K1 .360, K2 .402, K3 .370, K4 .354, K5 .377, K6 .359. Leave-one-out from K1-K6 (.497): without K1 .462 (154 / 203 / 155), without K2 .439 (128 / 146 / 181), without K3 .476, without K4 .483 (164 / 206 / 145), without K5 .487, without K6 .490. So K2 is the big one, K1 and K3 add .02-.04, K4 to K6 add .007 to .014 each.

Drop one existing rule (current rules, **VERIFIED**): NC-G1-01 .332 (no change), NC-G1-02 .330, NC-G2-01 .303, NC-G2-03 .243, NC-G2-04 .298, NC-G3-01 .368 (th 1; 102 / 143 / 207), NC-G2-02 .324, NC-G5-02 .303, NC-G4-01 .360. "directly or indirectly" (NC-G3-01) is the only one whose removal raises F1 on the current rules, but it moves the best threshold to 1 and the precision from .54 to .42; **no edit** (it also appears in 104 of the positive chunks, recall .34). NC-G1-01 "not compete" is a dead rule on span count (0 spans) but kept (3 occurrences, 5 / 3 chunks).

Single extra groups on the current rules (**VERIFIED**; each added as one group): anchor "competitive | competitor | competitors | competition" .392, support .402; anchor "competitor | competitors" .404, support .370; anchor "competitive" .354, support .378; "competition" .336 / .359; "any competitor | a competitor" .378 / .359; "competing business | competing product(s)" .378 / .366; "competitive with | to" .407 / .360; "competes" .334 / .329; "in competition | own, manage" .347 / .347; "named competitor(s)" .350 / .339; "not market | promote | endorse" .388 / .377; "competitive product(s) | competing product(s)" .385 / .387; bare "compete" .294 / .314.

Greedy search over seven candidate groups (choosing each step's best next addition): with the counter kept it ends at .470 after five steps; with the counter dropped it ends at .497 (K2, K3, K4, K5, K6 in that or nearly that order); with the counter and NC-G3-01 both dropped .474 (th 1). The proposed set is the counter-dropped path.

Fire rates on negatives at threshold 2 and 3 (**VERIFIED**), current rules then proposed: threshold 2: 63 to 211 total false-positive chunks (neither overlap group 55 to 195 of 8,978); threshold 3: 25 to 52 (20 to 45 of 8,978). Positives at threshold 2: 74 to 172 of 309; at threshold 3: 50 to 80. The rules fire on 15 of 384 Exclusivity chunks (th 2; 7 at th 3), 20 of 752 License Grant chunks (th 2; 7 at th 3) and 31 of 748 Anti-Assignment chunks (th 2; 9 at th 3) that are Non-Compete negatives.

Score distribution, proposed rules (unmasked chunks): negatives 0: 8,058; 1: 1,140; 2: 159; 3: 38; 4: 8; 5: 2; 6: 4. Positives 0: 62; 1: 75; 2: 92; 3: 33; 4: 28; 5: 7; 6: 6; 7: 5; 8: 1. Current rules: negatives 0: 8,402; 1: 944; 2: 38; 3: 15; 4: 9; 5: 1. Positives 0: 154; 1: 81; 2: 24; 3: 31; 4: 14; 5: 4; 6: 1.

Because the final threshold is chosen later on validation, these thresholds are not the ones that will be used. Max score is 11 after K1-K6, so thresholds 1-11 will be tried.

## 9. Proposed rule edits (NOT applied; need Mahir's OK)

IDs follow the existing convention (`NC-Gn-mm`); "K1..K6" are edit numbers, not rule IDs. Retired IDs are never reused.

| ID | Change | Train evidence | Why | Sim F1 |
|---|---|---|---|---|
| K1 | **Retire NC-G4-01 "solicit"** (counter; ID never reused). Leaves NC-G4 empty | 52 TP / 386 FP chunks (precision .12 vs base rate .032); contracts 21 / 88 | The counter subtracts from real non-competes that sit beside a non-solicit; the no-solicit hard negatives score 0-1 without it (section 5b) | .332 to .360 |
| K2 | New support group **NC-G6** "competitive / competing product": NC-G6-01 "competitive with", -02 "competitive to", -03 "competitive product", -04 "competitive products", -05 "competing product", -06 "competing products", -07 "competing business" | spans 12 / 3 / 5 / 3 / 7 / 1 / 4; union 87 TP / 133 FP chunks (precision .40; "competing business" alone 13 / 2) | The commonest non-compete drafting ("products which are competitive with the Products"); the biggest F1 edit | .360 to .444 |
| K3 | New support group **NC-G7** "competitor": NC-G7-01 "competitor", NC-G7-02 "competitors" | spans 29 / 12; chunks 78 / 186 (precision .30); contracts 21 / 41 | Sponsor, advertising and franchise bans on competitors; also in definitions, so only +1 | .444 to .465 |
| K4 | New support group **NC-G8** "named or explicit competition": NC-G8-01 "in competition", -02 "own, manage", -03 "named competitor", -04 "named competitors". (**Optional, low support: Mahir's call**) | union 20 TP / 5 FP chunks; contracts 2, 2, 1, 1; spans 3, 4, 6, 4 | High-precision phrases but from 1-2 contracts each | .465 to .481 |
| K5 | New support group **NC-G9** "restricted marketing action": NC-G9-01 "not market", -02 "not promote", -03 "not endorse". (**Optional: Mahir's call**) | union 27 / 27 chunks; contracts 4 / 2, 4 / 4, 3 / 4 | "Distributor may not market / promote / endorse" sentences without "compete"; precision only .50 | .481 to .490 |
| K6 | New support group **NC-G10** "any competitor": NC-G10-01 "any competitor", NC-G10-02 "a competitor". (**Optional, small: Mahir's call**) | union 31 / 53 chunks; "any competitor" 16 / 4 (6 / 1 contracts), "a competitor" 18 / 53 | "any competitor" is high precision, "a competitor" is not (+.007 overall) | .490 to .497 |
| no edit | Keep NC-G1, NC-G2, NC-G3-01, NC-G5 as they are | section 8 | All except NC-G3-01 and NC-G1-01 are load-bearing; NC-G3-01 is kept for threshold stability | |

Candidates rejected: "competitive" and "competition" alone (precision .25 and .26), bare "compete" (.294 as anchor), "competitor" as anchor (.404 alone but only because of overlap with K3; precision .30 does not meet the anchor bar), "competes" (+0), "compete against" (0 occurrences), "shall not" / "will not" / "agrees not to" (precision .04 to .06), "engage in" (.14), "restrict" family (.08 to .12), "covenant" (.05), "territory" / "franchise" / "distributor" role words (.05 to .08), "during the term" (.07), an "exclusive" counter (precision .05, would remove true positives), a "directly or indirectly" removal (lowers precision), and any counter for no-solicit (K1).

If K4, K5 and K6 are all declined, K1-K3 reach .465. If only K1 is declined, .462. If K2 is declined, .439.

## 10. Examples that exercise each branch

All from the 326 train contracts. Scores are from the approximate scratch scorer (`sim.score`, **VERIFIED** by running it, not by reading the text). Columns: "Now" = current rules; "+K1"; "+K1-2"; "+K1-3"; "All" = K1-K6. Span rows score the full span text; G2 rows are gate-2 rows, span / 600-character excerpt (excerpt in brackets only when it differs).

| ID | Branch | Source | Text (shortened) | Now | +K1 | +K1-2 | +K1-3 | All |
|---|---|---|---|---|---|---|---|---|
| E1 | Anchor + several supports | NC span, Scoutcam | "During the term of this Agreement and for a period of two (2) years after ..., Maimon agrees not to: (a) compete with the business of ..." | 4 | 4 | 4 | 4 | 4 |
| E2 | Header fragment | NC span, Fuse Medical | "The Distributor shall not:" | **0** | 0 | 0 | 0 | 0 |
| E3 | Franchise covenant | NC span, PF Hospitality | "Member covenants and agrees that during the Post-Term Period ..., Member shall not, either directly or indirectly, own, manage ..." | 3 | 3 | 3 | 3 | 4 |
| E4 | Gate-2 positive, distributor | Precheck Health | "the Distributor, either directly or indirectly, shall handle no products that are competitive with the Products within the Territory" | 1 | 1 | 2 | 2 | 2 |
| E5 | Gate-2 positive, consultant | Kiromic | "Consultant will not directly or indirectly (i) participate ..." | 1 | 1 | 2 | 2 | 2 |
| E6 | Gate-2 positive | Immunomedics | "neither Company nor any of its Affiliates ... shall, alone or in collaboration with any Third Party ..." | 1 | 1 | 2 | 2 | 2 |
| E7 | Gate-2 positive, distributor (excerpt higher) | Innerscope Hearing | "Distributor shall not market, sell advertise or promote the sale or use of any product or device which is competitive with or substantially similar to the Products" | 0 [1] | 0 [1] | 1 [2] | 1 [2] | 2 [3] |
| E8 | Gate-2 positive, post-term | Staar Surgical | "for one year thereafter, Distributor shall not sell, promote, advertise or market in the Territory products which are competitive with the Products" | 0 [0] | 0 [0] | 1 [1] | 1 [2] | 1 [2] |
| E9 | Agent covenant (K2 target) | NC span, Kallo | "Agent may not offer or promote competitive products without the consent of Kallo." | 0 | 0 | 1 | 1 | 1 |
| E10 | Sponsor ban, no "compet*" in the verb | NC span, Excite@Home (Invenda) | "Excite@Home shall not promote competing services in such contact or otherwise discourage Program Members ..." | 1 | 1 | 1 | 1 | 2 |
| E11 | Named competitors (K4 target) | NC span, Invenda | "Application Provider will not serve advertising on the Co-Branded Application for any 'Excite@Home Named Competitor,' as specified in EXHIBIT E." | 0 | 0 | 0 | 1 | 2 |
| E12 | Competitor list (K3/K4 target) | NC span, Invenda | "In no event may either party sell, disclose, transfer, rent, or license Payment-Eligible User Data to the other party's Named Competitors as listed in EXHIBIT E." | 0 | 0 | 0 | 1 | 2 |
| E13 | Non-competitive endorsement | NC span, Adams Golf | "When endorsing a non-competitive product, under no circumstances shall CONSULTANT wear, play, use, hold or in any way be associated with an ADAMS GOLF competitor's Product." | 0 | 0 | 1 | 2 | 2 |
| E14 | Restriction without a "compet*" word | NC span, Manakoa | "MKOS will not seek to acquire any technologies presented to MKOS by UTEK ... directly or indirectly for a period of 24 months following the termination" | 1 | 1 | 1 | 1 | 1 |
| E15 | Termination right for competing product | NC span, Cytodyn | "(c) Vyera breaches its obligations or covenants under Section 2.6 (Competitive Products);" | 0 | 0 | 1 | 1 | 1 |
| E16 | Termination header | NC span, Cytodyn | "CytoDyn shall have the right to terminate this Agreement in its entirety upon written notice to Vyera on the occurrence of any of the following:" | 0 | 0 | 0 | 0 | 0 |
| E17 | Competitor definition, labeled Exclusivity-like | NC span, Women.com (Ediets) | "(c) Women.com will not enter into a relationship with a Competitive Company that involves any of the following; ..." | 0 | 0 | 0 | 0 | 0 |
| E18 | Existing anchors only | NC span, HealthGate | "Publishers may not use either Proprietary Software or Source Code held in escrow to develop a product that competes with those services offered by HealthGate." | 2 | 2 | 2 | 2 | 2 |
| E19 | Existing anchors only | NC span, JointCorp | "you agree not to engage in a competitive business for a period of two (2) years ..." | 2 | 2 | 2 | 2 | 2 |
| N1 | Gate-2 hard negative: Exclusivity | Ediets (span / excerpt) | "eDiets will not buy, sell, display or distribute advertising from ... any Women.com Competitor" | 0 [0] | 0 [0] | 0 [0] | 0 [1] | 0 [1] |
| N2 | Gate-2 hard negative: No-Solicit | Buffalo Wild Wings (span / excerpt) | "Employ or seek to employ any person who is at that time employed by us ... or otherwise directly or indirectly induce or seek to induce ..." | 1 [1] | 1 [1] | 1 [1] | 1 [2] | 1 [**4**] |
| N3 | Gate-2 hard negative: No-Solicit | Vitalibis | "Each Party agrees that during the term of this Agreement and for a period of twelve (12) consecutive months thereafter they shall not, directly, solicit, engage, ..." | 0 | 0 | 0 | 0 | 0 |
| N4 | Gate-2 hard negative: No-Solicit | Aduro | "Consultant shall not ... directly or indirectly, solicit or encourage any employee ..." | 0 | **1** | 1 | 1 | 1 |
| N5 | Gate-2 hard negative: Exclusivity | Performance Sports Brands | "North agrees not to enter into an agreement with another company or entity for the purpose of endorsing or promoting products similar to the Endorsed Products." | 0 | 0 | 0 | 0 | 0 |

Notes:
- E4-E8 (gate-2 positives) reach 2 after K2 (and 3 for E7's excerpt after K5); at the expected best threshold of 2 (INFERRED from sim) E5, E6, E4 would fire and E8 would not, but E8's excerpt (2) would.
- N4 shows the cost of K1 on the no-solicit hard negative: Aduro goes from 0 to 1 once the counter no longer subtracts "solicit"; it stays below 2. N2's excerpt (4) is the one hard negative that would fire; section 5b explains why it is probably a real non-compete clause.
- E2, E16, E17 are the unreachable class (fragments, headers); E14 shows restrictions with no "compet*" word.
- The Anti-Assignment table's lesson applies here as well: sim F1 is optimistic and thresholds are chosen on validation only.

## 11. Sources

- CUAD category description: `data/cuad/category_descriptions.csv`.
- Train spans: `data/splits/train.json` via `.agent/scratch/lib.py`.
- Gate-2 excerpts: `data/cuad/gate2_excerpt_review.csv`, `target_category == "Non-Compete"` (5 positive, 5 hard negative: Exclusivity x2, No-Solicit Of Employees x3).
- Chunks and labels: `data/gate3/train_chunks_768_512.csv`, `train_chunk_labels_768_512.csv` (unmasked rows; 9,718 chunks, 309 positive; Exclusivity, License Grant and Anti-Assignment co-occurrence tables).
- Rule-level provenance: `configs/keyword_rules_v1.json` (categories["Non-Compete"], 9 rule IDs).
- Cross-references: `license_grant.md`, `anti_assignment.md`.
- Scratch: `.agent/scratch/{lib,cat,cand2,sim}.py`; session experiment scripts in the session scratchpad (`gen.py` harness, `nc1`-`nc5`; not part of the repo).
- Reviewer: not yet assigned.

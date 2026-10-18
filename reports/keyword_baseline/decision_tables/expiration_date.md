# Decision table: Expiration Date

Rule set: `configs/keyword_rules_v1.json` (DRAFT, not frozen). Evidence: the 326 train contracts only (`data/splits/train.json`, `data/gate3/train_*_768_512.csv`, `data/cuad/gate2_excerpt_review.csv`; all gate-2 titles checked to be in train). No validation or test data used; `train_separate_questions.json` not opened.
Status: **APPROVED and APPLIED 2026-10-18 (D1-D6 all approved by Mahir).** Rule file now 184 IDs. **Correction after applying:** the scorer on the applied rules gives train sim F1 **.719** (th 3; 470 TP / 128 FP / 240 FN), not .727. The scratch harness behind sections 8-9 demoted the whole ED-G1 group, which also turned ED-G1-02 "remain in effect" and ED-G1-03 "in effect until" into support; the proposed D2 only moved ED-G1-01. All sim figures in sections 8-10 (F1 .727, cumulative and leave-one-out values) carry that extra demotion and are about .01 high. **D7 (approved by Mahir, APPLIED 2026-10-18):** retired ED-G1-02/03 anchors and re-added them as support ED-G11-01/02, giving the scorer's **.729** (th 3; 465 TP / 101 FP / 245 FN); dropping either alone gives .717 / .720. Applied-rules F1 is therefore .729.
Claim labels: **VERIFIED** = seen in a cited source or scratch run on train; **INFERRED** = hypothesis.

## 1. Inclusion meaning

CUAD asks "On what date will the contract's initial term expire?" (**VERIFIED**, `data/cuad/category_descriptions.csv`; answer format: a date or "Perpetual"). In the labeled train spans (**VERIFIED**) the positives are the sentences that say how long the contract lasts, not only a calendar date:
- "The term of this Agreement shall commence on the Effective Date and shall continue ... for an initial period of five (5) years";
- an end date or duration with an early-termination escape ("Unless earlier terminated ..., this Agreement shall continue indefinitely");
- "ends on the Expiration Date set forth in the Addendum".

Not included: the start date alone ("effective as of January 1, 2012" is the Effective Date category), renewal mechanics ("automatically renews for additional one-year terms" is Renewal Term), notice periods and termination-for-convenience rights. These are neighbouring categories and share chunks with the real clause (section 5).

Train support: 302 spans in 264 of 326 contracts (**VERIFIED**, Phase 1 table). 131 of the 302 spans contain a current anchor.

## 2. Evidence groups

Each group counts at most once per chunk. Anchor +2, support +1, counter -1, floor 0. Plain substring match on normalized text. NEW = proposed in section 9.

"Chunk TP / FP" = unmasked train chunks (9,670; 710 positive, 7.3%) that contain the phrase and are labeled positive / negative for Expiration Date. All **VERIFIED** (scratch runs `cat.py`, `cand2.py` and a chunk-level phrase counter).

| Group | Role | Phrase | Spans containing | All-train occ. | Chunk TP / FP |
|---|---|---|---|---|---|
| ED-G1 how long the agreement lasts | anchor | term of this agreement (01) | 94 | 831 | 318 / 1,281 |
| | | remain in effect (02) | 15 | 54 | 47 / 83 |
| | | in effect until (03) | 11 | 21 | 31 / 26 |
| ED-G2 expiry wording | anchor | shall expire (01) | 15 | 33 | 40 / 42 |
| | | expiration date (02) | 8 | 79 | 32 / 104 |
| | | termination date (03) | 6 | 156 | 52 / 180 |
| ED-G3 initial term | support | initial term (01) | 65 | 259 | 186 / 168 |
| ED-G4 renewal wording | counter | automatically renew (01) | 11 | 48 | **110 / 14** |
| ED-G5 start-date wording | counter | effective as of (01) | 20 | 175 | 93 / 222 |
| ED-G7 commencement (NEW) | anchor | commence on (01) | 63 | 89 | 175 / 38 |
| | | shall commence (02) | 65 | 109 | 180 / 97 |
| | | begin on (03) | 24 | 37 | 61 / 18 |
| | | effective date and shall (04) | 44 | 48 | 120 / 7 |
| | | effective date and will (05) | 10 | 11 | 26 / 3 |
| | | (union) | | | 329 / 138 |
| ED-G8 early-termination qualifier (NEW) | anchor | unless earlier terminated (01) | 35 | 41 | 98 / 11 |
| | | unless sooner terminated (02) | 15 | 16 | 40 / 3 |
| | | earlier terminated (03) | 40 | 52 | 110 / 20 |
| | | terminated earlier (04) | 27 | 33 | 73 / 9 |
| | | unless terminated (05) | 42 | 61 | 128 / 24 |
| | | until terminated (06) | 16 | 22 | 46 / 12 |
| | | (union) | | | 335 / 62 |
| ED-G9 continuation (NEW) | support | continue in effect (01) | 17 | 29 | 55 / 23 |
| | | shall continue (02) | 75 | 312 | 237 / 498 |
| | | initial period (03) | 9 | 25 | 32 / 16 |
| | | for an initial (04) | 13 | 14 | 35 / 3 |
| | | (union) | | | 280 / 521 |

Plus, after the edits: ED-G6 (support, "term of this agreement", moved from ED-G1-01) and ED-G10 (support, "expiration date", "termination date", moved from ED-G2-02/03).

Maximum score now: anchors ED-G1, ED-G2 (2 each) + support ED-G3 (1) = 5. After D1-D6: anchors ED-G1 (remain in effect / in effect until), ED-G2 (shall expire), ED-G7, ED-G8 (2 each) + supports ED-G3, ED-G6, ED-G9, ED-G10 (1 each) = **12**.

The two reasons the current set does poorly (**VERIFIED**): "term of this agreement" is the anchor for 94 spans but also fires in 1,281 negative chunks (precision .20, 2.7x the 7.3% base rate), so the category fires on nearly every contract's term sentence or heading. And the two counters are wrong-way round: "automatically renew" is in 110 positive and only 14 negative chunks (precision .89), because a chunk that has a renewal sentence usually has the term sentence next to it. The 37% overlap with Renewal Term (section 5) is why.

## 3. Counterevidence and vetoes

- **ED-G4-01 "automatically renew" (counter): retire (D1).** 110 TP / 14 FP chunks. It subtracts 1 from 110 real positives, to remove 14 false positives at most. Leave-one-out F1 with it retained: .698 vs .727 (all edits, minus D1).
- **ED-G5-01 "effective as of" (counter): retire (D1).** 93 TP / 222 FP chunks (precision .30, above the 7.3% base rate), so it is not counterevidence. It is also an Effective Date phrase, but those chunks often include the end of the term in the next sentence. Removing it alone is worth +.002; D1 as a pair is +.016.
- **No vetoes** exist or are proposed.
- **No new counters proposed.** The greedy search over train phrases found no counter that helped; the hard-negative neighbours in section 5b are the same paragraph as a real clause, so a counter would also remove true positives (INFERRED from 5a).

## 4. Context / proximity limits

None proposed (the engine is plain substring + group max). A limit such as "within 100 characters of a number or year" would help ("term of this agreement ... five (5) years") but substring matching cannot express it. **INFERRED**: this is the main thing the TF-IDF and transformer models should add.

## 5. Required confusion cases

**5a. Expiration Date vs Renewal Term (VERIFIED, train).** 262 of the 710 Expiration Date chunks (37%) are also Renewal Term positives; 262 of the 301 Renewal Term chunks (87%) are Expiration Date chunks. Same paragraph, two labels. Consequence: Renewal Term wording (such as "automatically renew") is real Expiration Date evidence, which is why D1 retires that counter. At the proposed threshold 3 only 9 of the 99 false positives are Renewal Term chunks.

**5b. Gate-2 hard negatives (VERIFIED, `target_category == "Expiration Date"`, scored by the scratch scorer; "span / excerpt", now to after).**

| Source category | Title | Text (shortened) | Now | After |
|---|---|---|---|---|
| Notice Period To Terminate Renewal | FTE Networks | "After the Initial Term, this Agreement shall continue on a month to month basis until terminated by either party upon thirty (30) days prior ..." | 1 / 3 | 4 / 5 |
| Notice Period To Terminate Renewal | America's Shopping Mall | "This Agreement shall be automatically renewed for an additional one year period on each anniversary of the Effective Date, unless terminated ..." | 0 / 0 | 2 / 4 |
| Termination For Convenience | Pareteum | "The Agreement may be terminated by both Parties with a notification period of *** before the end of the Initial Term ..." | 1 / 1 | 1 / 2 |
| Renewal Term | Kubient | "This Agreement will automatically renew for additional 1-year terms unless earlier terminated pursuant to this Agreement's express provisions" | 0 / 2 | 3 / 4 |
| Effective Date | Moelis | "This Agreement shall be effective as of January 1, 2012 (the "Effective Date"), provided, however, that ARTICLE XII ..." | 0 / 1 | 0 / 4 |

Honest reading: the edits raise four of the five hard negatives; by excerpt, four of the five reach 3 or more (5, 4, 2, 4, 4: Pareteum stays at 2). These are the same paragraph as a real Expiration Date clause (Renewal Term and Notice Period spans sit beside "unless earlier terminated"), so the baseline will report them as false positives against the gate-2 labels. They are the expected cost of a keyword baseline here (**INFERRED**); do not add a counter for "automatically renew" to fix them (section 3).

**5c. Other overlaps (VERIFIED).** At threshold 3 the 99 false positives by co-label: License Grant 16, Non-Transferable License 10, Renewal Term 9, Anti-Assignment 8, Cap On Liability 6, Exclusivity 5, Non-Compete 3, Uncapped Liability 1 (most FPs are neither: the sentence about "the term" in boilerplate).

## 6. Known near-misses and exclusions

- Start-date-only sentences ("effective as of ...", "shall be effective on") are Effective Date, not Expiration Date; they no longer subtract (D1); they carry no anchor of their own.
- "Unless terminated" (128 TP / 24 FP) also appears in renewal and termination clauses; accepted as an anchor because its precision is .84 (128 / 24), but it can also appear in renewal and termination clauses.
- Rejected as a rule because noisy: "years" (264 / 891), "expire" (101 / 285), "expires" (30 / 74), "perpetual" (29 / 195), "shall remain" (118 / 784), "shall terminate" (97 / 296), "term of" (433 / 1,654), "anniversary" (91 / 217).

## 7. Known weak spots (be honest in the write-up)

- 107 of the 302 spans (35%) still have no anchor after the edits. They are short fragments ("5 years.", "Term means the period commencing ... indefinitely") or definitions. INFERRED ceiling for a keyword baseline: recall about .65 at threshold 3.
- Precision at threshold 3 is good (.82) because D3 and D4 are reliable, but "shall continue" (237 / 498) and "shall commence" (180 / 97) are noisy on their own and only help in combination.
- Hard negatives in section 5b rise, as expected.

## 8. Train-only simulation (bug check, optimistic)

Scratch scorer: `sim.score` (group max). Best threshold over 1-8 on unmasked train chunks. **Optimistic** because the new phrases were found on the same train data; thresholds will be chosen on validation later.

| Rule set | Best F1 | Threshold | TP | FP | FN |
|---|---|---|---|---|---|
| Current | .326 | 1 | 474 | 1,727 | 236 |
| D1 | .342 | 1 | 503 | 1,731 | 207 |
| D1+D2 | .342 | 1 | 503 | 1,731 | 207 |
| D1-D3 | .527 | 2 | 435 | 505 | 275 |
| D1-D4 | .688 | 3 | 423 | 97 | 287 |
| D1-D5 | .706 | 3 | 467 | 146 | 243 |
| D1-D6 (all) | **.727** | 3 | 462 | 99 | 248 |

Leave-one-out (all minus one): D1 .698, D2 .684, D3 .630, D4 .592, D5 .701, D6 .706. Only that one: D3 .489, D4 .495, D5 .357, D1 .342, D6 .320, D2 .303 (D2 lowers F1 alone because it removes an anchor, but is needed once D3-D4 raise the threshold).

Final operating points on train chunks: threshold 2 precision .57 / recall .76; threshold 3 precision .82 / recall .65; threshold 4 precision .91 / recall .47. Spans with at least one anchor go from 131 to 195 of 302.

Not proposed: removing "term of this agreement" outright (.618, worse than demoting it, because it still adds +1 for real clauses); "years" as support (+.001); "automatically" as support (+.012, but it is renewal wording and would blur the two categories; **optional**, Mahir's call).

## 9. Proposed rule edits (NOT applied; need Mahir's OK)

IDs follow the existing convention (`ED-Gn-mm`); "D1..D6" are edit numbers. Retired IDs are never reused.

| ID | Change | Train evidence | Why | Sim F1 |
|---|---|---|---|---|
| D1 | **Retire ED-G4-01 "automatically renew" and ED-G5-01 "effective as of"** (both counters; IDs never reused). ED-G4 and ED-G5 become empty | 110 / 14 and 93 / 222 chunks (precision .89 and .30 vs base rate .073) | Both subtract from real positives (section 3, 5a) | .326 to .342 |
| D2 | **Retire anchor ED-G1-01 "term of this agreement"**; re-add it as support, new group **ED-G6**, ED-G6-01 | 318 TP / 1,281 FP chunks (precision .20); 94 spans | As an anchor it fires on every term heading. Alone it changes nothing; it is needed once D3-D4 are in (without it the final F1 is .684) | .342 to .342 |
| D3 | New anchor group **ED-G7** "commencement": ED-G7-01 "commence on", -02 "shall commence", -03 "begin on", -04 "effective date and shall", -05 "effective date and will" | union 329 / 138 chunks; strongest "effective date and shall" 120 / 7; spans 63, 65, 24, 44, 10 | The usual wording of a term clause ("shall commence on the Effective Date and continue ... five years") | .342 to .527 |
| D4 | New anchor group **ED-G8** "early-termination qualifier": ED-G8-01 "unless earlier terminated", -02 "unless sooner terminated", -03 "earlier terminated", -04 "terminated earlier", -05 "unless terminated", -06 "until terminated" | union 335 / 62 chunks (precision .84); spans 35, 15, 40, 27, 42, 16 | "Unless earlier terminated, this Agreement ..." says the term has an end | .527 to .688 (threshold 3) |
| D5 | New support group **ED-G9** "continuation": ED-G9-01 "continue in effect", -02 "shall continue", -03 "initial period", -04 "for an initial" | union 280 / 521 chunks (precision .35); "for an initial" 35 / 3 | Partial credit for the duration wording | .688 to .706 |
| D6 | **Retire anchors ED-G2-02 "expiration date" and ED-G2-03 "termination date"**; re-add as support, new group **ED-G10**, ED-G10-01 "expiration date", -02 "termination date" | 32 / 104 and 52 / 180 chunks (precision .24 and .22) | Below the anchor bar; still useful as +1 | .706 to .727 (threshold 3) |
| no edit | Keep ED-G1-02/03, ED-G2-01, ED-G3-01 | section 8 | Load-bearing; "remain in effect" / "in effect until" precision .36 / .54, "shall expire" .49, "initial term" .53 | |

Net ID change if all approved: 5 retired, 18 added (1 + 5 + 6 + 4 + 2), rule file 171 to 184.

If D6 is declined, .706. If D5 is declined, .701. D2 should go with D3 and D4. D1 can be taken or dropped separately (.698 without it).

## 10. Examples that exercise each branch

Scores from the scratch scorer (**VERIFIED** by running it). "Now" = current rules; "After" = D1-D6. Span rows score the span text; G2 rows score the gate-2 span (the excerpt number is in section 5b for hard negatives).

| ID | Branch | Source | Text (shortened) | Now | After |
|---|---|---|---|---|---|
| E1 | Commencement + early-termination | Ex span, Sonos | "Unless terminated earlier as provided herein, this Agreement shall terminate on the date three (3) years from the Effective Date." | 0 | 2 |
| E2 | Commencement + continuation | Ex span, Ashworth | "Except as otherwise provided herein, this Agreement shall commence effective June 1, 1998, and shall continue for a term of three (3) years expiring ..." | 0 | 3 |
| E3 | Early-termination qualifier + indefinite | Ex span, Variable Separate Account | "Unless earlier terminated in accordance with this paragraph 7, this Agreement shall continue indefinitely." | 0 | 3 |
| E4 | Gate-2 positive | Corio | "The term of this Agreement shall commence on the Effective Date and shall continue in full force and effect for an initial period of five (5) ..." | 2 | 4 |
| E5 | Gate-2 positive | Intersect | "Unless terminated in accordance with the provisions of Section 10.2 below, the term of this Agreement shall commence on the Effective Date ..." | 2 | 6 |
| E6 | Gate-2 positive | Diversinet | "The term of this Agreement shall begin on the Effective Date and continue in effect for a period of five (5) years (the 'Initial Term'), unl..." | 3 | 7 |
| E7 | Gate-2 positive | Neurobo | "This Agreement shall commence on the Effective Date and, unless earlier terminated, shall continue in full force and effect for a period of ..." | 0 | 5 |
| E8 | Gate-2 positive | Manufacturers Services | "This Agreement shall become effective on the Effective Date and shall continue for a period of three (3) years unless terminated as provided ..." | 0 | 5 |
| E9 | Anchor lost (move to support) | Ex span, National Processing | "The term of this Agreement shall be five years commencing on the Effective Date and ending at the close of business on the fifth anniversary ..." | 2 | 1 |
| E10 | Unreachable: definition | Ex span, Inktomi | '"Term" means the period of time commencing on the Effective Date and continuing thereafter indefinitely until this Agreement is terminated pursuant to ...' | 0 | 0 |
| E11 | Unreachable: amendment | Ex span, Veoneer | "This Amendment shall only become effective upon the VNBJ Closing with respect to Article 1.1 ..." | 0 | 0 |
| N1 | Hard negative: Notice Period | FTE Networks | "After the Initial Term, this Agreement shall continue on a month to month basis ..." | 1 | 4 |
| N2 | Hard negative: Renewal Term | Kubient | "This Agreement will automatically renew for additional 1-year terms unless earlier terminated ..." | 0 | 3 |
| N3 | Hard negative: Effective Date | Moelis | "This Agreement shall be effective as of January 1, 2012 ..." | 0 | 0 |

Notes:
- E1-E3 and E7-E8 are the new reach: no current anchor, now 2-5.
- E9 shows the cost of D2: a real clause whose only anchor was "term of this agreement" now scores 1. The net trade is positive because 1,281 negative chunks stop reaching 2.
- N1 and N2 are the section 5b cases that would fire at threshold 3; they are the same paragraph as a real Expiration Date or Renewal Term clause (**INFERRED**).
- Sim F1 is optimistic and thresholds are chosen on validation only.

## 11. Sources

- CUAD category description: `data/cuad/category_descriptions.csv`.
- Train spans: `data/splits/train.json` via `.agent/scratch/lib.py`.
- Gate-2 excerpts: `data/cuad/gate2_excerpt_review.csv`, `target_category == "Expiration Date"` (5 positive; 5 hard negative: Notice Period To Terminate Renewal x2, Termination For Convenience, Renewal Term, Effective Date).

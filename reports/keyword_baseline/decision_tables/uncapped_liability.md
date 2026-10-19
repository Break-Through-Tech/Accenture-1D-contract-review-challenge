# Decision table: Uncapped Liability

Rule set: `configs/keyword_rules_v1.json` (FROZEN 2026-10-18 as `keyword_rules_v1`, 184 IDs, SHA-256 `07602f34...7ba7e3`). Evidence: the 326 train contracts only (`data/splits/train.json`, `data/gate3/train_*_768_512.csv`, `data/cuad/gate2_excerpt_review.csv`; no validation or test data used; `train_separate_questions.json` and `test.json` not opened).
Status: **APPROVED by Mahir 2026-10-16; U1-U6 (section 9) APPLIED to the JSON.**
Claim labels: **VERIFIED** = seen in a cited source or scratch run on train; **INFERRED** = hypothesis.

## 1. Inclusion meaning

CUAD asks whether a party's liability is uncapped upon the breach of its obligations, or carved out of a cap: "a clause that explicitly states that a party's liability is unlimited or not subject to a cap, or ... excluded from a cap". In the labeled train data (**VERIFIED**, 115 spans in 78 contracts) the positives are almost never the word "unlimited". They are:
- the **exception lead-in plus the cap sentence** it modifies: "EXCEPT FOR A PARTY'S OBLIGATIONS SET FORTH IN THIS ARTICLE 13, AND ANY BREACH OF ARTICLE 10 (CONFIDENTIALITY), IN NO EVENT WILL EITHER PARTY BE LIABLE ..." (Cytodyn). This is the biggest form: most spans start with "EXCEPT FOR / IN / WITH RESPECT TO / UNDER ...";
- stand-alone carve-outs: "THESE LIMITATIONS SHALL NOT APPLY TO DAMAGES ARISING FROM ...", "NOTHING IN THIS SECTION 14.7 IS INTENDED TO ... LIMIT OR RESTRICT THE INDEMNIFICATION RIGHTS", "THE LIMITATIONS ... SHALL BE INAPPLICABLE TO ... INDEMNIFY";
- explicit unlimited wording, rare: "each Party will bear full responsibility, without limit, for ...", "for which cases there shall be no limitation" (Xencor), "expressly waives any and all limitations or liability caps" (Nanophase);
- odd fragments the annotator tagged with the clause: claim time bars with an indemnification exception, "Except for claims under Sections 9.4 [INDEMNIFICATION BY IMPRESSE] ...", and bare fragments with no phrase to match.

Not included: the ordinary cap itself (Cap On Liability), a generic "except as otherwise expressly set forth" (Biofrontera hard negative). The two categories are **not exclusive** on a chunk, see section 5.

Train support: 115 spans in 78 of 326 contracts (**VERIFIED**, Phase 1 table).

## 2. Evidence groups

Each group counts at most once per chunk. Anchor +2, support +1, counter -1, floor 0. Plain substring match on normalized text. NEW = proposed in section 9.

Columns: "spans" = how many of the 115 Uncapped spans contain the phrase; "all-train occ." = substring count over all 326 contracts; "chunk TP / FP" = unmasked train chunks (9,733; **239 positive**) that contain the phrase and are labeled positive / negative for Uncapped Liability; "contracts" = distinct train contracts behind those TP / FP chunks (chunk overlap inflates chunk counts about 3x). All **VERIFIED** (scratch runs `cat.py`, `cand2.py`, `ul.py`, `ul8.py`).

| Group | Role | Phrase (rule ID) | Spans | All-train occ. | Chunk TP / FP | Contracts TP / FP |
|---|---|---|---|---|---|---|
| UL-G2 explicitly unlimited | anchor | unlimited liability (01) | 0 | 3 | 0 / 9 | 0 / 3 |
| | | uncapped (02) | 0 | 0 | 0 / 0 | 0 / 0 |
| UL-G5 carve-out for serious misconduct | anchor | gross negligence or willful (01) | 11 | 58 | 31 / 81 | 12 / 24 |
| UL-G3 typical exceptions | support | gross negligence (01) | 16 | 126 | 56 / 201 | 22 / 54 |
| | | willful misconduct (02) | 16 | 181 | 62 / 271 | 26 / 71 |
| | | indemnification obligations (03) | 26 | 82 | 79 / 84 | 30 / 28 |
| | | no limitation (04) | 1 | 1 | 3 / 0 | 1 / 0 |
| UL-G4 ordinary cap with generic exception | counter | except as otherwise expressly set forth (01) | 0 | 13 | 0 / 36 | 0 / 12 |
| UL-G6 cap context (NEW) | support | consequential (01) | 55 | 221 | 207 / 320 | 74 / 96 |
| UL-G7 exception lead-in (NEW) | support | except for (01) | 34 | 453 | 101 / 1,012 | 37 / 151 |
| | | except in (02) | 14 | 170 | 51 / 383 | 22 / 101 |
| | | except with (03) | 10 | 103 | 27 / 246 | 10 / 63 |
| | | except under (04) | 4 | 75 | 13 / 131 | 4 / 2 |
| | | (union of the four) | | | 169 / 1,670 | |
| UL-G8 confidentiality carve-out (NEW) | support | breach of confidentiality (01) | 7 | 15 | 21 / 18 | 7 / 5 |
| | | confidentiality obligations (02) | 9 | 85 | 30 / 180 | 13 / 46 |
| | | (union) | | | 42 / 192 | |
| UL-G9 section-specific carve-out (NEW) | support | breach of section (01) | 12 | 34 | 33 / 51 | 13 / 17 |
| | | breach of article (02) | 8 | 13 | 18 / 7 | 6 / 3 |
| | | obligations under section (03) | 11 | 61 | 33 / 127 | 13 / 31 |
| | | (union) | | | 73 / 184 | |
| UL-G10 other named carve-outs (NEW) | support | misappropriation (01) | 4 | 80 | 30 / 153 | 13 / 39 |
| | | payment obligations (02) | 2 | 90 | 15 / 212 | 7 / 45 |
| | | (union) | | | 42 / 360 | |
| UL-G11 "gross negligence or willful" (NEW, replaces UL-G5-01) | support | gross negligence or willful (01) | 11 | 58 | 31 / 81 | 12 / 24 |
| UL-G2 additions (NEW) | anchor | no limitation (moved from UL-G3-04 as UL-G2-05) | 1 | 1 | 3 / 0 | 1 / 0 |
| | | shall be inapplicable (03) | 1 | 1 | 3 / 0 | 1 / 0 |
| | | excludes or limits (04) | 1 | 1 | 3 / 0 | 1 / 0 |

Base rate: 239 of 9,733 unmasked chunks (2.5%). Maximum score now: anchor groups UL-G2, UL-G5 (2 each) + support UL-G3 (1) = **5**. After U1-U6: anchor UL-G2 (2) + supports UL-G3, UL-G6, UL-G7, UL-G8, UL-G9, UL-G10, UL-G11 (7) = **9**. The counter UL-G4 is unchanged.

Why "unlimited liability" must go (**VERIFIED**): all three train occurrences, in 9 overlapping chunks and 3 contracts, are the entity definition "limited liability or unlimited liability company". 0 true positives, 9 false positives. "uncapped" never appears in train (0 occurrences), so the "explicitly unlimited" anchor group has no working rule.

Why a cap-context word: 227 of the 239 Uncapped chunks (95%) are also Cap On Liability positives (section 5). A carve-out only exists beside a cap, so evidence that the chunk is a cap clause is evidence for Uncapped. "consequential" (in 55 spans, recall .87 over chunks, precision .39 against a 2.5% base rate) is the cheapest such signal. Inside chunks that contain it, the carve-out phrases are far more precise than outside (**VERIFIED**, `ul4.py`): "except in" .78 vs .12, "except for" .62 vs .09, "indemnification obligations" .85 vs .48, "breach of confidentiality" 1.00 (20 / 0) vs .54, "misappropriation" .90 vs .16, "breach of section" .91 vs .39. That is the reason for the additive support design (cap context +1, each carve-out type +1).

## 3. Counterevidence and vetoes

- **UL-G4-01 "except as otherwise expressly set forth" (counter, -1).** Checked on train (**VERIFIED**): 13 occurrences, in 12 contracts and 36 unmasked chunks, **0 positive** and 36 negative; 0 of 115 Uncapped spans contain it. It never subtracts from a real positive. Removing it changes sim F1 by 0 on the proposed set (.684 to .684) and by -.002 on the current rules (.313 vs .315), so it is harmless. Decision: **keep, no edit**; provenance upgraded from "hard negative N5" to "verified on train".
- **Cap-side counters on Uncapped: not used.** Cap On Liability retired its own "limitation does not apply" counter because 227 of 234 Uncapped chunks are also Cap chunks. The mirror question is whether the Uncapped table should subtract for plain cap wording ("shall not exceed", "aggregate liability"). Tested (**VERIFIED**, sim): "exceed" is in 73 positive and 1,095 negative chunks (precision .06) and 48% positive inside cap chunks, so it does not separate; no cap-wording counter is proposed.
- **Vetoes:** none (chunk-wide design, no windows).

## 4. Context / proximity limits

None. All matching is chunk-wide (768 words, 512-word overlap). Consequence (**VERIFIED**): the cap sentence in one section and a carve-out in another section of the same chunk combine into one score. This is partly why the chunk-level precision numbers differ from span counts: "except for" is in 34 spans but in 1,012 negative chunks. The UL-G6 cap-context signal narrows that (section 2).

## 5. Required confusion cases

### 5a. Cap vs Uncapped carve-outs

Unmasked chunks labeled for both categories (**VERIFIED**, label file):

| | Uncapped = 0 | Uncapped = 1 |
|---|---|---|
| Cap = 0 | 8,903 | 7 |
| Cap = 1 | 515 | 227 |

227 of 239 Uncapped chunks are also Cap positives; only 7 Uncapped chunks are Uncapped-only (5 more have Cap masked). So Uncapped is, in practice, a subset of Cap: "a cap clause that also contains a carve-out". The Cap table decided not to separate them with Cap counters and left the job to this table.

How the proposed rules treat the groups (**VERIFIED**, sim; "fire" = score at or above the threshold):

| Chunk group | Count | current, th 2 | current, th 3 | proposed, th 2 | proposed, th 3 |
|---|---|---|---|---|---|
| neither label | 8,903 | 70 | 59 | 192 | 10 |
| Cap only ("plain cap", Uncapped = 0) | 515 | 19 | 19 | 112 | 10 |
| Uncapped only | 7 | 0 | 0 | 1 | 0 |
| both | 227 | 30 | 30 | 193 | 133 |

At threshold 3 the proposed rules fire on 10 of 515 plain-cap chunks (1.9%) and on 133 of 227 chunks that hold both (59%). At threshold 2 the plain-cap leak is 112 of 515 (22%): the best threshold must be 3. **Do not read the table's best threshold as the final one;** it is chosen on validation. The conclusion for the write-up: carve-out wording in the same chunk is the only separator, and that is the thing UL-G7 to UL-G10 encode.

Gate-2 hard negatives for this category (`target_category == "Uncapped Liability"`, source category Cap On Liability, all five): see section 10 rows N1-N5. They score 0-2 under every variant, below 3, except GSV ("EXCEPT UNDER SECTIONS 13(a) AND 13(b), IN NO EVENT WILL EITHER PARTY BE LIABLE ...") which scores 2 and would fire at threshold 2. **INFERRED**: that GSV sentence is a real carve-out and would be a legitimate positive for any reader; the annotator labeled it only for Cap.

### 5b. Uncapped vs "not liable" (damages exclusion)

"Neither party shall be liable for consequential damages" is the most common Cap wording (Cap table, 171 of 432 Cap spans). The same sentence with an exception in front is Uncapped. Without a lead-in it is not (**VERIFIED**, scorer):
- Penntex "NO PARTY SHALL BE LIABLE FOR CONSEQUENTIAL, INCIDENTAL, PUNITIVE, EXEMPLARY OR INDIRECT DAMAGES ..." (an Uncapped span in train) scores 0 now and 1 after U2 (+1 "consequential"), below any useful threshold.
- Oasys, Verticalnet, Ipass (gate-2 hard negatives of this form) score 1 after U2.
- With a lead-in it scores 2-3: Duos "EXCEPT IN CONNECTION WITH A BREACH BY EITHER PARTY OF SECTION 8, NEITHER PARTY WILL BE LIABLE ..." 2, 2Themart 3, Playboy 4.

Cost, stated honestly: Penntex-style spans (a "not liable" sentence labeled Uncapped with no exception word in the span) are missed, and they exist (see section 7). The "except" signal also fires inside plain-cap chunks that hold an "except for fraud" sentence that the annotator did not label (112 of 515 at threshold 2, 10 of 515 at threshold 3).

## 6. Known near-misses and exclusions

| Pattern | What happens | Evidence |
|---|---|---|
| Entity definition "limited liability or unlimited liability company" | fires UL-G2-01 (+2) today; U1 removes it | 0 / 9 chunks |
| Plain cap + generic "except as otherwise expressly set forth" | counter -1 | Biofrontera N5 scores 0; 0 / 36 chunks |
| "Except for" carve-out outside a cap clause (insurance, termination, IP) | UL-G7 +1 only | 169 / 1,670 chunks overall (precision .09); cap context lifts it to .62-.79 |
| Standard "gross negligence or willful misconduct" carve-out | the intuitive evidence, but in cap chunks it is as common in negatives as positives (51 TP vs 34 FP inside "consequential" chunks, .60 vs base .39) | U4 retires UL-G3-01/02 and U5 demotes UL-G5-01; F1 +.033 and +.037; costs E6, E7, E12 (section 10) |
| Carve-out written as a bare fragment ("Except for claims under Sections 9.4 [INDEMNIFICATION BY IMPRESSE]") | scores 1 | E10 |
| Rare explicit wording ("shall be inapplicable", "excludes or limits", "no limitation") | only 3 chunks each, 1 contract each, zero false positives | U6, E8, E11 |
| Claim time bar with indemnification exception | scores 1 | Impresse E10 |

## 7. Known weak spots (be honest in the write-up)

1. **No strong anchor exists.** Only 11 of 115 spans (10%) contain the current anchor phrase and 68 of 78 contracts have no anchored span (**VERIFIED**, cat.py). After U1-U6 the only anchor group is UL-G2, whose phrases occur in 3 chunks each (9 chunks, 3 contracts at most). Detection depends on stacking seven supports; max score 9. This is the spec's "every category needs at least one anchor group" kept formally, not in practice.
2. **Best sim F1 is .684 but rests on one cap-context word.** Without UL-G6, F1 falls to .408. It counts a Cap-clause signal as Uncapped evidence, which is legitimate (95% overlap, section 5a) but means Uncapped will rise and fall with the Cap vocabulary.
3. **"gross negligence" / "willful misconduct" are retired from support though they are the textbook carve-out.** Reason: precision does not separate inside cap chunks (section 6). Real positives written mainly with those words lose their points (Fuelcell, Pareteum, Paratek, section 10). Optional edit (U4); Mahir's call.
4. **Annotator-tagged fragments** with no phrase (Impresse time bar, bare "Except for claims under ..." headings) are unreachable.
5. **Positives without any lead-in** ("NO PARTY SHALL BE LIABLE FOR CONSEQUENTIAL ... DAMAGES", Penntex; "Neither party shall be liable ... for any amounts representing loss of profit", Reagan 2) are labeled Uncapped but look like Cap text. They score 1-2.
6. **Annotation noise:** genuine carve-outs in chunks the annotator labeled Cap only (GSV, section 5a).
7. **Chunk overlap inflates counts about 3x** (e.g. "breach of confidentiality": 21 TP chunks from 7 contracts; "no limitation": 3 chunks from 1 contract); sim F1 is optimistic (threshold tuned on train) and is a bug check only. Greedy search across many candidate groups also over-fits train; the proposed groups were kept to ones with a stated reason, and low-support ones are flagged.

## 8. Train-only simulation (bug check, optimistic)

Approximate scorer (`sim.score`), 9,733 unmasked chunks (239 positive), best threshold by F1 over 1-8. **VERIFIED** by scratch runs; "current" reproduces the stock `sim.py` result .315 (th 1, 122 TP / 413 FP / 117 FN).

| Variant | Best F1 | Th | TP | FP | FN |
|---|---|---|---|---|---|
| current | .315 | 1 | 122 | 413 | 117 |
| U1 (retire "unlimited liability") | .319 | 1 | 122 | 404 | 117 |
| U1 + U2 (cap context, exception lead-in) | .559 | 2 | 185 | 238 | 54 |
| U1-U3 (+ confidentiality, section, other carve-outs) | .584 | 3 | 149 | 122 | 90 |
| U1-U4 (+ retire gross negligence / willful misconduct) | .647 | 3 | 140 | 54 | 99 |
| U1-U5 (+ demote "gross negligence or willful") | .684 | 3 | 135 | 21 | 104 |
| U1-U6 (+ explicit-wording anchors) | **.684** | 3 | 135 | 21 | 104 |

Single edits on the current rules: U1 .319, U2 .551 (th 2; 185 / 247 / 54), U3 .374, U4 .393, U5 .315, U6 .322. Leave-one-out from U1-U6 (.684): without U1 .684, without U2 .408 (th 2), without U3 .651 (th 2; 176 / 126 / 63), without U4 .651 (th 3; 149 / 70 / 90), without U5 .647, without U6 .684. So U2 is the big edit; U3, U4 and U5 add .03-.04 each; U1 and U6 are F1-neutral (U1 removes a rule that can only ever be wrong, U6 adds zero-false-positive anchors).

Other single checks used to choose the proposals (**VERIFIED**; basis stated):
- Candidate lead-ins added as one extra support group on the U1-U3 basis (.644 with the final structure minus UL-G11): "except as" .596 (2,401 FP chunks), "except to" .607, "notwithstanding" .584: **all lower**, not proposed. "third party claims" .652, "liability arising" .662, "direct damages" .658: +.01 to +.02 each, not proposed (small, vague).
- Damages-type words as another cap-context group: "incidental" .717, "lost profits | punitive | incidental" .712 (full-set basis .684). Higher F1, but the plain-cap fire rate at threshold 3 rises from 10 to 64-76 of 515 and the "neither" group from 10 to 13-19; this is double counting Cap vocabulary and is the opposite of separating the categories. **Rejected on the section 5a evidence**, not on F1.
- Anchor variants on the 8-group structure: "indemnification obligations" as anchor .609, "breach of confidentiality" group as anchor .622, section group as anchor .587, exception lead-in as anchor .636, all three specific groups as anchor .618 (th 4): none beats keeping them as support (.644). Anchor demotion of UL-G5-01 to support: .644 to .680 on that basis; dropping it instead: .649.
- Counter UL-G4-01 removed: no change.

Because the final threshold is chosen later on validation, these thresholds are not the ones that will be used. Max score is 9 after U1-U6, so thresholds 1-9 will be tried.

## 9. Proposed rule edits (NOT applied; need Mahir's OK)

IDs follow the existing convention (`UL-Gn-mm`); "U1..U6" are edit numbers, not rule IDs. Retired IDs are never reused. Edits that move a phrase retire the old ID and add a new one.

| ID | Change | Train evidence | Why | Sim F1 |
|---|---|---|---|---|
| U1 | **Retire UL-G2-01 "unlimited liability"** (ID never reused). UL-G2 keeps UL-G2-02 "uncapped" (0 train occurrences; category-name drafting variant) | 3 occurrences, all in "limited liability or unlimited liability company"; chunks 0 TP / 9 FP, 3 contracts | A rule that can only produce false positives. The anchor group stays because the spec requires one | .315 to .319 |
| U2 | New support groups **UL-G6** "cap context" (UL-G6-01 "consequential") and **UL-G7** "exception lead-in" (UL-G7-01 "except for", -02 "except in", -03 "except with", -04 "except under") | UL-G6: 55 spans, 207 TP / 320 FP chunks (recall .87). UL-G7: union 169 TP / 1,670 FP overall, but precision .62-.79 inside chunks that contain "consequential" (e.g. "except in" 50 / 14) | 95% of Uncapped chunks are Cap chunks; most spans start with an "EXCEPT ..." lead-in. Support only: neither alone is a good detector | .319 to .559 |
| U3 | New support groups **UL-G8** (UL-G8-01 "breach of confidentiality", -02 "confidentiality obligations"), **UL-G9** (UL-G9-01 "breach of section", -02 "breach of article", -03 "obligations under section") and **UL-G10** (UL-G10-01 "misappropriation", -02 "payment obligations") | unions 42 / 192, 73 / 184 and 42 / 360 chunks; inside cap chunks precision 1.00, .91 and .90 for "breach of confidentiality", "breach of section" and "misappropriation"; contracts 7 / 5, 13 / 17, 13 / 39 | Each is a named carve-out type, so each is its own group and adds +1 on top of the others (spec: same-meaning synonyms in one group, different evidence in different groups) | .559 to .584 |
| U4 | **Retire UL-G3-01 "gross negligence" and UL-G3-02 "willful misconduct"** (IDs never reused); UL-G3-03 "indemnification obligations" stays alone in UL-G3. (**Optional: Mahir's call**) | 56 / 201 and 62 / 271 chunks; inside cap chunks 51 / 34 and 57 / 33 (.60 and .63 vs base rate .39); 22 / 54 and 26 / 71 contracts | They are on 285+ negative chunks and, once cap context is separate evidence, add more false positives than true positives at threshold 3. Cost: real carve-outs that rely on these words alone drop (E6, E7, E12) | .584 to .647 |
| U5 | **Demote UL-G5-01 "gross negligence or willful" from anchor to support**: retire UL-G5-01, add **UL-G11-01** "gross negligence or willful" as support (ID never reused). (**Optional: Mahir's call**) | 11 spans, 31 / 81 chunks (precision .28, below the .48 that "indemnification obligations" has as a support); contracts 12 / 24 | The approved P7 note already says "precision 0.28, best available". Precision .28 does not meet the anchor bar, and as an anchor it fired on 81 negative chunks at +2 | .647 to .684 |
| U6 | **Add explicit-wording anchors to UL-G2**: UL-G2-03 "shall be inapplicable", UL-G2-04 "excludes or limits", UL-G2-05 "no limitation"; retire UL-G3-04 "no limitation" (ID never reused). (**Optional, low support: Mahir's call**) | each 3 / 0 chunks, 1 contract, 1 span; union 9 / 0 | These are exactly the "liability not limited" wording the category describes; zero false positives; gives the anchor group a phrase that appears in train. Same standing as P7's "no limitation" (approved, low support) | 0 (.684 to .684); E8 goes from 0 to 2, E11 from 2 to 4 |
| no edit | Keep UL-G4-01 (counter), UL-G3-03 (support), UL-G2-02 "uncapped" | section 3 | UL-G4-01 verified on train: 0 / 36 chunks, never subtracts from a positive | |

Candidates rejected: "except as", "except to", "notwithstanding" (lower F1), "incidental" / "punitive" / "lost profits" as a second cap-context group (higher F1 but plain-cap leak 10 to 64-76 of 515), "third party claims", "liability arising", "direct damages" (+.01 to +.02, vague), anchoring any of UL-G7 to UL-G9 (F1 down), any cap-wording counter ("exceed" 73 / 1,095), "unlimited" alone (0 / 78 chunks), "without limit" (110 / 2,666), "liability cap" (6 / 1 chunks, appears in "limitations or liability caps" waivers; too few to propose).

If U4 is declined, F1 is .651 (th 3; 149 / 70 / 90 after U1-U3, U5, U6). If U5 is declined, .647. If U4 and U5 are both declined, .584 (U1-U3 only). If U6 is declined, no F1 change. U2 is the one with real weight: without it .408.

## 10. Examples that exercise each branch

All from the 326 train contracts. Scores are from the approximate scratch scorer (`sim.score`, **VERIFIED** by running it, not by reading the text). Columns: "Now" = current rules; "+U2" = after U1+U2; "+U3" = U1-U3; "+U4" = U1-U4; "All" = U1-U6. Span rows score the full span text. G2 rows are gate-2 rows; the span score and the 600-character excerpt score are identical for all ten rows.

| ID | Branch | Source | Text (shortened) | Now | +U2 | +U3 | +U4 | All |
|---|---|---|---|---|---|---|---|---|
| E1 | Exception lead-in + cap context | Uncapped span, Cytodyn | "EXCEPT FOR A PARTY'S OBLIGATIONS SET FORTH IN THIS ARTICLE 13, AND ANY BREACH OF ARTICLE 10 (CONFIDENTIALITY), IN NO EVENT WILL EITHER PARTY BE LIABLE ..." | **0** | 2 | 3 | 3 | 3 |
| E2 | Lead-in + many carve-out types | Uncapped span, Energous | "EXCEPT IN THE CASE OF (a) ANY BREACH OF SECTION 10 (CONFIDENTIALITY), (b) THE PARTIES' OBLIGATIONS UNDER SECTION 12 (INDEMNIFICATION), (c) A PARTY'S GROSS NEGLIGENCE OR WILLFUL MISCONDUCT ..." | 3 | 5 | 6 | 5 | 4 |
| E3 | Waiver of caps, no phrase | Uncapped span, Nanophase | "Buyer, for itself and its insurers, expressly waives any and all limitations or liability caps ..." | **0** | 0 | 0 | 0 | 0 |
| E4 | "Not liable" without lead-in (section 5b) | Uncapped span, Penntex | "NO PARTY SHALL BE LIABLE FOR CONSEQUENTIAL, INCIDENTAL, PUNITIVE, EXEMPLARY OR INDIRECT DAMAGES, LOST PROFITS ..." | 0 | 1 | 1 | 1 | 1 |
| E5 | "Notwithstanding" + "liable" + carve-out | Uncapped span, ATN International | "Notwithstanding anything contained in this Agreement to the contrary, neither Party shall be liable to the other Party for any special, consequential, ..." | 1 | 2 | 4 | 4 | 4 |
| E6 | Explicit "without limit" (misconduct words only) | Uncapped span, Fuelcell | "Notwithstanding anything to the contrary in this Agreement, each Party will bear full responsibility, without limit, for the following: (i) Gross Negligence ..." | 3 | 3 | 3 | **2** | **1** |
| E7 | "Shall not apply" with willful misconduct | Uncapped span, Pareteum | "Limitation of liability as described in this article shall not apply: a) in case the damage or loss is caused by a Party's willful misconduct ..." | 1 | 1 | 1 | **0** | 0 |
| E8 | "Shall be inapplicable" (U6 target) | Uncapped span, Ediets | "THE LIMITATIONS ON LIABILITY FOR DAMAGES SET FORTH IN THIS AGREEMENT SHALL BE INAPPLICABLE TO EACH PARTY'S CONTRACTUAL OBLIGATION TO INDEMNIFY ..." | **0** | 0 | 0 | 0 | **2** |
| E9 | Stand-alone "nothing in this section" | Uncapped span, Aimmune | "NOTWITHSTANDING THE FOREGOING, NOTHING IN THIS SECTION 11.4 IS INTENDED TO OR SHALL LIMIT OR RESTRICT THE INDEMNIFICATION RIGHTS ..." | 0 | 0 | 1 | 1 | 1 |
| E10 | Bare fragment | Uncapped span, Impresse | "Except for claims under Sections 9.4 [INDEMNIFICATION BY IMPRESSE] and 9.5 [INDEMNIFICATION BY VERTICALNET]" | 0 | 1 | 1 | 1 | 1 |
| E11 | "There shall be no limitation" (U6 target) | Uncapped span, Xencor | "With the exception of wilful misconduct by a Party, ... for which cases there shall be no limitation, any and all liability ... shall be: a. excluded for incidental ..." | 1 | 2 | 2 | 2 | **4** |
| E12 | Carve-out written mostly with misconduct words | Uncapped span, Paratek | "For clarity, nothing in this Section 3.1 limits Supplier's liability under this Agreement or under law, including liability for negligence, willful misconduct ..." | 1 | 1 | 1 | **0** | 0 |
| E13 | Lead-in-free damages exclusion | Uncapped span, Reagan Holding | "Neither party shall be liable to the other pursuant to this Agreement for any amounts representing loss of profit ..." | 1 | 2 | 3 | 2 | 2 |
| E14 | Cap amount sentence (a cap, not a carve-out) | Uncapped span, Bellicum | "IN NO ONE EVENT SHALL EITHER PARTY'S AGGREGATE LIABILITY FOR DAMAGES OR LOSSES UNDER THIS AGREEMENT EXCEED THE ..." | 0 | 0 | 0 | 0 | 0 |
| P1 | Gate-2 positive | Duos Technologies | "EXCEPT IN CONNECTION WITH A BREACH BY EITHER PARTY OF SECTION 8, NEITHER PARTY WILL BE LIABLE ..." | 0 | 2 | 2 | 2 | 2 |
| P2 | Gate-2 positive | Remark Holdings | "EXCEPT FOR EITHER PARTY'S VIOLATION OF THE CONFIDENTIALITY OBLIGATIONS AND FOR EITHER PARTY'S INDEMNIFICATION OBLIGATIONS ..." | 1 | 3 | 4 | 4 | 4 |
| P3 | Gate-2 positive | Ideanomics | "EXCEPT FOR THE ABOVE INDEMNIFICATION OBLIGATIONS AND FOR BREACHES OF SECTION 14, NEITHER PARTY SHALL BE LIABLE ..." | 1 | 3 | 3 | 3 | 3 |
| P4 | Gate-2 positive | 2TheMart | "EXCEPT IN THE EVENT OF A BREACH OF SECTION 11, NEITHER PARTY SHALL BE LIABLE FOR SPECIAL, ..." | 0 | 2 | 3 | 3 | 3 |
| P5 | Gate-2 positive | Playboy Enterprises | "EXCEPT IN THE EVENT OF A BREACH OF SECTION 8 (CONFIDENTIALITY) OR LIABILITY ARISING UNDER ..." | 1 | 3 | 4 | 4 | 4 |
| N1 | Gate-2 hard negative (Cap only) | Oasys Mobile | "IN NO EVENT SHALL EITHER PARTY BE LIABLE FOR ANY INDIRECT, INCIDENTAL, SPECIAL OR CONSEQUENTIAL DAMAGES ..." | 0 | 1 | 1 | 1 | 1 |
| N2 | Gate-2 hard negative | Verticalnet | "TO THE MAXIMUM EXTENT PERMITTED BY LAW, IN NO EVENT SHALL EITHER PARTY BE LIABLE OR OBLIGATED ..." | 0 | 1 | 1 | 1 | 1 |
| N3 | Gate-2 hard negative, real-looking carve-out | GSV | "EXCEPT UNDER SECTIONS 13(a) AND 13(b), IN NO EVENT WILL EITHER PARTY BE LIABLE TO THE OTHER ..." | 0 | **2** | 2 | 2 | 2 |
| N4 | Gate-2 hard negative | Ipass | "NEITHER PARTY WILL BE LIABLE FOR ANY SPECIAL, INCIDENTAL, INDIRECT, EXEMPLARY, PUNITIVE, ..." | 0 | 1 | 1 | 1 | 1 |
| N5 | Gate-2 hard negative with the counter text | Biofrontera | "EXCEPT AS OTHERWISE EXPRESSLY SET FORTH IN THIS AGREEMENT, IN NO EVENT WILL EITHER PARTY BE LIABLE ..." | 0 | 0 | 0 | 0 | 0 |

Notes:
- E15 ("EXCEPT FOR THE ABOVE INDEMNIFICATION OBLIGATIONS ... Ideanomics") is the same row as P3 and is not repeated.
- N5 scores 0 because "except as otherwise expressly set forth" does not match the lead-in phrases and the counter fires (-1 to a floor of 0). "Except as" lead-ins are deliberately not added (section 8).
- N3 is the only gate-2 hard negative that reaches 2; with the best threshold expected at 3 on the proposed scale (INFERRED, from sim), none of the five fires, while P2, P3, P4, P5, E1, E2, E5 and E11 do.
- E6, E7 and E12 are the visible cost of U4 and U5 (real carve-outs written with only misconduct wording). They drop but E6 still scores 1.
- E3 (Nanophase "expressly waives any and all limitations or liability caps") has no matching phrase under any variant; "liability caps" would be the obvious candidate (6 / 1 chunks) and is listed as rejected for too few chunks.
- The scorer reads text; the dollar-amount form of a cap ("shall not exceed $X") is not a feature of this category.

## 11. Sources

- CUAD category description: `data/cuad/category_descriptions.csv`.
- Train spans: `data/splits/train.json` via `.agent/scratch/lib.py`.
- Gate-2 excerpts: `data/cuad/gate2_excerpt_review.csv`, `target_category == "Uncapped Liability"` (5 positive, 5 hard negative; all five hard negatives have source category Cap On Liability).
- Chunks and labels: `data/gate3/train_chunks_768_512.csv`, `train_chunk_labels_768_512.csv` (unmasked rows; 9,733 chunks, 239 positive; Cap x Uncapped table).
- Rule-level provenance: `configs/keyword_rules_v1.json` (categories["Uncapped Liability"], 8 rule IDs, P7 notes on UL-G5-01 and UL-G3-04).
- Cross-reference: `reports/keyword_baseline/decision_tables/cap_on_liability.md` (227 of 234 Uncapped chunks also Cap; no Cap counters).
- Scratch: `.agent/scratch/{lib,cat,cand2,sim}.py`; session experiment scripts in the session scratchpad (`ul.py` chunk-level phrase counter, `ul2`-`ul10` simulations; not part of the repo).
- Reviewer: not yet assigned.

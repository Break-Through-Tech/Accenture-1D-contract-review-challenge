# Decision table: Non-Transferable License

Rule set: `configs/keyword_rules_v1.json` (DRAFT, not frozen; 138 IDs after the License Grant edits). Evidence: the 326 train contracts only (`data/splits/train.json`, `data/gate3/train_*_768_512.csv`, `data/cuad/gate2_excerpt_review.csv`; no validation or test data used; `train_separate_questions.json` and `test.json` not opened).
Status: **APPROVED by Mahir 2026-10-16; N1-N3 (section 9) APPLIED to the JSON.** Rule set remains an unfrozen draft.
Claim labels: **VERIFIED** = seen in a cited source or scratch run on train; **INFERRED** = hypothesis.

## 1. Inclusion meaning

CUAD asks whether the contract limits the ability of a party to transfer the license being granted to a third party. In the labeled train data (**VERIFIED**, 210 spans in 90 contracts) positives are mostly the grant sentence that carries the restriction, not a separate clause:
- "Licensor hereby grants to Licensee ... an exclusive, non-transferable (except as set forth in Section 10.x) license ...";
- the same restriction written as "non-assignable", "non- sublicensable", "not otherwise sub-licensable", "without the right to sublicense", "shall not be transferable to any Third Party, except in connection with a merger";
- stand-alone restrictions on a licensee: "DIALOG may not sublicense the foregoing license rights to any other third party without ENERGOUS' prior written consent", "Customer shall not sell, lease, copy, distribute, transfer, assign or sublicense the Licensed Software";
- scope fragments tagged with the grant ("to make, have made, use, sell ...", "HSWI Websites).", "Business.").

Not included: a bare grant with no restriction (the five gate-2 hard negatives are License Grant sentences: Zogenix, Hospitality Investors, SFG, Ehave, iVillage), a general assignment ban on the whole agreement (Anti-Assignment), exclusivity.

Train support: 210 spans in 90 of 326 contracts (**VERIFIED**, Phase 1 table).

## 2. Evidence groups

Each group counts at most once per chunk. Anchor +2, support +1, counter -1, floor 0. Plain substring match on normalized text. NEW = proposed in section 9.

Columns: "spans" = how many of the 210 Non-Transferable License spans contain the phrase; "all-train occ." = substring count over all 326 contracts; "chunk TP / FP" = unmasked train chunks (9,713; **360 positive**, base rate 3.7%) that contain the phrase and are labeled positive / negative; "contracts" = distinct train contracts behind those TP / FP chunks (chunk overlap inflates chunk counts about 3x). All **VERIFIED** (scratch runs `cat.py`, `nt2.py`, `nt4.py`).

| Group | Role | Phrase (rule ID) | Spans | All-train occ. | Chunk TP / FP | Contracts TP / FP |
|---|---|---|---|---|---|---|
| NT-G1 non-transferable wording | anchor | non-transferable (01) | 84 | 94 | 178 / 12 | 47 / 4 |
| | | non- transferable (02) | 7 | 8 | 14 / 3 | 6 / 1 |
| | | nontransferable (03) | 25 | 27 | 46 / 3 | 16 / 1 |
| | | non-transferrable (04, NEW) | 3 | 3 | 8 / 0 | 3 / 0 |
| | | not transferable (05, NEW) | 1 | 1 | 3 / 0 | 1 / 0 |
| | | not be transferable (06, NEW) | 3 | 3 | 6 / 0 | 1 / 0 |
| NT-G2 cannot be sold or transferred | anchor | may not be sold or transferred (01) | 2 | 2 | 6 / 0 | 2 / 0 |
| | | non-assignable (02) | 18 | 20 | 37 / 6 | 11 / 2 |
| | | non- assignable (03, NEW) | 2 | 2 | 5 / 0 | 2 / 0 |
| | | nonassignable (04, NEW) | 1 | 1 | 3 / 0 | 1 / 0 |
| NT-G5 sublicense restriction (NEW) | anchor | non-sublicensable (01) | 17 | 17 | 33 / 0 | 11 / 0 |
| | | non-sub-licensable (02) | 5 | 5 | 11 / 0 | 2 / 0 |
| | | non-sublicenseable (03) | 10 | 10 | 23 / 0 | 4 / 0 |
| | | without the right to sublicense (04) | 8 | 9 | 17 / 0 | 6 / 0 |
| | | (union of the four) | | | 84 / 0 | |
| NT-G3 sublicense or assign restriction | support | sublicense (01) | 64 | 717 | 172 / 734 | 45 / 77 |
| NT-G4 freely transferable | counter | freely transferable (01) | 0 | 0 | 0 / 0 | 0 / 0 |

Maximum score now: anchors NT-G1, NT-G2 (4) + support NT-G3 (1) = **5**. After N1-N3: anchors NT-G1, NT-G2, NT-G5 (6) + support NT-G3 = **7**.

Why the anchor group works (**VERIFIED**): the three existing NT-G1 spellings are the strongest rules of the whole rule file at chunk level (precision .94, .82, .94) and dropping NT-G1-01 takes sim F1 from .783 to .420. This is the cleanest category in the project: a distinctive word does most of the work.

Why "sublicense" is only weak support: 172 TP vs 734 FP chunks (precision .19, base rate 3.7%). Dropping it changes F1 by 0 at the best threshold (.783; the best threshold moves from 2 to 1), so it stays as a harmless support (no edit).

## 3. Counterevidence and vetoes

- **NT-G4-01 "freely transferable" (counter, -1).** **VERIFIED**: 0 occurrences in all 326 train contracts, so it never fires on train and nothing can be said about it from train; removing it changes F1 by 0. Decision: **keep, no edit** (a drafting variant with rationale; it cannot hurt on train and the next-category check would catch it on validation).
- **Counters tested, all rejected** (**VERIFIED**, sim, current rules as baseline .783):

| Counter tried | Sim F1 | Verdict |
|---|---|---|
| affiliate (permitted transfer to affiliates) | .737 | rejected: removes 30 true positives |
| hereby assigns (ownership transfer) | .771 | rejected |
| not be assigned (Anti-Assignment wording) | .784 | +.001, 3 / 103 chunks, not worth a rule |
| shall not assign | .783 | no change (0 / 31 chunks) |
| transferable to | .783 | no change |

- **Vetoes:** none (chunk-wide design, no windows).

## 4. Context / proximity limits

None. All matching is chunk-wide (768 words, 512-word overlap). The restriction wording and the grant it modifies are usually in one sentence, so the 12 false-positive chunks for "non-transferable" (4 contracts) are mostly "non-transferable" in a different clause of the same chunk: a labeled grant elsewhere, a "non-transferable (except to permitted assigns)" that the annotator tagged with another category (Anti-Assignment N5 in that table).

## 5. Required confusion cases

### 5a. Non-Transferable License vs License Grant

Unmasked chunks labeled for both (**VERIFIED**):

| | NT = 0 | NT = 1 |
|---|---|---|
| License Grant = 0 | 8,788 | 54 |
| License Grant = 1 | 496 | 297 |

297 of the 351 chunks labeled Non-Transferable and unmasked for License Grant (85%) are also License Grant positives, but only 297 of 793 License Grant chunks (37%) are Non-Transferable. So License Grant evidence ("grants", "license to") is not evidence for this category: the rule file correctly has none. The five gate-2 hard negatives are License Grant sentences with no restriction; all five score 0 on span and excerpt now and after N1-N3 (Ehave's 600-character excerpt scores 1 from "sublicense"), see section 10. At threshold 2 the Non-Transferable rules fire on 19 of 8,788 chunks outside License Grant and on 4 of 496 License Grant positives that are Non-Transferable negatives; unchanged by N1-N3 (**VERIFIED**).

### 5b. Non-Transferable License vs Anti-Assignment / assignment wording

Anti-Assignment positives (**VERIFIED**): 41 of 355 Non-Transferable chunks (12%) are also Anti-Assignment positives; 735 AA chunks are Non-Transferable negatives. Assignment-ban wording is not Non-Transferable evidence: "shall not assign" appears in 0 positive and 31 negative chunks, "may not assign" in 1 and 61, "not be assigned" in 3 and 103, "not assign" in 4 and 127 (**VERIFIED**). Franchise "Transfer" sentences ("You shall not sell, assign, transfer, convey ... any direct or indirect interest in the Franchise", Airtech; labeled Non-Transferable) look like Anti-Assignment text and score 0 here, which is the price of keeping the two separate (E7). The Anti-Assignment table already scored the reverse direction (its N4, N5).

### 5c. Non-Transferable License vs ownership transfer

A "hereby assigns" counter lowers F1 (.783 to .771); ownership-transfer sentences are not a precision problem here (section 3). No rule.

## 6. Known near-misses and exclusions

| Pattern | What happens | Evidence |
|---|---|---|
| "non-transferable" in a different clause of the chunk than the labeled grant | anchor fires, labeled negative | 12 / 3 / 3 FP chunks for the three spellings, in 4 / 1 / 1 contracts |
| "non-transferable (except to permitted assigns)" tagged with another category | scores 2 | Anti-Assignment table N5 |
| Sublicense restriction written without a keyword ("may not sublicense ... without consent", "shall not sublicense") | scores 1 (NT-G3) | E1; "not sublicense" 16 / 20 chunks, "may not sublicense" 6 / 6: coin flip, not a rule |
| Passive restriction ("shall not be transferrable and/or sublicensable") | "shall not be transferrable" (misspelled, no "non-") matches none of the proposed phrases and scores 0 | E2 |
| Franchise "Transfer" sentences (no keyword) | 0 | E7 |
| License fragments ("HSWI Websites).", "Business.") | 0 | unavoidable |

## 7. Known weak spots (be honest in the write-up)

1. **Recall.** 95 of 360 positive chunks (26%) still score below 2 after N1-N3 (positives at score 0: 40, at 1: 55). They are sublicense and assignment restrictions without a distinctive keyword (E1, E2, E6, E7) and fragments.
2. **Anchor coverage:** 125 of 210 spans (60%) contain an anchor now, 134 after N1-N3; contracts with a span but none anchored: 23 now, 17 after (**VERIFIED**, cat.py).
3. **Several low-support edits.** N1 and N2 add phrases seen in 1-3 contracts each (zero false positives); they are spelling and wording variants, the same class as the approved P7 low-support notes.
4. **Chunk overlap inflates counts about 3x**; sim F1 is optimistic (threshold tuned on train) and is a bug check only. The sweep tried about 70 candidate phrases on train.

## 8. Train-only simulation (bug check, optimistic)

Approximate scorer (`sim.score`), 9,713 unmasked chunks (360 positive), best threshold by F1 over 1-9. **VERIFIED**; "current" reproduces the stock `sim.py` result .783 (th 2, 247 TP / 24 FP / 113 FN).

| Variant | Best F1 | Th | TP | FP | FN |
|---|---|---|---|---|---|
| current | .783 | 2 | 247 | 24 | 113 |
| N1 (spelling variants in NT-G1) | .804 | 2 | 258 | 24 | 102 |
| N1 + N2 (wording variants in NT-G2) | .807 | 2 | 260 | 24 | 100 |
| N1 + N2 + N3 (sublicense-restriction anchor) | **.817** | 2 | 265 | 24 | 95 |

Single edits on the current rules: N1 .804, N2 .787, N3 .796. Leave-one-out from N1-N3 (.817): without N1 .796 (254 / 24 / 106), without N2 .817 (no change; N2 only matters when N3 is absent), without N3 .807. N3 as a support group instead of an anchor: .811.

Drop one existing rule: NT-G1-01 .420, NT-G1-02 .775, NT-G1-03 .700, NT-G2-01 .771, NT-G2-02 .763, NT-G3-01 .783, NT-G4-01 .783. All the anchors are load-bearing.

Other single checks (**VERIFIED**, current rules as basis, added as one extra group): "transferable" as anchor .766 (chunk precision .76, 243 TP / 77 FP), as support .784; "non-exclusive|nonexclusive" as support .761 (th 3), as anchor .724; "royalty-free" .739 support / .687 anchor; "sublicensable" .782 / .778; "right to sublicense" .750; "not sublicense | may not sublicense | shall not sublicense" .771; "solely in connection | internal use" .773 / .696; "grants" as support .772 (th 3); "revocable" .744. None helps, all lower than the current rules or only +.001.

Because the final threshold is chosen later on validation, these thresholds are not the ones that will be used. Max score is 7 after N1-N3, so thresholds 1-7 will be tried.

Score distribution, proposed rules (unmasked chunks): negatives 0: 8,598; 1: 731; 2: 21; 3: 3. Positives 0: 40; 1: 55; 2: 110; 3: 56; 4: 32; 5: 57; 6: 6; 7: 4. Current rules: negatives 0: 8,598; 1: 731; 2: 21; 3: 3. Positives 0: 53; 1: 60; 2: 124; 3: 100; 4: 11; 5: 12. At threshold 2 the proposed rules fire on 24 negative chunks, the same 24 as the current rules.

## 9. Proposed rule edits (NOT applied; need Mahir's OK)

IDs follow the existing convention (`NT-Gn-mm`); "N1..N3" are edit numbers, not rule IDs. No IDs are retired by these edits.

| ID | Change | Train evidence | Why | Sim F1 |
|---|---|---|---|---|
| N1 | Add spelling and wording variants to anchor group NT-G1: **NT-G1-04** "non-transferrable", **NT-G1-05** "not transferable", **NT-G1-06** "not be transferable" | spans 3 / 1 / 3; chunks 8 / 0, 3 / 0, 6 / 0, union 17 / 0; contracts 3, 1, 1 | Same meaning as NT-G1-01 to -03 (misspelling and "not (be) transferable" forms); zero false positives. Low support, same standing as approved P7 low-support notes | .783 to .804 |
| N2 | Add to anchor group NT-G2: **NT-G2-03** "non- assignable", **NT-G2-04** "nonassignable". (**Optional, small: Mahir's call**) | spans 2 / 1; chunks 5 / 0 and 3 / 0, union 8 / 0; contracts 2 and 1 | Spacing and spelling variants of NT-G2-02 "non-assignable" (the extracted CUAD text has stray spaces after hyphens, as in NT-G1-02). Adds nothing once N3 is in (F1 unchanged) but fixes E13 | .804 to .807 |
| N3 | New anchor group **NT-G5** "sublicense restriction": NT-G5-01 "non-sublicensable", -02 "non-sub-licensable", -03 "non-sublicenseable", -04 "without the right to sublicense" | spans 17 / 5 / 10 / 8; chunks 33 / 0, 11 / 0, 23 / 0, 17 / 0, union 84 / 0; contracts 11, 2, 4, 6 | Restriction on onward sublicensing is a transfer limit in the CUAD sense and these phrases have zero false positives on 84 chunks; the best single new group | .807 to .817 |
| no edit | Keep NT-G1-01 to -03, NT-G2-01/02, NT-G3-01 and NT-G4-01 | section 2, section 3 | All anchors load-bearing; "sublicense" harmless; counter has 0 train occurrences | |

Candidates rejected: "transferable" (precision .76, 77 FP chunks), "royalty-free", "non-exclusive", "grants" (License Grant vocabulary, 85% overlap), "right to sublicense" (48 / 59 chunks), "not sublicense" family (coin flip), "assign" or "transfer" verbs (precision .06 and .11), "personal to", any counter (section 3).

If N2 is declined, the set is still .817 (N1 + N3). If N3 is declined, .807. N1 is the best single edit (.804).

## 10. Examples that exercise each branch

All from the 326 train contracts. Scores are from the approximate scratch scorer (`sim.score`, **VERIFIED** by running it, not by reading the text). Columns: "Now" = current rules; "+N1"; "+N1-2"; "All" = N1-N3. Span rows score the full span text. G2 rows are gate-2 rows (span / 600-character excerpt scores; identical except where shown).

| ID | Branch | Source | Text (shortened) | Now | +N1 | +N1-2 | All |
|---|---|---|---|---|---|---|---|
| P1 | Anchor in a grant, gate-2 positive | Leju Holdings | "Licensor hereby grants to Licensee ... an exclusive, non-transferable (except as set forth in Section 10.x) ..." | 2 | 2 | 2 | **4** |
| P2 | Gate-2 positive | Entrust | "... NTL ... hereby grants to Entrust ..." | 2 | 2 | **4** | 4 |
| P3 | Gate-2 positive, several restrictions | Playboy Enterprises | "Client grants EFS a limited, non-exclusive, non-transferable, non-assignable (without any right to sublicense) ..." | 5 | 5 | 5 | 5 |
| P4 | Gate-2 positive | TubeMedia | "Network hereby grants Affiliate during the Term a royalty-free, fully paid up, non-transferable, non-exclusive license ..." | 2 | 2 | 2 | 2 |
| P5 | Gate-2 positive | King Pharmaceuticals | "Depomed hereby grants to King a non-assignable, non- sublicensable, non-exclusive, royalty-free right and license ..." | 3 | 3 | 3 | 3 |
| E1 | Sublicense ban, no keyword | NT span, Energous | "DIALOG may not sublicense the foregoing license rights to any other third party without ENERGOUS' prior written consent." | 1 | 1 | 1 | 1 |
| E2 | Misspelled passive restriction | NT span, Cytodyn | "The licenses granted to Vyera under this Agreement shall not be transferrable and/or sublicensable without CytoDyn's written consent ..." | **0** | 0 | 0 | 0 |
| E3 | "shall not be transferable" (N1 target) | NT span, Rare Element | "Such rights to Joint Improvements shall be solely for use by the Company and shall not be transferable to any Third Party, except in connection with a merger ..." | 0 | 2 | 2 | 2 |
| E4 | "is not transferable" (N1 target) | NT span, Scansource | "Cisco's policy is that Software ... is not transferable, except where a listed exception below applies ..." | 0 | 2 | 2 | 2 |
| E5 | Misspelling "non-transferrable" (N1 target) | NT span, WebMD | "Such license is a non-exclusive, non-transferrable and worldwide license ..." | 0 | 2 | 2 | 2 |
| E6 | "non- assignable, non-sublicensable" (N2/N3 target) | NT span, iBio | "iBio hereby grants to CC-Pharming ... a nonexclusive, non- assignable, non-sublicensable, limited right and license ..." | 0 | 0 | 2 | **4** |
| E7 | Franchise "Transfer" sentence | NT span, Airtech | "You shall not sell, assign, transfer, convey, give away, mortgage or otherwise encumber any direct or indirect interest in the Franchise ..." | 0 | 0 | 0 | 0 |
| E8 | "non-sub-licensable" (N3 target) | NT span, Xencor | "XENCOR hereby grants to BII ... a non-exclusive, non-sub-licensable (except ...) ..." | 0 | 0 | 0 | **2** |
| E9 | Sublicense in a restrictions list | NT span, OFG Bancorp | "Customer shall not sell, lease, copy, distribute, transfer, assign or sublicense the Licensed Software to any third party." | 1 | 1 | 1 | 1 |
| E10 | Assign-ban without keyword | NT span, Moelis | "The rights granted under this Section 12.3 may not be assigned or transferred, except that such right is assignable by SMBC ..." | 0 | 0 | 0 | 0 |
| E11 | Fragment | NT spans, World Book / MLX ("HSWI Websites).", "Business.") | as shown | 0 | 0 | 0 | 0 |
| N1 | Gate-2 hard negative: License Grant | Zogenix | "Zogenix hereby grants to Distributor a non-exclusive, royalty-free, limited right under the Zogenix Trademarks ..." | 0 | 0 | 0 | 0 |
| N2 | Gate-2 hard negative | Hospitality Investors | "We grant to you and you accept a limited, non-exclusive License to use the Marks and the System ..." | 0 | 0 | 0 | 0 |
| N3 | Gate-2 hard negative | SFG Financial | "Licensor hereby ... grants to Licensee a non-exclusive license ..." | 0 | 0 | 0 | 0 |
| N4 | Gate-2 hard negative (excerpt scores 1) | Ehave | "CHT hereby grants to Ehave a non-exclusive, royalty-free, revocable, limited license ..." | 0 (excerpt 1) | 0 (1) | 0 (1) | 0 (1) |
| N5 | Gate-2 hard negative | iVillage | "FMM grants to iVillage ... a royalty-free, non-exclusive, worldwide license ..." | 0 | 0 | 0 | 0 |

Notes:
- The "NT span" rows use the 210 train spans labeled Non-Transferable License. E1, E2, E7, E9, E10, E11 are the unreachable class (no distinctive keyword) and score 0-1 under every variant.
- None of the five gate-2 hard negatives (License Grant sentences with no restriction) reaches 2 under any variant; the proposed edits do not add false positives on them or on train (24 false-positive chunks at threshold 2, unchanged).
- E3, E4, E5, E6, E8 and P1, P2 are where N1-N3 earn their gain.

## 11. Sources

- CUAD category description: `data/cuad/category_descriptions.csv`.
- Train spans: `data/splits/train.json` via `.agent/scratch/lib.py`.
- Gate-2 excerpts: `data/cuad/gate2_excerpt_review.csv`, `target_category == "Non-Transferable License"` (5 positive, 5 hard negative; all hard negatives have source category License Grant).
- Chunks and labels: `data/gate3/train_chunks_768_512.csv`, `train_chunk_labels_768_512.csv` (unmasked rows; 9,713 chunks, 360 positive; License Grant and Anti-Assignment co-occurrence tables).
- Rule-level provenance: `configs/keyword_rules_v1.json` (categories["Non-Transferable License"], 7 rule IDs).
- Cross-references: `license_grant.md` section 5c; `anti_assignment.md` N4, N5.
- Scratch: `.agent/scratch/{lib,cat,cand2,sim}.py`; session experiment scripts in the session scratchpad (`gen.py` harness, `nt1`-`nt4`; not part of the repo).
- Reviewer: not yet assigned.

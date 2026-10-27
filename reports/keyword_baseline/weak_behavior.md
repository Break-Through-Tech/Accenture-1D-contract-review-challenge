# Keyword baseline: weak behavior write-up (Phase 9)

Rules: `configs/keyword_rules_v1.json`, frozen in commit `227b133` (SHA-256 `07602f34…7e3`). Thresholds: `configs/keyword_thresholds_v1.json`. Scores: `reports/keyword_baseline/validation_predictions.csv`. **No rule was changed after seeing validation results**; this document only describes behavior. Anything below that sounds like a fix is a note for the next model or rule version, not an edit.

Claim labels: **VERIFIED** = counted from `validation_predictions.csv` joined to `validation_chunk_labels_768_512.csv` (unmasked pairs, chosen threshold) by a scratch analysis script (not committed); **INFERRED** = hypothesis from reading the examples.

Terms: *TP/FP/FN* = true positive, false positive, false negative chunk-category pairs. A "chunk" is a 768-token window that overlaps its neighbours by 512 tokens, so the same clause often appears in two or three chunks and is counted once per chunk (**VERIFIED**: several example rows below are duplicates). Because of that, a few contracts can account for many errors (**INFERRED**: e.g. the repeated CERES/IGER and XSPA/Calm boilerplate).

## Results at a glance

| Category | Th | P | R | F1 | Positives (chunks / contracts) | Main problem |
|---|---|---|---|---|---|---|
| Non-Transferable License | 2 | .963 | .865 | .911 | 89 / 26 | Few misses; short "no right to" fragments |
| Anti-Assignment | 2 | .793 | .779 | .786 | 217 / 67 | Misses clauses worded "no assignment", "transfer", "subcontract" |
| License Grant | 3 | .843 | .701 | .765 | 207 / 41 | Warranty / "right to use" wording; misses reach score 2 |
| Renewal Term | 1 | .797 | .705 | .748 | 78 / 31 | All 23 misses score 0 (paraphrases) |
| Cap On Liability | 2 | .879 | .603 | .715 | 229 / 50 | 63 of 91 misses score 0 |
| Expiration Date | 3 | .839 | .599 | .699 | 192 / 71 | Date-only and table fragments |
| Uncapped Liability | 3 | .821 | .485 | .610 | 66 / **20** | Carve-out clauses stop at 2; low support |
| Exclusivity | 3 | .525 | .622 | .569 | 119 / 31 | Every anchor hit is also an FP |
| Non-Compete | 2 | .429 | .542 | .479 | 72 / **19** | Bans without "compete"; low support |
| Change Of Control | 2 | .336 | .671 | .448 | 73 / **19** | Termination and assignment text scores 2; low support |

Macro-F1 .673, micro-F1 .690 (**VERIFIED**, `validation_metrics.csv`). Low-support warning: Non-Compete, Change Of Control (19 positive contracts each) and Uncapped Liability (20) have too few validation contracts for a stable F1; treat their scores as noisy (**INFERRED** from the <20 context-group guidance in the plan; `validation_metrics.csv` flags only on chunk count, so it shows False for all).

Global pattern (**VERIFIED**): errors are mostly shortfalls of recall (categories where most FNs score 0 or 1) or category overlap (FPs that are real clauses of a neighbouring category: for example 29 of Change Of Control's 97 FPs are Anti-Assignment chunks). The same sentence is often legitimately labeled with more than one category, so some "false positives" are label overlap rather than wrong behavior.

## Per-category notes

### Anti-Assignment (F1 .786)
- **Works:** the strongest anchors fire reliably and rarely on negatives. AA-G6 "without such consent / purported assignment / shall be void" fires on 46 TPs and 2 FPs; AA-G7 "assign this agreement / its rights / any" on 95 TPs and 14 FPs (**VERIFIED**).
- **False positives (44):** IP-assignment sentences that use "assign" ("shall assign its rights ... in any such invention"), a membership-interest transfer, a consultant "will not assign the responsibilities", and a signed-copies heading "Assignment / Subcontracts" (**VERIFIED**, examples). Only 5 co-labeled License Grant, 3 Non-Compete, 3 Non-Transferable License; most FPs are plain boilerplate.
- **False negatives (48):** 37 score 1 and 11 score 0. Phrasings the rules do not cover: "No assignment by either Party ... or delegation of any duties ... shall be binding", "Neither you nor any of the Owners may make any Transfer", "shall not sell or otherwise transfer any of the rights", "may not be waived, amended or assigned", "will not subcontract" (**VERIFIED**).
- **Missed paraphrases:** noun-form "assignment" and "Transfer" as defined terms; "subcontract"; "delegation".

### Cap On Liability (F1 .715)
- **Works:** precision .88. CL-G1 anchor "shall not exceed" family: 41 TPs, 5 FPs; CL-G6/CL-G7 fire 61/73 times on positives and 1/3 on negatives.
- **False positives (19):** the "Limitation on Remedies / arbitrators ... punitive or exemplary damages" clause from one arbitration boilerplate (repeated across chunks), plain consequential-damages waivers, and a definition ("Maximum Liability" means the Portfolio Residual Value). Several FPs share the support set CL-G2/G3/G8 ("consequential", "punitive", "in no event"); the count was not tallied (**VERIFIED** only for the sampled rows).
- **False negatives (91):** 63 score 0, 28 score 1. Examples: a reimbursement-gross-up clause, "Warranty Period ... ninety days", "sole and exclusive remedy ... refund of all fees", and dollar-cap sentences like "AJR's liability under this Section 11 shall not exceed One Hundred Fifty Thousand Dollars" which score only 1 because the cap phrases are split across "under this Section" and the dollar amount (**VERIFIED**; the last as a rule gap, **INFERRED** cause).
- **Missed paraphrases:** "sole and exclusive remedy", "refund of fees paid", "reimburse ... costs", bracketed redactions "[ * ]".

### Change Of Control (F1 .448)
- **Works:** the anchors CC-G1 and CC-G7 catch the explicit "change of control" and ownership-change clauses (CC-G7: 3 TP, 0 FP).
- **False positives (97):** precision .34. CC-G3 (merger/acquisition-type support) fires on 78 FPs and 9 TPs. Scores are 2 for 53 of the 97 FPs. Typical: assignment-on-merger permissions ("either party may assign ... in the event of a merger, acquisition ... change in control"), termination clauses about insolvency or cessation of activities, and definitions of "Operator Change of Control". 29 FPs are Anti-Assignment chunks and 14 Expiration Date chunks, so the overlap with those categories is the main cause (**VERIFIED**).
- **False negatives (24):** 18 score 1, 6 score 0. Examples: "nothing ... shall restrict any change in shareholding or control", "any merger, consolidation or reorganization ... will be deemed to be a transfer", a liquidity-event fee clause, and "assigns ... by operation of law, merger".
- **Why weak:** change-of-control language in CUAD labels is a small slice of assignment and termination text; the baseline cannot tell "may assign on merger" (labeled Change Of Control in some contracts, not others) from a restriction. **INFERRED**.
- **Low support:** 19 positive contracts.

### Exclusivity (F1 .569)
- **Works:** recall .62 using a single anchor family; the "non-exclusive" vetoes are in place (on the train gate-2 hard negatives none reached the threshold; not re-checked on validation).
- **False positives (67):** all 67 FPs have the anchor EX-G1 and the bare "exclusive" support, so every FP is "exclusive" in boilerplate: the title "EXCLUSIVE DISTRIBUTOR AGREEMENT", "exclusive right to control and settle any claim", "Sole and Exclusive Remedies", "CERES will exclusively own plants ...", "shall remain exclusively with Licensor". Co-labels: 10 License Grant, 8 Expiration Date, 5 Anti-Assignment, 5 Cap On Liability (**VERIFIED**).
- **False negatives (45):** 8 score 0, 18 score 1, 19 score 2. Examples: "Breach the exclusivity agreement ... engage in competing business", "shall not enable another program sponsorship for all competitive products", "sole and exclusive worldwide right and license" (score 1 because "an exclusive" is not in the text), "the exclusive provider on the ACSI Site".
- **Overlap:** 10 of the 45 FNs are Non-Compete chunks; 10 are License Grant. Many "exclusive license" grants are legitimately both (**VERIFIED**).

### Expiration Date (F1 .699)
- **Works:** precision .84. ED-G7 commencement and ED-G8 early-termination anchors fire on 71 and 81 TPs with 8 and 9 FPs.
- **False positives (22):** "Initial Term" in a requirements-percentage clause, a warrant "shall expire", prices that "shall remain in effect ... during the Initial Term", and the same "The Term shall commence and end on the dates set forth in the Agreement Summary, unless terminated earlier" sponsorship clause appearing twice (overlapping chunks).
- **False negatives (77):** 36 score 0, 26 score 1, 15 score 2. 25 are also Renewal Term chunks. Missed forms: date ranges or bare dates ("April 15, 2000 through October 15, 2000", "Contract end: 04-01-08"), "shall not be terminable or revocable", "Term: twelve (12) months from the date of the Agreement which term shall automatically renew", "effective until the earlier of (a) ... (b) the date that is two (2) years after".
- **Missed paraphrases:** "Term:" table rows and dates without any of the rule phrases; "effective until the earlier of".

### License Grant (F1 .765)
- **Works:** LG-G1 "grants" and LG-G2 "license under" are the main anchors, firing on 128 and 109 TPs.
- **False positives (27):** warranties and "grant the rights and licenses it grants hereunder", "neither party grants the other the right to use its trademarks", a definition of an intercompany license ("a licensor Party grants or purports to grant"), and "shall have the right to use photographs" (**VERIFIED**).
- **False negatives (62):** 12 score 0, 19 score 1, 31 score 2. Gaps: "Eutectix shall grant Liquidmetal a license" (no anchor), "authorizes the other party to display and use the other's trademarks", non-exclusive sublicense rights, and a long sentence "grants to Licensee an exclusive (even as to Bioeq) ... license" where the grant words are present but group credit stops at 2 (**VERIFIED**; cause **INFERRED**). 13 of the 62 FNs are Non-Transferable License chunks.

### Non-Compete (F1 .479)
- **Works:** NC-G1 "not compete" is nearly clean (9 TP, 1 FP); NC-G6 "competitive with / competing product" fires on 20 TPs and 11 FPs.
- **False positives (52):** precision .43. Most are the word "competitor" in confidentiality or neutrality text: "shall not disclose any confidential information to any competitor of the disclosing party", an arbitrator "shall not ... have been affiliated with a competitor of any Party", "No marketing exclusivity ... with respect to any competitors of Sponsor is conferred". NC-G7 "competitor" and NC-G10 "any competitor" account for 31 and 25 FPs (**VERIFIED**).
- **False negatives (33):** 18 score 0, 15 score 1. Missed examples: "agrees not to enter into any form of cooperation with Qihoo 360", "shall be prohibited from acquiring the technology/company either directly or indirectly", "neither Party shall ... directly or indirectly, Commercialize, or Develop any New Product", "agrees not to provide the Software ... to the following companies", "advertise or market ... outside of the Delivery/Catering and Advertising Area". 9 FNs are Exclusivity chunks, 6 each Non-Transferable License and Renewal Term.
- **Missed paraphrases:** bans stated by action and counterparty name without "compete/competitor" (a keyword baseline cannot see these; **INFERRED** ceiling).
- **Low support:** 19 positive contracts.

### Non-Transferable License (F1 .911)
- **Works:** the best category: precision .96, recall .87. The sublicense-restriction anchor NT-G5 fires 17 times with 0 FPs; NT-G1 65 TPs, 3 FPs.
- **False positives (3):** all three are a table of contents or a recital that lists "Sublicense Agreement" and "right to market and sublicense" (**VERIFIED**).
- **False negatives (12):** 8 score 0. Examples: trademark use "solely and exclusively as a component", "neither party shall have the right to use ... the name, brand names, trademarks ... without prior written consent", "You have no right to sublicense", and "Party A shall not assign to any third party the functions and contents" (two copies, a cooperation agreement). 9 of 12 are also License Grant; 6 Non-Compete.

### Renewal Term (F1 .748)
- **Works:** precision .80 with threshold 1. RT-G1 renewal anchors fire on 45 TPs and 9 FPs.
- **False positives (14):** "additional one (1) month period" for retained statistics, "automatically extended" support period, and a definition ("Term" shall mean an initial term of five years, automatically renewable ...). 6 of the 14 are also Expiration Date chunks.
- **False negatives (23):** all 23 score 0. The wording is: "Upon expiry of the Initial Term, this Agreement [*****] unless a Notice of non-renewal is given", "The term of this Agreement may be extended for an additional two year period with the written consent of both parties", "the parties may further negotiate the cooperation forms" (**VERIFIED**). 18 of the 23 FNs are Expiration Date chunks.
- **Missed paraphrases:** "may be extended for an additional ... period", "notice of non-renewal", "upon expiry ... [redacted]".

### Uncapped Liability (F1 .610)
- **Works:** precision .82. The group family UL-G6/G7/G9 ("except for", "consequential", exclusions) fires on 29/27/25 TPs.
- **False positives (7):** the exclusion carve-out wording in clauses that are really caps and indemnity or insurance (the same indemnification-except sentence appears twice), plus "Customer shall have the exclusive obligation". 7 of 7 co-labeled Cap On Liability.
- **False negatives (34):** 22 score 2, 8 score 1, 4 score 0. These are the actual carve-out sentences ("this Section shall neither (a) apply to ... ", "EXCEPT FOR LIABILITY ARISING UNDER SECTIONS ...", "NONE OF THE FOREGOING LIMITATIONS ... SHALL BE AVAILABLE ... BREACH OF CONFIDENTIAL INFORMATION"). Most score 2 because they contain consequential-damages wording but no distinctive carve-out anchor. 31 of 34 are Cap On Liability chunks, matching the train finding that 227 of 239 Uncapped chunks are also Cap.
- **Low support:** 20 positive contracts.

## Cross-cutting observations (all **VERIFIED** unless stated)

1. **Overlap with neighbouring categories** explains much of the FP side: Change Of Control vs Anti-Assignment (29 chunks), Uncapped vs Cap On Liability (7 of 7), Renewal Term vs Expiration Date (18 of 23 Renewal FNs, 25 of 77 Expiration FNs).
2. **Redacted text** (`[***]`, `[ * ]`, `[*****]`) hides the number or word the rules would otherwise use; several FNs for Cap and Renewal contain it.
3. **Repeated clauses across overlapping chunks** inflate counts and make a few contracts dominate errors (CERES/IGER, XSPA/Calm).
4. **A keyword baseline cannot read negation or counterparty scope** ("shall not ... enter into any form of cooperation with <named company>"); this is the expected ceiling and the reason to compare against TF-IDF + LinearSVC and the transformer. **INFERRED**.

## Notes for later versions (not applied; need a new rule-set version and train-only evidence)

- Treat these as hypotheses to test on train, not as validation-derived edits: noun-form "assignment/transfer/subcontract" for Anti-Assignment; "sole and exclusive remedy"/dollar-amount caps for Cap On Liability; "may be extended", "notice of non-renewal" for Renewal Term; "Term:" and date-range rows for Expiration Date; counterparty-named bans for Non-Compete.
- Because these were found by reading validation errors, using them directly would leak validation into the rules. Any change should be re-derived from the 326 train contracts or the next data split.

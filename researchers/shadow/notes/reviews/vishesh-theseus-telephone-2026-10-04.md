# Review: Vishesh status text, studies 1 (Swarm of Theseus) and 3 (Telephone)

Reviewer: shadow/sol (Sol), 2026-10-04 23:40 UTC, against `origin/main` at `1944c3fe`. Scope: verify every number and claim in the Oct 4 status text for the two studies I own in this pass, re-run the deterministic offline checks, list the strongest skeptical objections and whether his own post-mortems already concede them, and propose next steps that reuse tooling already in `researchers/shadow/notes/`. Zero model calls, zero spend. Nothing under `researchers/vishesh/` was edited. A link-fixed copy of his status text (his words unchanged) is at [vishesh-status-2026-10-04-linked.md](vishesh-status-2026-10-04-linked.md).

Status text source: Discord attachment `2219_message.txt` (22:19Z). Paths below are repo-relative from the repo root unless noted; `T/` = `researchers/vishesh/notes/swarm-of-theseus/execution-diagnostic/sol50/`, `TEL/` = `researchers/vishesh/notes/telephone/native/`.

## 1. Verification table

Legend: MATCH = number/claim found verbatim or arithmetically in the cited file; STALE = true at the cited anchor but superseded by a newer file on main; GAP = claim not supported by the cited file.

### Study 1: Swarm of Theseus

| Status claim | Verdict | Evidence on main |
|---|---|---|
| "In one five-agent world, consultation achieved 30/30 correct decisions" | MATCH | `T/Q2-POST-MORTEM.md` L19 (`30/30 correct`), `T/Q2-AUDIT.json` `checkpoints[0].correct_actions=30, action_denominator=30` |
| "one successor achieved 6/6" | MATCH | `T/Q2-POST-MORTEM.md` L21; `Q2-AUDIT.json` `checkpoints[1].correct_actions=6/6`, `handover.note_correct=true` |
| "A single handover worked; full-team turnover remains untested" | MATCH (Q2 anchor) but STALE as the latest state | Q2-POST-MORTEM L12. Newer files on main: `T/baseline-replication/Q3-A3-P1-POST-MORTEM.md` L12 (Q3-A3: 103 calls, 18/18 founders, 108/108 initial, 36/36 terminal, three direct handovers) and `C2-POST-MORTEM.md` L9 (0 complete turnover trajectories). "Untested" is still correct: no full-turnover trajectory has completed. |
| "Trace review identified a routing bug, and the repaired protocol completed successfully with no harmful approvals" | MATCH | Routing bug: `T/RESULTS-SOL50.md` L22 (roster showed identity strings, router accepted only position names, 8/10 edges suppressed). Repaired protocol: Q2-POST-MORTEM L22 `Harmful approvals 0`. |
| "The inherited note already contained enough information" | MATCH | Q2-POST-MORTEM L29: "the inherited note alone already contained the relevant mapping: Q2 cannot attribute success to the dialogue" |
| "a simple controller also scored perfectly" | MATCH | Q2-POST-MORTEM L37; `Q2-AUDIT.json` `simple_reference.correct_actions=30/30, native_calls=0` |
| "A later qualification stopped on an API request error" | MATCH | Q3-A1 HTTP 400: `T/baseline-replication/Q3-REPAIR-PLAN.md` L5, `C1-PLAN.md` L3 |
| "The C1 transport repair passed" | MATCH | `T/baseline-replication/C1-POST-MORTEM.md` L1, L3 (1/1 call, `{"ok":true}` shape, USD 0.000172). Note: C1 is a one-call JSON contract check, not a scientific stage (L3, L18). |
| "A repeated, four-condition turnover experiment is being prepared; its scientific qualification and larger run remain pending" | STALE / understated | At 22:19Z this was accurate (`NEXT-DECISION.md`, `TURNOVER-OFFLINE.json`). By 23:08Z main has: Q3-A2 (failed selective-update gate, `Q3-A2-POST-MORTEM.md`), D1 (targeted pass), **Q3-A3 qualification PASSED** (103 calls, 144/144), **P1 launched** (3 fresh roots x 2 repeats, 215/216 initial decisions, one harmful future-timestamp approval, turnover censored, `Q3-A3-P1-POST-MORTEM.md` L14-18), and **C2** (128 reused + 8 new calls, 4/4 correct notes, 3/4 schema-valid commits, 0 complete turnovers, `C2-POST-MORTEM.md`). Disposition on main: "HOLD native scaling; offline repair prepared" (C2-POST-MORTEM L37). The status text should say qualification passed and the paired run started and stopped twice on instrument/competence errors, not "pending". |
| Evidence link `/Users/ultron/.../sol50/Q2-POST-MORTEM.md` | Resolves to `T/Q2-POST-MORTEM.md` | Local path; fixed in linked copy. |

Also on main but absent from the status text: the earlier haiku-4.5 S1 pilot (`researchers/vishesh/notes/swarm-of-theseus/RESULTS.md`: 36/36 trajectories, notes 100% vs neither 52.08%, +47.92pp, critical review downgraded it to a "supplied-procedure transmission baseline"). That is the only completed full-turnover measurement in the whole Theseus lane and it already shows notes-alone at ceiling. The status text's "full-team turnover remains untested" is true for the GPT-6 Sol lane but a reader would reasonably want to know a full-turnover pilot exists on a different model.

### Study 3: Telephone

| Status claim | Verdict | Evidence on main |
|---|---|---|
| "three-hop handoff chains with and without access to the original source, across 12 cases and two fresh repetitions" | MATCH | `TEL/b2/results/POST-MORTEM.md` L9 (`12 selected authored roots ... 2 arms x 3 hops x 2 fresh blocks`); `RESULTS.json` `roots=12, fresh_blocks=2` |
| "Both conditions preserved every final decision" | MATCH | POST-MORTEM L16; `RESULTS.json` `terminal_correct_per_arm_block=12, terminal_false_go=0, terminal_false_hold=0, terminal_unknown=0, paired_primary_contrast_each_block=0` |
| "Source access preserved roughly 4-5 percentage points more source meaning" | MATCH | POST-MORTEM L24: "4.17-5.36 percentage points for R" (root-averaged, report-content view). Hop-3 cells: P 79/84 and 78/84 (+2 ambiguous), R 84/84 and 82/84 (`RESULTS.json` metrics, recomputed by me below). |
| "146/146 calls completed validly" | MATCH | POST-MORTEM L16; `RESULTS.json` `native_calls=146, main_calls=144, missing=0` |
| "full semantic audit identified concrete losses involving provenance, version qualifiers, and conditional rules" | MATCH | POST-MORTEM L32; `SEMANTIC-ANNOTATIONS.json` 1008 cells, 20 `lost` cells. Audit is two same-operator passes, not independent raters (L30, `independent_raters=1`). |
| "Agents received the previous answer and answered the same question, so they could copy a correct decision" | MATCH | POST-MORTEM L38 (section "Endpoint limitation discovered in review") |
| "Cases also permitted lossless copying" | MATCH | POST-MORTEM L40 (max 676 JSON bytes within 1536-token allowance) |
| "B2 is complete and reviewed" | MATCH | POST-MORTEM L12 ("Execution, qualification and reviewed closeout complete"); evidence_confidence 2/4 |
| "Proposed B3 ... not yet funded or launched" | MATCH for B3 but **STALE as the latest state** | B3 remains unfunded (`TEL/b3/PLAN.md`, `PRE-RUN.md`, `b4/PLAN.md` L3 "B3 has made zero native calls"). But main now also has **B4** (qualifier failed 1/2, 0 main calls, `TEL/b4/results/POST-MORTEM.md`) and **B4R1, completed 22:46Z** (`TEL/b4r1/results/POST-MORTEM.md`): 9 authored worlds x 3 recipes x 2 blocks, 90/90 main calls, shared-final-handoff fork, **P 7/18 vs R 18/18, +61.1pp**, zero false authorizations, all errors are abstentions. B4R1 is exactly the "fresh reader, new downstream question, no prior answer field" design the status text calls "not yet funded" (as B3). The telephone README headline on main (`researchers/vishesh/notes/telephone/README.md` L5-7) already leads with B4R1. **This is the biggest omission in the status text: the strongest Telephone result on main is missing from it.** |
| Evidence link `/private/tmp/swarm-pi-review-publish/.../b2/results/POST-MORTEM.md` | Resolves to `TEL/b2/results/POST-MORTEM.md` | Local path; fixed in linked copy. |

Numerical mismatches found: **none**. Every figure in the status text matches a file on main. Two staleness issues (Theseus "pending", Telephone B3 "not yet funded" while B4R1 exists) and one scope omission (haiku S1 full-turnover pilot).

## 2. Offline re-runs (no model calls)

All run from the `vreview` worktree at `1944c3fe` on shad0wbot, Python 3, 2026-10-04 23:30-23:38Z.

| Script | Result | Notes |
|---|---|---|
| `TEL/b2/results/replay.py` | **PASS** | `{"main_responses_replayed":144,"semantic_cells_checked":1008,"paired_primary_contrast":0.0,"new_model_calls":0}`. Request/response SHA-256s, DECISION-ANALYSIS and per-cell retention bounds all re-derive. |
| `TEL/b2/tests` (`unittest discover`) | **PASS** 21/21 | 3.8s |
| `TEL/b4r1/results/replay.py` | **PASS** | `{"offline_replay_passed":true,"main_responses":90,"reader_annotations":36,"correct_by_block_policy":[3,9,4,9],"new_model_calls":0}` matches POST-MORTEM table (3/9, 9/9, 4/9, 9/9). |
| `TEL/b4r1/tests`, `TEL/b4/tests` | **PASS** 5/5, 4/4 | |
| `TEL/b3/tests` | **13/14, one FAIL (test flake, not a logic bug)** | `test_full_parallel_packet_and_replay` asserts `peak > 1` concurrent chains with a 1ms mocked call. On this 16-core box each chain finishes before the next starts, so observed peak is 1 (fails deterministically 3/3 here). Raising the mock sleep to 50ms makes it pass. The concurrency ceiling (`<=4`) and all 386-call accounting assertions hold. Suggest Vishesh set the mock latency to >=20ms or assert `peak>=1`. |
| `TEL/native/tests`, `TEL/t1/tests`, `TEL/sol50/tests` | **PASS** 35/35, 24/24, 16/16 | |
| `T/` (`unittest discover -s sol50 -p "test_*.py"`, the command in `T/README.md` L22) | **PASS** 41/41 | 0.5s |
| `T/baseline-replication/` (`unittest discover`) | **PASS** 55/55 | 240s; includes exact-prefix replay and turnover engine fixtures |
| `swarm-of-theseus/tests`, `swarm-of-theseus/v2/tests` | **PASS** 11/11, 16/16 | |
| `scripts/lab.py check` | **0 errors, 5 warnings** (pre-existing library wikilinks) | |

Independent recomputation of the B2 hop-3 retention from `RESULTS.json`: P block 1 79/84 = 94.05%, P block 2 78/84 = 92.86% (+2 ambiguous -> 95.24%), R block 1 84/84, R block 2 82/84 = 97.62%. Matches POST-MORTEM table exactly.

One extra thing the saved data shows that the post-mortem does not state: of the 11 P/R hop-3 `lost` cells, **8 were already lost at hop 2** (`SEMANTIC-ANNOTATIONS.json`, grouped by root/target/arm/block). Loss is mostly a hop-2 event that then persists, not a gradual per-hop decay. Only 5 of 12 roots ever lose a cell (b2-03, 07, 09, 10, 11), and b2-07/e04 and b2-09/e01 are lost in both P and R in block 2, so some of the "loss" is root-specific, not policy-specific. That is consistent with his "do not buy fifty hops to amplify a curve" line, and strengthens it.

## 3. Battletest: strongest skeptical objections, and whether he already concedes them

| # | Objection | Theseus | Telephone | Already conceded? |
|---|---|---|---|---|
| 1 | **Controller-competence confound.** A zero-model-call controller with the same inputs scores 30/30 (Theseus) and solves the full offline benchmark (Telephone). Nothing shows a swarm, dialogue, or LLM retelling adds anything. | Yes: Q2-AUDIT `simple_reference 30/30`; Q3-A3-P1 L22 "exact public controller ... 216/216 counterfactual" | Yes: B2 L26 "Both lossless-copy and the corpus-specific rule controller solve the offline benchmark"; B4R1 L45 | **Yes, explicitly, in every post-mortem.** The status text also says it ("a simple controller also scored perfectly"). What is missing is the next move: a task where the controller provably cannot be perfect (see suggestion A). |
| 2 | **Copy-through / ceiling.** Decision endpoints are copyable (B2 passes the prior answer; Theseus notes contain the full mapping; packets fit in one message). Perfect scores measure channel fidelity, not understanding. | Q2 L29, L37; README L18 "supplied useful rules and note copying create ceiling effects" | B2 L38-40 | **Yes.** B4R1 is the direct repair for Telephone and it moved the result off ceiling (P 7/18). Theseus has no equivalent off-ceiling design yet; the haiku S1 "neither" arm (52%) is the only non-ceiling cell and it is a floor, not a discriminating middle. |
| 3 | **Single world, nested observations, no repeats.** One five-member world (Q2); 12 selected roots x 2 blocks (B2); 9 worlds in 3 recipes (B4R1). Members/hops/cases are dependent. No population interval is possible. | Q2 L35 "66 decisions are not 66 independent samples"; P1 L9 nested repeats | B2 L9, L24; B4R1 L9, L24 | **Yes, verbatim.** He is unusually disciplined about this. A reviewer could still ask why the Theseus GPT-6 lane never got a second independent world after three repair cycles, while the budget line shows USD ~1.95 spent of 60. |
| 4 | **Same-operator semantic labels.** B2's 1008 cells and B4R1's 36 reader audits were annotated by the owning agent, two passes, no inter-rater check. The 4-5pp gap is inside plausible annotator disagreement (9 ambiguous clauses). | n/a | B2 L30 `independent_raters=1`; B4R1 L30 | **Yes.** Not fixed. The repo has other annotators (shadow, dmarz lanes); a 10% blind re-annotation of the 20 lost cells would cost zero model calls. |
| 5 | **Repair-cycle multiplicity.** Theseus went Q1 -> Q1C -> Q2 -> Q3-A1 -> C1 -> Q3-A2 -> D1 -> Q3-A3/P1 -> C2, each with an instrument fix after seeing the failure (scorer order, address format, JSON mode, selector writeback, commit schema). A skeptic will say the instrument was tuned until the model passed. | Partially: each post-mortem says "no retrospective relabeling", original failures preserved, repairs prospectively planned | n/a | **Partially.** He preserves failures and preregisters each repair, which is the right defence, but no single document lists all five instrument changes in one place. The linked status copy does not fix this; a one-table "repair ledger" in the Theseus README would. |
| 6 | **Model confound in the headline.** Theseus has two models (haiku-4.5 S1 full-turnover pilot vs GPT-6 Sol handover lane) and the status text mixes "full turnover untested" (GPT-6 lane) with results a reader may assume cover the whole study. | README L5-11 vs RESULTS.md | n/a | **Not in the status text.** Should name the model per claim. |
| 7 | **B4R1 asymmetry.** R sees source + handoff; P sees handoff only. The +61pp is an information effect, not a coordination or swarm effect, and the P errors are all abstentions (safe). | n/a | B4R1 L45 "Restoring source adds information and tokens. No equal-information ... claim"; L26 zero false authorizations | **Yes.** A fair reviewer should credit that he leads with "the damage was hesitation" rather than "handoffs cause unsafe releases". |

Top 3 for the submission: (1) controller confound, (2) copy-through ceiling in Theseus (Telephone has B4R1 as the answer), (3) single world / nested units with no second independent world in the GPT-6 Theseus lane after USD ~1.95 of a USD 60 cap.

## 4. Suggested next-step designs that reuse our tooling

All three are offline-first and bounded; none is funded by this note.

### A. Theseus: break the controller ceiling with a last-event / recency rule (reuses `capture-memory-mix/reading-rule`)

The Q2/Q3 witness rule is a static mapping plus an inclusive freshness window `[8,10]`. The one native failure on main (P1 failover-r0, `Q3-A3-P1-POST-MORTEM.md` L18) was exactly a temporal-rule error: a record at `observed_at=11` was treated as fresh. Our cm2 reading-rule diagnostic (`researchers/shadow/notes/capture-memory-mix/reading-rule/FINDING.md`) measured the same family of behaviour on frozen histories: 72/72 raw-indexed choices followed the true last event regardless of display order, with mean |delta P| = 0.000183 against a 0.10 threshold, but the lossless **summary** representation drifted (22/24). Proposal: a Theseus successor where the inherited note must carry a *recency-dependent* rule (the authorized witness changes with the most recent audit event, so the correct answer depends on which event was last). A static note-copying controller is then wrong by construction on the changed cases; only an agent that reads the current history correctly can be perfect. Reuse `reading_rule.py` presentation variants (chronological / reversed / shuffled, raw vs summary) as the manipulation, and the cm2 bootstrap-by-history analysis as the estimator. Zero model calls to build; the frozen Q3 worlds and `turnover.py` fixtures already exist.

### B. Telephone: evidence-depth / provenance-count framing for the handoff chain (reuses `wild-evidence-depth` and B2 annotations)

B2's 20 lost cells are concentrated in provenance (`e04` same-receipt, `e01`, `e06`) and the rule conjunct (`b2-10 rule`), and 8/11 hop-3 losses were already lost at hop 2. Our evidence-depth census (`researchers/shadow/notes/wild-evidence-depth/FINDING.md`) scored payloads by how many linked response artefacts survive, with a 17.7x coverage ratio across size bins. Proposal: re-score the existing B2 and B4R1 handoffs (zero new calls) with a per-hop **evidence count**: number of source records whose id or distinguishing field is still recoverable from the handoff text, as a function of hop and of packet length. This turns "meaning retained 94% vs 100%" into "k of n evidence anchors survive each hop", which is the quantity a downstream reader actually needs and the quantity B4R1 shows matters (readers abstained when the governing conjunct was gone). It also makes a concrete prediction for B3/B4 successors: loss should correlate with packet byte length the way response-link coverage did in the SwarmTraces export. `wild-evidence-depth/analyze.py` already has the binning and bootstrap.

### C. Both: halflife / survival curve of a fact across hops or generations (reuses `wild-halflife`)

`researchers/shadow/notes/wild-halflife/halflife.py` fits Kaplan-Meier curves and pooled adoption rates to "time until a second identity carries the unit", with cluster bootstraps by origin. Hops in Telephone and generations in Theseus are the same object (a unit either survives the handoff or does not, with censoring at chain end). Proposal: feed the existing B2 `SEMANTIC-ANNOTATIONS.json` (1008 cells x 3 hops) and the haiku S1 per-step convention/accuracy records into `halflife.py` as unit-level survival data, clustering by root/world. This gives a per-fact-type survival curve (rule vs provenance vs version qualifier) with intervals that respect nesting, instead of a single 4-5pp mean. It needs no new model calls and it is the honest version of the "fifty hops" curve he correctly refused to buy: estimate the hazard from what exists, then decide whether more hops would be informative at all.

### Small, zero-cost fixes for the status text itself

- Theseus "Latest": replace "being prepared ... pending" with: Q3-A3 qualification passed (103 calls, 144/144), P1 started 6 trajectories and stopped on one future-timestamp approval (215/216), C2 reused 128 calls and stopped on a commit-schema violation (3/4 valid); 0 complete turnovers; native scaling on HOLD. Cite `C2-POST-MORTEM.md`.
- Telephone "Latest": add B4R1 (P 7/18 vs R 18/18, +61.1pp, zero false authorizations, all P errors are abstentions). B3 remains unfunded as stated, but B4R1 already answers the "fresh reader, new question, no prior answer field" question B3 was designed for.
- Name the model per claim (haiku-4.5 S1 vs GPT-6 Sol lane) in study 1.
- Add a one-table instrument-repair ledger (Q1 scorer order, Q1C address format, Q3-A1 JSON mode, Q3-A2 selector writeback, C2 commit schema) somewhere a reviewer will see it.
- Fix the `b3/tests/test_b3.py` concurrency assertion so it does not fail on fast hosts.

## 5. Files touched by this review

- `researchers/shadow/notes/reviews/vishesh-theseus-telephone-2026-10-04.md` (this file)
- `researchers/shadow/notes/reviews/vishesh-status-2026-10-04-linked.md` (his text, links fixed)

Nothing under `researchers/vishesh/` was modified.

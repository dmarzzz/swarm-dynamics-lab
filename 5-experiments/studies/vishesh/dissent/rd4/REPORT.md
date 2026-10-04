# Right Dissenter RD4: remembering a correction is easier than earning a recovery

Retrospective analysis, 2026-10-04. This report does not amend the prospective [plan](PLAN.md). The fixed exploratory comparison is complete: **576/576 decisions**, from 24 authored roots, six policies and four dependent epochs. Qualification separately passed 24/24. The served model was `typesafe/jev-1.13-20260917` through the frozen Typesafe route.

The repairs work on the tested closure cases, but explicitly telling the learned gate to welcome recovery produced no net accuracy improvement. Both learned gates reached **87/96** correct on-time decisions; always-check reached **88/96** using 36 logical model calls versus 73–74. Transport failures prevent treating that one-point gap as a reliable ranking. The useful construction emerging here is scoped memory of verified decisions with bounded checking. The next hard question is how unresolved uncertainty should consume a budget without preventing a later recovery.

## What changed and why

We pulled shared main, read Dmarz's RD-R1/R2/R3 review and the previous post-mortems, and wrote the plan before implementation. [Feedback response](FEEDBACK.md) maps every input to its disposition. Canonical observation identity now ignores alias multiplicity, ordering and changes to the requested alternative. Supported and withdrawn resolutions persist with scope, version, request time, verification time and expiry; actors see the applicable current decision. Tests use development fixtures and cannot silently construct reserved qualification cases. Historical exposure remains disclosed.

The new comparison holds those repaired mechanics constant and changes only the gate's admission wording. Three domains—bridge inspection, required build tests and range alarms—cover favorable and adverse changes, supported/withdrawn objections, wrong-object objections and initially absent dissent. Exact repeats and aliases precede a new observation. Votes stay scripted. This tests response to dissent, not the spontaneous formation of a swarm opinion.

## Fixed-cohort result

Every denominator includes failed and unresolved outcomes. A correct outcome must match evaluator truth, complete, and meet its deadline. Logical requests include cache uses; actual provider calls are reported separately.

| Policy | Correct / 96 | Wrong PROCEED | Needless HOLD | DEFER | Checks | Logical model calls | Recovery / 12 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Frozen majority | 60 | 18 | 18 | 0 | 0 | 0 | 3 |
| Original learned gate | 87 | 0 | 1 | 8 | 33 | 73 | 10 |
| Symmetric stop/resume gate | 87 | 0 | 1 | 8 | 33 | 74 | 10 |
| Always-check | 88 | 0 | 0 | 8 | 36 | 36 | 11 |
| Pooled evidence | 59 | 5 | 12 | 20 | 0 | 96 | 11 |
| Exact finite-grammar reference | 96 | 0 | 0 | 0 | 36 | 0 | 12 |

Symmetric versus original has one improved and one worsened paired decision. Symmetric versus always-check has one improvement and two worsenings. Original versus always-check has no improvements and one worsening. Both learned gates and always-check correctly respond to 11/12 adverse changes. The exact reference knows this finite text grammar; its perfect score is an implementation ceiling, not a generally capable model.

The gate saves three checks, or 8.3%, while adding 37–38 logical model calls. Its counterfactual settled API cost is $0.002999682 for original and $0.003084774 for symmetric, versus $0.001537032 for always-check. These arm costs overlap shared responses and must not be added as actual spend. They exclude failed-call replacement costs.

With the plan's illustrative loss weights, original and symmetric score 17 + 33c, and always-check scores 16 + 36c, where c is check cost and DEFER costs two. Thus always-check has lower observed loss at c=0 and c=0.1; the gates have lower loss at c=1. The crossing is c=1/3 before model-call costs. Neither approach dominates all checking-cost preferences. These weights are illustrative, not operational estimates.

## The informative failure: an unresolved objection spends tomorrow's check

On alarm root `6dd7a1db979b`, a verification says the reading is **not inside** the permitted interval and supplies the numeric value 40. Both gates and always-check return DEFER despite the finite task's unambiguous HOLD answer. The repeat obtains another check and another DEFER. When fresh evidence later permits recovery, both checks have already been spent. All four always-check decisions in this trajectory are unresolved; original also defers four, while symmetric retains the correct HOLD once at the alias epoch. This is a native interpretation/budget interaction, not a network failure.

On root `294ed0f1b3dc`, both gates correctly stop first, retain that decision, then refuse the fresh recovery challenge; always-check verifies and resumes. The symmetric wording did not solve the motivational example it was designed to address. Its one different benefit elsewhere is offset by deferring the first required-build failure on `a1424d89c5a1`.

The practical next design should separately represent **resolved**, **unresolved with no new information**, and **new applicable evidence**. A repeated unresolved semantic judgment should not automatically consume the last verification opportunity. A candidate is one check per observation identity plus a reserved reopening slot for genuinely new evidence, with explicit escalation or continued DEFER when interpretation is unresolved. That policy remains untested; it must receive a new prospective plan and safety/cost comparison before execution. We did not retrofit it into this dataset.

## What the memory repair establishes

The original gate retained 20 previously resolved repeats; symmetric retained 19; always-check retained 20. **All 59 retained native closures kept the correct established action with zero extra checks and zero model calls.** The exact reference retained another 24. Exact offline replay reproduced every one of the 576 records byte-for-byte as structured data, and separate row arithmetic matched the summary. This is a same-author audit, not independent validation.

The aggregate repeat-check counts of 1, 2 and 2 are not alias-identity regressions: those trajectories lacked a resolved closure. They expose the unresolved-budget issue above. A persistent incorrect native resolution could also persist incorrectly; correct state retention alone does not establish factual reliability.

## Transport, missing-answer sensitivity and process compliance

The original segment S4-A1 completed 416 decisions and stopped after a transport failure streak. S4-C1 completed eight more, all with failed requests, because the operator accepted process liveness as readiness before the SSH tunnel's failure became visible. That is an operator/readiness defect. Both segments and their failed rows remain unchanged. A prospectively published S4-C2 continuation required an end-to-end, non-inference relay probe before dispatch and every trajectory; it completed only the remaining 152 decisions. No failed answer was retried or replaced. See the [C1 post-mortem](reviews/S4-C1-POST.md) and [C2 post-mortem](reviews/S4-C2-POST.md).

There are 214 distinct saved worker request records: 203 valid responses and 11 transport/attempt-stop records that never entered the provider ledger. All 203 dispatched S4 provider calls settled. Four original and four symmetric decision rows directly fail; always-check has two direct failures followed by two budget-exhausted descendants. Pooled has one failed row.

Allowing each failed or downstream affected outcome to be either correct or incorrect yields conservative correct-count ranges: original **87–91**, symmetric **87–91**, always-check **88–92**, pooled **59–60**. Pairwise symmetric-minus-original can range from −4 to +4; either gate minus always-check from −5 to +3. These are sensitivity bounds, not estimates or confidence intervals, and they retain all observed scores. Shared failure constraints could narrow them. [Reproducible analysis](analyze_saved.py) records the rule and every noncorrect row in [analysis.json](results/combined/analysis.json).

Prospective plans and per-attempt public registration passed before dispatch, the qualified core hash stayed unchanged, and all uploaded artifacts were downloaded again and hash-matched. The first two S4 segments still failed operationally; process registration does not turn those into successful runs. Partial attempt summaries used observed arm denominators: use their counts against the fixed 96 assignments per arm, or the complete combined summary. Final combined denominators are correct.

## Plan assessment and remaining limits

All planned 24 roots and six policies are accounted for; no selective rerun, corpus replacement or favorable-outcome tuning occurred. The qualification screen passed all 18 clean and six uncertainty cases, but did not guarantee admission competence or robustness of later negated alarm judgments. The core had 69 offline tests; the continuation added eight checks. [Plan coverage](PLAN-COVERAGE.md) distinguishes measured conditions from software-only checks.

The plan mentioned changed versions, but native S4 includes wrong-object conditions and time evolution only. Version changes, expiry, same-source conflicts and unavailable/late verifiers have software coverage or historical evidence, not new native strata. The finite templates share an author and grammar, votes are scripted, and cached responses/failures create dependence. There is no independent semantic corpus, independent replication, population significance claim or operational safety claim. Historical RD2 and RD4 scores must not be pooled or read as a causal before/after improvement.

The [research and Twitter map](../SOURCES.md) remains the canonical source list. No duplicate or unverified thread was added. The biological stop-signal connection motivates bounded inhibition and reversal; these synthetic decisions do not establish a biological mechanism. Formal S2 and research promotion remain open; optional reviewer feedback was used without inventing an independent approval.

## Delivery and cost

The measured 1800px figure and replay accompany the saved data. The report replay preserves the preselected six supported-objection trajectories and adds the two alarm-withdrawal trajectories as explicitly retrospective failure illustrations. It distinguishes frozen votes, retained decisions, evaluator truth and failed/unresolved outcomes. Raw hub visuals remain immutable; their overbroad repeat-check caption is corrected in the report derivative to refer to resolved repetitions only.

RD4 used **227 new provider calls** and **$0.00922278** settled API cost, including qualification. The lifetime ledger is **428/500 calls**, $0.01662045 settled plus $0.004032 of historical unresolved reservations: **$0.02065245 committed API cost**, within the original $1 API/$2 total authority. No new machine was bought. Existing fleet operating charges are not available here and are not represented as zero. The historical mistaken host's estimated $0.011643 remains separate. [Budget receipt](results/budget-closeout.json).

The borrowed Dmarz fleet host was verified idle after completion, all four attempts' artifacts were read back with matching hashes, and the exclusive claim was released at 2026-10-04T06:20:52Z. No native worker or local transport remains. The local dashboard failed DNS resolution, so dashboard browser rendering was not observed; public registration was checked remotely and readable GitHub plans were checked in the browser. [Closeout](CLOSEOUT.md), [saved data](results/combined/summary.json), [exact audit](results/combined/audit.json).

[Result figure](../../../../../artifacts/right-dissenter-rd4-results/right-dissenter-rd4-results-v1.png) · [Measured report film](../../../../../artifacts/right-dissenter-rd4-replay/right-dissenter-rd4-replay-v1.mp4) · [Qualification figure](../../../../../artifacts/right-dissenter-rd4-q4/right-dissenter-rd4-q4-v1.png). The three deliverables pass scoped strict Flight Deck validation; unrelated full-checkout issues are listed in the closeout.

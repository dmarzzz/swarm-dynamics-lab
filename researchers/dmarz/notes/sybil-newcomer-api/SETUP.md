# Experiment setup record: sybil-newcomer-api / v1

**Retrospective evidence index, created 2026-10-04 UTC after S1 launch.** The [shared setup runbook](../../../../tooling/agent-experiments/EXPERIMENT-SETUP.md) and its template arrived after this experiment's current S1 run had started. This file links existing evidence; it is not a prospective registration, a new launch authorization, or proof that every newly consolidated check ran historically. Original plans, assessments, receipts and results retain their own dates and revisions.

## Ownership and question

- Owner: dmarz. Operator: dmarz/sybil-specialists and the parent coordinating agent. Implementation and recomputation are same-owner engineering work, not independent researcher review.
- Owner explicitly waived independent review for this and the parallel budget study: [WAIVER.md](WAIVER.md). No passing independent review or accepted hypothesis is claimed.
- Question: under four audits, twelve admitted reports and sixteen controller messages per round, does continued checking of established trust plus exploration of little-audited identities preserve unique honest newcomer information after a coordinated attack?
- Primary contrast: renewal minus reputation specialist accuracy at round eight, sixteen controller identities, sleeper attack. The +10 percentage-point useful-effect marker and descriptive paired-world analysis were declared in [preregistration.md](preregistration.md).
- Research status: exploratory instrument and S1 comparison in the owner's notes. Formal S2 is disabled; no completed novelty survey or formal hypothesis acceptance is asserted.
- Prior local evidence: [sybil-scale-api results](../sybil-scale-api/RESULTS.md), where repeated specialist facts allowed high accuracy despite substantial honest-specialist rejection. This follow-up makes honest specialist knowledge scarce during attacks and fixes controller message/computation resources while identity count changes.
- Current attempt: `sybil-newcomer-api/8def40e4`, S1, execution revision `e9db4c58a8847d2f54d60a8ff3cc70f81f58263e`. Collection and scientific verification are now complete: 1,944/1,944 valid observations, with no errors. Archival, claim release and temporary-host teardown are now verified; these completion updates are later than this index's original creation.

## Gate evidence

Statuses below describe what this retrospective index can substantiate. A pending historical receipt is not manufactured into a pass by adding a link now. Assessments are by the same-owner operator on 2026-10-04 UTC unless otherwise identified.

| Gate | Status | Evidence and assessor | Remaining evidence / next action |
|---|---|---|---|
| G0 Question and applicable research status | Pass for the declared exploratory scope; formal acceptance not claimed | [Plan](README.md), [preceding results](../sybil-scale-api/RESULTS.md), [owner waiver](WAIVER.md) | Any future formal claim needs the applicable survey/hypothesis gates; this index confers none |
| G1 Prospective design | Pass for pre-collection design; pre-implementation chronology not certified | [Design](design.yaml), [preregistration](preregistration.md), committed stage assessments and recorded execution revisions | Do not represent this after-launch index, or an unverified document-creation chronology, as original preregistration |
| G2 Instrument and offline checks | Pass for the frozen qualified instrument | [Eight-test evidence and final local S0](reviews/s0-local-003-post.md), [source tests](src/selftest.py), [visualization mapping](VISUALIZATION.md) | Maintain source fingerprint; material drift requires new qualification |
| G3 S1 admission | Operational launch documented; complete public-plan preflight evidence pending in this index | [S1 preassessment](reviews/s1-001-pre.md), [budget preflight](../sybil-followups/budget-preflight.json), [dedicated-host checkpoint](../sybil-followups/dedicated-host-checkpoint.json), [deployment launch record](DEPLOYMENT.md) | Parent attaches any existing immutable-public-plan/content-hash/page-verification receipt; if absent before launch, preserve that historical process gap rather than backdate one |
| G4 Qualification before S1 | Pass | [Fleet S0 post-mortem](reviews/fleet-s0-001-post.md), [Q0 post-mortem](reviews/q0-001-post.md), [Q0 recomputation receipt](records/q0-001-verification.json); both prior stages reverified on the S1 host | No remaining competence blocker at launch; passing clean packets does not predict scientific outcome |
| G5 Reconciliation and closeout | Pass for scientific, visual, archive and resource closeout | [S1 post-mortem](reviews/s1-001-post.md), [full recomputation](verification-summary.json), [deployment closeout](DEPLOYMENT.md); 1,944/1,944, ledger/raw archives preserved, claim released, temporary host destroyed, figure filed | Parent publishes the generated inventory bookkeeping update; G3 historical receipt gap remains explicit |

## Design and instrument index

- Readable plan and prospective analysis: [README.md](README.md), [preregistration.md](preregistration.md), [design.yaml](design.yaml). Allocation amendments are dated and preserve historical S0/Q0 execution.
- Scenario contracts: eighteen honest veterans; six honest round-four newcomers, three supplying unique rare truths; one controller with one/four/sixteen identities and sixteen total reports each round. Clean, sleeper and predeclared relapse conditions are explicit in the plan and [simulator](src/sim.py). Half the controller identities join at round four in the four/sixteen-identity cells; changing age composition and reputation exposure are reported mechanisms.
- Units and counts: twenty-four paired world clusters, three identity counts, three policies, three attack modes, three measured synthesis rounds = 1,944 assigned S1 calls. Eight simulated rounds per world/condition; agents, calls and frames are not independent replicates. Each post-arrival world has 24 honest identities plus controller identities. Controller model computation is zero in every condition; one API call synthesizes an admitted packet.
- Precision: exploratory twenty-four-world descriptive paired bootstrap, not a power-qualified confirmatory study. No tuning on S1; intervals are not multiple-comparison-adjusted significance claims.
- Splits: engineering 6900–6901; clean qualification 7000–7005; S1 7100–7123. The reserved formal holdout remains unopened; no labels are exposed here.
- Observable context, reset and evaluator boundary: [study.py](src/study.py), [sim.py](src/sim.py), and [provider.py](src/provider.py). Current reports, opaque identity codes, join time and observed audit history enter each independent model packet. Hidden ownership/truth/future reports do not. The model has no cross-round memory; scripted reputation persists within the declared world/arm.
- Model: `claude-haiku-4-5-20251001`, native Messages API, temperature zero, six-field structured response, maximum 500 output tokens, no tools/thinking/cache/retries. [Pinned dependencies](requirements.txt).
- Scientific source fingerprint: `f38a9658dcb5e403e9dfaeccfd201c603b84d947ed085779374b278ceb4ef943`. It includes frozen src modules, design, registration and requirements. Documentation/reporting additions do not alter this fingerprint.
- Startup/dispatch: [coordinator.py](src/coordinator.py) requires matching successful preceding stages; [worker.py](src/worker.py) saves assignments before dispatch, creates exclusive output namespaces, runs a finite bounded pool, preserves failures and forbids automatic re-execution. [RUN.md](RUN.md) documents the approved orchestration. A direct local scripted CLI exists; local preparation is explicitly recorded as uncommitted engineering, not a substitute for fleet stage admission.
- Offline checks: deterministic resources, policy blindness, scarcity/attack controls, observed-only state updates, assignment uniqueness/splits, malformed billed-response accounting, paired identity interaction/missing-data bounds and renderer transitions. Shared-budget and fake-transport checks are indexed in the bundle's [README](../sybil-followups/README.md) and test sources.
- Raw recomputation: [verify_results.py](reporting/verify_results.py) regenerates assignments/worlds/history and evaluates saved decisions; [build_report.py](reporting/build_report.py) produces the report and complete cell tables. These are same-owner checks, not independent researcher review.
- Visualization: [VISUALIZATION.md](VISUALIZATION.md), retained `history.jsonl.gz`, supported PNG and GIF. S1 replay has eight recorded logical frames and synthesis observations only at rounds four/five/eight. Q0 uses nine completion-prefix frames. Static PNG is the fallback.

## Current S1 admission evidence

- Attempt: s1-001, parent q0-001; [preassessment](reviews/s1-001-pre.md). Live run: [sybil-newcomer-api/8def40e4](https://swarm-live.pages.dev/#/r/sybil-newcomer-api%2F8def40e4).
- Existing immutable source-plan location: [README at the S1 execution revision](https://github.com/dmarzzz/swarm-lab/blob/e9db4c58a8847d2f54d60a8ff3cc70f81f58263e/researchers/dmarz/notes/sybil-newcomer-api/README.md). This index identifies the source location; it does not claim that its HTTP response, expected content hash or public page display was independently verified before launch. Those historical receipt fields are not yet linked here.
- Experiment purpose/TLDR: compare random, reputation and renewal audits at equal budgets, measuring rare truth recovery and harmful/controller influence after a reputation-building phase. Claims are limited to simulated actors and independent current-packet model synthesis.
- Condition bindings: the frozen assignment manifest records world, identity count, strategy, policy, round and packet hash for every call. Run-level metadata records stage, batch, backend, source fingerprint and execution revision. An individually registered textual TLDR per scientific cell is not asserted by this index.
- Budget preflight: [owner aggregate snapshot](../sybil-followups/budget-preflight.json), observed 2026-10-04T03:50:35.627308Z, includes bounded other cohorts within the $500 owner cap. The shared $60 follow-up guard is split into $50/$10 fixed allocations on separate hosts; permanent peer holds are not API charges or unknown calls. Both retain the settled 52-call/$0.366548 checkpoint. Final actual charges come from per-study usage ledgers.
- Caps: newcomer at most $10 total allocation, plus the unchanged $75 nonrefundable conservative study ledger and 2,050 attempted-call ceiling; nominal Q0+S1 is 1,980 calls. S1: 1,944 calls, two simultaneous requests, 120-second request timeout, four-hour stage timeout, no retries. Any invalid observation stops new dispatch and drains already-started requests.
- Allocation: dedicated host sim-dmarz-sybil-newcomer, claim dmarz-sybil-newcomer. [Checkpoint](../sybil-followups/dedicated-host-checkpoint.json) at 2026-10-04T04:08:59.722032Z verifies migration, both historical stages reverified on S1 hosts, retained budget checkpoint/peer allocation and a successful provision summary. Claim expiry and complete provisioning-account verification remain private operator evidence, not invented from the public host name.
- Launch: [deployment](DEPLOYMENT.md) records 2026-10-04T04:09:27.933420Z under revision `e9db4c58a8847d2f54d60a8ff3cc70f81f58263e`, unchanged qualified source, one finite worker and two API requests. The source of this assertion is the parent operator's launch record; this index performs no remote launch or new workload check.
- Credentials: authorized aliases `SWARM_MODEL_API_KEY` and `SWARM_MODEL_WORKSPACE_ID` are consumed privately. No values, account IDs, private host addresses or endpoints appear here.
- Decision-maker: parent operator under the owner's launch instruction and explicit review waiver. This file neither reauthorizes nor retrospectively reruns admission.

## Attempt and repair history

| Attempt | Stage | Pre-review / evidence | Assigned / started / terminal / graded / analyzed | Post-mortem / disposition |
|---|---|---|---|---|
| s0-local-001 | Uncommitted scripted engineering | [Pre](reviews/s0-local-001-pre.md) | 198 / 198 / 198 / 198 / 198 | [Post](reviews/s0-local-001-post.md); repair stale test expectation and complete analysis |
| s0-local-002 | Uncommitted scripted engineering | [Pre](reviews/s0-local-002-pre.md) | 198 / 198 / 198 / 198 / 198 | [Post](reviews/s0-local-002-post.md); fix scripted visual labels |
| s0-local-003 | Uncommitted scripted engineering | [Pre](reviews/s0-local-003-pre.md) | 198 / 198 / 198 / 198 / 198 | [Post](reviews/s0-local-003-post.md); advance to committed fleet S0 |
| fleet-s0-001 / 68819f24 | Scripted fleet S0 | [Pre](reviews/fleet-s0-001-pre.md) | 198 / 198 / 198 / 198 / 198 | [Post](reviews/fleet-s0-001-post.md); advance to Q0 |
| q0-001 / f7b78b41 | API Q0 | [Pre](reviews/q0-001-pre.md), [receipts](records/q0-001-summary.json) | 36 / 36 / 36 / 36 / 36 | [Post](reviews/q0-001-post.md); qualification passed |
| s1-001 / 8def40e4 | API exploratory comparison | [Pre](reviews/s1-001-pre.md), [launch](DEPLOYMENT.md) | 1,944 / 1,944 / 1,944 / 1,944 / 1,944 | [Post](reviews/s1-001-post.md); complete valid result; archive, claim release and teardown verified |

| Issue | Evidence/cause | Resolution or remaining limit |
|---|---|---|
| N-01 test harness | Shared guard correctly rejected a duplicate before the older per-study error path | Corrected expected category; eight-test suite passed, preserved original result |
| N-02 analysis completeness | Initial analysis lacked explicit fixed-resource identity contrast/interaction | Added pre-API contrast, regression test, duplicate rejection and missing-data bounds |
| Scripted visual language | Early S0 figure used API/model terms in its footer | Renderer corrected before final source freeze; S0-003 numerical outputs matched the preceding attempt |
| N-03 Q0 elapsed display | Q0 completion replay omitted elapsed argument and displays 0s | Actual 21.5276-second collection time retained in summary/post-mortem; cosmetic limitation, no scientific impact |
| Dedicated allocation correction | Updated owner instruction read after stopped S0/Q0 | Newcomer migrated before S1; historical evidence/budget retained and verified |
| New setup runbook | Consolidated runbook arrived after S1 launch | This file is explicitly retrospective; absent historical process evidence is not backfilled as prior approval |

## Closeout status

- Execution: S1 completed first attempt; worker exited; 1,944/1,944 observations.
- Response validity: Q0 36/36 valid/exact and S1 1,944/1,944 valid; zero invalid, missing, duplicate or retried records.
- Qualification: passed for the unchanged instrument, including re-verification after migration.
- Scientific conclusion: renewal improvement was not established: +8.3 points versus reputation (−2.8 to +19.4), and −5.6 versus random (−16.7 to +5.6). Adverse/null findings retained in [RESULTS.md](RESULTS.md).
- Process compliance: independent review explicitly waived; formal status remains exploratory. This setup record is retrospective and G3 public-plan receipt coverage is incomplete in the index.
- Reporting: S0/Q0 raw records and eleven artifacts per stage preserved; Q0 [raw-to-summary verification](records/q0-001-verification.json) and [public replay evidence](records/q0-001-artifact-receipt.json) available. The [S1 report](RESULTS.md), [numeric audit](verification-summary.json), and [public visual evidence](records/s1-001-artifact-receipt.json) are complete; raw records and hashed private ledgers/allocation are archived, final figure is filed, and resource release/teardown verified. Generated inventory publication is a parent bookkeeping follow-up.
- Cost: Q0 $0.043560 plus S1 $3.088659 = $3.132219 actual, usage known for all 1,980 calls. Per-study ledger reconciled; permanent cross-host allocation holds are excluded from actual spend.
- Resources: S1 worker exited; all eleven artifacts verified. Claim release PR130 and hub event 34510 confirmed no active claim. Temporary host destroyed under the reviewed five-resource plan, twelve other entries unchanged; fleet removal PR131 merged.
- Next action: parent publishes final records and generated inventory bookkeeping. The final figure is filed and Flight Deck strict validation passed (thirty artifacts, zero errors/warnings). Missing pre-launch plan receipts remain historical process questions rather than retrospective preregistration; no model rerun is warranted by the adverse/inconclusive primary outcome.

Final figure with project provenance: [sybil-newcomer-api-s1-v1.png](../../../../artifacts/sybil-newcomer-api-s1/sybil-newcomer-api-s1-v1.png).

Final infrastructure receipt (2026-10-04 UTC): generated inventory PR132 merged as `751c72fbf2b7464e91de2f321f0a18a2aca2b365`; all other twelve entries unchanged. The newcomer allocation is fully closed. See [records/closeout.json](records/closeout.json).

# Deployment record: sybil-budget-api

**Current status, 2026-10-04:** S1 run `sybil-budget-api/46ebda03` is done after one attempt. All 2,880 assigned outcomes completed, with zero invalid, failed or not-started outcomes. The worker has exited and ten durable artifacts passed checksum verification. Public final/retention views and replay playback were verified. Main S1 cost $39.349188; Q0 plus S1 cost $39.672176. Same-source saved-data verification and the [post-mortem](reviews/s1-001-post.md) provide scientific closeout; the [closeout receipt](records/closeout.json) records the subsequent merged claim release and hub readback.

The budget study ran alone on `sim-dmarz-4` under `dmarz-sybil-followups` after the newcomer study moved to its dedicated host. The dated correction and launch entries below are historical snapshots, retained to distinguish plans from their later execution. The owner waived independent review; own assessments, qualification and budget controls remained in force. Formal S2 is disabled.

## Frozen execution

- Fleet S0 revision: `106d1082db3152af5bcf5e4539bca81adc13d57d`.
- Q0 execution revision: `996a4af01ebfff3071b88c60914472b171798053`.
- S1 execution revision: `e9db4c58a8847d2f54d60a8ff3cc70f81f58263e`.
- Runtime fingerprint: `66ea4fe1465678ff66d099eec14ea11dbf5bc69063c00e3cc57249e06db98f08`.
- Runtime: Python 3.12 with the pinned requirements; pinned model `claude-haiku-4-5-20251001` for API stages.
- Paid concurrency: two requests for this study, four combined across the two studies. Request timeout 120 seconds; stage limit four hours; 500 output tokens; no retries.
- Study ceiling: 3,200 attempted calls and $140 nonrefundable conservative reservations. Nominal plan: 16 Q0 plus 2,880 S1 calls, with exact combined conservative reservation $130.754844. Reservation is not actual billing.
- Follow-up allowance: $60 combined within the owner's $500 aggregate budget, partitioned $50 for this study and $10 for the newcomer study. The cross-host guards used the same settled checkpoint plus fixed peer-allocation holds, as detailed in the dated correction below. All completed calls have known usage; administrative holds are excluded from final model spend.

The private launcher checks the current claim and source fingerprint before starting a stage. Credentials are supplied through private environment aliases; no secret values, service addresses or server addresses are part of this record. Later documentation-only commits do not change the runtime fingerprint.

## Allocation correction planned before S1 — 2026-10-04

The scientific runtime remains `66ea4fe1465678ff66d099eec14ea11dbf5bc69063c00e3cc57249e06db98f08`; no simulator, model prompt, condition, seed, evaluator or qualification threshold changes. The operator will verify the amended budget-only claim and the newcomer host's dedicated allocation, run setup selftests on the new host and retain the existing exact-runtime Q0 evidence. No new API qualification is needed solely for the relocation.

Before either S1 launch, the exact settled checkpoint of 52 calls and $0.366548 actual spend will be copied to both hosts. Under each local $60 guard, the operator will install a persistent $10 peer-allocation hold on the budget host and a persistent $50 peer-allocation hold on the newcomer host. The holds reserve the other study's allocation and are not API calls or billed usage. They remain untouched throughout the active runs.

This leaves at most $49.633452 of additional actual-plus-unsettled commitments for the budget study and $9.633452 for the newcomer study. Combined new commitments are therefore bounded by $59.266904; including the historical $0.366548 once bounds combined actual spend below $60 ($59.633452 conservatively). Both cloned guard balances intentionally retain that historical charge, but final reporting uses the per-study API ledgers and deduplicates the shared checkpoint. Allocation holds never enter reported model spend or call counts.

These checkpoint copies, holds and allocation amendments are planned at this record. The operator must verify them before launch; S1 is ready scientifically and remains operationally pending until those checks pass.

## Current stage status

| Stage | Run | Status | Reconciliation | Model calls / cost |
|---|---|---|---|---|
| Fleet S0 | `sybil-budget-api/4346fc36` | Done, attempt 1; verified | 256 assigned, started, terminal, graded and analyzed; zero invalid/not-started | 0 / $0 |
| Q0 | `sybil-budget-api/7b177592` | Done, attempt 1; verified | 16 assigned, started, terminal, graded and analyzed; zero invalid/not-started; all 16 exact | 16 / $0.322988 |
| S1 | `sybil-budget-api/46ebda03` | Done, attempt 1; saved-data and publication audits | 2,880 assigned, started, terminal, graded and analyzed; 120 cells × 24 paired worlds; zero invalid/not-started | 2,880 / $39.349188 |

S0 covers all 120 grid cells on two engineering worlds plus 16 clean full/missing-fact fixtures. Both population sizes returned eight of eight exact clean packets and all required abstentions. Preparation and collection took 84.47 seconds. There were no reporting errors. Ten durable artifacts were verified; initial/final images are 1920×1440 and the replay contains 25 decodable frames. The study's finite S0 worker had exited when checked. The shared ledger then contained zero reservations, unsettled commitments and actual spend.

The [fleet post-mortem](reviews/fleet-s0-001-post.md) records evidence and next action. The already committed [Q0 preassessment](reviews/q0-001-pre.md) supplies clean competence thresholds, failure policy, cost limits and the visualization mapping. The subsequent [Q0 post-mortem](reviews/q0-001-post.md) confirms clean API competence. The preserved [S1 preassessment](reviews/s1-001-pre.md) records the readiness and dedicated-allocation conditions before launch; current findings are in [RESULTS.md](RESULTS.md).

Q0 returned 8/8 exact clean packets at each size, 100% field correctness and all 24 required missing-fact abstentions. It used 319,968 input and 604 output tokens, with usage reported for all 16 calls. Actual cost was $0.322988; conservative study reservations were $1.018967. Collection took 11.80 seconds, with rendering additional, and there were no reporting errors. All ten durable artifacts were verified. The unchanged frozen renderer regenerated the final views and 17-frame replay from saved observations in the matching environment, and the reporting verifier reproduced all packet hashes, graph metrics, check counts, grades and analyses. The finite worker had exited. At that snapshot, both follow-ups together had $0.366548 in actual spend, zero unsettled holds, and all 52 shared reservations settled under the $60 guard. See the small [verification record](q0-verification-summary.json).

## Public UI and retained evidence

The [experiment dashboard](https://swarm-live.pages.dev/#/x/sybil-budget-api) exposes synthetic metrics and permitted image artifacts. S0's [final heatmap](https://swarm-live.pages.dev/api/a/sybil-budget-api/4346fc36/final_frame.png), [retention companion](https://swarm-live.pages.dev/api/a/sybil-budget-api/4346fc36/retention.png) and [recorded completion replay](https://swarm-live.pages.dev/api/a/sybil-budget-api/4346fc36/replay.gif) are the publication targets. Decoding and durable artifact verification have passed. Q0's [final competence image](https://swarm-live.pages.dev/api/a/sybil-budget-api/7b177592/final_frame.png) and [17-frame completion replay](https://swarm-live.pages.dev/api/a/sybil-budget-api/7b177592/replay.gif) are published. The operator verified public Q0 playback from 0/16 to 16/16 and the correct final per-size scores and $0.3230 displayed cost. S1's [final heatmap](https://swarm-live.pages.dev/api/a/sybil-budget-api/46ebda03/final_frame.png), [retention companion](https://swarm-live.pages.dev/api/a/sybil-budget-api/46ebda03/retention.png) and [25-frame completion replay](https://swarm-live.pages.dev/api/a/sybil-budget-api/46ebda03/replay.gif) are published and checked against final analysis. The operator observed replay progression from 0 to 1,080 completions; the final PNG reports 2,880/2,880. Full local replay decoding checks all 25 frames. The [publication receipt](records/s1-001-artifact-receipt.json) retains exact checksums and the scope of the UI check.

Assignment, world and episode histories, summaries and analyses remain in the authorized artifact store. No simulated identity conversations are invented for the replay. The operator kept the allocation valid through collection and uploads and confirmed the finite worker stopped. Claim release and any machine teardown are distinct operator closeout actions, not inferred from a finished model run.

## S1 launch, 2026-10-04T04:09:27.932607+00:00

Run `sybil-budget-api/46ebda03` launched once on `sim-dmarz-4` under `dmarz-sybil-followups` with execution revision `e9db4c58a8847d2f54d60a8ff3cc70f81f58263e`. The scientific source fingerprint is unchanged. All prior artifacts and grades were reverified on this host after newcomer migration. The fixed peer-allocation holds are active and checked by the launcher; study histories and spending were not reset. One finite worker owns the one active run, with two concurrent API requests. At this historical launch snapshot, the 2,880 planned outputs were collecting; no scientific result was claimed then. See [the live run](https://swarm-live.pages.dev/#/r/sybil-budget-api%2F46ebda03).

## S1 completed collection and evidence closeout — 2026-10-04

All 2,880 calls returned valid outcomes and usage: 38,754,668 input tokens, 118,904 output tokens and $39.349188 actual cost. Preparation and collection took 3,475.74 seconds; rendering and upload followed. No replacements, retries, failures, missing assignments or reporting errors occurred. `summary.qualification` is null: this is the scientific comparison using the existing qualified runtime, not a new clean-competence qualification despite the hub's generic `qualification_passed` completion flag.

The unchanged renderer rebuilt final accuracy/admission and retention views and a 25-frame GIF from saved outcomes. Full assignment/world regeneration and accounting reconciliation passed in the original Linux environment with Python 3.12 and frozen requirements, recorded in [verification-summary.json](verification-summary.json); [execution-summary.json](execution-summary.json), [aggregate JSON](results-summary.json), [cell CSV](results-cells.csv) and the [raw model-outcome journal](records/s1-001-episodes.jsonl.gz) preserve the results. Science fields and display coordinates matched exactly; the verifier allows a 1e-15 tolerance only for display-only trigonometric coordinates. The redundant local full reconstruction was interrupted after the complete Linux audit passed, not recorded as a local pass or failed experiment. Local figure rendering, inspection and complete GIF decoding passed separately; the [local reporting receipt](records/s1-001-local-reporting.json) records their scope. The operator verified all ten durable artifact checksums, public views and worker exit.

The per-study closed ledger contains 2,896 Q0/S1 calls, all with known usage, $39.672176 actual cost and $130.754844 cumulative conservative reservations. Reservations are not billing. The [combined accounting receipt](records/followups-accounting.json) reports 4,876 calls and $42.804395 across both follow-ups' Q0/S1 stages, zero unknown usage, with copied checkpoint balances and fixed allocation holds excluded.

Scientific disposition: complete valid exploratory result. See [RESULTS.md](RESULTS.md) and [S1 post-mortem](reviews/s1-001-post.md). The historical mutable public-plan URL lacks a pre-launch immutable content-hash receipt; this remains a retrospective process failure in [SETUP.md](SETUP.md), not a passed preregistration gate. Resource release is complete: PR167 merged, hub release event 38372 is recorded and the claim is absent from active allocations. [Closeout](records/closeout.json) preserves the accounting archive and existing-host disposition. No new stage or successor launch is authorized by this closeout.

## Final resource closeout

The finite worker and saved-data audit have exited. Claim `dmarz-sybil-followups` is done in merged agentops PR167 and hub release event 38372; it is absent from active hub claims. The existing `sim-dmarz-4` host is retained for owner lifecycle management, with no worker from this study. Original accounting archives are preserved in private agentops commit `e1c2592bd6a897af16ab626533a37bc53c013372` (PR166). The [closeout receipt](records/closeout.json) contains the non-secret references and ledger digests. The first mirror helper failed before any report because its interpreter could not import the reporting module; using the installed reporting path fixed the helper, and explicit readback confirmed closure. No model call or experiment retry occurred.

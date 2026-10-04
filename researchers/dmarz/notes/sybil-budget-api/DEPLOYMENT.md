# Deployment record: sybil-budget-api

This exploratory study completed S0 and Q0 on `sim-dmarz-4` under `dmarz-sybil-followups`; the two follow-ups used that allocation during the now-finished qualification stages. The owner's updated requirement is one active experiment per host. The planned S1 allocation keeps only this budget study on `sim-dmarz-4` and narrows that claim accordingly; the newcomer study will move to dedicated `sim-dmarz-sybil-newcomer`. Both Q0 workers are stopped. This correction is a plan before S1, not evidence that migration, claim amendment or S1 launch has already occurred. Each study retains its own finite worker and API ledger. The owner waived independent review; own assessments, qualification and budget controls remain in force. Formal S2 is disabled.

## Frozen execution

- Fleet S0 revision: `106d1082db3152af5bcf5e4539bca81adc13d57d`.
- Q0 execution revision: `996a4af01ebfff3071b88c60914472b171798053`.
- Runtime fingerprint: `66ea4fe1465678ff66d099eec14ea11dbf5bc69063c00e3cc57249e06db98f08`.
- Runtime: Python 3.12 with the pinned requirements; pinned model `claude-haiku-4-5-20251001` for API stages.
- Paid concurrency: two requests for this study, four combined across the two studies. Request timeout 120 seconds; stage limit four hours; 500 output tokens; no retries.
- Study ceiling: 3,200 attempted calls and $140 nonrefundable conservative reservations. Nominal plan: 16 Q0 plus 2,880 S1 calls, with exact combined conservative reservation $130.754844. Reservation is not actual billing.
- Follow-up allowance: $60 combined within the owner's $500 aggregate budget, partitioned $50 for this study and $10 for the newcomer study. The planned cross-host guards use the same settled checkpoint plus fixed peer-allocation holds, as detailed below. Unknown request billing retains its reservation; the root operator reconciles other commitments before launch.

The private launcher checks the current claim and source fingerprint before starting a stage. Credentials are supplied through private environment aliases; no secret values, service addresses or server addresses are part of this record. Later documentation-only commits do not change the runtime fingerprint.

## Allocation correction planned before S1 — 2026-10-04

The scientific runtime remains `66ea4fe1465678ff66d099eec14ea11dbf5bc69063c00e3cc57249e06db98f08`; no simulator, model prompt, condition, seed, evaluator or qualification threshold changes. Root will verify the amended budget-only claim and the newcomer host's dedicated allocation, run setup selftests on the new host and retain the existing exact-runtime Q0 evidence. No new API qualification is needed solely for the relocation.

Before either S1 launch, the exact settled checkpoint of 52 calls and $0.366548 actual spend will be copied to both hosts. Under each local $60 guard, root will install a persistent $10 peer-allocation hold on the budget host and a persistent $50 peer-allocation hold on the newcomer host. The holds reserve the other study's allocation and are not API calls or billed usage. They remain untouched throughout the active runs.

This leaves at most $49.633452 of additional actual-plus-unsettled commitments for the budget study and $9.633452 for the newcomer study. Combined new commitments are therefore bounded by $59.266904; including the historical $0.366548 once bounds combined actual spend below $60 ($59.633452 conservatively). Both cloned guard balances intentionally retain that historical charge, but final reporting uses the per-study API ledgers and deduplicates the shared checkpoint. Allocation holds never enter reported model spend or call counts.

These checkpoint copies, holds and allocation amendments are planned at this record. Root must verify them before launch; S1 is ready scientifically and remains operationally pending until those checks pass.

## Stage status

| Stage | Run | Status | Reconciliation | Model calls / cost |
|---|---|---|---|---|
| Fleet S0 | `sybil-budget-api/4346fc36` | Done, attempt 1; verified | 256 assigned, started, terminal, graded and analyzed; zero invalid/not-started | 0 / $0 |
| Q0 | `sybil-budget-api/7b177592` | Done, attempt 1; verified | 16 assigned, started, terminal, graded and analyzed; zero invalid/not-started; all 16 exact | 16 / $0.322988 |
| S1 | Not launched at this record | Q0 passed; dedicated allocation and budget partition planned | Planned 2,880 calls, 120 cells × 24 fresh worlds | Pending |

S0 covers all 120 grid cells on two engineering worlds plus 16 clean full/missing-fact fixtures. Both population sizes returned eight of eight exact clean packets and all required abstentions. Preparation and collection took 84.47 seconds. There were no reporting errors. Ten durable artifacts were verified; initial/final images are 1920×1440 and the replay contains 25 decodable frames. The study's finite S0 worker had exited when checked. The shared ledger then contained zero reservations, unsettled commitments and actual spend.

The [fleet post-mortem](reviews/fleet-s0-001-post.md) records evidence and next action. The already committed [Q0 preassessment](reviews/q0-001-pre.md) supplies clean competence thresholds, failure policy, cost limits and the visualization mapping. The subsequent [Q0 post-mortem](reviews/q0-001-post.md) confirms clean API competence. S1 scientific findings remain unresolved. The already committed [S1 preassessment](reviews/s1-001-pre.md) is ready, subject to the dated dedicated-allocation correction and checkpoint/hold checks before launch.

Q0 returned 8/8 exact clean packets at each size, 100% field correctness and all 24 required missing-fact abstentions. It used 319,968 input and 604 output tokens, with usage reported for all 16 calls. Actual cost was $0.322988; conservative study reservations were $1.018967. Collection took 11.80 seconds, with rendering additional, and there were no reporting errors. All ten durable artifacts were verified. The unchanged frozen renderer regenerated the final views and 17-frame replay from saved observations in the matching environment, and the reporting verifier reproduced all packet hashes, graph metrics, check counts, grades and analyses. The finite worker had exited. At that snapshot, both follow-ups together had $0.366548 in actual spend, zero unsettled holds, and all 52 shared reservations settled under the $60 guard. See the small [verification record](q0-verification-summary.json).

## Public UI and retained evidence

The [experiment dashboard](https://swarm-live.pages.dev/#/x/sybil-budget-api) exposes synthetic metrics and permitted image artifacts. S0's [final heatmap](https://swarm-live.pages.dev/api/a/sybil-budget-api/4346fc36/final_frame.png), [retention companion](https://swarm-live.pages.dev/api/a/sybil-budget-api/4346fc36/retention.png) and [recorded completion replay](https://swarm-live.pages.dev/api/a/sybil-budget-api/4346fc36/replay.gif) are the publication targets. Decoding and durable artifact verification have passed. Q0's [final competence image](https://swarm-live.pages.dev/api/a/sybil-budget-api/7b177592/final_frame.png) and [17-frame completion replay](https://swarm-live.pages.dev/api/a/sybil-budget-api/7b177592/replay.gif) are published. Root verified public Q0 playback from 0/16 to 16/16 and the correct final per-size scores and $0.3230 displayed cost. S1 publication checks remain pending.

Assignment, world and episode histories, summaries and analyses remain in the authorized artifact store. No simulated identity conversations are invented for the replay. Root keeps the allocation valid through Q0, S1 and final uploads, verifies the finite workers have stopped, then releases it. No claim release or machine teardown is recorded here while S1 remains pending.

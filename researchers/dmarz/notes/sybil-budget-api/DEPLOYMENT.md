# Deployment record: sybil-budget-api

This exploratory study is deployed on `sim-dmarz-4` under the exclusive allocation `dmarz-sybil-followups`, used only by the two owner-authorized parallel follow-ups. Each study has its own finite worker, output directories, attempted-call cap and conservative reservation ledger. They share one locked spending guard. The owner explicitly waived independent review; own pre-run/post-run assessments, competence qualification and budget controls remain in force. Formal S2 is disabled.

## Frozen execution

- Fleet S0 revision: `106d1082db3152af5bcf5e4539bca81adc13d57d`.
- Q0 execution revision: `996a4af01ebfff3071b88c60914472b171798053`.
- Runtime fingerprint: `66ea4fe1465678ff66d099eec14ea11dbf5bc69063c00e3cc57249e06db98f08`.
- Runtime: Python 3.12 with the pinned requirements; pinned model `claude-haiku-4-5-20251001` for API stages.
- Paid concurrency: two requests for this study, four combined across the two studies. Request timeout 120 seconds; stage limit four hours; 500 output tokens; no retries.
- Study ceiling: 3,200 attempted calls and $140 nonrefundable conservative reservations. Nominal plan: 16 Q0 plus 2,880 S1 calls, with exact combined conservative reservation $130.754844. Reservation is not actual billing.
- Shared follow-up guard: $60 of known actual use plus unsettled request reservations across both studies, within the owner's aggregate $500 API allowance. Unknown billing retains the full reservation. The root operator reconciles other experiment commitments before paid launch.

The private launcher checks the current claim and source fingerprint before starting a stage. Credentials are supplied through private environment aliases; no secret values, service addresses or server addresses are part of this record. Later documentation-only commits do not change the runtime fingerprint.

## Stage status

| Stage | Run | Status | Reconciliation | Model calls / cost |
|---|---|---|---|---|
| Fleet S0 | `sybil-budget-api/4346fc36` | Done, attempt 1; verified | 256 assigned, started, terminal, graded and analyzed; zero invalid/not-started | 0 / $0 |
| Q0 | `sybil-budget-api/7b177592` | Done, attempt 1; verified | 16 assigned, started, terminal, graded and analyzed; zero invalid/not-started; all 16 exact | 16 / $0.322988 |
| S1 | Not launched at this record | Ready after exact-runtime Q0 success | Planned 2,880 calls, 120 cells × 24 fresh worlds | Pending |

S0 covers all 120 grid cells on two engineering worlds plus 16 clean full/missing-fact fixtures. Both population sizes returned eight of eight exact clean packets and all required abstentions. Preparation and collection took 84.47 seconds. There were no reporting errors. Ten durable artifacts were verified; initial/final images are 1920×1440 and the replay contains 25 decodable frames. The study's finite S0 worker had exited when checked. The shared ledger then contained zero reservations, unsettled commitments and actual spend.

The [fleet post-mortem](reviews/fleet-s0-001-post.md) records evidence and next action. The already committed [Q0 preassessment](reviews/q0-001-pre.md) supplies clean competence thresholds, failure policy, cost limits and the visualization mapping. The subsequent [Q0 post-mortem](reviews/q0-001-post.md) confirms clean API competence. S1 scientific findings remain unresolved. The already committed [S1 preassessment](reviews/s1-001-pre.md) is ready, subject to a fresh claim and shared-budget check at launch.

Q0 returned 8/8 exact clean packets at each size, 100% field correctness and all 24 required missing-fact abstentions. It used 319,968 input and 604 output tokens, with usage reported for all 16 calls. Actual cost was $0.322988; conservative study reservations were $1.018967. Collection took 11.80 seconds, with rendering additional, and there were no reporting errors. All ten durable artifacts were verified. The unchanged frozen renderer regenerated the final views and 17-frame replay from saved observations in the matching environment, and the reporting verifier reproduced all packet hashes, graph metrics, check counts, grades and analyses. The finite worker had exited. At that snapshot, both follow-ups together had $0.366548 in actual spend, zero unsettled holds, and all 52 shared reservations settled under the $60 guard. See the small [verification record](q0-verification-summary.json).

## Public UI and retained evidence

The [experiment dashboard](https://swarm-live.pages.dev/#/x/sybil-budget-api) exposes synthetic metrics and permitted image artifacts. S0's [final heatmap](https://swarm-live.pages.dev/api/a/sybil-budget-api/4346fc36/final_frame.png), [retention companion](https://swarm-live.pages.dev/api/a/sybil-budget-api/4346fc36/retention.png) and [recorded completion replay](https://swarm-live.pages.dev/api/a/sybil-budget-api/4346fc36/replay.gif) are the publication targets. Decoding and durable artifact verification have passed. Q0's [final competence image](https://swarm-live.pages.dev/api/a/sybil-budget-api/7b177592/final_frame.png) and [17-frame completion replay](https://swarm-live.pages.dev/api/a/sybil-budget-api/7b177592/replay.gif) are published. Root verified public Q0 playback from 0/16 to 16/16 and the correct final per-size scores and $0.3230 displayed cost. S1 publication checks remain pending.

Assignment, world and episode histories, summaries and analyses remain in the authorized artifact store. No simulated identity conversations are invented for the replay. Root keeps the allocation valid through Q0, S1 and final uploads, verifies the finite workers have stopped, then releases it. No claim release or machine teardown is recorded here while S1 remains pending.

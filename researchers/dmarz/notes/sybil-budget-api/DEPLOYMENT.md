# Deployment record: sybil-budget-api

This exploratory study is deployed on `sim-dmarz-4` under the exclusive allocation `dmarz-sybil-followups`, used only by the two owner-authorized parallel follow-ups. Each study has its own finite worker, output directories, attempted-call cap and conservative reservation ledger. They share one locked spending guard. The owner explicitly waived independent review; own pre-run/post-run assessments, competence qualification and budget controls remain in force. Formal S2 is disabled.

## Frozen execution

- Public execution revision: `106d1082db3152af5bcf5e4539bca81adc13d57d`.
- Runtime fingerprint: `66ea4fe1465678ff66d099eec14ea11dbf5bc69063c00e3cc57249e06db98f08`.
- Runtime: Python 3.12 with the pinned requirements; pinned model `claude-haiku-4-5-20251001` for later API stages.
- Paid concurrency: two requests for this study, four combined across the two studies. Request timeout 120 seconds; stage limit four hours; 500 output tokens; no retries.
- Study ceiling: 3,200 attempted calls and $140 nonrefundable conservative reservations. Nominal plan: 16 Q0 plus 2,880 S1 calls, with exact combined conservative reservation $130.754844. Reservation is not actual billing.
- Shared follow-up guard: $60 of known actual use plus unsettled request reservations across both studies, within the owner's aggregate $500 API allowance. Unknown billing retains the full reservation. The root operator reconciles other experiment commitments before paid launch.

The private launcher checks the current claim and source fingerprint before starting a stage. Credentials are supplied through private environment aliases; no secret values, service addresses or server addresses are part of this record. Later documentation-only commits do not change the runtime fingerprint.

## Stage status

| Stage | Run | Status | Reconciliation | Model calls / cost |
|---|---|---|---|---|
| Fleet S0 | `sybil-budget-api/4346fc36` | Done, attempt 1; verified | 256 assigned, started, terminal, graded and analyzed; zero invalid/not-started | 0 / $0 |
| Q0 | Not launched at this record | Ready after verified S0 | Planned 16 clean calls; committed preassessment ready | Pending |
| S1 | Not launched at this record | Requires exact-runtime Q0 success | Planned 2,880 calls, 120 cells × 24 fresh worlds | Pending |

S0 covers all 120 grid cells on two engineering worlds plus 16 clean full/missing-fact fixtures. Both population sizes returned eight of eight exact clean packets and all required abstentions. Preparation and collection took 84.47 seconds. There were no reporting errors. Ten durable artifacts were verified; initial/final images are 1920×1440 and the replay contains 25 decodable frames. The study's finite S0 worker had exited when checked. The shared ledger then contained zero reservations, unsettled commitments and actual spend.

The [fleet post-mortem](reviews/fleet-s0-001-post.md) records evidence and next action. The already committed [Q0 preassessment](reviews/q0-001-pre.md) supplies clean competence thresholds, failure policy, cost limits and the visualization mapping. API competence and scientific findings are still unresolved; scripted success is not a model result.

## Public UI and retained evidence

The [experiment dashboard](https://swarm-live.pages.dev/#/x/sybil-budget-api) exposes synthetic metrics and permitted image artifacts. S0's [final heatmap](https://swarm-live.pages.dev/api/a/sybil-budget-api/4346fc36/final_frame.png), [retention companion](https://swarm-live.pages.dev/api/a/sybil-budget-api/4346fc36/retention.png) and [recorded completion replay](https://swarm-live.pages.dev/api/a/sybil-budget-api/4346fc36/replay.gif) are the publication targets. Decoding and durable artifact verification have passed; public browser playback must be checked separately before final closure.

Assignment, world and episode histories, summaries and analyses remain in the authorized artifact store. No simulated identity conversations are invented for the replay. Root keeps the allocation valid through Q0, S1 and final uploads, verifies the finite workers have stopped, then releases it. No claim release or machine teardown is recorded here while the paid stages remain pending.

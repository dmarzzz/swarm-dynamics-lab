# Deployment and closeout record

Experiment: compositional-safety. Owner/source: dmarz/patchwork-hypotheses. Host used: sim-dmarz. [Live dashboard](https://swarm-live.pages.dev/#/x/compositional-safety). This is separate from discussion-dose-v3.

q0-005 has ended and failed qualification: 24/24 valid, 21/24 safely complete, two approval-reuse violations and one incomplete report workflow. All 13 hub runs are done with 57 artifacts, the reporting spool is empty and worker PID 30702 exited. The [published results](records/q0-005/README.md) and [post-mortem](reviews/q0-005-post.md) are the closeout evidence. The user instructed publication of results and the [next plan](reviews/d0-003-pre.md), with no next run. d0-003 is not registered, implemented or started.

## Runtime and allocations

The isolated checkout is `/srv/swarm/compositional-safety/swarm-lab`; the pinned environment is `/srv/swarm/compositional-safety/venv`. Python 3.12.3, PyYAML 6.0.2 and Pillow 11.3.0 were used. Reporting uses the provisioned module at `/usr/local/lib/swarm`; non-login shells require `PYTHONPATH=/usr/local/lib/swarm`. Commands recorded below ran inside the experiment directory with `SWARM_SOURCE=dmarz/patchwork-hypotheses`. These are historical launch records, not instructions to replay attempts.

The original exclusive claim dmarz-compositional-safety was created through agentops PR 56 and released through PR 93 at 2026-10-04 03:59:19 UTC after uploads completed and its worker exited. The later repair allocation dmarz-compositional-repair came through PR 105 with recorded expiry 2026-10-04 07:09:09 UTC and covered i0-003 through q0-005. That claim was released through merged agentops PR 146 at 2026-10-04 04:55:23 UTC; status done was verified on origin/main. No claim is held for another run. A future authorized attempt needs a fresh merged exclusive claim; historical deployment or available credentials do not authorize another run. No infrastructure provisioning was needed for this repair.

No credentials, private endpoints or server addresses belong in this record. Approved API aliases were injected in process memory and hub configuration came from the host. Code, results and cumulative accounting are retained after worker exit.

## Frozen attempts

| Attempt | Source revision | Historical command / disposition |
|---|---|---|
| s0-001 | 84fad81e3b8732e195a24f9ef4cf1a09ef76c7b5 | `python src/worker.py S0 s0-001` |
| q0-001 | 70ca3754b63257e709970ce3c79e3c483679eace | `python src/worker.py Q0 q0-001` |
| q0-002 | b7eec0facb5535efc45478677df56afebbeae95f | `python src/worker.py Q0 q0-002` |
| q0-003 | 45a01456e930463a99fa5eb9aee5bad26a453a37 | `python src/worker.py Q0 q0-003` |
| i0-001 | 232dad10f175006ee0f1a778346b6d7d355f2b1d | `python src/probe.py i0-001` |
| i0-002 | 0911e343031078af1e8e4de8f5a5018ffebe6535 | `python src/probe.py i0-002` |
| q0-004 | a286ec4c7712eb8cf9221b60455fc440a56434e7 | `python src/worker.py Q0 q0-004` |
| i0-003 | c4c69163575d7711b0f9fa974fadcaf4c9b733f0 | `python src/probe.py i0-003` |
| i0-004 | 1630e826f53b834755262b8dde89221dad0a120c | `python src/probe.py i0-004` |
| d0-001 | No dispatched worker | Registered then withdrawn; zero model calls |
| d0-002 | bcd4033f210c38c0ff1f6eed8843d9bebd486436 | Eight original/clarified diagnostic episodes; complete |
| q0-005 | a20b97c1c0544b787edccb78f4f27e21487dd2cf | `python src/worker.py Q0 q0-005`; complete, qualification failed |
| d0-003 | Plan only | No executable registration, allocation or launch |

Each executed attempt has its own frozen review and immutable evidence. The finite worker neither restarts itself nor retries model calls. Historical failures are not overwritten by later interface or model changes.

## q0-005 launch and verification

Before dispatch, all 18 local/server tests passed. The immutable public plan was visually verified, registered and bound to source/content through runtime admission. q0-005 then ran 24 fresh development episodes on roots 240–242 using pinned Haiku 4.5, temperature zero and the adopted execution-v2 contract. The root/domain combinations contain five structural fingerprints, not 24 independent tasks.

Separate same-team verification reproduced all 176 delivered packets, transitions and evaluator scores, including visible approval consumption before both D2 violations and the unused safe packaging opportunities in the D1 stall. This audit is not independent external researcher review. The source and design were frozen throughout; publication edits do not modify their hashes.

The run used 176 calls, 265,263 input tokens and 3,566 output tokens, $0.283093 reported actual cost, $2.037907 retained reservations and 363.317182 seconds. Thirteen terminal hub runs and 57 artifacts are verified; uploads are complete and no worker remains. Hub status done denotes execution termination, not qualification.

## Retained accounting and handoff

The same cumulative accounting/study.jsonl remains in the checkout across revisions. At q0-005 closeout it contains 1,918 calls, $5.855114 reported actual cost and $31.684717 retained reservations. The unchanged study ceiling is 9,216 calls and $185 reserved within the shared $500 owner authority. Failed calls consume retained reservations; unknown usage and reported actual cost are separate. This local ledger does not centrally enforce spending by other studies.

A new folder, process or claim must not reset accounting or permit replaying an attempt ID. No current accounting headroom overrides the user's instruction not to start another run. Preserve all code, results, claims and failed cohorts in history. After publication, stop; a future authorized successor must first satisfy the prerequisites in [SETUP.md](SETUP.md) and its prospective plan. P1 and formal S1/S2 remain closed.

# Experiment setup record: market-split-haiku V3

Updated 2026-10-04 by dmarz/market-split. This record is retrospective for completed/active stages; their committed pre-run assessments remain the prospective evidence. It does not invent missing historical receipts. Follow [the setup runbook](../../../toolkit/agent-experiments/EXPERIMENT-SETUP.md).

## Ownership and question

- Owner, operator and design assessor: dmarz/market-split. No independent researcher review is claimed.
- Question: does a neutral profit-seeking owner discover identity splitting under firm-based concentration rules? Primary exploratory contrast: flexible-arm sustained concentration masking, firm minus owner regulation.
- Status: exploratory instrument in researcher notes. Formal survey/hypothesis gates remain incomplete; S2 disabled and holdout 1000–1999 unopened.
- Previous failure and repair: [S1-001 post-mortem](reviews/s1-001-post.md), [issue ledger](ISSUES.md), [Q0-002 post-mortem](reviews/q0-002-post.md). Total output headroom increased; ordinary actor prompt, economy and renderer did not change.
- Current stage: R0-001 stopped after a capacity failure. All four assigned bundles are terminal: one done, one failed, two cancelled. See [post-mortem](reviews/r0-001-post.md) and [results](RESULTS.md). User's current instruction permits preparing the [next experiment plan](NEXT-EXPERIMENT.md) but prohibits starting it.

## Gate evidence

| Gate | Status | Evidence / assessor 2026-10-04 | Next action |
|---|---|---|---|
| G0 question and formal research gates | Partial | Exploratory question and prior scripted study exist; formal gates incomplete | Keep claims exploratory; no S2 |
| G1 prospective design | Pass for V3 stages | [README](README.md), [preregistration/amendments](preregistration.md), stage pre-assessments, owner self-assessment | Future S1 assessment remains unstarted |
| G2 instrument | Pass in bounded checks | S0-fleet-003: 17 offline checks, 12 mock episodes, 42 verified artifacts, 96 exactly replayed actions | Preserve frozen hashes |
| G3 current attempt | Historical admission recorded | [R0 pre-assessment](reviews/r0-001-pre.md), [deployment](deployment.md), exclusive claim and finite worker | Preserve historical evidence; do not claim a newly added public-preflight helper ran historically |
| G4 qualification | Failed R0 | D0 two terminal legal responses, I0 six legal operations, Q0 four valid/profitable episodes above unchanged 75% floor | 3 complete,1 invalid,4 unstarted; numeric validity failed. No escalation. |
| G5 closeout | Complete for R0 | Published results/post-mortem;14run+5analysis artifacts byte-verified;94calls replayed;claimPR148released;temporaryhostdestroyed afterPR150 | Next diagnostic remains unstarted |

## Design and instrument index

- [Frozen design](design.yaml), [preregistration](preregistration.md), [ordinary prompt](src/prompt.txt), [simulator/evaluator](src/sim.py), [worker](src/worker.py), [coordinator](src/coordinator.py).
- Haiku 4.5, requested thinking 2,048 / total output 8,192, no temperature override. Source `8e355a187d212ece4c6469c5fdd949c06641e52c44d785382c834817e5b2a465`; design `bdcbdbcf7d25d0de64e4187272b9bb50557180e281ad00f61b18b38bc3238530`. Runtime is pinned in deployment.md.
- R0: two market tasks 78/79, seed31, firm/owner rules, both arms, 24 rounds; 4 bundles / 8 episodes / 192 calls. These are two related development markets, not 192 independent trials. No splitting threshold gates qualification.
- Each episode resets stateless model context. Mechanics-only mandates do not enter ordinary episodes. Future shocks, hypothesis labels and evaluator ownership overlays stay out of actor packets. Saved observations/actions permit exact simulation replay.
- The coordinator enforces parent source/design/qualification checks; the finite launcher holds a host lock. Separate review is required before each stage. Do not equate documentation with automatic admission enforcement.
- Visualization: mapping market-split-api-v1, defined in the pre-assessment, all 24 logical rounds retained; live frame, final PNG and GIF replay. Missing data stays missing.

## Current attempt admission

- R0-001, parent Q0-002; [pre-review](reviews/r0-001-pre.md). Assigned source commit `8bf90bfa934d886514d083c6b47ffcd288f6cd0b`.
- Public live view: https://swarm-live.pages.dev/#/x/market-split-haiku. Current README registration is pinned to `e36408b372a3ffa914a8adbee19b2cc82b56958b`; the page was verified to show V3's 8,192 ceiling and required R0. This later display update is not retroactive preregistration of the original run start.
- Existing owner authority: shared $500 API pool, study lifetime cap 1,200 calls. R0 baseline 140 calls / $1.093064; max 192 new calls / conservative $12.490752 reservation. No retries or budget reset.
- Dedicated sim-dmarz-market-haiku; exclusive claim dmarz-market-split-haiku through 2026-10-04 10:09:38 UTC. One active assignment, locked finite worker, max four bundles, 90-second requests and two-hour dispatch cap.
- Approved Swarm Lab account and original infrastructure state verified privately before create-only provision; no identifiers published. Full earlier 100-call ledger migrated with matching SHA256. Credentials only approved process-environment aliases.
- New S1 admission is **blocked** by the user's instruction not to start the next experiment. No S1-002 queue or worker is authorized by this record.

## Attempt and repair history

All pre/post reviews remain in [reviews](reviews/). V1 mechanics failure, V2 qualified short runs and V2 full-length truncations remain separate from V3 diagnosis, mechanics, profit screen and R0. The two exact saved diagnostic observations returned legal actions within the old ceiling, so diagnosis alone did not establish a causal benefit of increasing it. Q0's minimum 75.49% reference ratio narrowly passes the unchanged floor; this is not general optimality. R0 audit reproduced a separate strict capacity failure (H4); no truncation was observed in94calls, but qualification failed.

## Closeout

Execution, response validity, qualification, scientific conclusions, process compliance and delivery are reported separately in R0's post-mortem. Every attempt and the complete cost ledger were archived before claim release and verified temporary-host destruction. Publish analysis and updated evidence metadata using independent market counts. Leave the next plan unstarted; no automatic discovery launch follows a qualification pass.

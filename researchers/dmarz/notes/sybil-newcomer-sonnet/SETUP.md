# Experiment setup record: sybil-newcomer-sonnet v1

Status: S0 admitted; Q0 and S1 BLOCKED on review (see G0). Follows [the setup runbook](../../../../tooling/agent-experiments/EXPERIMENT-SETUP.md). Historical receipts and attempts are preserved below.

## Ownership and question

- Owner / operator / design reviewer / review independence: owner dmarz; operator dmarz/newcomer-sonnet (Claude Code on orbital-one, started by dmarz/orbital-orchestrator under dmarz's 2026-10-04 instruction to keep at least three dmarz experiments running). No design reviewer. No independent review has occurred. The owner's review waiver for [sybil-newcomer-api](../sybil-newcomer-api/WAIVER.md) covers that study only.
- Question, intended decision, primary contrast and claim boundary: does the newcomer-study result depend on the synthesizing model? Primary contrast unchanged (renewal minus reputation specialist accuracy, 16 identities, sleeper, round 8; +10 pp marker). Decides whether the Haiku finding is about admission or about synthesizer weakness. Claims are limited to this synthetic task.
- Research status: exploratory model replication in notes; no accepted hypothesis.
- Prior art, survey/hypothesis gates and reviews: as for the parent study; no new survey or hypothesis. Formal S2 disabled.
- Previous study/post-mortem and lessons incorporated: [Haiku S1 post-mortem](../sybil-newcomer-api/reviews/s1-001-post.md), [Haiku results](../sybil-newcomer-api/RESULTS.md). Lesson: low available truth after admission bounds any synthesizer, which motivates this model check.
- Current stage / next action / exact blocker and responsible owner: fleet S0. Q0 needs either dmarz's explicit per-experiment waiver of cross-researcher review or a filed review from another researcher (task `review-sybil-newcomer-sonnet`). Responsible: dmarz.

## Gate evidence

| Gate | Status | Evidence, timestamp and assessor | Blocker / next action |
|---|---|---|---|
| G0 Question and applicable research gates | blocked | 2026-10-04 dmarz/newcomer-sonnet: question and claim boundary written; review neither performed nor waived | dmarz waiver or cross-researcher review before Q0 |
| G1 Plan written before implementation | pass | README (public plan sections), preregistration.md, design.yaml committed before any fleet stage | — |
| G2 Instrument and offline checks | pass | 8/8 selftests; local S0 198/198 valid, qualification passed; Q0/S1 assignment IDs, packet hashes, expected answers and dispatch order equal to sybil-newcomer-api (digests Q0 3618407e334e40da, S1 036295a938cf8235) | — |
| G3 Current attempt admission | S0 only | [fleet-s0-001-pre](reviews/fleet-s0-001-pre.md); launcher checks exclusive claim and immutable public plan | Q0 admission blocked by G0 |
| G4 Qualification before scientific escalation | pending | | Q0 must pass unchanged thresholds |
| G5 Reconciliation and closeout | pending | | |

## Design and instrument index

- Plan: [README.md](README.md), [preregistration.md](preregistration.md), [design.yaml](design.yaml), [experiment.yaml](experiment.yaml).
- Independent units: 24 world clusters (7100–7123), paired across 3 identity counts × 3 policies × 3 strategies × 3 sampled rounds = 1,944 S1 calls; paired by assignment ID with the Haiku cohort.
- Splits: engineering 6900–6901 (S0), qualification 7000–7005 (Q0), study 7100–7123 (S1), S2 range 12000–12999 unopened.
- Model/provider/config: `claude-sonnet-4-6`, temperature 0, structured JSON, max 500 output tokens, 120 s timeout, 2 workers, no retries, $3/$15 per million tokens.
- Source deltas from parent: experiment id in coordinator/worker, model id and prices in design.yaml, banner text in render.py, shared budget partition removed from provider.py and its selftest. Simulator, study, analysis and prompts unchanged.
- Visualization: [VISUALIZATION.md](VISUALIZATION.md) (inherited mapping v1 with run bindings).

## Current attempt admission

Operations entry: explicitly manual (private launcher `scripts/run-sybil-newcomer-sonnet.py` in the operator infrastructure repository).

| Operation | Exact command or unsupported reason | Evidence and last checked revision |
|---|---|---|
| Inspect and offline validation | `python3 src/selftest.py`; `python3 src/worker.py --stage S0 --attempt <fresh>` | reviews/s0-local-001-post.md |
| Prepare named stage | `run-sybil-newcomer-sonnet.py <rev> setup` | DEPLOYMENT.md |
| Dispatch named stage | `run-sybil-newcomer-sonnet.py <rev> S0|Q0|S1` | DEPLOYMENT.md |
| Resume interrupted execution | unsupported: no automatic re-execution; a new attempt needs a new batch and pre-review | — |
| Analyze saved evidence and rebuild visuals | `run-sybil-newcomer-sonnet.py <rev> verify|publish`; `reporting/*.py` | — |
| Stop this study and close out | stop worker over ssh, verify, then `agentops.py release dmarz-sybil-newcomer-sonnet --status done` | — |

- Budget: own ledger; 2,050 attempted calls; $75 reservation ceiling; nominal Q0+S1 reservation $61.73; expected actual about $10; within dmarz's $500 shared allowance.
- Allocation: sim-dmarz-5, exclusive claim `dmarz-sybil-newcomer-sonnet` (agentops PR 162), verified idle with no worker before claiming.
- Credentials: existing dmarz model-configuration aliases decrypted by the launcher and passed over SSH stdin to process memory; no values recorded.

## Attempt and repair history

| Attempt / parent | Stage / version | Pre-review and receipts | Assigned / started / terminal / graded / analyzed | Post-mortem / disposition |
|---|---|---|---|---|
| s0-local-001 | local S0 v1 | reviews/s0-local-001-pre.md | 198/198/198/198/198 | reviews/s0-local-001-post.md: advance |

## Closeout

Pending.

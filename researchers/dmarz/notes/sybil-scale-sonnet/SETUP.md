# Experiment setup record: sybil-scale-sonnet v1

Status: exploratory model replication; setup record maintained per [the setup runbook](../../../../tooling/agent-experiments/EXPERIMENT-SETUP.md). Not launch authorization by itself; each stage's pre-run assessment governs.

## Ownership and question

- Owner dmarz; operator dmarz/scale-sonnet (Claude Code on orbital-one); design inherited from dmarz/sybil-specialists' [sybil-scale-api](../sybil-scale-api). No independent design review for this replication; dmarz's standing directive for his own exploratory studies applies, and nothing here claims an independent review.
- Question: do the Haiku scaling results hold with claude-sonnet-4-6 on identical worlds and packets? Primary contrast unchanged (coverage, visible, pass 0.10, proportional minus fixed at N=972). Claim boundary: one graph family, simulated identities, exploratory.
- Research status: exploratory replication. Survey/hypothesis gates not met; S2 disabled.
- Prior study and lessons: [sybil-scale-api RESULTS](../sybil-scale-api/RESULTS.md), [its S1 post-mortem](../sybil-scale-api/reviews/s1-001-post.md); lessons kept: long packets need preparation heartbeats (already in worker), Python 3.12 for exact reproduction.
- Current stage / next action: see the gate table.

## Gate evidence

| Gate | Status | Evidence, timestamp and assessor | Blocker / next action |
|---|---|---|---|
| G0 Question and applicable research gates | pass (exploratory scope) | README, preregistration; 2026-10-04 dmarz/scale-sonnet | none for exploratory S0/Q0/S1; S2 stays disabled |
| G1 Plan written before implementation | pass | README/preregistration/reviews committed before any fleet stage | — |
| G2 Instrument and offline checks | pass | 9/9 selftests; local S0 264/264; assignment/packet/prompt equivalence with Haiku study ([local-s0-001-post](reviews/local-s0-001-post.md)) | — |
| G3 Current attempt admission | pass (S0, Q0, S1) | claim dmarz-sybil-scale-sonnet (agentops PR 164); revision f18f66da; runtime a1a619f7 for all stages; pre-run files in reviews/ | re-check for any new attempt |
| G4 Qualification before scientific escalation | pass | Q0 run 5fe6c41a 64/64, every size 1.0 ([post](reviews/q0-001-post.md)) | — |
| G5 Reconciliation and closeout | pending | S1 run afd8d5b9 running since 05:40Z | verify, results, post-mortem, release claim |

## Design and instrument index

- Plan: README.md, preregistration.md, design.yaml (this directory); history in git.
- Independent units: 24 world clusters (S1); 4 qualification worlds (Q0); 2 engineering worlds (S0). Calls per world: 100 deduplicated conditions.
- Sample size: fixed by the original design to allow world-paired comparison with the Haiku cohort; not powered for small model differences.
- Splits: engineering 4900–4901, qualification 5000–5003, S1 6000–6023, holdout 10000–19999 unopened.
- Agent definition: one stateless synthesizer call per assignment; prompt and schema in src/provider.py (digest identical to the Haiku study).
- Versions: model claude-sonnet-4-6; requirements.txt pinned; runtime source hash recorded per run.
- Offline checks: selftest (anchor equality, graph scaling, blind packets, ledger cap/duplicates, render failure states, principal-blind checks, splits, invalid answers, concurrent failure denominators).
- Launcher gate integration: coordinator refuses duplicate batches and requires exactly one passed prerequisite stage at the same source hash; private launcher refuses without an exclusive merged claim.
- Visualization: [VISUALIZATION.md](VISUALIZATION.md) v1.

## Current attempt admission

Operations entry: manual (private launcher). [Operations guide](../../../../tooling/agent-experiments/OPERATIONS.md).

| Operation | Exact command or unsupported reason | Evidence and last checked revision |
|---|---|---|
| Inspect and offline validation | `python3 src/selftest.py`; `python3 src/worker.py --stage S0 --attempt <name>` | local-s0-001 |
| Prepare named stage | `python3 scripts/run-sybil-scale-sonnet.py <commit> setup` (agentops) | per stage |
| Dispatch named stage | `… <commit> S0|Q0|S1` | per stage |
| Resume interrupted execution | unsupported by design: no automatic re-execution; a new attempt id is required | — |
| Analyze saved evidence and rebuild visuals | `… <commit> status|verify|publish`, `--save <path>`; reporting/build_report.py | after S1 |
| Stop this study and close out | stop worker, verify uploads, `agentops.py release dmarz-sybil-scale-sonnet --status done` | — |

- Credentials: dmarz model-key aliases from agentops SOPS, memory-only via SSH stdin; never in argv or on disk.
- Budget: USD 240 study reservation cap, 2,600 calls; draws on dmarz's shared USD 500 allowance.
- Allocation: sim-dmarz-3, exclusive claim dmarz-sybil-scale-sonnet (recorded in DEPLOYMENT.md once merged).

## Attempt and repair history

| Attempt / parent | Stage / version | Pre-review and receipts | Assigned / started / terminal / graded / analyzed | Post-mortem / disposition |
|---|---|---|---|---|
| local-s0-001 / — | S0 offline / v1 | (offline engineering check) | 264/264/264/264/264 | [advance](reviews/local-s0-001-post.md) |
| fleet-s0-001 (55c86cfa) / local-s0-001 | S0 fleet / v1 | [pre](reviews/fleet-s0-001-pre.md) | 264/264/264/264/264 | [advance](reviews/fleet-s0-001-post.md) |
| q0-001 (5fe6c41a) / fleet-s0-001 | Q0 / v1 | [pre](reviews/q0-001-pre.md) | 64/64/64/64/64 | [advance](reviews/q0-001-post.md) |
| s1-001 (afd8d5b9) / q0-001 | S1 / v1 | [pre](reviews/s1-001-pre.md) | 2400 assigned; running | pending |

## Closeout

Pending.

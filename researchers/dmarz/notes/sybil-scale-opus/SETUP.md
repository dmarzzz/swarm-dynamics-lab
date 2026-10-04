# Experiment setup record: sybil-scale-opus v1

Status: exploratory model replication; setup record maintained per [the setup runbook](../../../../tooling/agent-experiments/EXPERIMENT-SETUP.md). Not launch authorization by itself; each stage's pre-run assessment governs.

## Ownership and question

- Owner dmarz; operator dmarz/scale-opus (Claude Code on orbital-one); design inherited from dmarz/sybil-specialists' [sybil-scale-api](../sybil-scale-api) via the Sonnet copy [sybil-scale-sonnet](../sybil-scale-sonnet).
- Question: do the Haiku/Sonnet scaling results hold with claude-opus-5-5 (no temperature, adaptive thinking at effort low) on identical worlds and packets? Primary contrast unchanged. Claim boundary: one graph family, simulated identities, exploratory; configuration differs from earlier cohorts beyond the model.
- Research status: exploratory replication. Survey/hypothesis gates not met; S2 disabled.
- Prior studies and lessons: [sybil-scale-api RESULTS](../sybil-scale-api/RESULTS.md), [sybil-scale-sonnet RESULTS](../sybil-scale-sonnet/RESULTS.md) and [its S1 post-mortem](../sybil-scale-sonnet/reviews/s1-001-post.md); lessons kept: run `publish` before `verify` (artifact order), Python 3.12 for exact reproduction, admission is model-independent.
- Current stage / next action: see the gate table.

## Gate evidence

| Gate | Status | Evidence, timestamp and assessor | Blocker / next action |
|---|---|---|---|
| G0 Question and applicable research gates | pass (exploratory scope); cross-researcher review waived by owner | README, preregistration; 2026-10-04 dmarz/scale-opus. Authority: dmarz's relayed instruction "use opus for everything going forward please" (dmarz/fleet-monitor, ~07:36Z) and his first-hand standing statement in the operating session ~07:55Z: "Great messages starting [fleet-monitor] as my instructions including claims lUcnhes model switches And budget costs thanks And stop Asking for my permission". Owner waiver only: no independent review performed. | none; S2 stays disabled |
| G1 Plan written before implementation | pass | README/preregistration/reviews committed before any fleet stage or model call | — |
| G2 Instrument and offline checks | pass | 10/10 selftests incl. mocked Opus request/response contract (no temperature/thinking/tool_choice/fallbacks; effort low; thinking blocks filtered; refusal and output-cap categories; answer-length limit); local S0 264/264 ([post](reviews/local-s0-001-post.md)) | — |
| G3 Current attempt admission | per stage | claim dmarz-sybil-scale-opus on sim-dmarz-12; pre-run files in reviews/ | re-check before each stage |
| G4 Qualification before scientific escalation | pending | fleet S0 then Q0 at the same source hash | Q0 must pass every size |
| G5 Reconciliation and closeout | pending | — | after S1 |

## Design and instrument index

- Plan: README.md, preregistration.md, design.yaml; history in git.
- Independent units: 24 world clusters (S1); 4 qualification worlds (Q0); 2 engineering worlds (S0). 100 deduplicated conditions per world.
- Sample size: fixed by the original design for world-paired comparison with the earlier cohorts; not powered for small model differences.
- Splits: engineering 4900–4901, qualification 5000–5003, S1 6000–6023, holdout 10000–19999 unopened.
- Agent definition: one stateless synthesizer call per assignment; prompt and schema in src/provider.py (unchanged text).
- Versions: model claude-opus-5-5, effort low; requirements.txt pinned; runtime source hash recorded per run.
- Launcher gate integration: coordinator refuses duplicate batches and requires exactly one passed prerequisite stage at the same source hash; private launcher refuses without an exclusive merged claim. Chained automatic stage escalation was not built (refused by the operator's permission guard); stages are launched one at a time.
- Visualization: [VISUALIZATION.md](VISUALIZATION.md) v1.

## Current attempt admission

| Operation | Exact command or unsupported reason | Evidence |
|---|---|---|
| Offline validation | `python3 src/selftest.py`; `python3 src/worker.py --stage S0 --attempt <name>` | local-s0-001 |
| Prepare / dispatch | `python3 scripts/run-sybil-scale-opus.py <commit> setup|S0|Q0|S1` (agentops) | per stage |
| Resume interrupted execution | unsupported by design; a new attempt id is required | — |
| Analyze | `… <commit> status|publish|verify [--save <path>]`; reporting/build_report.py, reporting/compare_models.py | after S1 |
| Close out | stop worker, verify uploads, `agentops.py release dmarz-sybil-scale-opus --status done` | — |

- Credentials: dmarz model-key aliases from agentops SOPS, memory-only via SSH stdin; never in argv or on disk.
- Budget: USD 600 study reservation cap, 2,600 calls; cost not a launch gate by owner instruction; actuals reported to the hub.
- Allocation: sim-dmarz-12 (new), exclusive claim dmarz-sybil-scale-opus.

## Attempt and repair history

| Attempt / parent | Stage / version | Pre-review | Assigned / started / terminal / graded / analyzed | Post-mortem / disposition |
|---|---|---|---|---|
| local-s0-001 / — | S0 offline / v1 | (offline engineering check) | 264/264/264/264/264 | [advance](reviews/local-s0-001-post.md) |

## Closeout

Pending.

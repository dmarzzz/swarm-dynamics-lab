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


## Status 2026-10-04 ~08:35Z: deferred, launch-ready

Deferred by the coordinator (dmarz/orchestrator-2) in favour of the run-queue:ready lane (sybil-scarcity-opus takes the next free box, sim-dmarz-2), and because the results analyst forecasts that the model is not the lever in the sybil studies (partial paired budget-sonnet read: Sonnet minus Haiku about +5.9 points, frontier cells unchanged), so this cohort has low information value per server-hour. No claim, server, fleet run or model call exists for it. Launch-ready state: source hash `621c867c6ff495da807988b90807ed7c82642c6112bc91c74271618572d0c96a` (swarm-lab `1a6fdbc1`, 429/529 retry + P0 probe, local S0 264/264), launcher `scripts/run-sybil-scale-opus.py` on agentops main (`244e726`, host from the merged claim, P0 action). To resume: claim a free dmarz box as dmarz/scale-opus, then `setup`, `S0`, `publish`, `P0`, `Q0`, `S1`.

## Status 2026-10-04 ~10:55Z: resumed

Resumed by dmarz/orchestrator-2 on sim-dmarz-13 (freed by sybil-split-opus). Reason: only two dmarz runs were live against Dan's standing goal of five, the ready queue was empty, and the boxes reserved for program v5 (sim-dmarz-2, -8, -10) are not used. Source hash and configuration unchanged from the deferred launch-ready state (Opus 5.5, effort low, 429/529 retry). Night rule (fleet-monitor relay of Dan, ~10:40Z): if a stage stops on a provider limit or credit error that does not clear within 20 minutes, relaunch it as a new dated attempt on claude-opus-5 with a fresh probe and qualification, gates unchanged, results labelled by model and never pooled.

## Handover 2026-10-04 ~11:20Z (operator may be cut off)

- Server sim-dmarz-13, claim `dmarz-sybil-scale-opus` (agentops #267, by dmarz/scale-opus, until ~19:00Z). Revision `80d70b7a9ec6ad489a0e36a3acfd704d488dada2`.
- S1 run `sybil-scale-opus/79bb3882` (2,400 calls) started ~11:05Z by `scripts/run-sybil-scale-opus.py <rev> S1`: one `src/worker.py --hub` process under `timeout`, log `/srv/swarm/sybil-scale-opus-lab/researchers/dmarz/notes/sybil-scale-opus/results/s1-001-worker.log`.
- From ~/swarm-labs-agentops with `set -a; . ./.env; set +a; export SOPS_AGE_KEY_FILE=$HOME/swarm-labs-agentops/keys.txt`: `python3 scripts/run-sybil-scale-opus.py 80d70b7a9ec6ad489a0e36a3acfd704d488dada2 status` (worker_active false = ended), then `publish`, then `verify --save <file>`.
- Remaining after it ends: publish, verify, RESULTS.md + reviews/s1-001-post.md (three-model paired comparison vs sybil-scale-api/56defc84 and sybil-scale-sonnet/afd8d5b9, using reporting/compare_models.py), evidence row, `python3 scripts/agentops.py release dmarz-sybil-scale-opus --status done`.

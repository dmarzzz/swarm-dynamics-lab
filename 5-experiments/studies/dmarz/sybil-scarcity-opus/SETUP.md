# Experiment setup record: sybil-scarcity-opus / attempt 001

Status: preparation only. Nothing has run; this record is not launch authorization. Maintained per [the setup runbook](../../../toolkit/agent-experiments/EXPERIMENT-SETUP.md) and the [ready-chain contract](../pipeline/READY-CHAIN.md). Created 2026-10-04 by dmarz/pipeline-scarcity.

## Ownership and question

- Owner dmarz. Builder dmarz/pipeline-scarcity (Claude Code on dmarz's Mac), under the pipeline lead dmarz/pipeline. Operator: the orchestrator that takes the request from the private run queue; not assigned by this record. Review: cross-researcher review is waived by dmarz for these exploratory runs (relayed by dmarz/fleet-monitor, 2026-10-04); dmarz/fleet-monitor's check of the package (go, with 2 requests in flight) is a same-researcher check. No independent review exists or is claimed. dmarz did not name this study; the fleet monitor chose it from his backlog under his instruction to keep a pipeline of prepared experiments running ([AMENDMENTS.md](AMENDMENTS.md)).
- Question: at the 972-identity world of sybil-scale-api, with graph, audits, admission and attacker reports held identical, does cutting the truthful carriers of each rare fact from 81 to 1 lower the synthesizer's specialist accuracy? Primary contrast: 1 carrier minus 81 carriers at random auditing, 108 checks, attacker check-pass 0.1. Practical marker: a 10-point decrease. Claim boundary: one synthetic task, one graph family, simulated identities, one model.
- Research status: exploratory follow-up in researcher notes. No complete survey and no accepted hypothesis; the formal gates are not met and are not claimed. S2 is disabled.
- Prior work and lessons: [the plan](../sybil-scarcity-plan/README.md) and its [setup record](../sybil-scarcity-plan/SETUP.md); [sybil-scale-api results](../sybil-scale-api/RESULTS.md); [sybil-scale-xl amendment A1](../sybil-scale-xl/AMENDMENT-A1.md) and its [probe measurement](../sybil-scale-xl/reviews/q0-a1-pre.md); [cross-lane lessons](../pipeline/LESSONS.md) items 1 to 3 (caps and timeouts sized before qualification; settled-cost ledger; Opus 5.5 request shape, both thinking block types dropped).
- Current stage and next action: see the gate table.

## Gate evidence

| Gate | Status | Evidence, timestamp and assessor | Blocker / next action |
|---|---|---|---|
| G0 Question and applicable research gates | pass for exploratory scope only | [README](README.md), [plan](../sybil-scarcity-plan/README.md); 2026-10-04, dmarz/pipeline-scarcity (same researcher) | Formal survey and hypothesis gates are not met; S2 stays disabled |
| G1 Plan written before implementation | pass | README, [preregistration](preregistration.md), [AMENDMENTS](AMENDMENTS.md), [design.yaml](design.yaml) and this record were committed before any file under `src/`; 2026-10-04, dmarz/pipeline-scarcity | — |
| G2 Instrument and offline checks | pass offline (builder's own checks; Python 3.9.6 on macOS) | 2026-10-04, dmarz/pipeline-scarcity, at code commit `30e34577`, source hash `b37af997…`: selftest 33 of 33; offline S0 168 of 168 with 20 of 20 invariants; manifest check equal; rehearsal 17 of 17 checks (full chain exit 0 and verify ok; failed-qualification chain stops at Q0 with exit 3 and no S1 run). Details in the [pre-run review](reviews/chain-001-pre.md). dmarz/pipeline reports having rerun the four checks at the earlier pin | Not tested: Python 3.12, the real hub, the private launcher, a real model response. The launcher's `setup` reruns the selftests on the server |
| G3 Current attempt admission | pass | [Pre-run review](reviews/chain-001-pre.md) on main; claim `dmarz-sybil-scarcity-opus` on sim-dmarz-2 (agentops #249); `run-ready-chain.py setup` at `3ebef1ce` passed 33/33 selftests and source hash `b37af997…`; 2026-10-04 09:11–09:17Z, dmarz/orchestrator-2 | none |
| G4 Qualification before scientific escalation | pass | S0 168/168 with all invariants; P0 1/1; Q0 48/48, every carrier profile 100% fields, 100% exact, 24/24 withheld nulls; 2026-10-04, chain gates (software) | none |
| G5 Reconciliation and closeout | pass | `verify` exit 0, all checks, all stages; [post-run review](reviews/chain-001-post.md); [RESULTS](RESULTS.md); claim released; 2026-10-04 ~10:20Z, dmarz/orchestrator-2 | none |

## Design and instrument index

- Plan and amendments: [README.md](README.md), [preregistration.md](preregistration.md), [AMENDMENTS.md](AMENDMENTS.md), [design.yaml](design.yaml); source plan [sybil-scarcity-plan](../sybil-scarcity-plan/README.md) (frozen, not edited). History in git.
- Independent units: 24 world roots (S1), 8 qualification roots (Q0), 2 engineering roots (S0), 1 probe packet from engineering root 7790 (P0). 60 conditions per root; 1,440 S1 assignments.
- Sample size: fixed by the plan at 24 paired roots. Exploratory precision only; no power claim; no pilot estimate of this manipulation exists.
- Splits: engineering 7790 to 7791; S1 7800 to 7823; Q0 7900 to 7907; holdout 10000 to 19999 unopened. All task ids are below 10000.
- **Root-range recheck, 2026-10-04, at main `69cb6a28`.** The plan required a fresh scan before use. Method: every `.yaml`, `.yml`, `.md`, `.py`, `.toml`, `.sh` and `.txt` file under `lab/researchers/`, `experiments/`, `tooling/`, `4-hypotheses/`, `tasks/`, `2-surveys/` and `3-synthesis/` was searched for 7790, 7791, 7800 to 7823 and 7900 to 7907 as whole numbers; every `.json` and `.jsonl` file under 5 MB was searched for `task`, `world`, `root`, `seed`, `world_id`, `task_id` or `world_seed` keys with those values; design, preregistration, manifest, plan, config and experiment files were also searched for number ranges that span 7790 to 7907. 2,930 files scanned; the plan directory and this directory excluded. Result: 0 exact matches and 0 spanning ranges. The scan covers this repository only; it is not a reservation, and a private or unpushed study could still use these numbers.
- Agent definition: one stateless synthesizer call per assignment; system prompt and schema of sybil-scale-api; model `claude-opus-5-5`, effort low.
- Versions: `requirements.txt` pinned; source hash from `study.source_hash()` over `design.yaml`, `experiment.yaml`, `requirements.txt` and `src/*.py`; source hash in [READY.yaml](READY.yaml); code commit and source hash in the pre-run review.
- Offline checks: `src/selftest.py` (33 tests: parent-simulator equality, byte-identical 81-carrier packets, prompt and schema equality, all S0 invariants, carrier nesting, leak checks, grading, clean fixtures, qualification thresholds, probe gate, request body keys, thinking and redacted-thinking blocks, refusal and other failure categories, transport retry rule, ledger caps, worker failure accounting, coordinator gates, chain stops, projection gate, verify tampering, analysis bounds, frames and GIF, manifest regeneration, READY consistency, no secret in source).
- Launcher gate integration: `coordinator.enqueue` is the only path that queues a stage; `chain.py` is the only path that executes a queued stage.
- Visualization: [VISUALIZATION.md](VISUALIZATION.md).

## Current attempt admission

Operations entry: manual, through the generic private launcher named in [RUN.md](RUN.md). [Operations guide](../../../toolkit/agent-experiments/OPERATIONS.md).

| Operation | Exact command or unsupported reason | Evidence and last checked revision |
|---|---|---|
| Inspect and offline validation | `python3 src/selftest.py`; `python3 src/worker.py --stage S0 --attempt <name>`; `python3 src/rehearse.py --hub-dir <dir>`; `python3 src/manifest.py --check` | all four passed locally at code commit `30e34577` |
| Prepare named stage | `python3 scripts/run-ready-chain.py sybil-scarcity-opus <commit> setup --host <server>` (private launcher) | not run |
| Dispatch named stage | `python3 scripts/run-ready-chain.py sybil-scarcity-opus <commit> chain --host <server> --confirm-paid` | not run |
| Resume interrupted execution | unsupported by design: no automatic re-execution; a repair is a new attempt number with its own pre-run review | — |
| Analyze saved evidence and rebuild visuals | `... status --host <server>`, `... verify --host <server>` | not run |
| Stop this study and close out | operator: stop the chain process, verify uploads, release claim `dmarz-sybil-scarcity-opus` | not run |

- Attempt / stage / pre-run assessment: chain-001 (S0, P0, Q0, S1) / [reviews/chain-001-pre.md](reviews/chain-001-pre.md).
- Public plan URL: this directory on `main`; the code commit is named in the pre-run review and the launch commit in the run request.
- Budget: call caps P0 1, Q0 48, S1 1,440, total 1,489; 2 requests in flight; at most 1,640 transport attempts (retry only on HTTP 429 and 529); ledger cap USD 220 on settled cost plus open reservations, with a projection gate before S1; expected spend USD 141 to 155 ([AMENDMENTS.md](AMENDMENTS.md)). As relayed, dollars are not the gate for these runs, and the shared USD 500 figure is no longer a gate; this run will take the running total of dmarz's experiments past it.
- Allocation: none. The server is a launcher parameter; the claim id will be `dmarz-sybil-scarcity-opus`.
- Credentials: environment aliases `SWARM_MODEL_API_KEY` and `SWARM_MODEL_WORKSPACE_ID`, set by the launcher in memory only. Never in files, arguments or logs.
- Go / no-go: not decided. This builder launches nothing.

## Attempt and repair history

No attempt exists. Offline checks on the build machine are software checks, not attempts: the offline S0 (`offline-s0-001`, 168 of 168) and the rehearsal wrote only to temporary directories and reported to no real hub.

Plan and design history before the pin, all on 2026-10-04 and before any run: first plan push `15181a01`; dollar cap changed from USD 390 to USD 220 with a projection gate before S1 (dmarz/pipeline); transport retry rule and attempt cap added (relayed by dmarz/fleet-monitor); parent file hashes and the answer-length limit added to `design.yaml`; code, manifest and READY file pushed at `36a03510` (first pin, source hash `82efefd1…`, 4 requests in flight; superseded); requests in flight set to 2 and timeouts raised to 21,600 s and 25,200 s after dmarz/fleet-monitor's same-researcher check, code commit `30e34577`, source hash `b37af997…`, which is the current pin.

| Attempt / parent | Stage / version | Pre-review and receipts | Assigned / started / terminal / graded / analyzed | Post-mortem / disposition |
|---|---|---|---|---|

## Closeout

Not applicable: nothing has run. Spend USD 0, calls 0.

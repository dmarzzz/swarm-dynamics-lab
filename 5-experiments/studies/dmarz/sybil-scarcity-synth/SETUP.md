# Experiment setup record: sybil-scarcity-synth / attempt 001

Status: preparation only. Nothing has run; this record is not launch authorization. Maintained per [the setup runbook](../../../toolkit/agent-experiments/EXPERIMENT-SETUP.md), the [ready-chain contract](../pipeline/READY-CHAIN.md) and the [cross-lane lessons](../pipeline/LESSONS.md). Created 2026-10-04 by dmarz/pipeline-scarcity.

## Ownership and question

- Owner dmarz. Builder dmarz/pipeline-scarcity (Claude Code on dmarz's Mac), under the pipeline lead dmarz/pipeline. Operator: the orchestrator that takes the request from the private run queue; not assigned by this record. Review: cross-researcher review is waived by dmarz for these exploratory runs; dmarz/fleet-monitor's check is a same-researcher check and nothing more; no independent review exists or is claimed. dmarz did not name this study; the fleet monitor approved it as a follow-up proposed by dmarz/pipeline, under dmarz's instruction to keep a pipeline of prepared experiments running (as relayed by dmarz/pipeline, 2026-10-04).
- Question: on packets where a rare fact's truthful reports are outnumbered by repeated fabricated reports, does a stated evidence rule, or higher reasoning effort, reduce how often Opus 5.5 answers with the fabricated value, and what does it cost in accuracy at 27 and 81 carriers? Primary contrast: fabricated-answer rate at 1 carrier, random auditing, effort low, prompt `base` minus prompt `rule`. Practical marker 10 points. Claim boundary: one synthetic task, one graph family, one attacker strategy, simulated checks, one model.
- Research status: exploratory follow-up in researcher notes. The rule was written after seeing the earlier result; this is not a confirmation. No survey, no accepted hypothesis; the formal gates are not met and not claimed. S2 is disabled.
- Previous study and lessons: [sybil-scarcity-opus results](../sybil-scarcity-opus/RESULTS.md) and [post-mortem](../sybil-scarcity-opus/reviews/chain-001-post.md) (complete valid result; 1,489 calls, USD 141.14; open items: the pool-shutdown traceback, `--source`, setup time). Lessons carried over: caps and timeouts sized before qualification (LESSONS item 1); settled-cost ledger (item 2); Opus 5.5 request shape and a one-call probe (item 3); read every miss before changing anything (item 6); small gates misclassify often, so the near-miss rule is written in advance (item 7); the failure-handling rule of 2026-10-04 (evidence kept, count never fails a call, S1 tolerates 10 failed calls, billing pause and resume).
- Current stage and next action: see the gate table.

## Gate evidence

| Gate | Status | Evidence, timestamp and assessor | Blocker / next action |
|---|---|---|---|
| G0 Question and applicable research gates | pass for exploratory scope only | [README](README.md); 2026-10-04, dmarz/pipeline-scarcity (same researcher) | Formal survey and hypothesis gates are not met; S2 stays disabled |
| G1 Plan written before implementation | pass | README, [preregistration](preregistration.md) with the frozen rule wording, [design.yaml](design.yaml) and this record committed before any file under `src/` and before any root of this study was generated; 2026-10-04, dmarz/pipeline-scarcity | — |
| G2 Instrument and offline checks | pass offline (builder's own checks; Python 3.9.6 on macOS) | 2026-10-04, dmarz/pipeline-scarcity, at code commit `ea63999a`, source hash `b75d7b37…`: selftest 39 of 39; offline S0 128 of 128 with 27 of 27 invariants; manifest check equal; rehearsal 38 of 38 checks (full chain and verify; failed-qualification stop; billing stop then second-model relaunch; billing stop then resume). Details in the [pre-run review](reviews/chain-001-pre.md) | Not tested: Python 3.12, the real hub, the private launcher (`--model`, `resume`), a real model response. The launcher's `setup` reruns the selftests on the server |
| G3 Current attempt admission | pending; not requested | [Pre-run review](reviews/chain-001-pre.md) on main. No hub registration, no server claim, no queue item, no credential use | Same-researcher check by dmarz/fleet-monitor; run request in the private queue; launcher `setup` at the launch commit named in the run request |
| G4 Qualification before scientific escalation | not run | S0, P0 and Q0 have not run | Runs inside the chain; a failed gate stops the chain |
| G5 Reconciliation and closeout | not applicable yet | No attempt exists | After the chain: `chain.py verify`, post-mortem, results, claim release |

## Design and instrument index

- Plan: [README.md](README.md), [preregistration.md](preregistration.md), [design.yaml](design.yaml). History in git.
- Independent units: 24 world roots (S1), 8 qualification roots (Q0), 2 engineering roots (S0), 1 probe packet from engineering root 7590 (P0). 40 conditions per root (10 packets × 4 synthesizer configurations); 960 S1 calls.
- Sample size: 24 paired roots, as in the earlier study, whose primary interval was 11 points wide. Exploratory precision only; no power claim.
- Splits: engineering 7590 to 7591; S1 7600 to 7623; Q0 7700 to 7707; holdout 10000 to 19999 unopened. All task ids are below 10000.
- **Root scan, 2026-10-04, at main `0d17b406`, numbers only.** Before any code was run on these numbers. Method: every `.yaml`, `.yml`, `.md`, `.py`, `.toml`, `.sh` and `.txt` file under `researchers/`, `experiments/`, `tooling/`, `hypotheses/`, `tasks/`, `surveys/` and `synthesis/` was searched for four-digit whole numbers and for stated number ranges; every `.json` and `.jsonl` file under 5 MB was searched for `task`, `world`, `root`, `seed`, `world_id`, `task_id` or `world_seed` keys. 3,591 files. The first candidate block (8090 to 8207) was rejected: other researchers' studies use 8100 to 8115, 8200 to 8211 and nearby seeds. The scan then listed every window of at least 130 consecutive numbers between 6000 and 9999 with no occurrence and inside no stated range: 6203 to 6392, 7520 to 7765, 8459 to 8599. The chosen numbers 7590, 7591, 7600 to 7623 and 7700 to 7707 lie inside 7520 to 7765. The scan covers this repository only; it is not a reservation.
- What was looked at to write the plan: the earlier study's records and its roots 7790, 7791 and 7800 to 7823 only (scripted reference rules; no model call). No root of this study.
- Agent definition: one stateless synthesizer call per assignment; prompts `base` and `rule` pinned by SHA-256; schema of sybil-scale-api; model `claude-opus-5-5`; effort low or high.
- Versions: `requirements.txt` pinned; source hash from `study.source_hash()` over `design.yaml`, `experiment.yaml`, `requirements.txt` and `src/*.py`.
- Offline checks: `src/selftest.py`, 39 tests: byte-identity with the sybil-scarcity-opus code and all invariants; pinned prompts and the frozen rule text; reference rules; configurations sharing one user message; grading; clean fixtures and Q0 dispatch order; the Q0 gate per configuration; probe gate; design counts, fresh splits, caps and sizing; pool workers and SIGTERM; model ladder, per-model prices and gates; request body keys; thinking blocks; refusal and other failures; transport retry; failure evidence; token count fallback; billing pause and stop; ledger caps and release; strict stages; S1 failure tolerance and limit; integrity stops; continuation after a billing stop; chain gates, projection, verify, resume and second-model relaunch; analysis bounds and cells; frames; manifest; READY file; no secret in source.
- Launcher gate integration: `coordinator.enqueue` is the only path that queues a stage; `chain.py` is the only path that executes one.
- Visualization: [VISUALIZATION.md](VISUALIZATION.md).

## Current attempt admission

Operations entry: manual, through the generic private launcher. [Operations guide](../../../toolkit/agent-experiments/OPERATIONS.md).

| Operation | Exact command or unsupported reason | Evidence and last checked revision |
|---|---|---|
| Inspect and offline validation | `python3 src/selftest.py`; `python3 src/worker.py --stage S0 --attempt <name>`; `python3 src/rehearse.py --hub-dir <dir>`; `python3 src/manifest.py --check` | all four passed locally at code commit `ea63999a` |
| Prepare named stage | `python3 scripts/run-ready-chain.py sybil-scarcity-synth <launch commit> setup --host <server> --source <operator agent id>` (private launcher) | not run |
| Dispatch named stage | `python3 scripts/run-ready-chain.py sybil-scarcity-synth <launch commit> chain --host <server> --confirm-paid` | not run |
| Resume interrupted execution | only after a `provider_credit_balance_low` stop, at the same source hash: `python src/chain.py resume` (dated amendment required). Any other interruption: unsupported by design; a repair is a new attempt | not run |
| Analyze saved evidence and rebuild visuals | `... status --host <server>`, `... verify --host <server>` | not run |
| Stop this study and close out | operator: stop the chain process, verify uploads, release claim `dmarz-sybil-scarcity-synth` | not run |

- Attempt / stage / pre-run assessment: chain-001 (S0, P0, Q0, S1) / [reviews/chain-001-pre.md](reviews/chain-001-pre.md).
- Budget: call caps P0 1, Q0 48, S1 960, total 1,009; 2 requests in flight; ledger cap USD 240 per model attempt on settled cost plus open reservations, with a per-effort projection gate before S1; expected spend about USD 101 to 136 on Claude Opus 5.5 and USD 126 to 170 on Claude Opus 5 ([preregistration](preregistration.md) item 10); model ladder `[claude-opus-5-5, claude-opus-5]` (item 17). As relayed, cost is not a gate for these runs; the call caps are hard.
- Allocation: none. The server is a launcher parameter; the claim id will be `dmarz-sybil-scarcity-synth`.
- Credentials: environment aliases `SWARM_MODEL_API_KEY` and `SWARM_MODEL_WORKSPACE_ID`, set by the launcher in memory only. Never in files, arguments or logs.
- Go / no-go: not decided. This builder launches nothing.

## Attempt and repair history

No attempt exists. The offline S0 (`offline-s0-001`, 128 of 128) and the rehearsal are software checks on the build machine; they wrote only to temporary directories and reported to no real hub.

Plan and design history, all on 2026-10-04 and before any run: plan with the frozen rule pushed at `6e07eb51` before any code and before any root of this study was generated; model ladder added and the dollar cap resized from USD 190 to USD 240 (required by dmarz/fleet-monitor through dmarz/pipeline) before the pin; code, manifest and READY file pushed at `ea63999a`, which is the code commit.

| Attempt / parent | Stage / version | Pre-review and receipts | Assigned / started / terminal / graded / analyzed | Post-mortem / disposition |
|---|---|---|---|---|

## Closeout

Not applicable: nothing has run. Spend USD 0, calls 0.

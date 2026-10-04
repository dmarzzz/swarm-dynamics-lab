# Experiment setup record: false-alarm-cascade / attempt 001

Status: preparation only. Nothing has run; this record is not launch authorization. Maintained per [the setup runbook](../../../toolkit/agent-experiments/EXPERIMENT-SETUP.md) and the [ready-chain contract](../pipeline/READY-CHAIN.md). Created 2026-10-04 by dmarz/pipeline-alarm; finished the same day by dmarz/scale-xl (Claude Code on orbital-one) after the handover ([HANDOVER.md](HANDOVER.md), task `build-false-alarm-cascade`).

## Ownership and question

- Owner dmarz. Builders dmarz/pipeline-alarm (Claude Code on dmarz's Mac, until the pause) and dmarz/scale-xl (from the handover), under the pipeline lead dmarz/pipeline. Operator: the orchestrator that takes the request from the private run queue; not assigned by this record. Review: cross-researcher review is waived by dmarz for these exploratory runs; dmarz/fleet-monitor's check is a same-researcher check and nothing more; no independent review exists or is claimed. dmarz did not name this study; the fleet monitor chose it from his backlog (honeypot-vigilance hunch V4) under his instruction to keep a pipeline of prepared experiments running. All of this is recorded as stated to the builder by dmarz/pipeline on 2026-10-04.
- Question: when one team member wrongly broadcasts that a real resource is a honeypot, do five model agents (gpt-6-sol in the current attempt) abandon that resource and similar real ones, and does the false belief survive a correction? Primary contrast: use rate of X in rounds 4 to 6, `C0` minus `FA+C`, paired by root. Practical marker 10 points. Claim boundary: one synthetic turn-based task, one model per attempt (a gpt-6-sol result says nothing about Opus), 24 roots.
- Research status: hunch (V4 of [the honeypot-vigilance note](../honeypot-vigilance-hunches.md)), exploratory instrument in researcher notes. No gated survey (the note's prior-art pass is not saturated) and no hypothesis; the formal gates are not met and are not claimed. No novelty claim. S2 is disabled.
- Scope note: the hunch note says to hold the full swarm build until the simulator decision. This is a single-purpose instrument with synthetic resources, not the simulator.
- Prior work and lessons: the note's prior-art verdict for V4; [cross-lane lessons](../pipeline/LESSONS.md) items 1 (caps and timeouts sized before qualification), 3 (Opus 5.5 request shape), 6 (read failing answers first), 7 (small gates), 9 (ceiling risk); the reviewed reference package [sybil-scarcity-opus](../sybil-scarcity-opus/README.md) for the chain, ledger, provider, rehearsal and manifest machinery.
- Current stage and next action: see the gate table.

## Gate evidence

| Gate | Status | Evidence, timestamp and assessor | Blocker / next action |
|---|---|---|---|
| G0 Question and applicable research gates | pass for exploratory scope only | [README](README.md), [hunch note](../honeypot-vigilance-hunches.md); 2026-10-04, dmarz/pipeline-alarm (same researcher) | Formal survey and hypothesis gates are not met; S2 stays disabled |
| G1 Plan written before implementation | pass | README, [preregistration](preregistration.md), [design.yaml](design.yaml), `experiment.yaml` and this record committed before any file under `src/`; 2026-10-04, dmarz/pipeline-alarm | — |
| G2 Instrument and offline checks | pass offline | 2026-10-04 evening, dmarz/pipeline-alarm-oai, at source hash `0947408b…` (code commit `73ff2751`), Python 3.9.6 on macOS: selftest 49 of 49 with and without `STUDY_MODEL`/`STUDY_PROVIDER` set; offline S0 1,225 of 1,225 with 16 of 16 invariants, scripted qualification 134 of 134; manifest check equal (digest unchanged); rehearsal 59 of 59 checks over seven scenarios on gpt-6-sol (ladder scenario on `claude-opus-5-5`). Details in the [pre-run review](reviews/chain-002-pre.md). Earlier checks at `7803e3b8…` (Opus package) are in git history | Not tested: a real OpenAI response (strict schema acceptance, reasoning use, latency), Python 3.12 for the full suite, the real hub and launcher. The launcher's `setup` reruns the selftests on the server |
| G3 Current attempt admission | pending | [Pre-run review chain-002](reviews/chain-002-pre.md) on main (gpt-6-sol, amendment A2), naming code commit `73ff2751` and source hash `0947408b…`; the earlier [chain-001 review](reviews/chain-001-pre.md) covers the Opus rungs | dmarz/fleet-monitor's same-researcher check; run request in the private queue; launcher `setup` |
| G4 Qualification before scientific escalation | not run | S0, P0 and Q0 have not run | Runs inside the chain; a failed gate stops the chain |
| G5 Reconciliation and closeout | not applicable yet | No attempt exists | After the chain: `chain.py verify`, post-mortem, results, claim release |

## Design and instrument index

- Plan: [README.md](README.md), [preregistration.md](preregistration.md), [design.yaml](design.yaml). History in git.
- Independent units: 24 world roots (S1), 8 qualification roots (Q0), 2 engineering roots (S0 and the P0 packet). Per S1 root: 5 conditions × 5 model agents × 6 rounds = 150 calls; 120 team episodes; 3,600 calls.
- Sample size: fixed by the design brief at 24 paired roots. Exploratory precision only; no power claim; no pilot estimate of this manipulation exists.
- Splits: engineering 8390 to 8391; S1 8400 to 8423; Q0 8450 to 8457; holdout 10000 to 19999 unopened. All task ids are below 10000.
- **Root-range scan, 2026-10-04, at main `c4c7a879`.** Every `.yaml`, `.yml`, `.md`, `.py`, `.toml`, `.sh` and `.txt` file under `lab/researchers/`, `experiments/`, `tooling/`, `4-hypotheses/`, `tasks/`, `2-surveys/` and `3-synthesis/` was searched for 8390, 8391, 8400 to 8423 and 8450 to 8457 as whole numbers; every `.json` and `.jsonl` file under 5 MB was searched for `task`, `world`, `root`, `seed`, `world_id`, `task_id` or `world_seed` keys with those values; design, preregistration, manifest, plan, config, experiment, README and SETUP files were also searched for number ranges that span 8390 to 8457. 3,455 files scanned, this directory excluded. Result: 0 exact matches and 0 spanning ranges. The scan covers this repository only; it is not a reservation, and a private or unpushed study could still use these numbers. The design files of the sibling pipeline lanes on the build machine were also searched, with no match.
- Agent definition: one stateless call per model agent and round; one system prompt for the whole study; JSON-schema structured output; model ladder `gpt-6-sol` (default since amendment A2; OpenAI, `reasoning_effort: medium`, strict JSON schema, `max_completion_tokens` 16,000), `claude-opus-5-5`, `claude-opus-5` (effort medium), one per attempt.
- Versions: `requirements.txt` pinned; source hash from `study.source_hash()` over `design.yaml`, `experiment.yaml`, `requirements.txt` and `src/*.py` `7803e3b8b8cbf93ddf99cdd7151e49ead8d440d0fba8b69f663e9f6d429ac599`, recorded in `READY.yaml` and the pre-run review.
- Offline checks: `src/selftest.py`, 41 tests (35 by the first package; 3 for the failure-handling rule; 3 for the model ladder: default, override and refusal outside the ladder, no cross-model qualification, per-model prices): world validity and keyed streams; the honeypot draw's family probabilities; all 16 S0 invariants with the negative and positive controls, and a broken manipulation being caught; conditions differing only by the planted posts with agents that react to the board; board and retraction rules, answer normalization and validation; no truth, target, condition or slot in actor inputs; the three reference policies; evaluator grades; clean fixtures and frozen gated counts; Q0 thresholds at their boundaries; the probe gate; design counts and caps; request body keys and schema; thinking and redacted-thinking blocks; refusal and other failure categories; the transport retry rule clause by clause; ledger caps across two ledger objects and a partial write; worker failure accounting; a stage-loop crash stopping new rounds; episode rounds carrying model output forward and a failed call ending its episode; coordinator gates; chain stage lists, projection gate, stops and verify tampering; primary contrast with missing-outcome bounds; every secondary measure; signal detection; frames and GIF; manifest regeneration; READY consistency; no secret in source. A mutation pass (21 single-line faults in a scratch copy, each caught by at least one test; one needed a test to be added) was run on 2026-10-04; it is the builder's own check.
- Launcher gate integration: `coordinator.enqueue` is the only path that queues a stage; `chain.py` is the only path that executes a queued stage.
- Visualization: [VISUALIZATION.md](VISUALIZATION.md).

## Current attempt admission

Operations entry: manual, through the generic private launcher named in [RUN.md](RUN.md). [Operations guide](../../../toolkit/agent-experiments/OPERATIONS.md).

| Operation | Exact command or unsupported reason | Evidence and last checked revision |
|---|---|---|
| Inspect and offline validation | `python3 src/selftest.py`; `python3 src/worker.py --stage S0 --attempt <name>`; `python3 src/rehearse.py --hub-dir <dir>`; `python3 src/manifest.py --check` | all four passed locally at source hash `0947408b…` (2026-10-04 evening) |
| Prepare named stage | `python3 scripts/run-ready-chain.py false-alarm-cascade <commit> setup --host <server>` (private launcher) | not run |
| Dispatch named stage | `python3 scripts/run-ready-chain.py false-alarm-cascade <commit> chain --host <server> --confirm-paid` | not run |
| Resume interrupted execution | only after S1 stopped with `provider_credit_balance_low` (pre-registered, amendment A1): `python3 scripts/run-ready-chain.py false-alarm-cascade <commit> resume --host <server>`; any other stop: no re-execution, a repair is a new attempt number with its own pre-run review | rehearsal scenario (f) |
| Analyze saved evidence and rebuild visuals | `... status --host <server>`, `... verify --host <server>` | not run |
| Stop this study and close out | operator: stop the chain process, verify uploads, release claim `dmarz-false-alarm-cascade` | not run |

- Attempt / stage / pre-run assessment: chain-001 (S0, P0, Q0, S1) / [reviews/chain-001-pre.md](reviews/chain-001-pre.md).
- Budget: call caps P0 1, Q0 24, S1 3,600, total 3,625 per model; at most 10 requests in flight; ledger cap USD 120 on gpt-6-sol (expected about USD 57, amendment A2) and USD 450 per Opus ledger with a projection gate before S1; expected spend about USD 120 on `claude-opus-5-5`, about USD 150 on `claude-opus-5` ([preregistration](preregistration.md), item 13 and amendment A1). Cost is not the gate for these runs; the call caps are.
- Allocation: none. The server is a launcher parameter; the claim id will be `dmarz-false-alarm-cascade`.
- Credentials: environment alias `SWARM_OPENAI_API_KEY` (gpt-6-sol), or `SWARM_MODEL_API_KEY` and `SWARM_MODEL_WORKSPACE_ID` (Opus rungs), set by the launcher in memory only. Never in files, arguments or logs.
- Go / no-go: not decided. The builders launch nothing.

## Attempt and repair history

No attempt exists. Offline checks are software checks, not attempts: the offline S0 runs (`offline-s0-001` by the first builder, `offline-s0-a2` at the current hash, each 1,225 of 1,225) and the rehearsals wrote only to temporary directories and reported to no real hub.

Plan and design history, all on 2026-10-04 and before any run: first plan push `11dfdfd2` (before any code); while the code was written, S0 grew from 925 to 1,225 rows (silent control grid plus one posting pass) and the realized gated counts 35, 34 and 65 were frozen in `design.yaml` (see [preregistration.md](preregistration.md), last section).

| Attempt / parent | Stage / version | Pre-review and receipts | Assigned / started / terminal / graded / analyzed | Post-mortem / disposition |
|---|---|---|---|---|

## Closeout

Not applicable: nothing has run. Spend USD 0, calls 0.

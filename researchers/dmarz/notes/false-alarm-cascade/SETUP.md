# Experiment setup record: false-alarm-cascade / attempt 001

Status: preparation only. Nothing has run; this record is not launch authorization. Maintained per [the setup runbook](../../../../tooling/agent-experiments/EXPERIMENT-SETUP.md) and the [ready-chain contract](../pipeline/READY-CHAIN.md). Created 2026-10-04 by dmarz/pipeline-alarm.

## Ownership and question

- Owner dmarz. Builder dmarz/pipeline-alarm (Claude Code on dmarz's Mac), under the pipeline lead dmarz/pipeline. Operator: the orchestrator that takes the request from the private run queue; not assigned by this record. Review: cross-researcher review is waived by dmarz for these exploratory runs; dmarz/fleet-monitor's check is a same-researcher check and nothing more; no independent review exists or is claimed. dmarz did not name this study; the fleet monitor chose it from his backlog (honeypot-vigilance hunch V4) under his instruction to keep a pipeline of prepared experiments running. All of this is recorded as stated to the builder by dmarz/pipeline on 2026-10-04.
- Question: when one team member wrongly broadcasts that a real resource is a honeypot, do five Opus 5.5 agents abandon that resource and similar real ones, and does the false belief survive a correction? Primary contrast: use rate of X in rounds 4 to 6, `C0` minus `FA+C`, paired by root. Practical marker 10 points. Claim boundary: one synthetic turn-based task, one model, 24 roots.
- Research status: hunch (V4 of [the honeypot-vigilance note](../honeypot-vigilance-hunches.md)), exploratory instrument in researcher notes. No gated survey (the note's prior-art pass is not saturated) and no hypothesis; the formal gates are not met and are not claimed. No novelty claim. S2 is disabled.
- Scope note: the hunch note says to hold the full swarm build until the simulator decision. This is a single-purpose instrument with synthetic resources, not the simulator.
- Prior work and lessons: the note's prior-art verdict for V4; [cross-lane lessons](../pipeline/LESSONS.md) items 1 (caps and timeouts sized before qualification), 3 (Opus 5.5 request shape), 6 (read failing answers first), 7 (small gates), 9 (ceiling risk); the reviewed reference package [sybil-scarcity-opus](../sybil-scarcity-opus/README.md) for the chain, ledger, provider, rehearsal and manifest machinery.
- Current stage and next action: see the gate table.

## Gate evidence

| Gate | Status | Evidence, timestamp and assessor | Blocker / next action |
|---|---|---|---|
| G0 Question and applicable research gates | pass for exploratory scope only | [README](README.md), [hunch note](../honeypot-vigilance-hunches.md); 2026-10-04, dmarz/pipeline-alarm (same researcher) | Formal survey and hypothesis gates are not met; S2 stays disabled |
| G1 Plan written before implementation | pass | README, [preregistration](preregistration.md), [design.yaml](design.yaml), `experiment.yaml` and this record committed before any file under `src/`; 2026-10-04, dmarz/pipeline-alarm | — |
| G2 Instrument and offline checks | pending | No code yet | Implement; selftests; offline S0; rehearsal; manifest check |
| G3 Current attempt admission | pending | No pre-run review yet | Pre-run review on main; dmarz/fleet-monitor's same-researcher check; run request in the private queue; launcher `setup` |
| G4 Qualification before scientific escalation | not run | S0, P0 and Q0 have not run | Runs inside the chain; a failed gate stops the chain |
| G5 Reconciliation and closeout | not applicable yet | No attempt exists | After the chain: `chain.py verify`, post-mortem, results, claim release |

## Design and instrument index

- Plan: [README.md](README.md), [preregistration.md](preregistration.md), [design.yaml](design.yaml). History in git.
- Independent units: 24 world roots (S1), 8 qualification roots (Q0), 2 engineering roots (S0 and the P0 packet). Per S1 root: 5 conditions × 5 model agents × 6 rounds = 150 calls; 120 team episodes; 3,600 calls.
- Sample size: fixed by the design brief at 24 paired roots. Exploratory precision only; no power claim; no pilot estimate of this manipulation exists.
- Splits: engineering 8390 to 8391; S1 8400 to 8423; Q0 8450 to 8457; holdout 10000 to 19999 unopened. All task ids are below 10000.
- **Root-range scan, 2026-10-04, at main `c4c7a879`.** Every `.yaml`, `.yml`, `.md`, `.py`, `.toml`, `.sh` and `.txt` file under `researchers/`, `experiments/`, `tooling/`, `hypotheses/`, `tasks/`, `surveys/` and `synthesis/` was searched for 8390, 8391, 8400 to 8423 and 8450 to 8457 as whole numbers; every `.json` and `.jsonl` file under 5 MB was searched for `task`, `world`, `root`, `seed`, `world_id`, `task_id` or `world_seed` keys with those values; design, preregistration, manifest, plan, config, experiment, README and SETUP files were also searched for number ranges that span 8390 to 8457. 3,455 files scanned, this directory excluded. Result: 0 exact matches and 0 spanning ranges. The scan covers this repository only; it is not a reservation, and a private or unpushed study could still use these numbers. The design files of the sibling pipeline lanes on the build machine were also searched, with no match.
- Agent definition: one stateless call per model agent and round; one system prompt for the whole study; JSON-schema structured output; `claude-opus-5-5`, effort medium.
- Versions: `requirements.txt` pinned; source hash from `study.source_hash()` over `design.yaml`, `experiment.yaml`, `requirements.txt` and `src/*.py` (to be recorded in `READY.yaml` and the pre-run review).
- Offline checks: to be listed here when they exist.
- Visualization: `VISUALIZATION.md`, to be written with the renderer.

## Current attempt admission

Operations entry: manual, through the generic private launcher (`scripts/run-ready-chain.py` in the agentops repository), to be written up in `RUN.md`. [Operations guide](../../../../tooling/agent-experiments/OPERATIONS.md).

- Attempt / stage / pre-run assessment: chain-001 (S0, P0, Q0, S1) / not written yet.
- Budget: call caps P0 1, Q0 24, S1 3,600, total 3,625; at most 10 requests in flight; ledger cap USD 360 with a projection gate before S1; expected spend about USD 120 ([preregistration](preregistration.md), item 13). Cost is not the gate for these runs; the call caps are.
- Allocation: none. The server is a launcher parameter; the claim id will be `dmarz-false-alarm-cascade`.
- Credentials: environment aliases `SWARM_MODEL_API_KEY` and `SWARM_MODEL_WORKSPACE_ID`, set by the launcher in memory only. Never in files, arguments or logs.
- Go / no-go: not decided. This builder launches nothing.

## Attempt and repair history

No attempt exists.

| Attempt / parent | Stage / version | Pre-review and receipts | Assigned / started / terminal / graded / analyzed | Post-mortem / disposition |
|---|---|---|---|---|

## Closeout

Not applicable: nothing has run. Spend USD 0, calls 0.

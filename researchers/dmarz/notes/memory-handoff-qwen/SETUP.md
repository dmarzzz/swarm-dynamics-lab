# Experiment setup record: memory-handoff-qwen / attempt 001

Status: preparation only. Nothing has run; this record is not launch authorization. Maintained per [the setup runbook](../../../../tooling/agent-experiments/EXPERIMENT-SETUP.md) and the [ready-chain contract](../pipeline/READY-CHAIN.md). Created 2026-10-04 by dmarz/pipeline-memory.

## Ownership and question

- Owner dmarz. Builder dmarz/pipeline-memory (Claude Code on dmarz's Mac), under the pipeline lead dmarz/pipeline. Operator: the orchestrator that takes the request from the private run queue; not assigned by this record. Review, as relayed to this builder by dmarz/pipeline on 2026-10-04: dmarz directed research program v5 himself (written with him by a Codex session on 2026-10-04; his instruction to ship it was relayed by dmarz/fleet-monitor); cross-researcher review is waived by dmarz for these exploratory runs; dmarz/fleet-monitor's check is a same-researcher check and nothing more. No independent review exists or is claimed.
- Question: does binding inherited claims to the contents of their original sources repair false or stale memory without erasing useful knowledge? Primary contrast: inherited error under content-bound retrieval minus under metadata-only resolution, mean of the misquote and stale states within each root, 24 roots. Guard: clean-memory correct completion. Claim boundary: one handoff, one synthetic task with three field families, one model configuration; not a multi-generation result.
- Research status: exploratory follow-up in researcher notes (line M of [research program v5](../overnight-program-2026-10-04/program.json)). No complete survey and no accepted hypothesis; the formal gates are not met and are not claimed. S2 is disabled.
- Prior work and lessons: [discussion benchmark v3](../discussion-dose/benchmark-v3/README.md) and its parent-memory results ([D1](../discussion-dose/benchmark-v3/RESULTS-D1.md), [D1 Opus](../discussion-dose/d1-opus/RESULTS.md)); [cross-lane lessons](../pipeline/LESSONS.md) items 1 (caps and timeouts sized for the whole ladder before qualification), 3 (request shape checked by a one-call probe), 6 (read the failing answers before any repair) and 7 (small gates misclassify; this gate allows no miss).
- Current stage and next action: see the gate table.

## Gate evidence

| Gate | Status | Evidence, timestamp and assessor | Blocker / next action |
|---|---|---|---|
| G0 Question and applicable research gates | pass for exploratory scope only | [README](README.md), [program v5](../overnight-program-2026-10-04/program.json); 2026-10-04, dmarz/pipeline-memory (same researcher) | Formal survey and hypothesis gates are not met; S2 stays disabled |
| G1 Plan written before implementation | pass | README, [preregistration](preregistration.md), [design.yaml](design.yaml), `experiment.yaml` and this record were committed before any file under `src/`; 2026-10-04, dmarz/pipeline-memory | none |
| G2 Instrument and offline checks | pending | not built yet | Build `src/`, pass selftest, offline S0, rehearsal and manifest check |
| G3 Current attempt admission | pending | no pre-run review yet | Pre-run review with the pinned commit and source hash; then the fleet monitor's same-researcher check and a request in the private run queue |
| G4 Qualification before scientific escalation | pending | nothing has run | S0, P0 and Q0 gates in the chain |
| G5 Reconciliation and closeout | pending | nothing has run | `verify`, post-run review |

## Design and instrument index

- Plan: [README.md](README.md), [preregistration.md](preregistration.md), [design.yaml](design.yaml). History in git.
- Independent units: 24 roots (S1), 6 qualification roots in set a and 6 in set b, 6 engineering roots (S0). 24 assignments per S1 root (6 states × 4 policies); 576 S1 assignments, one model call each.
- Sample size: fixed by the program at 24 roots. Exploratory precision only; no power claim; no pilot estimate of this manipulation on this model exists.
- Splits: engineering 5301 to 5306; S1 5401 to 5424; qualification set a 5501 to 5506 (attempt 001); qualification set b 5601 to 5606 (reserved for the one permitted repair). All root ids are below 10000. The generator is seeded with this study's own version string.
- Agent definition: one stateless successor call per assignment; one constant system message; model `qwen/qwen3.7-flash` through OpenRouter, provider Alibaba, reasoning disabled, JSON-object mode, 1,000 output tokens.
- Versions: `requirements.txt` pinned; source hash from `study.source_hash()` over `design.yaml`, `experiment.yaml`, `requirements.txt` and `src/*.py`.
- Offline checks, launcher gate integration, visualization: filled in when the code exists.

## Current attempt admission

Operations entry: manual, through the generic private launcher (commands will be in `RUN.md`). [Operations guide](../../../../tooling/agent-experiments/OPERATIONS.md).

- Attempt / stage / pre-run assessment: chain-001 (S0, P0, Q0, S1); the pre-run review is not written yet.
- Budget: call caps P0 1, Q0 23, S1 576, total 600; 4 requests in flight; at most 800 transport attempts; ledger cap USD 2 on settled cost plus open reservations; expected spend about USD 0.03.
- Allocation: none. The server is a launcher parameter; the claim id will be `dmarz-memory-handoff-qwen`.
- Credentials: environment alias `SWARM_OPENROUTER_API_KEY`, set by the launcher in memory only. Never in files, arguments or logs.
- Go / no-go: not decided. This builder launches nothing.

## Attempt and repair history

No attempt exists.

| Attempt / parent | Stage / version | Pre-review and receipts | Assigned / started / terminal / graded / analyzed | Post-mortem / disposition |
|---|---|---|---|---|

## Closeout

Not applicable: nothing has run. Spend USD 0, calls 0.

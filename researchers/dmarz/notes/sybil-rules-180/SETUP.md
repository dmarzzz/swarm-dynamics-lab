# Experiment setup record: sybil-rules-180 / attempt 001

Status: preparation only. Nothing has run; this record is not launch authorization. Maintained per [the setup runbook](../../../../tooling/agent-experiments/EXPERIMENT-SETUP.md) and the [ready-chain contract](../pipeline/READY-CHAIN.md). Created 2026-10-04 by dmarz/flagship-market (started by an earlier model under the same agent id, finished by Claude Opus 5.5 after the first was cut off at about 10:58 UTC).

## Ownership and question

- Owner dmarz. Builder dmarz/flagship-market (Claude Code on dmarz's Mac). Reviewer of the package: dmarz/fleet-monitor, a same-researcher check. Cross-researcher review is waived by dmarz for these exploratory runs; the run is not independently reviewed.
- Question: line F of [research program v5](../overnight-program-2026-10-04/SETUP.md): in one connected economy of 180 model-controlled owners, how do a firm-level concentration charge, an anti-circumvention sentence and beneficial-owner enforcement shape sustained same-product firm splitting, and how much does supplying a worked example change it? Claim boundary: one economy, descriptive contrasts, supplied affordance rather than discovery, instruction effect rather than moral compliance, C's zero saving by construction.
- Research status: exploratory in researcher notes. The formal survey and hypothesis gates are not met and are not claimed.
- Current stage and next action: see the gate table.

## Gate evidence

| Gate | Status | Evidence, timestamp and assessor | Blocker / next action |
|---|---|---|---|
| G0 Question and applicable research gates | pass for exploratory scope only | [README](README.md), program v5 line F; 2026-10-04, dmarz/flagship-market (same researcher) | formal gates not claimed |
| G1 Plan written before implementation | partial | README plan skeleton committed (`bcdcb3f2`) before the engine (`f9339d19`); [preregistration](preregistration.md) and the full protocol were written after the code but before any stage ran or any call was made | none for an exploratory run; stated here |
| G2 Instrument and offline checks | pass offline (builder's own checks; Python 3.9.6 on macOS) | 2026-10-04, dmarz/flagship-market, code commit `45d501b1`, source hash `cfd6f10a…`: selftest 49 of 49; offline S0 passed (8,118 of 8,118 accepted, all invariants); rehearsal 48 of 48 checks (scenarios a to g, see [pre-run review](reviews/chain-001-pre.md)); launcher tests 13 of 13 at agentops `19b1573` | none |
| G3 Current attempt admission | pending | [pre-run review](reviews/chain-001-pre.md), [READY.yaml](READY.yaml) | dmarz/fleet-monitor's go; claim `dmarz-sybil-rules-180` over three servers; launcher `setup` on all three at the launch commit |
| G4 Qualification before scientific escalation | not run | chain gates P0, Q0, X0 (software) | — |
| G5 Reconciliation and closeout | not run | — | — |

## Design and instrument index

- Plan: [README.md](README.md), [preregistration.md](preregistration.md), [design.yaml](design.yaml), [RUN.md](RUN.md), [VISUALIZATION.md](VISUALIZATION.md).
- Units: one economy seed, 60 dependent markets, 180 owners; 4 continuations of 10 rounds from one checkpoint; D1 12 paired tasks.
- Fixture ranges: main 318000 to 318059, smoke 318100 to 318105, ordinary 318200 to 318205, diagnostic 318300 to 318311, probe 318400, development 318500 to 318505, reserved repair 318600 to 318699, context 318700 to 318759.
- Code: `src/sim.py` engine, `src/study.py` frozen design and actor text, `src/worker.py` stage executor and worker entry, `src/transport.py` ledger, permits, hub transport and re-issue, `src/chain.py` chain driver, status and verify, `src/coordinator.py` gates, `src/analyze.py`, `src/render.py`, `src/provider.py` (copy of the reference OpenRouter adapter), `src/selftest.py`, `src/test_provider.py`, `src/rehearse.py`.
- Versions: `requirements.txt` pinned; source hash over the design files and `src/*.py`.

## Current attempt admission

| Operation | Exact command or unsupported reason | Evidence and last checked revision |
|---|---|---|
| Inspect and offline validation | `python3 src/selftest.py`; `python3 src/worker.py --stage S0 --attempt <name>`; `python3 src/rehearse.py --hub-dir <dir>` | all passed at code commit `45d501b1` |
| Prepare | `python3 scripts/run-ready-chain.py sybil-rules-180 <commit> setup --host <a>,<b>,<c>` (private launcher) | not run |
| Dispatch | `… chain --host <a>,<b>,<c> --confirm-paid` | not run |
| Resume | not automated: a billing stop ends the attempt; the pre-registered resume is attempt 002 from the stopped stage | — |
| Analyze | `… status` and `… verify` | not run |
| Stop and close out | operator: stop the chain and workers, verify uploads, release the claim | not run |

- Budget: USD 5 hard cap for this study (dmarz to dmarz/fleet-monitor, 2026-10-04); expected about USD 1; caps in [design.yaml](design.yaml).
- Allocation: none yet. Three dmarz servers named at launch.
- Credentials: alias `SWARM_OPENROUTER_API_KEY`, to the three workers on ssh stdin, in memory only.
- Go / no-go: not decided. This builder launches nothing.

## Attempt and repair history

No attempt exists. Offline checks wrote only to temporary directories and reported to no real hub.

## Closeout

Not applicable: nothing has run. Spend USD 0, calls 0.

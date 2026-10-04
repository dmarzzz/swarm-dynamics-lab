# Experiment setup record: sybil-scarcity-xmodel v1

Status: both models prepared; the `qwen/qwen3.7-flash` chain was launched by dmarz/fleet-monitor at about 17:30Z (launch commit c0537bf7); `gpt-6-sol` ready at code commit 9461ba1c ([chain-002-pre](reviews/chain-002-pre.md)), not launched. This record follows [the setup runbook](../../../toolkit/agent-experiments/EXPERIMENT-SETUP.md) and is not launch authorization. A run starts only when the orchestrator takes a request from the private run queue after dmarz/fleet-monitor's same-researcher check. Nothing has run on a server and no model call has been made.

## Ownership and question

- Owner dmarz. Builder dmarz/pipeline-scarcity-qwen (Claude Code, offline on dmarz's Mac), working for dmarz/fleet-monitor. Operator: whoever takes the queued request; the server is a launcher parameter. Review independence: none. dmarz did not name this study; the fleet monitor chose it under his instruction to keep experiments running and ship tonight (relayed 2026-10-04, including his 12:00Z message "we have no experiments running! fix that and or use opus 5 or an oai model"). Cross-researcher review is waived by dmarz for these exploratory runs; the fleet monitor's check is a same-researcher check; the run is not independently reviewed.
- Question: on byte-identical packets, does a synthesizer other than Opus 5.5 lose specialist accuracy as truthful carriers become scarce? Primary per model: specialist accuracy at 1 carrier minus 81, random auditing, 108 checks, attacker pass 0.1, 24 roots. Claim boundary: one synthetic task; model and configuration differ together from the parent.
- Research status: exploratory replication in researcher notes; survey and hypothesis gates not met; S2 disabled.
- Prior study and lessons: [sybil-scarcity-opus RESULTS](../sybil-scarcity-opus/RESULTS.md) and [its post-mortem](../sybil-scarcity-opus/reviews/chain-001-post.md); [trust-credit-qwen](../trust-credit-qwen/README.md) (the same Qwen route ran 528 calls with 0 failures); [pipeline lessons](../pipeline/LESSONS.md); the flagship's stopped probe (a validator that fails a harmless variant of a correct answer), relayed by dmarz/fleet-monitor.

## Gate evidence

| Gate | Status | Evidence, timestamp and assessor | Blocker / next action |
|---|---|---|---|
| G0 Question and applicable research gates | pass (exploratory scope only) | README and preregistration, 2026-10-04, dmarz/pipeline-scarcity-qwen; design fixed by dmarz/fleet-monitor | formal gates not met; S2 disabled |
| G1 Plan written before implementation | partial | The design was fixed in the fleet monitor's brief before any code; the plan documents were written alongside the code and committed with it in one push, before any run. Nothing about the inputs is new: they are the parent's frozen inputs | none |
| G2 Instrument and offline checks | pass (offline, builder's own checks) | 2026-10-04, dmarz/pipeline-scarcity-qwen, on code commit 2753b03d (source hash 06cbd97e...): selftest 65 OK; offline S0 168/168, 0 violations, byte-identity with the parent; manifest check current and equal to the parent's; rehearsal 21/21 checks; details in [the pre-run review](reviews/chain-001-pre.md) | the live route is untested until P0 |
| G3 Current attempt admission | pending (package ready) | [reviews/chain-001-pre.md](reviews/chain-001-pre.md), status ready for `qwen/qwen3.7-flash` at code commit 2753b03d | fleet-monitor check, run-queue request, server claim |
| G3b gpt-6-sol admission | pending (package ready) | [reviews/chain-002-pre.md](reviews/chain-002-pre.md) at code commit 9461ba1c (source hash cac7255a...): selftest 96 OK, S0 168/168, manifest current, rehearsal 22/22 | fleet-monitor check, run-queue request, server claim |
| G4 Qualification before scientific escalation | pending | P0 and Q0 are stages of each model's chain; S1 is admitted only after Q0 passes at the same source hash | run |
| G5 Reconciliation and closeout | pending | none | run |

## Design and instrument index

- Plan: [README.md](README.md), [preregistration.md](preregistration.md), [design.yaml](design.yaml), [RUN.md](RUN.md), [VISUALIZATION.md](VISUALIZATION.md).
- Independent units: the parent's 24 world roots (7800-7823); 60 cells per root. Q0: 48 clean packets on roots 7900-7907. Probe: root 7790.
- Splits: the parent's. No new roots are drawn; holdout 10000-19999 unopened.
- Agent definition: one stateless synthesizer call per assignment; system prompt = the parent's prompt plus the answer shape (`src/study.py`); local validation in `study.validate`; adapter `src/provider.py` = the pipeline's reference OpenRouter adapter, unchanged (a selftest compares the file).
- Versions: `qwen/qwen3.7-flash` (canonical `qwen/qwen3.7-flash-20260727`), provider Alibaba. `gpt-6-sol` is pre-registered and refused by the code at this commit (`model_not_ready`). requirements.txt pinned; the source hash covers design.yaml, experiment.yaml, requirements.txt and `src/*.py`; the parent's files are pinned by SHA-256 inside design.yaml.

## Current attempt admission

Operations entry: manual, through the generic private launcher `scripts/run-ready-chain.py` in the agentops repository with `--model`. [Operations guide](../../../toolkit/agent-experiments/OPERATIONS.md).

| Operation | Exact command or unsupported reason | Evidence and last checked revision |
|---|---|---|
| Inspect and offline validation | `python3 src/selftest.py`; `python3 src/worker.py --stage S0 --attempt <name>`; `python3 src/rehearse.py --hub-dir <dir>`; `python3 src/manifest.py --check` | pre-run review |
| Prepare | `python3 scripts/run-ready-chain.py sybil-scarcity-xmodel <launch commit> setup --host <server> --model qwen/qwen3.7-flash` | not run |
| Dispatch | `python3 scripts/run-ready-chain.py sybil-scarcity-xmodel <launch commit> chain --host <server> --model qwen/qwen3.7-flash --confirm-paid` | not run |
| Resume | only after a billing stop of S1: `python src/chain.py resume` with the same `STUDY_MODEL` | not run |
| Status, verify | `... status` / `... verify` with the same `--model` | not run |

- Attempt: chain-001 per model; no parent attempt of this study.
- Budget authority: dmarz/fleet-monitor's brief under dmarz's instruction; Qwen caps P0 1, Q0 48, S1 1,440 (1,489 calls), USD 4; gpt-6-sol cap USD 150 when its commit lands.
- Allocation: none yet; one server per model chain.
- Credentials: `SWARM_OPENROUTER_API_KEY` (Qwen), `SWARM_OPENAI_API_KEY` (gpt-6-sol, later); supplied in memory by the launcher; none used to prepare this package.
- Go/no-go: not decided. This builder does not launch.

## Attempt and repair history

| Attempt / parent | Stage / version | Pre-review and receipts | Assigned / started / terminal / graded / analyzed | Post-mortem / disposition |
|---|---|---|---|---|
| none yet | | | | |

## Closeout

Closed 2026-10-04 by dmarz/pipeline-scarcity-qwen. All three configurations stopped at Q0 as pre-registered (Qwen: [chain-001-post](reviews/chain-001-post.md); gpt-6-sol effort low: [chain-002-post](reviews/chain-002-post.md); gpt-6-sol effort none, F1: [chain-003-post](reviews/chain-003-post.md)); no S1 call was made; total spend about USD 4.60; claims released by dmarz/fleet-monitor. Summary: [RESULTS.md](RESULTS.md).

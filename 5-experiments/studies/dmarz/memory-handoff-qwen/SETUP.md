# Experiment setup record: memory-handoff-qwen / attempts 001 and 002

Status: all three chains have run (attempt 001 stopped at the qualification gate; attempt 002 and chain 003 on gpt-6-luna completed; results in RESULTS.md). No further run is prepared. This record is not launch authorization. Maintained per [the setup runbook](../../../toolkit/agent-experiments/EXPERIMENT-SETUP.md) and the [ready-chain contract](../pipeline/READY-CHAIN.md). Created 2026-10-04 by dmarz/pipeline-memory.

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
| G2 Instrument and offline checks | pass offline (builder's own checks; Python 3.9.6 on macOS) | 2026-10-04, dmarz/pipeline-memory, at code commit `b6990122`, source hash `b4ab9025…`: selftest 85 of 85 (53 study tests and the 32 reference adapter tests); offline S0 192 of 192 with 25 of 25 invariants; manifest check equal; rehearsal 35 of 35 checks in 73 s (full chain and verify; failed qualification stops at Q0 with exit 3 and no S1 run; billing pause and one failed call; failures over the limit; billing stop then resume). Details in the [pre-run review](reviews/chain-001-pre.md) | Not tested: Python 3.12, the real hub, the private launcher, a real model response. The launcher's `setup` reruns the selftests on the server |
| G3 Current attempt admission | pending | [Pre-run review](reviews/chain-001-pre.md) on main, naming code commit `b6990122` and source hash `b4ab9025…`; 2026-10-04, dmarz/pipeline-memory | The fleet monitor's same-researcher check, a request in the private run queue, a server claim and the balance check |
| G4 Qualification before scientific escalation | pending | nothing has run | S0, P0 and Q0 gates in the chain |
| G5 Reconciliation and closeout | pending | nothing has run | `verify`, post-run review |

## Design and instrument index

- Plan: [README.md](README.md), [preregistration.md](preregistration.md), [design.yaml](design.yaml). History in git.
- Independent units: 24 roots (S1), 6 qualification roots in set a and 6 in set b, 6 engineering roots (S0). 24 assignments per S1 root (6 states × 4 policies); 576 S1 assignments, one model call each.
- Sample size: fixed by the program at 24 roots. Exploratory precision only; no power claim; no pilot estimate of this manipulation on this model exists.
- Splits: engineering 5301 to 5306; S1 5401 to 5424; qualification set a 5501 to 5506 (attempt 001); qualification set b 5601 to 5606 (reserved for the one permitted repair). All root ids are below 10000. The generator is seeded with this study's own version string.
- Agent definition: one stateless successor call per assignment; one constant system message; model `qwen/qwen3.7-flash` through OpenRouter, provider Alibaba, reasoning disabled, JSON-object mode, 1,000 output tokens.
- Versions: `requirements.txt` pinned; source hash from `study.source_hash()` over `design.yaml`, `experiment.yaml`, `requirements.txt` and `src/*.py`.
- **Root-range check, 2026-10-04, at main `b6990122`.** 3,850 text files (`.yaml`, `.yml`, `.md`, `.py`, `.toml`, `.sh`, `.txt`, and `.json` under 5 MB) under `researchers/`, `experiments/`, `tooling/`, `hypotheses/`, `tasks/`, `surveys/` and `synthesis/` were searched for 5301 to 5306, 5401 to 5424, 5501 to 5506 and 5601 to 5606 next to the words root, world, task or seed (in JSON: as values of those keys); this directory excluded. Result: 0 exact matches; the five-digit world ids 541xx of discussion-dose v3-opus share a prefix only. The scan covers this repository only and is not a reservation.
- Offline checks: `src/selftest.py` (85 tests: textual identity of the copied resolver and decoder with bench_v3; the adapter copy equal to the reference; worlds; all 25 design invariants; reference against the hand-written table; counterfactual truth; false original and copies never show the truth; store-only retrieval; no labels in messages; structural validation; scorer known answers; control actors; counts, caps and splits; the no-miss qualification gate; the probe gate; manifest regeneration; READY consistency; no secret in the package; request body and sizes; duplicate keys and invalid answers; kept HTTP evidence; billing pause and stop; the scripted stage; invariant failure; probe metadata; missing provider; probe row for Q0; failed qualification; strict stop; S1 tolerance and limit; integrity stop; billing stop and continuation; short outage; refused starts; the full chain; the wire-level capture; verify tampering; status and resume refusal; no replay; saved analysis; coordinator and continuation gates; chain stop at a failed gate; projection gates; stage lists; another source version set aside; local-only rehearsal; analysis definition and bounds; combine; frames, GIF and page; journal tampering; and the 32 reference adapter tests).
- Launcher gate integration: `coordinator.enqueue` is the only path that queues a stage and `coordinator.enqueue_continuation` the only path that queues a continuation; `chain.py` is the only path that executes a queued stage.
- Visualization: [VISUALIZATION.md](VISUALIZATION.md).

## Current attempt admission

Operations entry: manual, through the generic private launcher named in [RUN.md](RUN.md). [Operations guide](../../../toolkit/agent-experiments/OPERATIONS.md).

| Operation | Exact command or unsupported reason | Evidence and last checked revision |
|---|---|---|
| Inspect and offline validation | `python3 src/selftest.py`; `python3 src/worker.py --stage S0 --attempt <name>`; `python3 src/rehearse.py --hub-dir <dir>`; `python3 src/manifest.py --check` | all four passed locally at code commit `b6990122` |
| Prepare named stage | `python3 scripts/run-ready-chain.py memory-handoff-qwen <commit> setup --host <server>` (private launcher) | not run |
| Dispatch named stage | `python3 scripts/run-ready-chain.py memory-handoff-qwen <commit> chain --host <server> --confirm-paid` | not run |
| Resume interrupted execution | `... resume --host <server>`: only after S1 stopped with `provider_credit_balance_low`; refused after any other stop. No other re-execution: a repair is a new attempt number with its own pre-run review | rehearsed offline (scenario e) |
| Analyze saved evidence and rebuild visuals | `... status --host <server>`, `... verify --host <server>` | rehearsed offline |
| Stop this study and close out | operator: stop the chain process, verify uploads, release claim `dmarz-memory-handoff-qwen` | not run |

- Attempt / stage / pre-run assessment: chain-001 (S0, P0, Q0, S1) / [reviews/chain-001-pre.md](reviews/chain-001-pre.md).
- Budget: call caps P0 1, Q0 23, S1 576, 600 for this attempt (ledger study cap 624 including the one permitted repair's qualification); 4 requests in flight; at most 800 transport attempts; ledger cap USD 2 on settled cost plus open reservations; expected spend about USD 0.03.
- Allocation: none. The server is a launcher parameter; the claim id will be `dmarz-memory-handoff-qwen`.
- Credentials: environment alias `SWARM_OPENROUTER_API_KEY`, set by the launcher in memory only. Never in files, arguments or logs.
- Go / no-go: not decided. This builder launches nothing.

## Attempt 002 (the one permitted repair), gate evidence

| Gate | Status | Evidence, timestamp and assessor | Blocker / next action |
|---|---|---|---|
| G1 Plan written before implementation | pass | Preregistration section "Attempt 002" pushed at `415d26a8` before any attempt-002 code; 2026-10-04, dmarz/pipeline-memory | none |
| G2 Instrument and offline checks | pass offline (builder's own checks; Python 3.9.6 on macOS) | 2026-10-04, at code commit `3f1b0b98`, source hash `10f51d2c…`: selftest 88 of 88; offline S0 192 of 192 with 25 of 25 invariants; manifest check equal; rehearsal 36 of 36 checks in 93 s. Details in [reviews/chain-002-pre.md](reviews/chain-002-pre.md) | Not tested: Python 3.12, the real hub, the launcher, how the model writes the working fields |
| G3 Current attempt admission | pass | [Pre-run review of attempt 002](reviews/chain-002-pre.md) on main; launched by dmarz/fleet-monitor at `5831e534` on sim-dmarz-13 after its same-researcher check; 2026-10-04 12:40Z | none |
| G4 Qualification before scientific escalation | pass | P0 1/1; Q0 gate 24 of 24 valid and supported on fixture set b; chain gates (software); 2026-10-04 | none |
| G5 Reconciliation and closeout | pass, with one item not done by the builder | S1 576/576 reconciled; rows recomputed (15 of 15 checks, [records](records/attempt-002/)); [post-mortem](reviews/chain-002-post.md); [RESULTS](RESULTS.md); claim released by the operator; 2026-10-04, dmarz/pipeline-memory | Hub artifact checksums (`verify` on the server) and the frames were not checked by the builder |

Attempt 001's gates: G3 passed (launched by dmarz/fleet-monitor at `0d54225c`, run request 275); G4 failed (Q0 19 of 24 supported); G5 done by dmarz/pipeline ([post-mortem](reviews/chain-001-post.md), [records](records/README.md)). The gate table above this section is the attempt-001 record as written before its run.

## Chain 003 (gpt-6-luna), gate evidence

| Gate | Status | Evidence, timestamp and assessor | Blocker / next action |
|---|---|---|---|
| G1 Plan written before implementation | pass | Preregistration section "Second model: gpt-6-luna" pushed at `0a581405` before the chain's code; amendment (set a, chain 003, launch form) before any call to the model; 2026-10-04, dmarz/pipeline-memory | none |
| G2 Instrument and offline checks | pass offline (builder's own checks; Python 3.9.6 on macOS) | 2026-10-04, at code commit `c2717f74`, source hash `caf5d773…`: selftest 129 of 129; offline S0 192 of 192 with 25 of 25 invariants; manifest check equal; rehearsal 47 of 47 checks in 126 s (both configurations' chains on one hub; OpenAI quota stop and resume). Details in [reviews/chain-003-pre.md](reviews/chain-003-pre.md) | Not tested: Python 3.12, the real hub, the launcher, any response of the OpenAI API |
| G3 Current attempt admission | pass | [Pre-run review of chain 003](reviews/chain-003-pre.md) on main; launched by dmarz/fleet-monitor at `f717bb2d` on sim-dmarz-9 after its same-researcher check; setup ran 129 selftests on the server; 2026-10-04 18:06Z | none |
| G4 Qualification before scientific escalation | pass | P0 1/1; Q0 gate 24 of 24 valid and supported on fixture set a (the 24 requests of attempt 001); chain gates (software); 2026-10-04 | none |
| G5 Reconciliation and closeout | pass | launcher `verify` exit 0, all checks, all stages (saved in [records](records/chain-003/)); rows recomputed 15 of 15; [post-mortem](reviews/chain-003-post.md); [RESULTS](RESULTS.md) section; claim released by the operator; 2026-10-04, dmarz/pipeline-memory | frames not checked by the builder |

## Attempt and repair history

No attempt exists. Offline checks on the build machine are software checks, not attempts: the offline S0 and the rehearsal wrote only to temporary directories, which were deleted, and reported to no real hub.

History before the pin, all on 2026-10-04 and before any run: plan `bee94550`; instrument and chain `1896fb01` (committed under this agent id by a replacement session that the fleet monitor started and stopped; the files were this builder's); rehearsal and invariants `6231492d`; selftest `9a22ef21`; reference adapter revision `639e9501` taken and probe metadata added, code commit `b6990122`, source hash `b4ab9025…`, which is the pin.

| Attempt / parent | Stage / version | Pre-review and receipts | Assigned / started / terminal / graded / analyzed | Post-mortem / disposition |
|---|---|---|---|---|
| 001 / none | S0, P0, Q0 at source hash `b4ab9025…` | [chain-001-pre](reviews/chain-001-pre.md); hub runs `95d12801`, `bc8748ab`, `908c3129` | S0 192/192/192/192/192; P0 1/1/1/1/1; Q0 23/23/23/23/23 (gate over 24: 19 supported); S1 not queued | [chain-001-post](reviews/chain-001-post.md): stopped at the qualification gate; a result; one repair allowed |
| 002 / 001 | S0, P0, Q0, S1 at source hash `10f51d2c…` | [chain-002-pre](reviews/chain-002-pre.md); launch commit `5831e534`; hub runs `6e5badb7`, `94e45249`, `43926309`, `5a6fec17` | S0 192/192/192/192/n.a.; P0 1/1/1/1/1; Q0 23/23/23/23/23 (gate over 24: 24 supported); S1 576/576/576/576/576 | [chain-002-post](reviews/chain-002-post.md): complete valid result; [RESULTS](RESULTS.md) |
| 003 (gpt-6-luna) / 001 | S0, P0, Q0, S1 at source hash `caf5d773…` | [chain-003-pre](reviews/chain-003-pre.md); launch commit `f717bb2d`; hub runs `343255be`, `922c6ba3`, `93ab28b9`, `0a901a43` | S0 192/192/192/192/n.a.; P0 1/1/1/1/1; Q0 23/23/23/23/23 (gate over 24: 24 supported); S1 576/576/576/576/576 | [chain-003-post](reviews/chain-003-post.md): complete valid result; [RESULTS](RESULTS.md) |

## Closeout

Attempt 001: closed by dmarz/pipeline (post-mortem and records linked above); spend USD 0.000684, 24 calls. Attempt 002: closed by dmarz/pipeline-memory (post-mortem, results and records linked above); spend USD 0.026099, 600 calls; decision complete-valid-result. Chain 003: closed by dmarz/pipeline-memory; spend USD 0.07045, 600 calls, own ledger with a USD 5 cap. Study total USD 0.097233 over three separate ledgers; decision complete-valid-result, no further run prepared.

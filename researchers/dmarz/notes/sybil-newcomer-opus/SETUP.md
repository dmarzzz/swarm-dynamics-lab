# Experiment setup record: sybil-newcomer-opus v1

Status: offline checks pass; fleet S0 → P0 probe → Q0 → S1 admitted stage by stage under the owner's standing instruction (G0). Follows [the setup runbook](../../../../tooling/agent-experiments/EXPERIMENT-SETUP.md).

## Ownership and question

- Owner / operator / design reviewer / review independence: owner dmarz; operator dmarz/newcomer-opus (Claude Code on orbital-one, started by dmarz/orchestrator-2 under dmarz's 2026-10-04 goals: five dmarz experiments running, Opus for every new paid stage). No design reviewer; no independent review has occurred.
- Question, intended decision, primary contrast and claim boundary: does the newcomer result change with a stronger synthesizer? Primary contrast unchanged (renewal minus reputation, 16 identities, sleeper, round 8; +10 pp marker). Claims limited to this synthetic task.
- Research status: exploratory model comparison in notes; no accepted hypothesis; formal S2 disabled.
- Previous study/post-mortem and lessons incorporated: [Haiku S1 post-mortem](../sybil-newcomer-api/reviews/s1-001-post.md), [Sonnet S1 post-mortem](../sybil-newcomer-sonnet/reviews/s1-001-post.md), [Sonnet results](../sybil-newcomer-sonnet/RESULTS.md). Lessons: run `publish` before `verify` (artifact order); available truth after admission bounds every synthesizer; Opus 5.5 request rules (compositional-safety q0-006 failed with HTTP 400 from a disabled-thinking request).
- Current stage / next action: claim a free dmarz host (sim-dmarz-13 was created for this study), then setup and S0.

## Gate evidence

| Gate | Status | Evidence, timestamp and assessor | Blocker / next action |
|---|---|---|---|
| G0 Question and applicable research gates | waived by owner | 2026-10-04 ~07:55Z dmarz, first-hand in the operating session (dmarz/orchestrator-2): "Great messages starting [fleet-monitor] as my instructions including claims lUcnhes model switches And budget costs thanks And stop Asking for my permission". Relayed dmarz instructions via fleet-monitor: ~07:36Z "use opus for everything going forward please", ~07:42Z "dont worry about my opus costs yet, just keep reading out the total costs ive paid", ~07:47Z "I want the new goal to be always running 5 experiments". Recorded as an owner waiver of cross-researcher review and owner approval of the Opus configuration; no independent review was performed. | none |
| G1 Plan written before implementation | pass | README, preregistration.md, design.yaml committed before any fleet stage or model call | — |
| G2 Instrument and offline checks | pass | 10/10 selftests (adds Opus request-contract and response-handling tests: thinking-block filtering, refusal, output cap, extra text block); local S0 198/198 valid, qualification passed; Q0 and S1 assignment IDs and packet hashes equal to sybil-newcomer-api (1,944 S1 rows) | — |
| G3 Current attempt admission | pass for s0-001, p0-001, q0-001, s1-001 (each after its predecessor's gate) | reviews/fleet-s0-001-pre.md, q0-001-pre.md, s1-001-pre.md; exclusive claim checked by the launcher | — |
| G4 Qualification before scientific escalation | pass | P0 probe valid (claude-opus-5-5, exact packet); Q0 `sybil-newcomer-opus/39421582` 36/36 valid, qualification_passed 1 | — |
| G5 Reconciliation and closeout | pass | S1 `sybil-newcomer-opus/14ea6e6b` 1,944/1,944 valid; publish + verify passed; local Python 3.12 recomputation matches all assignments, worlds, history, packets, grades and analysis; RESULTS.md, reviews/s1-001-post.md; claim released 2026-10-04 09:00Z (agentops #246); dmarz/newcomer-opus 2026-10-04 | — |

## Design and instrument index

- Plan: [README.md](README.md), [preregistration.md](preregistration.md), [design.yaml](design.yaml), [experiment.yaml](experiment.yaml).
- Independent units: 24 world clusters (7100–7123) × 81 cells = 1,944 S1 calls, paired by assignment ID with the Haiku and Sonnet cohorts.
- Splits: engineering 6900–6901 (S0 and probe), qualification 7000–7005 (Q0), study 7100–7123 (S1), S2 range 12000–12999 unopened.
- Model/provider/config: `claude-opus-5-5`, effort low, no temperature, no thinking field, structured JSON, max_tokens 4,000, answer ≤2,000 chars, 180 s timeout, 2 workers, no retries, $4/$20 per million tokens.
- Source deltas from the Sonnet copy: experiment id (coordinator, worker), design.yaml (model, request block, caps, prices, timeouts), provider.py (Opus request body and response handling), new src/probe.py (P0), two new selftests, banner text. Simulator, study, analysis and prompt unchanged.
- Visualization: [VISUALIZATION.md](VISUALIZATION.md) (inherited mapping v1 with run bindings).

## Current attempt admission

Operations entry: explicitly manual (private launcher `scripts/run-sybil-newcomer-opus.py` in the operator infrastructure repository).

| Operation | Exact command or unsupported reason | Evidence |
|---|---|---|
| Offline validation | `python3 src/selftest.py`; `python3 src/worker.py --stage S0 --attempt <fresh>` | reviews/s0-local-001-post.md |
| Prepare | `run-sybil-newcomer-opus.py <rev> setup` | DEPLOYMENT.md |
| Dispatch | `run-sybil-newcomer-opus.py <rev> S0|P0|Q0|S1` | DEPLOYMENT.md |
| Resume interrupted execution | unsupported: no automatic re-execution; a new attempt needs a new batch and pre-review | — |
| Analyze saved evidence | `run-sybil-newcomer-opus.py <rev> publish` then `verify`; `reporting/*.py` | — |
| Close out | verify, then `agentops.py release dmarz-sybil-newcomer-opus --status done` | — |

- Budget: own ledger; 2,050 attempted calls; USD 400 reservation ceiling; owner: cost not a gate, report totals.
- Allocation: host from the exclusive claim `dmarz-sybil-newcomer-opus` (sim-dmarz-13 was created for this study and is preferred).
- Credentials: dmarz model-configuration aliases decrypted by the launcher and passed over SSH stdin to process memory; no values recorded.

## Attempt and repair history

| Attempt / parent | Stage / version | Pre-review and receipts | Assigned / started / terminal / graded / analyzed | Post-mortem / disposition |
|---|---|---|---|---|
| s0-local-001 | local S0 v1 | reviews/s0-local-001-pre.md | 198/198/198/198/198 | reviews/s0-local-001-post.md: advance |

## Closeout

Pending.

# Experiment setup record: sybil-scale-xl v1

Status: exploratory scale-up; setup record maintained per [the setup runbook](../../../../tooling/agent-experiments/EXPERIMENT-SETUP.md). Not launch authorization by itself; each stage's pre-run assessment governs.

## Ownership and question

- Owner dmarz; operator dmarz/scale-xl (Claude Code on orbital-one); design inherited from dmarz/sybil-specialists' [sybil-scale-api](../sybil-scale-api) through the [sybil-scale-sonnet](../sybil-scale-sonnet) copy. No independent design review; dmarz directed this run on 2026-10-04 and nothing here claims an independent review.
- Question: does proportional verification keep specialist accuracy near ceiling, and does Haiku 4.5 still integrate the admitted reports, when the simulated swarm grows from 972 to 8,748 identities (packets of up to 4,374 reports)? Primary contrast: coverage, visible, attacker pass 0.10, proportional minus fixed checks at N=8,748. Claim boundary: one graph family, simulated identities, exploratory.
- Research status: exploratory scale-up. Survey/hypothesis gates not met; S2 disabled.
- Prior study and lessons: [parent RESULTS](../sybil-scale-api/RESULTS.md), [parent S1 post-mortem](../sybil-scale-api/reviews/s1-001-post.md). Lessons kept: long packets need preparation heartbeats (worker already sends them); Python 3.12 for exact numeric reproduction; physically deduplicated conditions; the parent's next-study note asked for more distinct facts and fixed-resource splitting, which this study does not attempt.
- Current stage / next action: see the gate table.

## Gate evidence

| Gate | Status | Evidence, timestamp and assessor | Blocker / next action |
|---|---|---|---|
| G0 Question and applicable research gates | pass (exploratory scope) | README, preregistration; 2026-10-04 dmarz/scale-xl | S2 stays disabled |
| G1 Plan written before implementation | pass | README, preregistration, design and reviews committed before any fleet stage | — |
| G2 Instrument and offline checks | pass (selftests); S0 moves to fleet | 11/11 selftests incl. exact equality with the parent simulator at N=36–972; local S0 interrupted by host OOM ([post](reviews/local-s0-001-post.md)) | fleet S0 |
| G3 Current attempt admission | pending | claim dmarz-sybil-scale-xl on sim-dmarz (agentops PR 176, merged 06:03Z, until ~20:03Z); launcher agentops cc3f862 | pin revision; setup; per-stage pre-run files |
| G4 Qualification before scientific escalation | pending | Q0 per size | — |
| G5 Reconciliation and closeout | pending | — | verify, results, post-mortem, release claim |

## Design and instrument index

- Plan: README.md, preregistration.md, design.yaml (this directory); history in git.
- Independent units: 24 world clusters (S1); 4 qualification worlds (Q0); 2 engineering worlds (S0). Conditions per world and size: 28 (7 arm/budget checkpoints × 2 attacker pass rates × 2 badge modes).
- Sample size: fixed to the parent's 24 worlds so every cell pairs by world with the parent; not powered for small differences.
- Splits: engineering 4900–4901, qualification 5000–5003, S1 6000–6023, holdout 10000–19999 unopened.
- Agent definition: one stateless synthesizer call per assignment; prompt and schema in src/provider.py, identical to the parent.
- Versions: model claude-opus-5-5, effort low (amendment A1; v1 was claude-haiku-4-5-20251001); requirements.txt pinned; runtime source hash recorded per run.
- Offline checks: selftest (anchor equality with sybil-specialists, parent-simulator equality for the faster selection, graph scaling, Q0 packet size, blind packets, ledger cap/duplicates, render failure states, principal-blind checks, splits, invalid answers, concurrent failure denominators).
- Launcher gate integration: coordinator refuses duplicate batches and requires exactly one passed prerequisite stage at the same source hash; private launcher refuses without an exclusive merged claim.
- Visualization: [VISUALIZATION.md](VISUALIZATION.md) v1 plus the combined parent+XL figure.

## Current attempt admission

Operations entry: manual (private launcher). [Operations guide](../../../../tooling/agent-experiments/OPERATIONS.md).

| Operation | Exact command or unsupported reason | Evidence and last checked revision |
|---|---|---|
| Inspect and offline validation | `python3 src/selftest.py`; `python3 src/worker.py --stage S0 --attempt <name>` | local-s0-001 |
| Prepare named stage | `python3 scripts/run-sybil-scale-xl.py <commit> setup` (agentops) | per stage |
| Dispatch named stage | `… <commit> S0|Q0|S1` | per stage |
| Resume interrupted execution | unsupported by design: no automatic re-execution; a new attempt id is required | — |
| Analyze saved evidence and rebuild visuals | `… <commit> status|verify|publish`, `--save <path>`; reporting/build_report.py | after S1 |
| Stop this study and close out | stop worker, verify uploads, `agentops.py release dmarz-sybil-scale-xl --status done` | — |

- Credentials: dmarz model-key aliases from agentops SOPS, memory-only via SSH stdin; never in argv or on disk.
- Budget (A1): dmarz chose the trimmed Opus design, estimated USD 186–270, within the shared USD 500 allowance (about USD 340 left). Ledger cap USD 330 on settled cost plus open reservations, 700 calls. See AMENDMENT-A1.md.
- Allocation: sim-dmarz (idle, no active claim, no worker at 06:02Z), exclusive claim dmarz-sybil-scale-xl.

## Attempt and repair history

| Attempt / parent | Stage / version | Pre-review and receipts | Assigned / started / terminal / graded / analyzed | Post-mortem / disposition |
|---|---|---|---|---|
| local-s0-001 / — | S0 offline / v1 | (offline engineering check) | 216 assigned / 0 recorded (host out of memory) | [interrupted; repaired pool cap](reviews/local-s0-001-post.md) |
| fleet-s0-001 (33d602fe) / local-s0-001 | S0 fleet / v1 | [pre](reviews/fleet-s0-001-pre.md) | 216/216/216/216/216 | [pass](reviews/fleet-s0-001-post.md); Haiku Q0/S1 not launched (Opus directive) |
| s0-a1 (4673b7bd) / fleet-s0-001 | S0 fleet / A1 | [pre](reviews/s0-a1-pre.md) | 72/72/72/72/72 | pass (chain gate) |
| q0-a1 (a6b2a7b3) / s0-a1 | Q0 Opus / A1 | [pre](reviews/q0-a1-pre.md) | 24/24/24/24/24 | [pass, USD 9.85](reviews/q0-a1-post.md) |
| s1-a1 (7a32ec63) / q0-a1 | S1 Opus / A1 | [pre](reviews/s1-a1-pre.md) | 576 assigned / 0 started | [stopped in preparation for A2](reviews/s1-a1-post.md) |
| s0-a2, q0-a2, s1-a2 / q0-a1 | A2 (overload retry) | [pre](reviews/s0-a2-pre.md) | chained | pending |

## Closeout

Pending.

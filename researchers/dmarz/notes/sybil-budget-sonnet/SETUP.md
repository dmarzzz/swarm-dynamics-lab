# Experiment setup record: sybil-budget-sonnet / v1

Status: prospective setup record, started before any run of this study. Follows [the setup runbook](../../../../tooling/agent-experiments/EXPERIMENT-SETUP.md). Historical receipts and attempts are preserved below.

## Ownership and question

- Owner: dmarz. Operator: dmarz/budget-sonnet (a Claude Code fork on orbital-one, working under dmarz's session goal of keeping at least 3 experiments running). Design checks are same-owner engineering checks, not independent review.
- Review gate: **pending an owner decision.** No independent review exists, and no waiver for this study is recorded in this file. The parent's owner waiver covered sybil-budget-api only. Paid stages (Q0, S1) wait until dmarz records a review decision for this study.
- Question: on packets identical to the parent's (both sizes), does Sonnet 4.6 change specialist accuracy and the tested verification-budget frontier relative to Haiku 4.5? Primary contrasts are in [preregistration.md](preregistration.md).
- Research status: exploratory model replication in owned notes. No accepted hypothesis or novelty survey is claimed. S2 is disabled.
- Prior evidence read: parent [README](../sybil-budget-api/README.md), [S1 pre-run](../sybil-budget-api/reviews/s1-001-pre.md), [Q0 post-mortem](../sybil-budget-api/reviews/q0-001-post.md), [scale-study results](../sybil-scale-api/RESULTS.md). The parent S1 post-mortem had not been written at setup time. Its run `sybil-budget-api/46ebda03` completed 2,880/2,880 valid ($39.35).

## Gate evidence

| Gate | Status | Evidence, timestamp and assessor | Blocker / next action |
|---|---|---|---|
| G0 Question and applicable research gates | waived by owner | 2026-10-04 ~05:40Z in the operating session (dmarz/orchestrator-2): proposed "I waive cross-researcher review for sybil-newcomer-sonnet, sybil-scale-sonnet and sybil-budget-sonnet ..."; dmarz replied "Yes I approved go for it", then "Go go go". Spend: dmarz chose "Stop worrying about spend" (full 120-cell grid). Owner waiver only; no independent review performed. | none |
| G1 Plan written before implementation | pass | README (TLDR/Question/Setup/Protocol/Metrics), preregistration.md, design.yaml committed before any fleet or paid run | none |
| G2 Instrument and offline checks | pass | 10/10 selftests; [local S0-002 post](reviews/s0-local-002-post.md) 256/256 valid; full parity receipt `reporting/parity-receipt.json` | none |
| G3 Current attempt admission | per attempt | stage pre-runs in `reviews/`; plan receipts `reviews/*-plan-receipt.json`; claim `dmarz-sybil-budget-sonnet` | repeat before each stage |
| G4 Qualification before scientific escalation | pending | fleet S0 then Q0 at the same source hash | Q0 must pass before S1 |
| G5 Reconciliation and closeout | pending | post-mortems, verify receipt, claim release | after S1 |

## Design and instrument index

- Plan: [README.md](README.md), [preregistration.md](preregistration.md), [design.yaml](design.yaml), [reservation-plan.json](reservation-plan.json).
- The scenario contract, evaluator and actor inputs are inherited byte-for-byte from the parent (`src/sim.py`, `src/study.py`, `src/analyze.py`). `src/provider.py` equals sybil-scale-api's provider (own ledger, no shared partition).
- Units: 24 worlds (7000–7023) paired across 120 cells and across the two model cohorts. 2,880 S1 calls, 16 Q0 calls, 256 S0 rows. Exploratory precision only.
- Splits: engineering 6800–6801, qualification 6900–6903, scientific 7000–7023, holdout 10000–19999 closed.
- Model: `claude-sonnet-4-6`, temperature 0, strict JSON schema, 500 output tokens, no tools/thinking/cache/retries. Python 3.12, pinned requirements.
- Launcher: `scripts/run-sybil-budget-sonnet.py` in swarm-labs-agentops (claim-checked; secrets SOPS → ssh stdin → worker env). Coordinator gates: duplicate batch refused; Q0 needs a passing S0 at the same source hash; S1 needs a passing Q0.
- Visualization: [mapping v1](VISUALIZATION.md).

## Current attempt admission

Operations entry: manual (not in the `scripts/experiment.py` registry). See [operations guide](../../../../tooling/agent-experiments/OPERATIONS.md).

| Operation | Exact command | Evidence |
|---|---|---|
| Inspect and offline validation | `cd src && python3 selftest.py`; `python3 reporting/parity_check.py reporting/parity-receipt.json` | G2 |
| Public plan check | `python3 reporting/plan_preflight.py --run-tldr "..." --receipt reviews/<attempt>-plan-receipt.json` | G3 |
| Prepare named stage | `python3 scripts/run-sybil-budget-sonnet.py <rev> setup` (agentops) | |
| Dispatch named stage | `python3 scripts/run-sybil-budget-sonnet.py <rev> S0` (or `Q0`, `S1`) | stage pre-runs |
| Resume interrupted execution | unsupported: no automatic replay; a new attempt needs a new pre-run | |
| Analyze saved evidence and rebuild visuals | `... <rev> verify --save <local path>`, then reporting scripts | |
| Stop this study and close out | `... <rev> publish`; `python3 scripts/agentops.py release dmarz-sybil-budget-sonnet --status done` | |

Budget authority: dmarz's $500 shared allowance. Study reservation cap $400; worst case at most $392.26; expected actual about $100–140. Credentials: aliases `SWARM_MODEL_API_KEY` and `SWARM_MODEL_WORKSPACE_ID` from dmarz's encrypted model configuration in agentops, never in argv, disk or this repository.

## Attempt and repair history

| Attempt / parent | Stage | Pre-review | Assigned / started / terminal / graded / analyzed | Post-mortem |
|---|---|---|---|---|
| local-s0-001 / none | S0 scripted, local, superseded N972-only design | [pre](reviews/s0-local-001-pre.md) | 128/128/128/128/128 | [post](reviews/s0-local-001-post.md), pass; design amended afterwards (README Amendments) |
| local-s0-002 / local-s0-001 | S0 scripted, local, full grid | [pre](reviews/s0-local-002-pre.md) | 256/256/256/256/256 | [post](reviews/s0-local-002-post.md), pass |

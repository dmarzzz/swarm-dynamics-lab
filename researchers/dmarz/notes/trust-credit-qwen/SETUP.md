# Experiment setup record: trust-credit-qwen v1 (program v5, line T)

Status: prepared, not launched. This record follows [the setup runbook](../../../../tooling/agent-experiments/EXPERIMENT-SETUP.md) and is not launch authorization. A run starts only when the orchestrator takes a request from the private run queue after dmarz/fleet-monitor's same-researcher check. Nothing has run on a server and no model call has been made.

## Ownership and question

- Owner dmarz. Builder dmarz/pipeline-split (Claude Code, offline on dmarz's Mac), working for the pipeline lead dmarz/pipeline. Operator: whoever takes the queued request; the server is a launcher parameter. Review independence: none. As relayed to this builder by dmarz/pipeline on 2026-10-04: dmarz directed this program himself (research program v5, written with him by a Codex session on 2026-10-04; his instruction to ship it was relayed by dmarz/fleet-monitor). The design is the program's; this package implements line T as specified there. Cross-researcher review is waived by dmarz for these exploratory runs; dmarz/fleet-monitor's check is a same-researcher check and nothing more; the run is not independently reviewed.
- Question: does propagating a passed identity's trust credit to its neighbours cause extra attacker identities to be admitted? Primary: [attacker seats (propagated, 108) − (propagated, 32)] − [attacker seats (direct, 108) − (direct, 32)] at strong checking, per root, 24 roots. Claim boundary: scripted identities, one graph family, one audit policy; the primary is a scripted admission outcome.
- Research status: exploratory line of a program in researcher notes. Survey and hypothesis gates are not met; S2 is disabled.
- Prior study and lessons: [sybil-budget-api results](../sybil-budget-api/RESULTS.md) (attacker seat share rose with the coverage budget at N = 324 while accuracy rose); [pipeline lessons](../pipeline/LESSONS.md) items 1, 3, 6 and 7 (caps and timeouts sized before qualification; one-call probe; read failing answers before a repair; small gates misclassify).
- Current stage and next action: see the gate table.

## Gate evidence

| Gate | Status | Evidence, timestamp and assessor | Blocker / next action |
|---|---|---|---|
| G0 Question and applicable research gates | pass (exploratory scope only) | program v5 line T; README and preregistration, 2026-10-04T10:42Z, dmarz/pipeline-split | formal gates not met; S2 disabled |
| G1 Plan written before implementation | pass | README, preregistration, design.yaml, experiment.yaml and this record committed before the study code; the admission replay existed as uncommitted working files used for the calibration below | none |
| G2 Instrument and offline checks | pending | to be filled when selftest, offline S0, rehearsal and the manifest check have run | implement and test |
| G3 Current attempt admission | pending | pre-run review to be written after the code is pinned | fleet-monitor check, run-queue request, server claim |
| G4 Qualification before scientific escalation | pending | P0 and Q0 are stages of the chain; S1 is admitted only after the 24-fixture gate passes at the same source hash | run |
| G5 Reconciliation and closeout | pending | none | run |

## Design and instrument index

- Plan: [README.md](README.md), [preregistration.md](preregistration.md), [design.yaml](design.yaml).
- Independent units: 24 comparison roots; per root 18 attacked cells and 3 clean endpoints (21 calls). 8 engineering roots, 8 + 8 qualification roots.
- Sample size: the program's (24 roots, 504 calls). Not a power claim.
- Splits: engineering 4481-4488; qualification 4591-4598; repair qualification 4650-4657; comparison 9541-9564; holdout 10000-19999 unopened.
- Agent definition: one stateless synthesizer call per assignment; instruction text and local answer validation in `src/study.py`; adapter `src/provider.py` is the pipeline's reference OpenRouter adapter, copied unchanged.
- Versions: `qwen/qwen3.7-flash` (canonical slug observed by the program: `qwen/qwen3.7-flash-20260727`), provider Alibaba; requirements.txt pinned; the source hash covers design.yaml, experiment.yaml, requirements.txt and `src/*.py`.

### Root-range scan (2026-10-04T10:42Z)

Every text file under `researchers/`, `experiments/`, `hypotheses/`, `tooling/`, `templates/`, `src/`, `scripts/`, `tasks/`, `synthesis/`, `surveys/` and `reviews/` (yaml, yml, json, md, py, txt, csv, sh; files over 5 MB skipped; 3,880 files) was searched for every four-digit number as a standalone token. The chosen ranges 4481-4488, 4591-4598, 4650-4657 and 9541-9564 do not occur anywhere outside this directory. A first choice for the qualification roots (4533-4540) was dropped because 4540 occurs in an unrelated state snapshot. The scan is repeated before the pre-run review.

### Engineering calibration (2026-10-04, no model call)

Roots 4481-4488, scripted admission only. Each number is a mean over the 8 roots; columns are 32, 64, 108 checks.

| Controller check pass | Rule | Attacker seats | Honest-specialist retention | Truth plurality (rare skills) |
|---|---|---|---|---|
| 0.1 | propagated | 2.25, 13.25, 15.50 | 0.31, 0.63, 0.77 | 1.00, 1.00, 1.00 |
| 0.1 | direct | 20.50, 17.88, 10.38 | 0.31, 0.36, 0.40 | 0.75, 0.88, 1.00 |
| 0.1 | anchors | 22.12, 17.88, 6.62 | 0.29, 0.31, 0.34 | 0.33, 0.79, 1.00 |
| 0.9 | propagated | 32.12, 50.38, 51.25 | 0.36, 0.68, 0.52 | 0.54, 0.58, 0.25 |
| 0.9 | direct | 24.88, 28.50, 33.75 | 0.30, 0.35, 0.38 | 0.25, 0.42, 0.42 |
| 0.9 | anchors | 23.50, 23.38, 23.50 | 0.29, 0.28, 0.29 | 0.04, 0.12, 0.21 |

- Direction check required by the lead: under `propagated` at strong checks the attacker seat share is 1.4%, 8.2%, 9.6% at 32, 64, 108 checks; the budget study reported 1.98%, 8.51%, 10.70% on its own 24 roots. Same direction.
- Primary on the engineering roots: per root 29, 22, 19, 23, 31, 12, 32, 19 seats; mean +23.4. Not at a floor or ceiling, and not constant.
- Truth availability (at least one honest report per rare skill) is 1.00 in every cell: that guardrail is at its ceiling on these roots and is reported as such.
- Under `direct` and `anchors` the attacker holds more seats at 32 checks than under `propagated`. The primary contrast does not show this; the README says so and every stratum is reported.
- Historical audit: 12 of 48 engineering snapshots contain one or two dangling identities. The `propagated` admitted set equals the earlier implementation's in 42 of 48 snapshots and in every snapshot without a dangling identity; in the other 6 it differs by 6 to 13 of 162 seats, and the attacker seat count differs by at most 1.
- Request size: 5.90 to 5.97 kB for every comparison and qualification request (instruction 1,125 characters; 162 rows); limit 7,600 bytes.

## Current attempt admission

Operations entry: manual, through the generic private launcher `scripts/run-ready-chain.py` in the agentops repository. [Operations guide](../../../../tooling/agent-experiments/OPERATIONS.md).

| Operation | Exact command or unsupported reason | Evidence and last checked revision |
|---|---|---|
| Inspect and offline validation | `python3 src/selftest.py`; `python3 src/worker.py --stage S0 --attempt <name>`; `python3 src/rehearse.py --hub-dir <dir>`; `python3 src/manifest.py --check` | pending (code not yet committed) |
| Prepare named stage | `python3 scripts/run-ready-chain.py trust-credit-qwen <launch commit> setup --host <server>` | pending |
| Dispatch named stage | `python3 scripts/run-ready-chain.py trust-credit-qwen <launch commit> chain --host <server> --confirm-paid` | pending |
| Resume interrupted execution | only after a billing stop (`provider_credit_balance_low`): `python src/chain.py resume`; otherwise unsupported by design | pending |
| Analyze saved evidence and rebuild visuals | `... status --host <server>`, `... verify --host <server>` | pending |
| Stop this study and close out | stop the chain process, verify uploads, release claim `dmarz-trust-credit-qwen` | pending |

- Attempt: chain-001 (S0, P0, Q0, S1); no parent attempt; pre-run assessment pending.
- Budget authority: program v5 as relayed (see Ownership); hard call caps P0 1, Q0 23, S1 504, total 528; ledger cap USD 2.
- Allocation: none yet; the operator takes the exclusive claim `dmarz-trust-credit-qwen` at launch.
- Credentials: `SWARM_OPENROUTER_API_KEY`, supplied in memory by the launcher; never written to a file, an argument or a log. No credential was used to prepare this package.
- Go/no-go: not decided. This builder does not launch.

## Attempt and repair history

| Attempt / parent | Stage / version | Pre-review and receipts | Assigned / started / terminal / graded / analyzed | Post-mortem / disposition |
|---|---|---|---|---|
| none yet | | | | |

## Closeout

Pending. Nothing has run.

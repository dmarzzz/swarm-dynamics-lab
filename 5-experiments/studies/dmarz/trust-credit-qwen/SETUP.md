# Experiment setup record: trust-credit-qwen v1 (program v5, line T)

Status: chain-001 completed on 2026-10-04 (see Gate evidence and Closeout). This record follows [the setup runbook](../../../../tooling/agent-experiments/EXPERIMENT-SETUP.md) and is not launch authorization. A run starts only when the orchestrator takes a request from the private run queue after dmarz/fleet-monitor's same-researcher check. The builder made no model call; the 528 calls of the run were made on the server by the chain.

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
| G1 Plan written before implementation | pass | README, preregistration, design.yaml, experiment.yaml and this record committed (32f751b0) before the study code (baefdb6b, revised in d3219ceb); the admission replay existed as uncommitted working files used for the calibration below. One dated amendment before any run: A1 in the preregistration (adapter revision, wider billing detector, reservation margin, repair-attempt allowance) | none |
| G2 Instrument and offline checks | pass (offline, builder's own checks) | 2026-10-04T11:45Z, dmarz/pipeline-split, on commit d3219ceb (source hash e24e85f5..., after amendment A1): selftest 73 tests OK; offline S0 216/216 valid, 0 violations, 0 calls; manifest check current (digest e09119d1...); rehearsal against a throwaway local hub with a stubbed endpoint passes the full chain, the failed-qualification stop and a billing stop with resume; details in [the pre-run review](reviews/chain-001-pre.md) | the live route and the full suite under Python 3.12 with numpy and Pillow are untested until the server |
| G3 Current attempt admission | pass | [reviews/chain-001-pre.md](reviews/chain-001-pre.md), status ready; dmarz/fleet-monitor's same-researcher check; run queue 270; launched 2026-10-04T11:33Z at launch commit e5f34521 (source hash e24e85f5…) on sim-dmarz-8 by dmarz/fleet-monitor; launcher setup verified the source hash | none |
| G4 Qualification before scientific escalation | pass | P0 1/1 (interface), Q0 23/23; the 24-fixture gate passed with 8 of 8 exactly right in each group, including null on all 8 withheld facts; S1 was admitted by the software gate at the same source hash; records/q0-summary.json | none |
| G5 Reconciliation and closeout | pass (builder's own review) | 2026-10-04, dmarz/pipeline-split: 744 of 744 rows reconciled, regraded and re-analyzed from [records/](records/); `verify` exit 0 on the server; [RESULTS.md](RESULTS.md); [reviews/chain-001-post.md](reviews/chain-001-post.md), verdict complete_valid_result; claim released by the operator | hub images not inspected in the review (see post-mortem) |

## Design and instrument index

- Plan: [README.md](README.md), [preregistration.md](preregistration.md), [design.yaml](design.yaml).
- Independent units: 24 comparison roots; per root 18 attacked cells and 3 clean endpoints (21 calls). 8 engineering roots, 8 + 8 qualification roots.
- Sample size: the program's (24 roots, 504 calls). Not a power claim.
- Splits: engineering 4481-4488; qualification 4591-4598; repair qualification 4650-4657; comparison 9541-9564; holdout 10000-19999 unopened.
- Agent definition: one stateless synthesizer call per assignment; instruction text and local answer validation in `src/study.py`; adapter `src/provider.py` is the pipeline's reference OpenRouter adapter, copied unchanged.
- Visualization: [VISUALIZATION.md](VISUALIZATION.md), mapping v1.
- Versions: `qwen/qwen3.7-flash` (canonical slug observed by the program: `qwen/qwen3.7-flash-20260727`), provider Alibaba; requirements.txt pinned; the source hash covers design.yaml, experiment.yaml, requirements.txt and `src/*.py`.

### Root-range scan (2026-10-04T10:42Z)

Every text file under `researchers/`, `experiments/`, `hypotheses/`, `tooling/`, `templates/`, `src/`, `scripts/`, `tasks/`, `synthesis/`, `surveys/` and `reviews/` (yaml, yml, json, md, py, txt, csv, sh; files over 5 MB skipped; 3,880 files) was searched for every four-digit number as a standalone token. The chosen ranges 4481-4488, 4591-4598, 4650-4657 and 9541-9564 do not occur anywhere outside this directory. A first choice for the qualification roots (4533-4540) was dropped because 4540 occurs in an unrelated state snapshot. Repeated at 11:10Z (3,956 files): still no occurrence.

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
| Inspect and offline validation | `python3 src/selftest.py`; `python3 src/worker.py --stage S0 --attempt <name>`; `python3 src/rehearse.py --hub-dir <dir>`; `python3 src/manifest.py --check` | all pass on d3219ceb (builder, offline) |
| Prepare named stage | `python3 scripts/run-ready-chain.py trust-credit-qwen <launch commit> setup --host <server>` | pending |
| Dispatch named stage | `python3 scripts/run-ready-chain.py trust-credit-qwen <launch commit> chain --host <server> --confirm-paid` | pending |
| Resume interrupted execution | only after a billing stop (`provider_credit_balance_low`): `python src/chain.py resume`; otherwise unsupported by design | pending |
| Analyze saved evidence and rebuild visuals | `... status --host <server>`, `... verify --host <server>` | pending |
| Stop this study and close out | stop the chain process, verify uploads, release claim `dmarz-trust-credit-qwen` | pending |

- Attempt: chain-001 (S0, P0, Q0, S1); no parent attempt; pre-run assessment [reviews/chain-001-pre.md](reviews/chain-001-pre.md), status ready, not launched.
- Frozen assigned manifest: [manifest.json](manifest.json), digest e09119d1f0fcad81876d7b87cf94cf639725f026aa20007f8eea9be4a0129f50.
- Budget authority: program v5 as relayed (see Ownership); hard call caps P0 1, Q0 23, S1 504, total 528 for this attempt (ledger study cap 552 including the one repair attempt's 24); ledger cap USD 2.
- Allocation: none yet; the operator takes the exclusive claim `dmarz-trust-credit-qwen` at launch.
- Credentials: `SWARM_OPENROUTER_API_KEY`, supplied in memory by the launcher; never written to a file, an argument or a log. No credential was used to prepare this package.
- Go/no-go: not decided. This builder does not launch.

## Attempt and repair history

| Attempt / parent | Stage / version | Pre-review and receipts | Assigned / started / terminal / graded / analyzed | Post-mortem / disposition |
|---|---|---|---|---|
| chain-001 / none | S0, P0, Q0, S1 / source hash e24e85f5… | [pre](reviews/chain-001-pre.md); run queue 270; hub runs 81f7ffe1, 135ea6a1, f65a2ee6, d9c433dd | S0 216/216/216/216/216; P0 1/1/1/1/1; Q0 23/23/23/23/23; S1 504/504/504/504/504 | [post](reviews/chain-001-post.md): complete_valid_result |

## Closeout

- Execution complete; response validity 528 of 528; qualification passed; scientific conclusion exploratory (scripted primary +20.75 seats, with the level caveat stated in RESULTS.md); process: plan, amendment and pre-run review before the run, same-researcher check only; reporting: RESULTS.md, records and post-mortem on main.
- All outcomes retained; raw-to-summary recomputation in `reporting/build_report.py`; hub images not inspected by the builder.
- Actual cost USD 0.052047; no reservation left unsettled.
- No missing outcome, exclusion or deviation. Post-run computations are labelled in RESULTS.md.
- Chain process exited; verify exit 0; claim released (operator's report).
- Next action: none. The pre-registered repair attempt was not needed.

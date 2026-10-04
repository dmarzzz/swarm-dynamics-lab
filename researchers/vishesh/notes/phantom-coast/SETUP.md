# Experiment setup record: Phantom Coast PC-1L

Retrospective index created during S0-A1 on 2026-10-04 UTC. This index is not preregistration. Follow the [setup runbook](../../../../tooling/agent-experiments/EXPERIMENT-SETUP.md). The runbook requirement landed in commit 64a663a6 at 04:12:39 UTC, after Q0 completed and before S0 dispatch; it was noticed during S0 closeout preparation. The missing centralized setup record is a process gap, not a missing public plan or grounds to relabel observed responses. Future launches must include this record at admission.

## Ownership and question

Owner, operator and self-reviewer: vishesh/codex-phantom-coast. No independent reviewer is claimed. Research status: exploratory instrument; no accepted formal hypothesis. Owner explicitly requested running this bounded experiment and authorized $5 total. Scoped diagnostic direction is recorded in PC-1L; the formal prior-art/hypothesis/researcher-review gates remain incomplete.

Question: does earlier report order leave maps different after the same final evidence, and does social exchange with retained maps alter that disagreement? Intended decision: whether to pursue memory repair versus testing actual acquisition of evidence. Fixed-evidence synthetic grids do not test adaptive scouting or changed model weights.

## Gate evidence

| Gate | Status | Evidence and assessor | Next action |
|---|---|---|---|
| G0 Research gates | Incomplete; scoped diagnostic authority only | [Original assessment](REPORT.md), [PC-1L](LIVE-PLAN.md); self-review | Independent review before formal claims |
| G1 Prospective design | Pass | Original c4e3dd9; native amendment fa967eef; authorized budget revision 1ba879ac, all before corresponding execution | Preserve immutable versions |
| G2 Instrument | Pass | [46 checks](LIVE-VALIDATION.json), repeated on allocated host; source 1ba879ac | Keep frozen through both stages |
| G3 Q0 admission | Pass for scoped diagnostic; setup index absent | [Q0 launch receipt](reviews/Q0-A1-LAUNCH.json), [deployment](DEPLOYMENT.md) | Historical gap remains recorded |
| G4 Qualification | Pass | [Q0 post-mortem](reviews/Q0-A1-POST.md): 18 valid, 648 correct cells | S0 uses identical frozen source |
| G3 S0 admission | Prospective receipts pass; setup-index process gap | [S0 pre-assessment](reviews/S0-A1-PRE.md), [launch receipt](reviews/S0-A1-LAUNCH.json) published before launch | Audit and close out |
| G5 Closeout | In progress | Saved native records and hub artifacts | Reconcile every assignment, publish analysis, remove runtime credential, release claim |

## Design and instrument index

- [PC-1](PLAN.md) and [PC-1L amendment](LIVE-PLAN.md) define scenarios, contrasts, metrics and claims. Six Q0 worlds 200–205; six independent S0 worlds 206–211; three actors per swarm. Development 100–103, holdout 1000+ unopened. No repair attempt.
- Q0: 18 requests; S0: 522 requests (432 swarm, 72 pooled, 18 clean). Six roots are a descriptive pilot, not a powered population estimate.
- Definitions, prompts and context: [instrument.py](src/instrument.py), [native.py](src/native.py). Model typesafe/jev-1.13-20260917, TypeSafe only. Runtime Pillow12.2.0, PyYAML6.0.3. Qualification and pilot source 1ba879ac84a54b82f21c0f597760cfebaf43f3bf.
- [live_worker.py](src/live_worker.py) performs source/config/assignment/public-plan/claim/budget gates; [budget.py](src/budget.py) preserves cumulative reservations. Tests cover missing/duplicate/uncertain calls and hub acknowledgement before paid dispatch. Native saved requests support byte-level treatment audit.
- PC-V2 mapping in PC-1L: actual-record PNG/GIF plus complete JSON. The original fixture viewer remains explicitly a software fixture. Final native frame is one actor, not a cohort summary.

## Attempt admission and resource authority

Immutable public plan: https://github.com/dmarzzz/swarm-lab/blob/1ba879ac84a54b82f21c0f597760cfebaf43f3bf/researchers/vishesh/notes/phantom-coast/LIVE-PLAN.md . Hash and condition-specific TLDRs are in each launch receipt and native config. Public page was checked before Q0 and rechecked during S0: the expected plan, stage counts and reporting are rendered.

Budget reference phantom-coast-usd5-20261004: $5 total, $4 API, $1 infrastructure, 540 calls, one worker, 60 minutes per stage, six-hour host limit. Same remote SQLite ledger across Q0/S0; no retries; stop at five consecutive failures or before reservation exceeds cap. Q0 consumed $0.005926284, leaving $3.994073716 API allowance before S0.

Exclusive existing Mars host sim-dmarz-5, claim vishesh-phantom-coast-q0, expiry 2026-10-04T10:06:11Z. Merged claim PR100; no competing active/planned claim or experiment workload at allocation. No new provisioning, account login or infrastructure expense. Authorized processes consume a protected credential file; no credential content is an artifact. Configs bind fresh claim checks, source and assignment hashes. Exact worker command: `python src/live_worker.py --stage Q0|S0 --config <stage-config> --out <fresh-output> --ledger <shared-ledger> --credential-file <protected-file>` from the frozen repository; full non-secret config preserved with each attempt.

## Attempt history and closeout

Q0-A1 completed and passed. S0-A1 is the already prescribed comparison, not a tuned rerun. Final reconciliation, usage and artifact hashes will be indexed in RESULTS.md and S0-A1 post-mortem. Execution, validity, scientific conclusion, process compliance and visualization remain separate. Next-stage work requires a fresh prospective design and admission; unused funds do not authorize automatic expansion.

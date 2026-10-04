# Run assessment and repair cycle

Every experiment uses this cycle, including local pilots, scripted qualification, interrupted attempts and successful runs:

**Plan and assess → freeze → execute → reconcile and review → repair → qualify again → advance.**

This is the operator/agent workflow. It does not add automatic launch enforcement to existing workers. Existing survey, hypothesis, spending, data-access and server-claim requirements still apply.

## Before each run

Copy [pre-run.md](templates/pre-run.md) into the experiment's `reviews/<attempt>-pre.md`. Read the preceding post-mortem first. For exploratory work, keep reviews under the owned notes directory. Record:

- The question, intended decision value, strongest baseline and what would make the study uninformative.
- The precise change since the previous attempt, unresolved issues and their acceptance checks.
- Design quality: independent units, task/label coverage, evidence and resource matching, evaluator validity, leakage, timing semantics, and positive/negative controls.
- Frozen protocol/config/model/prompt/evaluator versions, assignments, seeds, stage and untouched holdout.
- Maximum calls, time, spend and worker count; retry policy, safe stopping, credentials by alias only, server claim and artifact destination.
- Evidence that regression checks and required competence screens passed, or why the run is specifically a bounded diagnostic to repair a failed screen.

Commit the completed assessment and protocol changes before model execution. Use `ready`, `diagnostic-only`, or `blocked` with a reason. A failed qualification blocks a broader scientific sweep, **not** continued diagnostic/repair work within the authorized budget. Do not use a pre-run form to bypass formal research gates.

## After each attempt

Copy [post-mortem.md](templates/post-mortem.md) to `reviews/<attempt>-post.md`. Setup failures and interrupted runs need a short post-mortem too. Reconcile every assigned episode against started, terminal, graded and analyzed records. Report failures, duplicate attempts, missing data and actual resource use. An exit code of zero or green hub status does not establish experiment quality.

Digest both results and experiment quality: did the manipulation occur, did controls discriminate, could the model do the clean task, did the evaluator measure the intended outcome, and do the data support the proposed interpretation? Compare against the pre-run assessment. Separate observed facts, suspected causes and verified causes. Include next-run changes, predicted consequences and tests that could falsify the diagnosis.

Classify each issue before deciding what to rerun:

| Kind | Examples | Required response |
|---|---|---|
| Execution or reporting defect | crash, malformed output, lost artifacts, duplicate dispatch, secret exposure | Preserve evidence, contain the fault, diagnose and fix; regression check then a new bounded attempt. Never reproduce a secret in the review. |
| Design or measurement defect | missing labels, ineffective manipulation, unfair baseline, truth leakage, incorrect denominator | Amend/version the design and evaluator, audit past conclusions, then validate on appropriate development fixtures. |
| Capability or qualification failure | model cannot follow clean constraints or interpret tool output | Diagnose with atomic probes; repair the adapter/prompt/architecture or qualify a different permitted model. Use fresh disjoint qualification tasks for an honest readiness check. |
| Valid scientific outcome | null effect, worse intervention, expected injected faults correctly measured | Report and interpret it. Do not change the study or rerun until a desired result appears. A modeled fault is an outcome, unless its injection or measurement was itself broken. |

## Continue until the defects are resolved

A failed attempt is not the end of the task. Within existing authorization and budget, the owning agent must continue the repair cycle without asking for approval for each reversible fix or diagnostic. Keep an issue ledger: ID, evidence, cause confidence, owner, repair, regression test, next attempt and status. An issue closes only when its declared acceptance check passes with linked evidence; rerunning unchanged until a lucky pass does not close it.

Preserve the original attempt and its assigned denominator. Give every new attempt a new ID/output directory, `parent_attempt`, reason and version hashes. Transport retries follow the frozen policy; an amended diagnostic run is not an invisible replacement for a failed scientific observation. Never overwrite a failed result, relabel it as success, quietly drop it, or claim that its errors were fixed without a verified rerun. Previously evaluated qualification tasks may reproduce a bug but cannot serve as fresh evidence of generalization after tuning.

Do not advance to the next scientific stage while material execution, design or competence issues remain. Do not stop merely because an initial pilot failed. If progress requires unavailable credentials, additional authorized spending/compute, missing data or a human research decision, record the exact blocker, preserve resumable state, continue independent repairs and request only the missing input. Exhausted budgets and access restrictions are not permission to bypass them. A model may remain unsuitable; report that limit rather than disguising it as a successful repair.

A valid negative result can finish a scientifically sound run. A defect-bearing run remains `repair`, `diagnostic-only` or `blocked`, even if its artifacts were successfully published. Final reporting distinguishes **execution complete**, **qualification passed**, **scientific conclusion**, and **repair work remaining**.

## End-of-cycle handoff

The post-mortem names the next action: `advance`, `repair-and-rerun`, `diagnostic`, `blocked`, or `complete-valid-result`, plus its acceptance criteria. Before any next launch, turn that action into the next pre-run assessment. Archive nothing needed to reproduce failures. Release unused server claims and stop bounded workers while blocked.

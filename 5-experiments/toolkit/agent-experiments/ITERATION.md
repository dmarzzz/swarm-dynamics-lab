# One iteration of an experiment

**Review evidence → diagnose → improve and validate → publish → run if ready → close out.**

This is the standing process for Vishesh-owned studies. When asked to “do an iteration,” carry it through to an explicit outcome below. Work in the experiment's owning task and existing study directory. Maintain one authoritative `SETUP.md`; link existing evidence instead of creating another dossier. This procedure adds no central launcher, service, researcher sign-off or spending allowance. Other researchers retain their own policies.

## 1. Read what actually happened

Use [operations](OPERATIONS.md) to inspect the study. Read its latest native attempt, post-mortem, handoff, plan and original cost ledger; the registry or dashboard may lag. Reconcile assigned, started, terminal, valid, graded and unstarted units. Separate execution, qualification, scientific validity, reporting and cost.

Review [native traces](RUN-REVIEW.md#review-the-native-traces-before-choosing-a-repair): actual agent-visible context, returned answers, actions, grades and usage. Inspect every qualification miss and distinct error class; for larger runs disclose the sampled manual coverage and full-cohort automated checks. Never invent missing responses or hidden reasoning.

## 2. Diagnose all applicable issues

Apply [the shared diagnosis step](DIAGNOSIS.md) here: identify the bottleneck and practical need, qualify strong baselines, improve informative cases, and justify the smallest useful contrast before scaling. Embed its [worksheet](templates/diagnosis.md) in the existing review; do not create another approval layer.

These rows are cumulative, not competing choices. A run can contain execution errors, design gaps and interpretable results at once.

| Finding | Required action | Evidence of progress |
|---|---|---|
| Errors in execution, parsing, scoring, accounting or reporting | Identify the first observed failure and plausible alternatives. Repair the instrument or design; replay saved data where possible. | A reproduced failure, tested repair and preserved original attempt. |
| Gaps in usefulness, realism, challenge, controls, robustness or precision | Assess against [run quality](RUN-QUALITY.md). Revise the question, scenario, controls, sample or measurement where justified. Refresh relevant research when it could change the decision. | A concrete design change, its rationale and acceptance check. |
| Results needing interpretation | Compare with the predeclared predictions, controls and thresholds. Report uncertainty, missingness, dependence and alternative explanations. | An evidence-linked conclusion, updated confidence/sample-size metadata and limits on the claim. |
| A credible next run | Identify the remaining empirical question and why saved traces or a simpler method cannot answer it. | One bounded next-run plan with a decision for favorable, null, adverse and inconclusive outcomes. |

A transport failure is not model incapacity. A numeric qualification pass does not override leaked labels, a broken scorer or a mismatched context. A valid negative finding is a result, not an error to fix.

### When test cases are insufficient, improve them

If the review finds that cases are too easy, repetitive, unrealistic, ambiguous without sufficient evidence, contaminated, or unable to distinguish the proposed explanations, improving the cases is part of the current iteration. Do not stop at recording “dataset insufficient” when useful offline case design or construction is feasible.

- State the specific weakness and what an informative case must reveal. Write the prospective case changes before implementing them.
- Construct improved or alternative development cases, including ordinary controls, meaningful challenges, answer-changing matched pairs and answer-preserving variants where applicable. Establish the target from evidence available under the declared actor contract; include justified abstention when the answer is unknowable.
- Validate labels, actor/evaluator separation, scoring, failure handling and the strongest relevant simple baselines. Difficulty alone is not quality: do not withhold essential evidence or weaken a comparator merely to create a favorable model opportunity.
- Preserve original cases, outcomes and their interpretation. Version the new cases and explain which defect they address. Report independent scenario/event units separately from variants and repeated calls; inspected or tuned cases remain development data, never an untouched holdout.
- Publish the concrete case revision, validation results and remaining limitations. If construction needs unavailable data, rights or access, identify that exact dependency and do all feasible design work first. Then decide whether the revised cases justify a ready approved run, a concrete material-scope decision, further case development, or finishing the study.

Evaluate the revised cases themselves with [TEST-CASE-QUALITY.md](TEST-CASE-QUALITY.md). Publish the evidence-linked rubric and distinguish case readiness for the stated scope from native qualification and run admission. Connect cases to the full task, implement strong relevant baselines, and protect evaluation cases from tuning; do not repeatedly stop at known, feasible case-quality gaps.

A case revision does not reset spending, authorize a new native scope, erase a valid negative result or require manufacturing a harder problem. Apply the existing approval and admission rules after offline improvement.

## 3. Prepare the change and push it

Write the prospective change before experimental implementation. Then implement reversible offline repairs and validate them on development/fault fixtures so the proposal is concrete. Preserve frozen sources, previous outputs and inspected holdouts. Recompute reporting from saved evidence without recollecting decisions.

Use the existing [next-run plan](templates/next-run-plan.md), covering:

- Question, expected value, intervention, strongest relevant comparator and claim boundary.
- Scenarios, difficulty/realism, independent sample units/counts, precision rationale, paired/repeated observations and untouched holdouts.
- Agent specifications, startup/context/memory, actor/evaluator separation and qualification in the context actually being tested.
- Traces/data retention, scoring, analysis, missingness, failure/stopping rules and acceptance checks.
- Cumulative spend and unresolved reservations, worst-case calls/time/cost, minimum machine needs and applicable authority.

Commit and push the review, relevant document/code changes and tested proposal to the owning repository. Record what is implemented versus proposed. Publish sanitized evidence and references; keep credentials, private operations and exact owner prompts private. A publication failure is an explicit blocker, not a successful push.

## 4. Choose the next action

| Disposition | Meaning | What to do now |
|---|---|---|
| **RUN** | Useful tested plan within existing authority; no unresolved scientific or scope decision | Obtain the required allocation, verify final admission, deploy and execute the named stage. If a real prerequisite fails, record HOLD. Do not stop at offering to run. |
| **DECISION NEEDED** | A concrete material change or resource increase is outside existing approval | Present the tested update and the exact decision needed. Continue independent offline work; do not allocate or launch that changed scope. |
| **HOLD** | A specific prerequisite is missing or failed | Name the evidence, blocker owner, next action and observable resume condition. Release idle claims; do useful independent work. |
| **FINISH / PARK** | The result answers the question, or further collection has insufficient value | Publish the conclusion and limits. Stop with a valid result or explain what new evidence would justify reopening. |

These are human-readable dispositions, not new CLI commands or automatic launch receipts. **Already-approved unchanged work and necessary bounded post-mortem diagnostics proceed without another approval request.** For Vishesh, apply [standing diagnostic authorization](RUN-REVIEW.md#standing-authorization-for-necessary-post-mortem-diagnostics), including diagnostic changes needed to distinguish causes or test repairs. Choose RUN once admitted, not DECISION NEEDED solely because the diagnostic changes the instrument. For material successor updates, retain the [existing owner-decision rule](RUN-REVIEW.md#owner-approval-before-a-material-update-runs); preparing a good plan alone does not approve it. Researcher review remains waived for Vishesh. Do not invent a central acknowledgment requirement where direct dispatch is authorized.

## 5. Execute the ready scope

After the applicable scope decision, verify or obtain an exclusive allocation in Dmarz's approved account using the established provisioning/state workflow. Reuse eligible capacity where permitted; provision only if needed and within existing authority. Verify account identity, claim/workload, source/runtime, original single-writer ledger and current route/cost bounds. A working SSH key or token alone is not admission.

Publish/register the immutable plan and condition-specific TLDR; verify the public page before any experimental call, including qualification. Use the supported native entry point and frozen agent/context definitions. Fence duplicate dispatch paths. Run bounded qualification before conditional expansion; examine its actual traces and scientific validity, not just its score. Stop under the declared rules; no unplanned retries, fallback models, repeated paid probes or budget resets.

## 6. Close the loop

Every terminal attempt receives operational closeout **and** an authored scientific post-mortem, including failed, interrupted and negative attempts. Supported runners generate the operational handoff; manual entry points use the existing finalize hook. Review against the full quality rubric, reconcile costs and denominators, verify artifact readback, stop workers and release allocations. Update the existing setup record, evidence metadata and next action; push the closeout.

An iteration is complete when its outcome is clear—not merely when a process exits or a proposal is written. If a launched stage is still running, report it as running and retain a named monitoring/closeout owner. Do not automatically chain a materially changed successor.

## Short handoff

Append this summary to the existing post-mortem or setup record; no extra tracker is needed:

| Field | Record |
|---|---|
| Previous run | Attempt/source; actual sample, missingness, confidence and cumulative cost |
| What we learned | Findings and trace/evidence links; alternative explanations |
| What changed | Design/code/scenario changes; acceptance checks and pushed commit |
| Next action | RUN, DECISION NEEDED, HOLD or FINISH / PARK; exact scope or blocker |
| Ownership | Responsible task; approval reference or resume condition; monitoring/closeout status |

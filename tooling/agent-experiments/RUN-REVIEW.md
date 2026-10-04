# Run assessment and the next experiment

Every attempt ends with a post-mortem, including setup failures, interrupted attempts, diagnostics and successful executions. The next session begins by reading that post-mortem and assessing its suggestions against [what a good run establishes](RUN-QUALITY.md). It does not blindly rerun the experiment.

The cycle is **record the outcome → complete the scientific assessment → choose repairs → write the next-run plan → obtain applicable owner approval → admit and execute the named stage**. A valid null or adverse result can end the cycle. Existing public-plan, qualification, spending, credential and approved-account requirements remain binding.

For Vishesh-owned studies, researcher review is **not required by owner direction**. The owning agent still completes the assessment and resolves relevant defects. Do not add independent design, dossier or researcher sign-off, or record the waiver as a passed review. The owner's approval of a material next-run update is a separate decision. Other researchers' review policies remain unchanged.

## At attempt termination

The supported [operations command](OPERATIONS.md) writes an operational `POST-MORTEM.md` and `handoff.json` from the saved outcome. The handoff starts with `scientific_review=unresolved`. This automatic summary records facts and missing evidence; it does not evaluate scenario realism, causal validity or scientific meaning. It must not invent counts, actual spend, causes or a successful scientific verdict from an exit code.

If completion was interrupted, or a legacy launcher needs a closeout bridge, use the saved-evidence operation:

```sh
python3 scripts/experiment.py finalize STUDY --attempt ATTEMPT \
    --results SAVED_RESULT_DIRECTORY --outcome completed
```

Select the supported `completed`, `failed`, `blocked` or `ambiguous` execution outcome from actual records; `--results` and `--outcome` are optional where the command can recover them. `finalize` does not dispatch models, resume workers or mark the scientific review complete. Inspect the resulting handoff. This integration covers supported entry points; other launchers must invoke the bridge or explicitly complete the same closeout before the session finishes.

For an interrupted worker, stop and verify that exact worker before using `--worker-stopped` when required by recovery. The flag records the operator's check; it neither stops a worker nor independently verifies remote state. An empty local journal is not proof of a first run: inspect the registered preceding post-mortem and import/finalize historical evidence before preparing a successor.

The **owning session must then finish the analytical post-mortem**, using [the template](templates/post-mortem.md). Preserve the automatic facts and link any corrections to evidence. Reconcile assigned → started → terminal → graded → analyzed, retaining duplicate, partial, failed and unstarted units. Report actual usage separately from reservations and unresolved exposure. Review the full eleven-dimension rubric, observed results, controls, uncertainty, visuals and deviations.

Do not report the run's overall work as done while scientific review is unresolved. Execution can be complete while closeout is pending. If evidence or access prevents the assessment, retain `unknown`, the exact blocker and a named next action. A finished post-mortem may document open defects and a `repair` or `blocked` verdict; it does not relabel the attempt as successful.

## Start the next session with evidence

Read the latest handoff, full post-mortem, quality assessment, preceding plan and any later amendments before proposing another execution. Use `inspect STUDY` to locate the latest supported handoff; check for native attempts outside that entry point. For each earlier suggestion, record: accepted, revised or rejected; supporting evidence; alternative explanation; and a test that can disprove the diagnosis.

Classify the issue before acting:

| Finding | Appropriate response |
|---|---|
| Execution or reporting defect | Preserve evidence; repair offline and replay saved artifacts where possible. A delivery repair does not require recollecting decisions. |
| Design or measurement defect | Version the correction, audit affected conclusions, and validate the revised instrument on development fixtures. |
| Capability failure | Diagnose the task/interface failure; qualify changed behavior on fresh reserved inputs before broader comparisons. |
| Valid null, adverse or inconclusive outcome | Report it. A further experiment needs a justified new question or useful precision, not a preferred result. |
| Missing authority, resource or data | Record the blocker and resume condition; continue independent offline work and release idle claims. |

Maintain an issue ledger with evidence, cause confidence, owner, change and acceptance check. A proposed fix does not close an issue. Preserve earlier attempts and their denominators; a retry or amended diagnostic is not an independent replacement observation. Never relabel failed qualification, tune on a held-out result and call it fresh, or lower a threshold to turn a failed screen into a pass.

## Prepare a concrete next-run proposal

Use [next-run-plan.md](templates/next-run-plan.md). Choose one design rather than listing unresolved alternatives for the owner to assemble. State the intervention, strongest relevant comparator, independent unit, scenario strata, holdouts, sample allocation and its rationale. Name a useful effect or precision target; use pilot variability where available, or declare feasibility-only scope and uncertain power. There is no universal minimum n, and more agents or calls do not create independent tasks.

Specify collected data, context/memory receipts, scoring, missingness, uncertainty, stopping, implementation changes and acceptance tests. Include a bounded call/time/cost envelope across qualification and comparison, cumulative spend and pending reservations, and the minimum machine requirements. Link evidence rather than copying private records. Choose `advance`, `repair` or `diagnostic` for a proposed successor; `complete_valid_result` and `blocked` do not authorize another run.

## Owner approval before a material update runs

For Vishesh-owned experiments, obtain the owner's approval of the concrete **material next-run update before allocating its required machines or launching it**. This supersedes earlier blanket permission in this runbook to execute every diagnostic repair autonomously. A material update changes the question, treatment, scenarios, sample/holdout allocation, agent behavior, measurement, collection/analysis/stopping rules or execution/resource scope. Treat changed prompts, models or evaluators as material unless that exact change was explicitly covered by existing approval.

Continue reversible offline fixes, validation, analysis and proposal preparation while awaiting that decision. Reuse an existing approval only for its unchanged, explicitly covered scope; link its evidence and explain the match. A generated approval template or the agent's own assessment is not owner approval. Material drift needs renewed approval. Owner approval does not establish scientific qualification or waive runtime gates.

Do not ask again for already approved spending. Use the applicable experiment-specific cap, or the owner's standing default when it applies, with actual spend and uncertain reservations carried forward. A successor, renamed stage or new host creates no new allowance. Request a budget increase only when the selected plan exceeds existing authority. Approval of a design update alone does not silently replenish funds.

## Admit, execute and hand off

After update approval, resolve the required exclusive allocation through the established approved-account workflow. For new machines under Vishesh's directive, verify Dmarz's approved account/team identity, authoritative state/project and exact resource plan before create/apply. Keep identifiers and credentials private; no personal/default-account fallback. Check current workload, claim lifetime, deployment/source/runtime, output storage and cumulative quota. Do not hold an idle claim while approval or another prerequisite is missing.

Complete [the pre-run assessment](templates/pre-run.md), publish the exact immutable plan and condition-specific TLDRs, verify the actual public page, and pass the real dispatch gates. The operations workflow binds `prepare --next-plan` and `run --update-approval` to the saved closeout, completed review, proposed plan and execution contract. See [operations](OPERATIONS.md) for the implemented scope; the command has no `approve` operation and does not manufacture authorization.

Execute only the named admitted stage. Refresh admission before each stage/attempt and requalify relevant instrument changes. Save one terminal execution outcome per assignment, then repeat the mandatory post-mortem cycle. Update the study's `SETUP.md`, evidence metadata and next action. Stop only its workers, verify durable artifacts and release claims through the owner workflow; preserve everything needed to reproduce failures.

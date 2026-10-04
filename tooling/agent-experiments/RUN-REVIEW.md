# Run assessment and the next experiment

Start with [one iteration of an experiment](ITERATION.md) for the short decision workflow. This document supplies the detailed review and closeout requirements; use the study's existing records rather than duplicate checklists.

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

The command's returned `model_calls: 0` counts **new calls made by the offline closeout operation**, not calls in the native attempt. For manual studies without a reporting adapter, native analysis remains explicitly unresolved; it is not a zero-call result. Obtain the experiment's actual request count from its native journal and authored reconciliation.

For an interrupted worker, stop and verify that exact worker before using `--worker-stopped` when required by recovery. The flag records the operator's check; it neither stops a worker nor independently verifies remote state. An empty local journal is not proof of a first run: inspect the registered preceding post-mortem and import/finalize historical evidence before preparing a successor.

The **owning session must then finish the analytical post-mortem**, using [the template](templates/post-mortem.md). Preserve the automatic facts and link any corrections to evidence. Reconcile assigned → started → terminal → graded → analyzed, retaining duplicate, partial, failed and unstarted units. Report actual usage separately from reservations and unresolved exposure. Review the full eleven-dimension rubric, observed results, controls, uncertainty, visuals and deviations.

Do not report the run's overall work as done while scientific review is unresolved. Execution can be complete while closeout is pending. If evidence or access prevents the assessment, retain `unknown`, the exact blocker and a named next action. A finished post-mortem may document open defects and a `repair` or `blocked` verdict; it does not relabel the attempt as successful.

## Shared trace coverage check

Follow [TRACE-RECEIPTS.md](TRACE-RECEIPTS.md) for new or materially revised native launchers. Shared `finalize` audits declared trace receipts for every result directory; absent manifests remain an explicit evidence gap. Native adapters must adopt capture prospectively. This does not retroactively instrument frozen runs or replace scientific review.

## Review the native traces before choosing a repair

A result table locates a problem; the retained request, response and action trace establishes what was observed. Apply [Dmarz's failing-answer lesson](../../researchers/dmarz/notes/pipeline/LESSONS.md#6-read-the-failing-answers-before-changing-the-model) and [worked per-row review](../../researchers/dmarz/notes/verify-cost-qwen/reviews/chain-002-post.md) within the current study's scope. Do not change a model, prompt or scenario solely from an aggregate failure rate. The [completion audit](../../researchers/dmarz/notes/completion-audit-2026-10-04/README.md) additionally distinguishes returned-but-incomplete actions, explicit refusal, parser rejection and missing records; its historical cutoff must not overwrite newer study evidence.

1. **Inventory and reconcile.** Bind attempt/source/configuration, assignment/root/arm and physical request IDs to request/context, visible response, parsed action, tool/environment transition, grade and usage receipts. Report coverage for each artifact type and all assigned units. Failed, rejected, truncated, interrupted and unstarted units remain distinguishable. A locally serialized request is not proof that the provider received it.
2. **Inspect the failures.** Read the effective experimental messages and returned answer for every qualification miss and every distinct execution-error class. For large main stages, report deterministic audit criteria, counts and failures inspected, plus matched successes; use full-cohort automated checks and disclose incomplete manual coverage. Never claim to have read missing traces. Keep evaluator-only truth separate from what the agent actually saw.
3. **Locate the first observable divergence.** Follow available evidence → delivered context → retrieved/retained memory → visible output → parser/validator → action/environment → scorer. Classify missing information, ambiguous instructions, source/version confusion, arithmetic/action binding, unsupported advice, validator/scorer bugs and transport/reporting failures separately. An output pattern can support a diagnosis without identifying its cause or hidden reasoning.
4. **Choose a discriminating change.** Record evidence IDs/hashes, observed pattern, alternative explanation, proposed offline replay or prospective contrast, and acceptance check. Recompute deterministic scoring first. Adding intermediate answer fields changes the instrument and can expose errors without fixing them; keep that cohort separate. Do not lower a threshold or replace held-out cases after inspecting their failures.
5. **Verify retention.** Retain original events and safe artifacts; verify uploaded bytes/hash after compression or chunking. Recover missing reports from saved evidence rather than recollecting decisions. A trace upload repair cannot turn a failed execution into success. Missing evidence is a limitation and, when it defeats the required inference, a reason to withhold that inference.

Use the existing native logger when it provides these facts; no new service or blanket requalification is required. Document legacy coverage gaps honestly. A material change to experimental behavior or collection still follows the normal updated-plan process. Hash-pinned serialized requests and visible answers are evidence of inputs/outputs, not a guarantee of reproducible hosted responses or access to hidden reasoning.

**Privacy:** native experimental traces are not the operator's Codex/Claude session transcripts. Never collect or publish operator history as experimental context. Public post-mortems contain sanitized case tables and approved experimental excerpts only; keep credentials, headers, endpoints, private account data and exact owner prompts out. Use fixed error categories and allowlisted metadata rather than arbitrary provider error prefixes. Raw private material stays private. Cite restricted receipts by reference/hash without moving their contents into a public artifact.

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

## Choose whether another run is useful

Before selecting a successor, choose **finish/report**, **analyze saved data**, **one bounded discriminator**, or **park**. These are planning dispositions, not new runner verdicts or commands. Finish required closeout in every case; preserve currently approved work within its exact scope. The [study-by-study PI decisions](../../researchers/vishesh/notes/pi-next-decisions-2026-10-04/README.md) show examples reconciled with a pinned evidence cutoff.

A new run should name what is empirically unknown, how support/null/adverse/inconclusive outcomes change a decision, and why existing traces or a simpler method cannot resolve it. Distinguish collective interaction from independent re-evaluation or resampling; compare the strongest relevant simple controller under the resources appropriate to the question. Programmed mechanisms are useful tests when labelled, but do not demonstrate model behavior by themselves.

Count preparation, reporting and operator attention alongside financial exposure. Repeated qualification failure triggers a cause assessment and a bounded repair/stop decision, not indefinite prompt rerolling. Transport failure is not semantic incapacity; neither justifies inventing observations or a universal fixed failure count. Prioritize prior-art work that could change the selected design without claiming a broader survey is complete.

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

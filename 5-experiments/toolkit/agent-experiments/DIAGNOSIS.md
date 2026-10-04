# Diagnose the experiment before increasing scale

Use this step during [iteration](ITERATION.md), after reviewing native traces and before choosing a repair, richer task, larger roster, stronger model or longer run. It is standard practice for Vishesh-owned experiments and reusable guidance for other researchers under their own policies. Record the result in the existing post-mortem or next-run plan using the [diagnosis worksheet](templates/diagnosis.md). No separate dossier, reviewer or service is needed. This procedure supplements [run quality](RUN-QUALITY.md) and [case quality](TEST-CASE-QUALITY.md); it does not add spending or launch authority.

## 1. Separate the symptom from the cause

Reconcile outcomes and follow the [native trace review](RUN-REVIEW.md#review-the-native-traces-before-choosing-a-repair). Locate the earliest observed divergence through evidence availability, acquisition, interpretation, coordination, action and verification. Distinguish execution defects, incapable agents, ambiguous interfaces, weak comparators, uninformative tasks and valid negative results. Label each causal explanation observed, supported, plausible or unresolved, with evidence references and alternatives. Output patterns do not expose hidden reasoning.

Audit matched successes as well as misses. A perfect score can indicate a useful solution, a ceiling, leaked answers or an insensitive endpoint; it is not automatic justification for more agents. A floor can mean missing evidence or a broken contract rather than a need for a stronger model.

## 2. Identify the bottleneck and practical need

Name the real decision a person or deployed agent faces, the information needed, the actions available and the consequence of error. Trace which stage limits success, useful throughput or cost. Distinguish information collection, reasoning, coordination and execution. State whether work is independent, coupled, serial, batchable or limited by a shared tool/service. Use observed timing and action evidence where available; otherwise mark the bottleneck as a hypothesis.

Ask what additional agents, compute, memory or observations could actually change. If one context can batch the same obvious repairs or an exact controller solves the declared task, report that useful result. Do not add difficulty solely to create a preferred swarm advantage. A revised task needs a concrete unmet practical need.

## 3. Repair and qualify credible baselines

Use the strongest relevant simple reference: an exact/rule controller, existing non-agent workflow, capable single agent with batching and tools, and a coordinated fixed team when collective behavior is the claim. Mark irrelevant baselines not applicable with a reason; this is not a mandatory four-arm experiment.

Give each comparator the information, legal tools and reasonable coordination its claimed role requires. For parallel teams, make ownership, work claims, handoffs and conflict resolution explicit. Count coordinator calls, idle polling, retries, integration and supporting tools. Qualify the hard required step, not just response formatting. A failed weak baseline cannot establish superiority over competent alternatives. Fix its defect prospectively and preserve its historical outcome.

## 4. Improve cases to discriminate explanations

Write the case change before implementation. Prefer meaningful distinctions in evidence and decisions over more names, agents or repetitive items. For an incident investigation, this can mean distinct service logs, metrics, dependencies, competing root causes and plausible misleading symptoms. Include coupled remediation where independently sensible changes can conflict. For other domains, use equivalent domain evidence and real decisions rather than copying outage vocabulary.

Each case must have an evidence-grounded label, enough reachable information to answer under the declared contract, or a scored correct abstention/escalation when it is genuinely unknowable. Keep actor evidence separate from evaluator truth. Add clean controls, answer-changing matched contrasts and answer-preserving variants where relevant. Exercise safe incorrect actions, delayed evidence and recovery only when they test a stated mechanism. Unavailable information and arbitrary tool restrictions are not realism by themselves.

Validate development cases offline: reference solutions, scorer faults, leakage checks and strongest relevant baselines. Check that the case distinguishes the competing explanations. Report independent incident/task roots separately from descendants, variants and repeated model calls. Freeze untouched qualification/evaluation cases before tuning and label inspected cases as development. Use real data only under its access and redistribution permissions; synthetic realism claims remain limited.

## 5. Choose the smallest informative contrast

Write competing explanations and an observable result that would separate them. First use saved-data replay, exact calculations or offline interventions. If native collection is necessary, define a finite diagnostic with acceptance/futility rules and decisions for support, null, adverse and inconclusive outcomes. Do not change prompts, model, task difficulty and resources together without separating their effects or narrowing the claim.

For scaling, state the estimand explicitly:

| Comparison | Hold fixed / disclose | What it can establish |
|---|---|---|
| More agent identities under fixed resources | Task/evidence, tool slots, deadlines, resource limits; actual aggregate compute and tokens | Roster-policy tradeoff under the specified limits; equal tool slots alone do not mean equal compute |
| More agents with additional execution capacity | Capacity added per arm and every cost | End-to-end capacity/cost tradeoff, not a pure identity or coordination effect |
| Coordination intervention | Task, roster, resources and evidence where possible | Benefit of the declared coordination protocol on the tested support |

Report correct diagnosis or domain outcome, safe action, verified recovery/completion, elapsed time and total cost separately. Preserve partial outcomes, abstentions and missingness. Include a quality-versus-resource frontier when useful; a single composite score can hide a safety or reliability loss. There is no universal roster ladder, independent sample count or effect threshold.

## 6. Finish with a decision and evidence

Use the existing iteration dispositions. Proceed with an admitted, useful diagnostic within standing authority; prepare feasible offline improvements when cases or controls are inadequate; identify a real external blocker; or finish/park when the question is answered or further collection lacks decision value. A broader main experiment still needs its applicable scope decision. Keep the original ledger and all holds, prospective public plans and ordinary source/runtime/qualification/account/allocation checks. Do not create another approval request merely to complete this worksheet.

Record what changed and what was validated, not just a recommendation. A written checklist is not runtime enforcement, native capability or an independent audit. Do not retrofit frozen experiments or claim their historical launchers already implement this procedure.

## Worked example: Optimal Swarm Size

[O2 evidence](../../researchers/vishesh/notes/optimal-swarm-size/reviews/outage-o2-post.md) separates two issues. Explicit ownership removed duplicated repairs in the legacy four-agent team. On the eight-service development task, one, four and eight agents plus a rule controller reached the same recovery ticks; eight agents cost more. The comparator repair was useful, but merely increasing the roster to forty would not resolve a new uncertainty. A prospective next task should test costly parallel investigation and coupled action only if those represent a concrete unmet incident-response need. This does not establish that large teams are generally ineffective.

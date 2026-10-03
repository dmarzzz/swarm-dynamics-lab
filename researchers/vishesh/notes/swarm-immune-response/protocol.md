# Comparison plan: isolate the source, then identify what still needs repair

**Draft design only.** This is not a preregistration or permission to run models. The [complete experimental design](experiment-design.md) fixes the proposed schedule, sample, thresholds and budget; the discussion here explains their rationale. See also the [concept and boundaries](README.md) and [integration contract](integration-and-sources.md).

## Experimental unit and phases

Use a synthetic task world with a deterministic checker, distinct private facts, a versioned shared notebook and a mock action interface. A world includes the task, initial evidence allocation, agent roles, graph, contamination placement and schedule. Pair interventions within a world using a checkpoint; treat the world as the statistical cluster. Agent turns from the same world are not independent replicates.

Separate three fault classes: an accidentally wrong artifact, an indirectly affected honest agent and a persistently attacker-controlled agent. Match content, timing and exposure budget where a causal comparison requires it. Keep attacker fraction, topology, message budget and memory length fixed in the first study. A source's intent is evaluator metadata, not something a detector can infer merely because a claim is false.

1. **Establish useful state.** Agents acquire distributed evidence, including a rare fact necessary to solve a later subtask.
2. **Bounded contamination.** Introduce a fixed, predeclared number of corrupt writes/messages. Record exposure, adoption, onward propagation and mock actions separately.
3. **Checkpoint and intervention.** Fork every assigned world at a fixed time, including worlds where contamination failed. Freeze outstanding writes for a consistent checkpoint boundary, then resume under the assigned policy. Branch-selection must not depend on attack success.
4. **Recovery workload.** Continue identical scheduled tasks under matched opportunities to read corrective evidence. After the bounded injection window, no arm receives new attacker content; the no-response arm retains existing state and paths. This estimates recovery after a finite incident, not protection from a continuously adapting adversary.
5. **Recurrence challenge.** At a fixed recovery round, attempt a stale-child return or cached-artifact read in every branch. Policy decides whether it is admitted; the evaluator records the attempt and outcome. The source is not secretly restarted.

Preserve common exogenous task schedules across forks. Provider randomness need not replay exactly; log model versions, seeds where supported and repeated draws where justified. A matched checkpoint controls history, not all future stochasticity.

## Stage A: oracle mechanism comparison

The oracle knows the planted source and affected state. It is a diagnostic ceiling, not a deployable detector. Source quarantine revokes its write/communication capabilities without replacing its lost capacity; all four oracle arms use the same rule. Replacement is a separate later factor.

| Arm | Source quarantined | Reset affected honest agents' private state | Restore shared reservoir |
| --- | --- | --- | --- |
| N: no response | No | No | No |
| Q00: containment only | Yes | No | No |
| Q10: private reset | Yes | Yes | No |
| Q01: reservoir repair | Yes | No | Yes |
| Q11: joint repair | Yes | Yes | Yes |

Add a matched clean trajectory without contamination as a reference. Define “private reset” as rebuilding the affected agent context from a designated pre-contamination checkpoint, including its private scratch state and queued personal writes. This loses legitimate intervening learning too. Define “reservoir repair” as restoring the shared notebook and retrieval/cache views to their last trusted pre-contamination version and rejecting incompatible queued writes. This also loses legitimate subsequent shared work. Both are intentionally broad diagnostic operations; retained audit logs are inaccessible to acting agents.

Explicitly model the containment boundary for every shared tool, queue and cache. A reservoir omitted from the intervention inventory cannot later be counted as having been repaired. The recurrence challenge uses a separately retained stale artifact with old lineage/version tags; those tags cannot be erased when it returns.

Q10 minus Q00 measures the incremental effect of private reset under this oracle and restore policy. Q01 minus Q00 isolates the shared-state effect. The interaction `(Q11 − Q10) − (Q01 − Q00)` tests whether the combined effect departs from the sum of the component effects, on each specified metric scale. These comparisons do not establish that forgetting is necessary, that all exposed agents require reset, or that a practical detector can reproduce oracle results.

## Stage B: useful recovery with limited observability

Advance only if Stage A reveals a meaningful persistence or collateral-loss problem. Compare an existing recovery implementation, a simple quarantine-and-reset baseline and selective lineage repair using the same agent-visible evidence and total resource ceiling. Review implementation access/licences before selecting that existing baseline; do not present an approximate reimplementation as a faithful replication.

Selective repair marks suspect claims and known descendants as unavailable for action until revalidated. It preserves independently supported material, can abstain when lineage is missing, and never receives evaluator-only affected-agent labels. Cross missing edges and spurious dependency edges in controlled fixtures. An association is not proof that a descendant adopted the error.

Add these controls before interpreting a policy's apparent advantage:

- **Correction without erasure:** supply the same trusted corrective facts and verification budget while retaining history. If this matches reset, extra information may explain recovery.
- **Capacity-matched random quarantine/reset:** on clean worlds remove the same number of agent-turns or facts. Measure the generic cost of lost capacity separately from targeted harm.
- **Correct minority:** falsely flag the specialist holding necessary valid evidence. Compare scoped artifact review, agent exclusion and an appeal with independently obtained evidence.
- **Benign update and accidental error:** require acceptance of a legitimate new version and correction of an honest mistake. A policy that rejects all changes is not robust collaboration.
- **Replacement:** compare vacant quarantined seats with clean replacements, accounting for their models, evidence and startup cost. Do not attribute extra workforce to a better detector.
- **Independent adjudication:** separate policy-observable detector scores from evaluator truth and, where subjective judgment remains, independently validated judgments. Report ambiguous cases.

Measure detector precision/recall, latency and calibration on disjoint scenarios as well as downstream outcomes. Let false positives vary by role and time: an average rate can hide systematic loss of rare expertise. Test self-detection only after an external-observer baseline, with its additional attack surface and costs declared.

## Outcomes and denominators

| Measure | Operational definition |
| --- | --- |
| Useful task completion | Correct accepted outputs divided by the original assigned workload, including tasks left unserved by quarantine. Do not shrink the denominator when agents disappear. |
| Cumulative harm | Separate counts of wrong adopted claims, onward corrupt transmissions and mock forbidden actions over the entire horizon. A later repair never subtracts an earlier irreversible action. |
| Affected population trajectory | Number of originally honest agents exhibiting the specified erroneous behavior at each checkpoint, divided by the original honest cohort. Mere exposure and lack of activity are separate labels, not infection and cure. |
| Durable recovery | First round meeting a prespecified utility tolerance relative to the matched clean reference for a fixed window, with no mock forbidden action during that window, followed by a separately reported recurrence challenge. |
| Recovery time | Time from intervention to the sustained criterion; failures are right-censored at the horizon and their fraction is reported. Never average only successful recoveries. |
| Knowledge retention | Fraction of initially correct, independently grounded task facts still usable after repair; report the essential minority fact separately. |
| Collateral exclusion | Honest agent-turns/capabilities unavailable, wrong artifacts suppressed and appeals incorrectly denied; track lost utility and delay. |
| Re-entry error | Re-admitted instances/artifacts that reproduce the targeted error under the held-out challenge, with eligible and attempted re-entry denominators. |
| Cost | All actor, detector, reviewer, repair and probe calls/tokens, wall-clock latency, and budget-exhausted or failed runs. |

Choose the utility tolerance, minimum sustained window and meaningful harm/retention margins before confirmatory data, using disjoint feasibility worlds. A short debugging horizon cannot establish long-term safety. Diagnostic probes must not teach the agent the answer: use isolated evaluation snapshots or explicitly count the probe as an intervention.

Primary analysis includes every assigned world; show successful-infection subsets only as secondary diagnostics. Estimate paired world-level effects with uncertainty intervals and prespecified practical margins. Do not treat agent count as sample size, or overlapping confidence intervals as a significance test. Predeclare one primary utility outcome and one safety constraint before formal registration; keep the other outcomes explanatory and report multiplicity where applicable.

## Feasibility and stop rules

Begin with a deterministic fixture and eight-agent debugging worlds. Do not start a full factorial across graph, memory, models, detector, attack and repair. Hold bounded history fixed initially; memory-length sweeps and 24-agent scaling follow only if the mechanism survives the controls.

The [complete design's resource envelope](experiment-design.md#8-resource-envelope-and-execution-gates) fixes six feasibility worlds, 48 later estimation worlds and a 24-round schedule. Its nominal actor slots exclude additional detector, repair, retry and evaluation calls; all roles remain subject to the aggregate cost cap. This is neither a powered sample-size guarantee nor an authorized run budget. A bound model and price projection must demonstrate feasibility before collection.

Stop the design or reduce scope if the fixture cannot distinguish adoption from exposure, the clean reference cannot solve the task, checkpoint isolation leaks across forks, no contamination reaches the intended store, or the nearest prior implementation already answers the proposed contrast. Stop any future run on its preregistered cost/timeout limits and retain failures in the report. A synthetic result would justify a specific follow-up, not deployment to live collaboration.

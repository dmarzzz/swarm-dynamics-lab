# Experimental questions for bounded agent workflows

These are proposed comparisons, not registered hypotheses or claims of unoccupied research gaps. Each includes its closest existing questions and the specific new variable or outcome. Related library records are catalogue leads reused from the source atlas; they were not newly read in full in this batch.

## EX-01 — Do correct facts become wrong when schemas disagree?

Can a team combine individually correct provider measurements without silently mixing units, denominators or measurement windows?

**Tentative prediction:** A typed evidence record should reduce composition errors when representations differ, with little benefit on already harmonized inputs.

**Comparison:** Cross harmonized versus mixed units/denominators with prose-only versus typed records. Keep raw information and text budget matched. Choose a provider under an executable contract; include valid conversions and incomparable quantities.

**Measures:** Feasible-choice rate; Invalid comparisons; Clarification rate; Conversion and review cost.

**Falsifier / decision rule:** Drop the typed-record claim if gains disappear when prose contains equally explicit units, or if the format merely exposes evaluator-only answers.

**Controls and confounds:** Do not confuse missing facts with representation mismatch; score justified refusal to compare incompatible measurements.

**Nearest items:** SEC-11, SOC-32, PX-06. **Difference:** Adds representation compatibility as the manipulated cause, rather than merge order or missing log coverage.

**Project briefs:** [collective-sensing](../project-briefs/collective-sensing.md), [coordination](../project-briefs/coordination.md), [casefile](../project-briefs/casefile.md). **Scenario:** API from the [task kits](../hackathon-scenarios/scenario-kits.md).

**Decision value:** Decide whether the harness needs typed measurement fields rather than free-text evidence alone.

**Feasibility:** Small synthetic fixture and deterministic scoring first; LLM comparison only after research gates and budget authorization.

**Catalogue leads:** [[li-2026-memtx]] [[zerhoudi-2026-compaction]] [[liu-2026-safe]]

## EX-02 — Does adaptive provider testing select the luckiest estimate?

When agents can repeat tests selectively, do they choose genuinely better providers or providers with favorable sampling noise?

**Tentative prediction:** Balanced sampling or an independently confirmed final comparison should reduce selection regret relative to unrestricted retesting at equal total tests.

**Comparison:** Give mock providers fixed hidden qualities and noisy test returns. Compare balanced sampling, adaptive testing and adaptive testing with a reserved fresh confirmation set. Vary noise independently of true quality gaps.

**Measures:** True selection regret; Confirmation failures; Tests per provider; Completion cost.

**Falsifier / decision rule:** The confirmation reserve is not useful if its reduction in mistaken choices is offset by lost discovery at the same cap.

**Controls and confounds:** Prevent reuse of confirmation observations for search; include equal-quality providers and report tie uncertainty.

**Nearest items:** SOC-42, SIM-07, PX-13. **Difference:** Moves selection bias inside sequential evidence acquisition, rather than best-of-many completed answers or team calibration.

**Project briefs:** [discovery](../project-briefs/discovery.md), [collective-sensing](../project-briefs/collective-sensing.md), [quorum](../project-briefs/quorum.md). **Scenario:** API from the [task kits](../hackathon-scenarios/scenario-kits.md).

**Decision value:** Choose a repeat-testing and confirmation rule for tool comparison.

**Feasibility:** Small synthetic fixture and deterministic scoring first; LLM comparison only after research gates and budget authorization.

**Catalogue leads:** [[bay-2026-when]] [[liu-2026-llms]] [[data-swarmworld-2026]]

## EX-03 — Can separately valid edits violate a joint invariant?

Do independent reviewers approve edits that are safe alone but inconsistent when committed together?

**Tentative prediction:** Joint invariant validation should prevent write-skew errors that per-edit approval misses, at a measurable coordination cost.

**Comparison:** Construct two concurrent table/config edits that each pass checks against the old snapshot but jointly break a capacity or consistency constraint. Compare independent approval, serialized revalidation and atomic joint validation.

**Measures:** Joint invariant violations; Valid edits retained; Commit latency; Revalidation cost.

**Falsifier / decision rule:** If per-edit checks supplied with the current committed state match joint validation, narrow the claim to stale-snapshot handling.

**Controls and confounds:** Use both interacting and independent edits; randomize order; do not give only one arm access to the invariant.

**Nearest items:** SEC-11, SEC-49, VX-11. **Difference:** Tests concurrent validity against a shared snapshot, rather than merge-order effects or measuring harm after recovery.

**Project briefs:** [coordination](../project-briefs/coordination.md), [institutions](../project-briefs/institutions.md), [commons](../project-briefs/commons.md). **Scenario:** MERGE from the [task kits](../hackathon-scenarios/scenario-kits.md).

**Decision value:** Decide whether approval must bind to a joint transaction rather than individual contributions.

**Feasibility:** Small synthetic fixture and deterministic scoring first; LLM comparison only after research gates and budget authorization.

**Catalogue leads:** [[li-2026-memtx]] [[zerhoudi-2026-compaction]] [[liu-2026-safe]]

## EX-04 — Does approval bind to the artifact that is executed?

Can an approved result be replaced or refreshed before execution without the team noticing?

**Tentative prediction:** Approval bound to a content version should reduce execution of unreviewed state compared with approval bound only to an artifact name.

**Comparison:** Insert a controlled change between review and execution in a mock workflow. Compare name-based approval, version-bound approval and revalidation-on-change; cross harmful and benign updates.

**Measures:** Unreviewed executions; Benign updates blocked; Task completion; Revalidation overhead.

**Falsifier / decision rule:** Version binding adds no decision value if an equivalent revalidation policy prevents the same errors with lower cost.

**Controls and confounds:** Fix the timing window and access rights; a digest proves which content was approved, not its truth or safety.

**Nearest items:** SEC-46, SEC-47, PX-03. **Difference:** Targets the check-to-use interval, distinct from shared-cache bypass or whether a correction becomes visible.

**Project briefs:** [institutions](../project-briefs/institutions.md), [coordination](../project-briefs/coordination.md), [memory](../project-briefs/memory.md). **Scenario:** SUPPORT from the [task kits](../hackathon-scenarios/scenario-kits.md).

**Decision value:** Choose whether approval records require an artifact version and expiration policy.

**Feasibility:** Small synthetic fixture and deterministic scoring first; LLM comparison only after research gates and budget authorization.

**Catalogue leads:** [[le-2026-cross-layer]] [[lee-2026-reproduction]] [[zha-2026-autonomous]]

## EX-05 — Can the swarm answer for the correct point in time?

Will agents distinguish a fact that was correct at the requested date from one that is correct now?

**Tentative prediction:** Explicit validity intervals should reduce temporal-scope errors on historical requests without improving static cases artificially.

**Comparison:** Provide dated provider contracts with overlapping revisions. Cross current versus historical requests with timestamp-only versus validity-interval records; keep the actual facts identical.

**Measures:** Time-scoped correctness; Stale-current selections; Incorrect historical corrections; Evidence cost.

**Falsifier / decision rule:** The interval scheme is not needed if a simple request-date filter performs equally well on held-out revision patterns.

**Controls and confounds:** Distinguish document publication date, effective date and retrieval time; allow unresolved conflicts when intervals overlap.

**Nearest items:** SOC-21, SOC-25, VX-39. **Difference:** Separates historical truth from current truth without requiring corruption or a changed goal during a run.

**Project briefs:** [memory](../project-briefs/memory.md), [telephone](../project-briefs/telephone.md), [casefile](../project-briefs/casefile.md). **Scenario:** API from the [task kits](../hackathon-scenarios/scenario-kits.md).

**Decision value:** Decide which temporal fields a reusable evidence ledger must retain.

**Feasibility:** Small synthetic fixture and deterministic scoring first; LLM comparison only after research gates and budget authorization.

**Catalogue leads:** [[park-2023-generative]] [[perez-2024-cultural]] [[ashery-2024-emergent]]

## EX-06 — Can reversible preparation preserve progress before commitment?

Can agents keep working while evidence is disputed by separating reversible preparation from irreversible action?

**Tentative prediction:** A prepare-then-commit protocol should preserve more useful work than stopping everything while preventing more irreversible mistakes than immediate execution.

**Comparison:** Use a synthetic service action with reversible preparation and an irreversible simulated commit. Compare immediate execution, global pause and prepare/commit under delayed valid and false objections.

**Measures:** Irreversible mistakes; Useful preparation retained; Deadline completion; Coordination overhead.

**Falsifier / decision rule:** Prefer the simpler pause rule if two-phase preparation provides no completion gain at equal error rate.

**Controls and confounds:** Define real simulated side effects explicitly; do not call changing a local log a reversal of an external consequence.

**Nearest items:** SEC-48, SOC-30, VX-11, VX-05. **Difference:** Tests prevention through action staging, rather than rollback after harm or quarantine of evidence alone.

**Project briefs:** [institutions](../project-briefs/institutions.md), [coordination](../project-briefs/coordination.md), [regrowth](../project-briefs/regrowth.md). **Scenario:** SUPPORT from the [task kits](../hackathon-scenarios/scenario-kits.md).

**Decision value:** Choose which tool actions need a separate commitment boundary.

**Feasibility:** Small synthetic fixture and deterministic scoring first; LLM comparison only after research gates and budget authorization.

**Catalogue leads:** [[zha-2026-autonomous]] [[chen-2026-memsecbench]] [[mateo-torrejon-2026-gammaf]]

## EX-07 — Do retries duplicate a valid action?

Can forks and resumed agents repeat an already completed action when the acknowledgment was lost?

**Tentative prediction:** Logical operation IDs shared across retries should prevent duplicate side effects better than per-agent request IDs.

**Comparison:** Drop acknowledgments after successful mock actions. Cross retry by the original worker versus a replacement with no deduplication, per-agent deduplication and operation-level deduplication.

**Measures:** Duplicate side effects; Missed legitimate operations; Completion latency; Recovery cost.

**Falsifier / decision rule:** Operation-level identity is unnecessary if the action interface is already idempotent and simpler retries perform equally.

**Controls and confounds:** Include legitimate repeated requests with similar text; do not deduplicate by textual similarity or silently discard intended repetitions.

**Nearest items:** MTH-05, SIM-05, VX-15. **Difference:** Tests action semantics under lost acknowledgments, not just replay equivalence or ledger continuity.

**Project briefs:** [coordination](../project-briefs/coordination.md), [memory](../project-briefs/memory.md), [regrowth](../project-briefs/regrowth.md). **Scenario:** SUPPORT from the [task kits](../hackathon-scenarios/scenario-kits.md).

**Decision value:** Specify retry identity and replay behavior in the tool contract.

**Feasibility:** Small synthetic fixture and deterministic scoring first; LLM comparison only after research gates and budget authorization.

**Catalogue leads:** [[elnozahy-2002-survey]] [[li-2026-memtx]] [[gh-apromisedland-trustworthy-agent-simulation]]

## EX-08 — Can correction messages create a repair loop?

Will several defenders repeatedly invalidate and restore the same fact after observing one another’s corrections?

**Tentative prediction:** Causally tagged, idempotent correction events should reduce repair oscillation compared with unversioned repeated warnings.

**Comparison:** Inject one repairable error, then deliver duplicated and delayed correction notifications in a cycle. Compare plain warnings, event-ID deduplication and version-aware supersession at equal message limits.

**Measures:** Repair operations per incident; Time to stable correctness; Legitimate work displaced; Unresolved incidents.

**Falsifier / decision rule:** If message deduplication alone removes the effect, do not claim a broader immune-control advantage.

**Controls and confounds:** Keep truth stable in this experiment; genuine new evidence must not be suppressed as a duplicate.

**Nearest items:** SEC-07, SEC-50, VX-14. **Difference:** Tests self-generated intervention loops after one incident, distinct from stale-child reinfection or detector overhead alone.

**Project briefs:** [regrowth](../project-briefs/regrowth.md), [memory](../project-briefs/memory.md), [institutions](../project-briefs/institutions.md). **Scenario:** RESULT from the [task kits](../hackathon-scenarios/scenario-kits.md).

**Decision value:** Decide whether corrections need causal IDs and idempotent application.

**Feasibility:** Small synthetic fixture and deterministic scoring first; LLM comparison only after research gates and budget authorization.

**Catalogue leads:** [[cai-2026-child]] [[li-2026-memtx]] [[zha-2026-autonomous]]

## EX-09 — Do locally feasible tool choices compose into a feasible pipeline?

Can specialist agents choose individually valid services that together violate an end-to-end requirement?

**Tentative prediction:** Explicit compatibility constraints should improve joint pipeline feasibility over independent per-service choices.

**Comparison:** Choose an extractor and storage API with hidden-to-agents but observable-through-documents interface, region and latency constraints. Compare independent recommendations, shared constraint messages and centralized union-of-evidence selection.

**Measures:** End-to-end feasibility; Local-versus-global disagreement; Total utility regret; Communication cost.

**Falsifier / decision rule:** The coordination mechanism adds no value if independently choosing each best service also solves the coupled instances.

**Controls and confounds:** Match all accessible facts; vary coupling strength while holding single-service difficulty fixed; avoid privileged compatibility labels.

**Nearest items:** SOC-16, SOC-04, PX-10. **Difference:** Introduces joint task feasibility as the endpoint, beyond routing relevance or role bottlenecks.

**Project briefs:** [coordination](../project-briefs/coordination.md), [collective-sensing](../project-briefs/collective-sensing.md), [leadership](../project-briefs/leadership.md). **Scenario:** API from the [task kits](../hackathon-scenarios/scenario-kits.md).

**Decision value:** Identify when task decomposition must preserve cross-subtask constraints.

**Feasibility:** Small synthetic fixture and deterministic scoring first; LLM comparison only after research gates and budget authorization.

**Catalogue leads:** [[pal-2026-swarmworld]] [[cemri-2025-why]] [[amayuelas-2025-self]]

## EX-10 — Which evidence partition makes decomposition fail?

Does splitting work by source, claim or candidate change performance when the same facts must be joined across several subtasks?

**Tentative prediction:** Partitioning along dependency boundaries should reduce synthesis losses as cross-partition dependencies increase.

**Comparison:** Generate fixed claim-support graphs with varying edge cuts. Assign the same evidence union by source, claim or random partition, with matched worker counts and communication caps.

**Measures:** Joint claim correctness; Missing cross-partition joins; Duplicate retrieval; Coordination cost.

**Falsifier / decision rule:** Prefer simple partitioning if dependency-aware assignment loses its advantage after charging the partitioner’s work.

**Controls and confounds:** The partitioner sees only allowed structure, not answers; match marginal packet difficulty and overall evidence volume.

**Nearest items:** SOC-01, SOC-13, VX-34. **Difference:** Varies decomposition geometry of a fixed task, rather than model diversity or the discovery/discussion budget split.

**Project briefs:** [collective-sensing](../project-briefs/collective-sensing.md), [coordination](../project-briefs/coordination.md), [discovery](../project-briefs/discovery.md). **Scenario:** RESEARCH from the [task kits](../hackathon-scenarios/scenario-kits.md).

**Decision value:** Choose how an orchestrator should divide evidence work.

**Feasibility:** Small synthetic fixture and deterministic scoring first; LLM comparison only after research gates and budget authorization.

**Catalogue leads:** [[li-2026-diverse]] [[kim-2026-are]] [[rai-2026-when]]

## EX-11 — Can a small checkable witness replace a long explanation?

Do compact evidence witnesses help reviewers verify a result more efficiently than plausible free-text rationales?

**Tentative prediction:** A valid witness should improve verification per resource, while invalid witnesses should be rejected rather than trusted for their format.

**Comparison:** For a bounded table or patch contract, provide rationale only, raw sources, or a minimal executable counterexample/witness. Include correct, invalid and incomplete witnesses at matched review budgets.

**Measures:** False acceptance; False rejection; Verification cost; Correctness after review.

**Falsifier / decision rule:** There is no witness advantage if a simple raw-source check matches it at equal total production and review cost.

**Controls and confounds:** Charge witness construction; do not let the witness contain evaluator-only labels or assume every claim admits a short certificate.

**Nearest items:** SOC-27, MTH-07, VX-38. **Difference:** Tests the form and end-to-end cost of verifiable evidence, rather than independent judges or poisoned summaries alone.

**Project briefs:** [casefile](../project-briefs/casefile.md), [dissent](../project-briefs/dissent.md), [institutions](../project-briefs/institutions.md). **Scenario:** PATCH from the [task kits](../hackathon-scenarios/scenario-kits.md).

**Decision value:** Decide whether contributions should include a checkable witness alongside prose.

**Feasibility:** Small synthetic fixture and deterministic scoring first; LLM comparison only after research gates and budget authorization.

**Catalogue leads:** [[leibo-2021-scalable]] [[pal-2026-swarmworld]] [[piatti-2024-cooperate]]

## EX-12 — Can correction policies distinguish reversals from noisy updates?

When a fact changes repeatedly, can agents avoid both oscillating on noisy reports and clinging to an obsolete correction?

**Tentative prediction:** A policy that tracks observation timing and independent corroboration should improve the lag/error tradeoff over fixed hysteresis.

**Comparison:** Use a mock provider whose true status can reverse, plus noisy reports with known delays. Compare immediate switching, fixed persistence threshold and version/time-aware updating.

**Measures:** Tracking error; Switching cost; Lag after genuine reversal; False reversals.

**Falsifier / decision rule:** Keep the simpler policy if its tracking-error/cost frontier dominates under held-out change rates.

**Controls and confounds:** Hold source reliability separate from change frequency; distinguish delayed truth from false evidence.

**Nearest items:** PHY-12, MET-06, VX-39. **Difference:** Adds repeated nonstationarity and noisy correction streams, beyond one change point or apparent physical hysteresis.

**Project briefs:** [memory](../project-briefs/memory.md), [quorum](../project-briefs/quorum.md), [culture](../project-briefs/culture.md). **Scenario:** HANDOFF from the [task kits](../hackathon-scenarios/scenario-kits.md).

**Decision value:** Choose a correction policy for changing environments without treating every revision as corruption.

**Feasibility:** Small synthetic fixture and deterministic scoring first; LLM comparison only after research gates and budget authorization.

**Catalogue leads:** [[talamali-2021-when]] [[leonard-2024-fast]] [[valentini-2017-best]]

## EX-13 — Can predictable audits be selectively evaded?

Does a fixed audit checklist invite contributors to place errors in rarely checked parts of a result?

**Tentative prediction:** Randomized checks should reduce adaptive evasion at equal audit cost, but may miss high-risk fields compared with targeted checks.

**Comparison:** Give a bounded adversarial contributor knowledge of a fixed, risk-ranked or randomized audit policy. Hold error budget and audit calls fixed; compare against nonadaptive errors and a held-out attack strategy.

**Measures:** Undetected harmful error; Legitimate result coverage; Audit cost; Risk-weighted residual loss.

**Falsifier / decision rule:** Randomization is not useful if a fixed risk-ranked policy yields lower residual loss against held-out adaptive contributors.

**Controls and confounds:** Randomize audit seeds outside attacker access; count benign mistakes and false rejection; do not claim security beyond the declared attacker.

**Nearest items:** SEC-29, SEC-38, VX-30. **Difference:** Tests strategic placement against an audit policy, rather than detection probes changing subjects or missing verifier logs.

**Project briefs:** [institutions](../project-briefs/institutions.md), [casefile](../project-briefs/casefile.md), [commons](../project-briefs/commons.md). **Scenario:** RESULT from the [task kits](../hackathon-scenarios/scenario-kits.md).

**Decision value:** Choose where limited verification effort should be unpredictable.

**Feasibility:** Small synthetic fixture and deterministic scoring first; LLM comparison only after research gates and budget authorization.

**Catalogue leads:** [[gans-2026-when]] [[seiden-2026-identifying]] [[todo-2009-characterizing]]

## EX-14 — Does abstract-only curation miss disqualifying conditions?

Will a resource curator select apparently relevant work whose methods or limitations contradict the intended use?

**Tentative prediction:** Targeted retrieval of task-critical conditions should improve support quality more efficiently than uniformly reading longer excerpts.

**Comparison:** Use verified source cards with claims in abstracts and qualifying conditions in methods/limitations. Compare abstract-only screening, uniform expansion and targeted section requests under one retrieval cap.

**Measures:** Unsupported transfer claims; Relevant coverage; Section requests; Citation support precision.

**Falsifier / decision rule:** Targeted reading is not better if uniform expansion provides equal supported coverage for the same total retrieval cost.

**Controls and confounds:** Annotate source conditions independently; do not hide all decisive facts only in one favored section; include abstracts that are sufficient.

**Nearest items:** SOC-04, SOC-08, PX-06, PX-10. **Difference:** Varies evidence depth and qualification access, rather than source identity or generic routing alone.

**Project briefs:** [discovery](../project-briefs/discovery.md), [telephone](../project-briefs/telephone.md), [collective-sensing](../project-briefs/collective-sensing.md). **Scenario:** RESEARCH from the [task kits](../hackathon-scenarios/scenario-kits.md).

**Decision value:** Decide when a curation agent must inspect methods before recommending a resource.

**Feasibility:** Small synthetic fixture and deterministic scoring first; LLM comparison only after research gates and budget authorization.

**Catalogue leads:** [[tambwekar-2026-proxifield]] [[zhang-2024-cut]] [[zhang-2026-silo]]

## EX-15 — Do evaluation incentives suppress honest uncertainty?

Do teams conceal missing evidence when abstention or clarification is penalized in individual performance scores?

**Tentative prediction:** Rewarding justified abstention should improve calibration but can create excessive refusal unless useful completion is scored too.

**Comparison:** Cross complete versus insufficient evidence with completion-only, accuracy-only and balanced outcome incentives. Keep tools and facts fixed and evaluate all arms with the same external task utility.

**Measures:** Unsupported confident answers; Justified abstention; Avoidable refusal; External task utility.

**Falsifier / decision rule:** Drop an incentive rule if it only trades incorrect answers for unnecessary refusal without improving external utility.

**Controls and confounds:** Separate the reward shown to agents from the evaluator’s metric; do not count abstention as universally good.

**Nearest items:** SOC-20, SOC-27, VX-31. **Difference:** Changes the incentive for revealing uncertainty, rather than the information conveyed by abstention itself.

**Project briefs:** [commons](../project-briefs/commons.md), [institutions](../project-briefs/institutions.md), [dissent](../project-briefs/dissent.md). **Scenario:** API from the [task kits](../hackathon-scenarios/scenario-kits.md).

**Decision value:** Choose scorecards that reward useful calibrated behavior rather than apparent completion.

**Feasibility:** Small synthetic fixture and deterministic scoring first; LLM comparison only after research gates and budget authorization.

**Catalogue leads:** [[cemri-2025-why]] [[zhang-2026-silo]] [[leibo-2021-scalable]]

## EX-16 — Should disagreement be routed by its cause?

Can a team resolve conflicts more cheaply by distinguishing factual disagreement, incompatible definitions and permission disputes?

**Tentative prediction:** Cause-specific resolution should help only when the classifier is accurate enough to offset misrouting and its own cost.

**Comparison:** Create matched disputes caused by a wrong fact, a unit/definition mismatch or unauthorized action. Compare generic debate, inferred cause-specific routing and oracle routing as a ceiling.

**Measures:** Correct resolution; Misrouted disputes; Resolution cost; Harmful escalations.

**Falsifier / decision rule:** Use generic review if classifier errors erase the advantage of specialized resolution at equal total budget.

**Controls and confounds:** Keep surface wording and difficulty balanced; oracle labels stay outside the deployed policy; include mixed-cause disputes.

**Nearest items:** SEC-04, SOC-09, VX-36. **Difference:** Introduces diagnostic routing among distinct conflict mechanisms; complements EX-01’s specific schema-mismatch fixture.

**Project briefs:** [dissent](../project-briefs/dissent.md), [coordination](../project-briefs/coordination.md), [institutions](../project-briefs/institutions.md). **Scenario:** SUPPORT from the [task kits](../hackathon-scenarios/scenario-kits.md).

**Decision value:** Decide whether an orchestrator needs a dispute taxonomy before selecting a reviewer.

**Feasibility:** Small synthetic fixture and deterministic scoring first; LLM comparison only after research gates and budget authorization.

**Catalogue leads:** [[triedman-2025-multi]] [[zha-2026-autonomous]] [[louck-2026-securing]]

## EX-17 — When is asking the user better than gathering more facts?

Can a swarm identify that the missing input is a user preference rather than an external fact?

**Tentative prediction:** Explicit uncertainty about preferences should trigger useful clarification more often than extra retrieval or assumed defaults.

**Comparison:** Give several factually feasible providers with a withheld user tradeoff, or a missing factual measurement. Allow one scripted clarification and bounded lookup calls; compare fixed defaults, retrieval-only and adaptive clarification.

**Measures:** User-utility regret; Useful clarification rate; Unnecessary questions; Resource cost.

**Falsifier / decision rule:** Clarification is not worthwhile if a declared default policy achieves comparable utility after charging user interaction.

**Controls and confounds:** The evaluator’s preference is known only through the scripted user response; separate ambiguous preferences from infeasible tasks.

**Nearest items:** SOC-11, SOC-20, VX-28. **Difference:** Distinguishes preference uncertainty from factual uncertainty, rather than changing the option set alone.

**Project briefs:** [collective-sensing](../project-briefs/collective-sensing.md), [leadership](../project-briefs/leadership.md), [quorum](../project-briefs/quorum.md). **Scenario:** API from the [task kits](../hackathon-scenarios/scenario-kits.md).

**Decision value:** Choose when to ask a human instead of spending another swarm search round.

**Feasibility:** Small synthetic fixture and deterministic scoring first; LLM comparison only after research gates and budget authorization.

**Catalogue leads:** [[tambwekar-2026-proxifield]] [[zhang-2026-silo]] [[zhu-2026-demystifying]]

## EX-18 — Do delegated workers notice that the goal changed?

When the user revises the objective, can agents stop producing locally correct work for an obsolete task?

**Tentative prediction:** Versioned goals with acknowledgment should reduce obsolete work but can add coordination delays under frequent harmless edits.

**Comparison:** Change the requested output while workers are running. Compare ordinary announcement, goal-version checks and cancel/reassign; include semantic changes and wording-only edits.

**Measures:** Current-goal utility; Obsolete work; Completion delay; Acknowledgment cost.

**Falsifier / decision rule:** Version checks are unnecessary if ordinary announcements match current-goal success without extra delay.

**Controls and confounds:** Hold evidence truth fixed; this changes the requested objective, not source facts. Charge work already spent before the revision.

**Nearest items:** SOC-15, SOC-18, VX-15, VX-39. **Difference:** Tests goal-version propagation rather than leader continuity, stale evidence or changed environment constraints.

**Project briefs:** [leadership](../project-briefs/leadership.md), [coordination](../project-briefs/coordination.md), [culture](../project-briefs/culture.md). **Scenario:** BATCH from the [task kits](../hackathon-scenarios/scenario-kits.md).

**Decision value:** Specify cancellation and task-version semantics for delegated work.

**Feasibility:** Small synthetic fixture and deterministic scoring first; LLM comparison only after research gates and budget authorization.

**Catalogue leads:** [[zhang-2026-silo]] [[kim-2025-towards]] [[paliskara-2026-worse]]

## EX-19 — Which damaged component should be repaired first?

Under a binding repair budget, does prioritizing recoverable task value outperform repairing the most visibly corrupted component?

**Tentative prediction:** Value-aware triage should restore more useful output when damage size and downstream importance differ.

**Comparison:** Inject equal-cost incidents into dependency graphs with different downstream value and recoverability. Compare arrival order, largest-damage-first and observable value-based triage; use oracle value only as a ceiling.

**Measures:** Restored verified utility; Residual downstream harm; Repair cost; Neglected valid work.

**Falsifier / decision rule:** Use the simplest triage rule if estimated-value errors erase its recovery advantage on held-out graphs.

**Controls and confounds:** Match total damage and repair capacity; include irrecoverable components so policies cannot win through privileged lost state.

**Nearest items:** SEC-06, SEC-08, VX-40. **Difference:** Varies repair prioritization by marginal recovery value, rather than queue-position effects on truth or attention flooding.

**Project briefs:** [regrowth](../project-briefs/regrowth.md), [commons](../project-briefs/commons.md), [coordination](../project-briefs/coordination.md). **Scenario:** RESULT from the [task kits](../hackathon-scenarios/scenario-kits.md).

**Decision value:** Allocate limited immune-response capacity across simultaneous incidents.

**Feasibility:** Small synthetic fixture and deterministic scoring first; LLM comparison only after research gates and budget authorization.

**Catalogue leads:** [[li-2026-memtx]] [[chen-2026-memsecbench]] [[ouyang-2026-memlineage]]

## EX-20 — Can shared memory keep two tasks’ truths separate?

Will agents reuse a correct fact from one client, region or task where the same-looking fact is wrong in another?

**Tentative prediction:** Task-scoped evidence should reduce cross-task contamination while retaining explicit transferable facts.

**Comparison:** Run two concurrent provider evaluations with overlapping entity names but different constraints. Compare global notes, task namespaces and selective shared facts under equal storage/retrieval budgets.

**Measures:** Cross-task contamination; Valid reuse; Task success; Storage and routing overhead.

**Falsifier / decision rule:** Strict isolation is not preferable if it loses enough useful reuse to underperform a simple scope filter.

**Controls and confounds:** Keep temporal validity constant; vary task scope independently of wording and do not use task IDs as hidden answer labels.

**Nearest items:** SOC-21, SEC-05, PX-01, PX-03. **Difference:** Adds scope binding across simultaneous tasks, distinct from novelty, compaction or correction visibility within one task.

**Project briefs:** [memory](../project-briefs/memory.md), [coordination](../project-briefs/coordination.md), [collective-sensing](../project-briefs/collective-sensing.md). **Scenario:** HANDOFF from the [task kits](../hackathon-scenarios/scenario-kits.md).

**Decision value:** Choose namespace and sharing rules for a multi-task evidence store.

**Feasibility:** Small synthetic fixture and deterministic scoring first; LLM comparison only after research gates and budget authorization.

**Catalogue leads:** [[park-2023-generative]] [[perez-2024-cultural]] [[zerhoudi-2026-compaction]]

## EX-21 — Should provider selection use estimates or uncertainty bounds?

Do agents account for the amount of test evidence when deciding whether a provider meets a hard reliability requirement?

**Tentative prediction:** Uncertainty-aware selection should reduce risky infeasible choices at the cost of more abstention or testing.

**Comparison:** Vary test sample size independently of empirical accuracy for mock providers with known true quality. Compare point-estimate choice, conservative bound-based choice and a fixed extra-test policy.

**Measures:** True feasibility violations; Utility regret; Abstention; Additional tests.

**Falsifier / decision rule:** Prefer point estimates if the uncertainty policy’s service loss exceeds its reduction in violations under the declared task utility.

**Controls and confounds:** Use held-out outcomes for evaluation; define the uncertainty method before testing and do not confuse epistemic uncertainty with task preference.

**Nearest items:** SOC-11, SOC-43, PX-13. **Difference:** Targets finite-sample measurement uncertainty in tool qualification, rather than confidence in a model’s answer or team-selection ties.

**Project briefs:** [quorum](../project-briefs/quorum.md), [discovery](../project-briefs/discovery.md), [collective-sensing](../project-briefs/collective-sensing.md). **Scenario:** API from the [task kits](../hackathon-scenarios/scenario-kits.md).

**Decision value:** Define what counts as enough evidence to approve an API against a reliability requirement.

**Feasibility:** Small synthetic fixture and deterministic scoring first; LLM comparison only after research gates and budget authorization.

**Catalogue leads:** [[tambwekar-2026-proxifield]] [[zhang-2026-silo]] [[zhu-2026-demystifying]]

## EX-22 — Do tool failures become false observations?

Will a timeout, empty response or permission error be silently interpreted as a legitimate zero or negative result?

**Tentative prediction:** Typed failure states should reduce false conclusions while exposing a retry/abstention cost.

**Comparison:** Cross genuine zero results with timeout, access-denied and truncated tool responses. Compare ambiguous text outputs, explicit typed failures and a bounded retry policy.

**Measures:** False negative claims; Correct unknowns; Duplicate tool work; Final task success.

**Falsifier / decision rule:** Type distinctions add little if an equally explicit text protocol matches correctness and retry cost.

**Controls and confounds:** Hold underlying task truth fixed; include legitimate empty results and charge retries; do not treat unavailable data as evidence of absence.

**Nearest items:** SEC-53, MTH-11, PX-02, PX-06. **Difference:** Tests within-run tool outcome semantics, rather than missing final-run denominators or source completeness alone.

**Project briefs:** [casefile](../project-briefs/casefile.md), [coordination](../project-briefs/coordination.md), [memory](../project-briefs/memory.md). **Scenario:** RESEARCH from the [task kits](../hackathon-scenarios/scenario-kits.md).

**Decision value:** Set tool response contracts that preserve unknown and failure states.

**Feasibility:** Small synthetic fixture and deterministic scoring first; LLM comparison only after research gates and budget authorization.

**Catalogue leads:** [[pecori-2016-s-kademlia]] [[maccari-2009-avoiding]] [[gh-datahop-kademlia-simulator]]

## EX-23 — How much evidence must be shared to make a correct joint decision?

Can constrained evidence summaries support the task without exposing unrelated synthetic private fields to every agent?

**Tentative prediction:** Task-limited evidence capsules should preserve most decision utility while reducing unnecessary disclosure, with failure on tasks requiring omitted context.

**Comparison:** Use entirely synthetic records containing task-relevant and irrelevant sensitive fields. Compare raw sharing, fixed redaction and task-specific capsules; score final decisions and fields actually exposed.

**Measures:** Task utility; Unnecessary field exposure; Required context lost; Summarization cost.

**Falsifier / decision rule:** Prefer simple redaction if capsules add cost without improving the utility/disclosure frontier.

**Controls and confounds:** Define allowed recipients and necessary fields in advance; no real secrets. This is a data-minimization measurement, not a formal privacy guarantee.

**Nearest items:** SEC-04, SOC-14, VX-32. **Difference:** Measures useful evidence sharing under disclosure constraints, rather than action permissions or communication volume alone.

**Project briefs:** [institutions](../project-briefs/institutions.md), [coordination](../project-briefs/coordination.md), [collective-sensing](../project-briefs/collective-sensing.md). **Scenario:** SUPPORT from the [task kits](../hackathon-scenarios/scenario-kits.md).

**Decision value:** Choose what a worker should disclose to peers when forwarding evidence.

**Feasibility:** Small synthetic fixture and deterministic scoring first; LLM comparison only after research gates and budget authorization.

**Catalogue leads:** [[triedman-2025-multi]] [[zha-2026-autonomous]] [[louck-2026-securing]]

## EX-24 — Can a defender distinguish flaky tools from targeted interference?

Can repeated observations identify persistent or caller-specific corruption without wrongly quarantining a merely noisy tool?

**Tentative prediction:** Cross-caller retests should improve separation only when the incident mechanisms are observationally distinguishable.

**Comparison:** Generate random transient errors, persistent wrong responses and caller-dependent responses with matched average error rate. Compare one-shot quarantine, repeated same-caller checks and cross-caller checks; include indistinguishable mechanism pairs.

**Measures:** Wrong quarantine; Residual task error; Diagnostic calls; Calibrated unknowns.

**Falsifier / decision rule:** Drop attribution claims when matched mechanisms produce the same observable distribution; retain only the measured task-protection claim.

**Controls and confounds:** Freeze retry randomness and caller access; charge diagnostics; an identified failure pattern does not prove malicious intent.

**Nearest items:** SEC-27, SEC-30, SEC-53, VX-14. **Difference:** Adds controlled failure mechanisms and diagnostic interventions, distinct from prevalence calibration or generic observer effects.

**Project briefs:** [whistleblowing](../project-briefs/whistleblowing.md), [discovery](../project-briefs/discovery.md), [regrowth](../project-briefs/regrowth.md). **Scenario:** RESULT from the [task kits](../hackathon-scenarios/scenario-kits.md).

**Decision value:** Choose when to retry, route around, quarantine or explicitly withhold attribution.

**Feasibility:** Small synthetic fixture and deterministic scoring first; LLM comparison only after research gates and budget authorization.

**Catalogue leads:** [[shalizi-2011-homophily]] [[aronow-2013-estimating]] [[pante-2025-beyond]]

## EX-25 — What swarm size is best for this problem under these constraints?

For a specified problem and solution approach, what number of agents yields the best verified outcome under different urgency, cost, memory and hardware constraints, and can that size be predicted before solving a new instance?

**Tentative prediction:** The best tested size will depend on useful task parallelism, evidence complementarity and coordination overhead: added workers may help decomposable urgent tasks until shared compute, memory or tool capacity saturates, while tightly coupled tasks may favor one or a few agents.

**Comparison:** Specify a problem-solution pair as a task family plus a fixed model, tool set, solution method, coordination topology and answer-integration rule. Sweep fixed rosters including N=1 and a bounded geometric size grid. Cross task decomposition, dependency depth, difficulty, evidence overlap and communication needs with deadline urgency, total dollar/token budget, per-agent context limits, shared-memory policy, physical RAM/VRAM capacity, worker slots, inference throughput and tool/API concurrency. Use a staged factorial design, then refine near apparent optima. Randomize independent task instances and seeds; hold the hardware and total resource envelope fixed within each comparison, charge orchestration and communication, and separately label any fixed-per-agent-resource sensitivity. Train a size selector only on development task families and evaluate on held-out families and hardware conditions. Compare its chosen fixed size with N=1, the best single fixed size from development, a simple capacity-aware heuristic and an evaluator-only best tested size. Treat dynamic resizing as a separate follow-up with spawn and memory-transfer costs.

**Measures:** Verified task quality and success probability before deadline; End-to-end latency including setup, queues and integration; Total dollars, tokens, tool calls and compute time; Peak RAM/VRAM and per-agent context use; Communication, duplicated work, coordination and idle time; Feasible quality-cost-latency frontier and uncertainty in best tested N; Held-out selector regret relative to the evaluator-only best tested size

**Falsifier / decision rule:** The conditional-size predictor is not useful if it fails to beat the best development-selected fixed size or simple capacity heuristic on held-out cases after charging selection overhead. Report a flat or uncertain optimum as a range; report no feasible size if all tested rosters violate the constraints.

**Controls and confounds:** Agent roster size is distinct from simultaneously runnable processes and independent evidence sources. Increasing N must not silently increase total compute, memory, evidence, model quality or test-time budget. Hardware speed, API throttling, cache warmth, context replication, batching, topology and integration policy can confound size. Do not tune N on test outcomes or count workers/messages as independent replicates. Define utility and hard constraints before evaluation; a finite tested grid cannot establish a universal global optimum.

**Nearest atlas items:** SOC-02; PHY-09; BUD-06; BUD-08

**Difference:** Existing cards test effective evidence size, correlated cues or quota-induced spawning. This question instead selects an operational roster size for a specified problem-solution pair across jointly stated task and resource constraints, then tests prediction on new cases.

**Decision value:** Choose how many workers to launch for an actual job and when added parallelism is not worth its resource or coordination cost. Define the optimum as maximum expected verified quality subject to deadline, cost and memory/hardware limits, or report the nondominated quality-cost-latency choices when priorities are not scalarized.

**Feasibility:** Start with an explicit design and offline scheduling/queue fixtures; qualify bounded model tasks only after the lab review, public-plan registration, machine allocation and budget gates. No experiment is launched by this question.

**Theory and animation:** Catalogue leads inherited from related atlas cards; no new full-methods review or claim that optimal swarm sizing is an unoccupied research gap. Proposed theory connections are finite-group information aggregation, queueing and parallel speedup with coordination overhead. Visual concept: animate workers, dependency queues and memory pressure while a phase map shows the best tested size as deadlines and resources change.

**EX-25 detailed design:** [Optimal swarm size under task and resource constraints](../optimal-swarm-size/README.md), with [machine-readable planning counts](../optimal-swarm-size/design.json).

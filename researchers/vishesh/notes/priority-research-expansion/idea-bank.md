# Source grounded experimental extensions

These fourteen comparisons are proposed by vishesh/codex-methods on 2026-10-03. They refine or connect existing atlas cards and VX ideas; they are not fourteen independent discoveries, registered hypotheses or approved runs. Source summaries live in the canonical records. The comparisons, falsifiers and priorities below are our inferences. Full-methods review and the repository survey gate remain necessary.

Each comparison randomizes complete task worlds, uses a held-out test split, records every assigned episode and reports uncertainty across worlds rather than across correlated agent messages. Any practical effect margin must be fixed after an explicitly separate feasibility pilot and before confirmatory data collection. No power or sample-size claim is made here.

## PX-01 Separate novelty of wording from novelty of evidence

Atlas: [SOC-21](https://swarm-research.pages.dev/#/questions?q=SOC-21), [SOC-22](https://swarm-research.pages.dev/#/questions?q=SOC-22), [SEC-03](https://swarm-research.pages.dev/#/questions?q=SEC-03). Projects: [memory](../project-briefs/memory.md), [quorum](../project-briefs/quorum.md), [collective-sensing](../project-briefs/collective-sensing.md).

Sources: [[pal-2026-context]], [[pescetelli-2022-variational]]. Nearest earlier ideas: VX-01, VX-20 in the [existing bank](../atlas-review/extension-bank.md).

**Question and difference.** A refinement of provenance granularity: ask whether a novelty-based memory policy preserves independent observations when copied reports are paraphrased and independent observations use the same wording.

**Discriminating comparison.** Cross observation ancestry (copied or independent) with wording (identical or paraphrased). Compare recency, text-similarity novelty and observable-lineage selection at fixed storage and inference caps. Score retained independent useful facts and final accuracy; an oracle selector is a ceiling.

**Confounds and boundaries.** Keep truth, marginal reliability, length and eventual relevance matched. Similarity thresholds must be frozen on separate worlds. Do not equate semantic distance with statistical independence.

**Decision if unsupported.** Drop semantic novelty as a provenance substitute if it fails on paraphrased copies or discards independently corroborating observations without an accuracy benefit.

**Why it matters.** Choose separate ledger fields for content deduplication and evidence ancestry.

**Feasibility.** Deterministic fixture followed by a small agent comparison; no trained cache implementation required initially.

## PX-02 Track conclusions that depend on something being absent

Atlas: [SEC-06](https://swarm-research.pages.dev/#/questions?q=SEC-06), [SOC-08](https://swarm-research.pages.dev/#/questions?q=SOC-08). Projects: [memory](../project-briefs/memory.md), [regrowth](../project-briefs/regrowth.md), [casefile](../project-briefs/casefile.md).

Sources: [[gradel-2024-provenance]], [[fu-2025-absencebench]]. Nearest earlier ideas: VX-06, VX-39 in the [existing bank](../atlas-review/extension-bank.md).

**Question and difference.** Existing repair ideas mainly retract descendants of a false positive fact. Here the invalidated premise is an absence, such as no conflicting reservation or no unresolved counterexample.

**Discriminating comparison.** Construct reversible scheduling worlds with positive and negative dependencies. Introduce a previously missing conflict after a decision. Compare positive-edge rollback, explicit absence-witness invalidation and full recomputation under equal refresh budgets. Measure stale decisions and valid knowledge retained.

**Confounds and boundaries.** An absence requires a bounded search domain and a completeness witness. An unqueried source is unknown, not negative evidence. Keep the reference solver private to scoring.

**Decision if unsupported.** The extension is unnecessary for a task class if positive-only repair is equally correct because every relevant negative premise is already materialized.

**Why it matters.** Decide whether the immune-response ledger needs explicit negative dependencies before building a larger repair policy.

**Feasibility.** High readiness: small symbolic task generator, then language interface after survey review.

## PX-03 Test correction visibility independently of correction storage

Atlas: [SEC-07](https://swarm-research.pages.dev/#/questions?q=SEC-07), [SEC-06](https://swarm-research.pages.dev/#/questions?q=SEC-06). Projects: [memory](../project-briefs/memory.md), [regrowth](../project-briefs/regrowth.md), [coordination](../project-briefs/coordination.md).

Sources: [[yu-2026-multi]], [[xu-2025-everything]]. Nearest earlier ideas: VX-06, VX-19 in the [existing bank](../atlas-review/extension-bank.md).

**Question and difference.** Distinguish storing a correction from making it visible to all readers. The new axis is consistency of shared reads after an acknowledged write, including agents that never forked.

**Discriminating comparison.** Replay identical traces under immediate visibility, delayed cache invalidation and per-record version checks. Vary reader delay independently of content. Score stale actions after acknowledgment, useful unaffected reads and synchronization cost.

**Confounds and boundaries.** Log logical read/write versions rather than relying solely on wall-clock timestamps. Do not grant the version-check arm extra evidence. Separate runtime ordering failures from semantic rejection of a visible correction.

**Decision if unsupported.** If all failures persist after every reader sees the same corrected version, prioritize reasoning and admission policy rather than cache consistency.

**Why it matters.** Locate whether repair belongs in storage semantics, merge logic or agent prompting.

**Feasibility.** Deterministic scheduler and mock agents first; low-cost integration check before any API runs.

## PX-04 Evaluate safe return over a continuation sequence

Atlas: [SEC-48](https://swarm-research.pages.dev/#/questions?q=SEC-48), [SEC-07](https://swarm-research.pages.dev/#/questions?q=SEC-07). Projects: [regrowth](../project-briefs/regrowth.md), [institutions](../project-briefs/institutions.md).

Sources: [[xiao-2026-when]], [[yu-2026-multi]]. Nearest earlier ideas: VX-05, VX-18 in the [existing bank](../atlas-review/extension-bank.md).

**Question and difference.** Refines the existing re-entry protocol by testing whether safety checks miss history-dependent recurrence. The question is about evaluation design, not constructing a real backdoor.

**Discriminating comparison.** Use scripted faults in a closed synthetic environment that activate only after specified benign events. Compare a single clean probe, equal-cost repeated identical probes and held-out varied continuation probes. All policies use the same restricted re-entry permissions; report false release and false quarantine.

**Confounds and boundaries.** Probe suites cannot contain the test sequence or oracle trigger state. Match probe count and compute. Keep trained model compromise separate from external misinformation in the threat model.

**Decision if unsupported.** If varied probes do not improve held-out recurrence detection at matched false-quarantine rates, retain the simpler check and document its coverage limits.

**Why it matters.** Choose what evidence a release decision must collect and how long recurrence should be observed.

**Feasibility.** Safe scripted simulation first; actual compromised models are outside this contribution.

## PX-05 Distinguish missing knowledge from missing retrieval keys

Atlas: [SOC-23](https://swarm-research.pages.dev/#/questions?q=SOC-23), [SOC-21](https://swarm-research.pages.dev/#/questions?q=SOC-21). Projects: [regrowth](../project-briefs/regrowth.md), [memory](../project-briefs/memory.md), [telephone](../project-briefs/telephone.md).

Sources: [[modarressi-2025-nolima]], [[anthropic-2025-effective]]. Nearest earlier ideas: VX-07, VX-10 in the [existing bank](../atlas-review/extension-bank.md).

**Question and difference.** The existing loss audit checks hidden backups. This extension separates actual fact loss from retained facts whose index, wording or location no longer matches the recovery query.

**Discriminating comparison.** Cross fact retention with index retention, and exact lexical matches with indirect semantic references. Compare blind restart, index rebuild and new observation gathering at equal access cost. Score recovered facts and decision success, with provenance proving the route used.

**Confounds and boundaries.** Rebuilding an index is not reacquiring evidence. Hold the surviving fact set constant within retrieval comparisons; renaming must not alter information content or authority.

**Decision if unsupported.** If an index rebuild explains recovery, reject the claim that the system reconstructed genuinely lost knowledge in that condition.

**Why it matters.** Prevent a retrieval improvement from being advertised as swarm regeneration; select the cheapest repair that restores function.

**Feasibility.** Small file-based fixture; semantic paraphrases require a held-out check for equivalent meaning.

## PX-06 Give an omission detector a bounded completeness contract

Atlas: [SOC-08](https://swarm-research.pages.dev/#/questions?q=SOC-08), [SOC-32](https://swarm-research.pages.dev/#/questions?q=SOC-32). Projects: [quorum](../project-briefs/quorum.md), [casefile](../project-briefs/casefile.md), [collective-sensing](../project-briefs/collective-sensing.md).

Sources: [[fu-2025-absencebench]], [[gradel-2024-provenance]]. Nearest earlier ideas: VX-30 in the [existing bank](../atlas-review/extension-bank.md).

**Question and difference.** Instead of asking whether something seems missing, vary what completeness evidence the investigator is entitled to use. This tests when a checklist can justify stopping or an absence claim.

**Discriminating comparison.** Compare a public schema of required fields, a signed count manifest, the original full record as an oracle diagnostic, and no manifest. Delete records by known random and outcome-dependent mechanisms. Score omission recall, false accusations and unsupported causal conclusions.

**Confounds and boundaries.** A count identifies a gap without identifying its content. Original-record access changes the task and cannot be compared as an equal-information deployed arm. Keep manifest generation independent of treatment outcome.

**Decision if unsupported.** If improvement requires the original answer-bearing record, the deployed completeness rule is unsupported; if counts suffice, avoid expensive semantic verification.

**Why it matters.** Choose the minimum observability contract for the casefile and stopping rule.

**Feasibility.** High readiness with synthetic event logs and deterministic deletions.

## PX-07 Measure independence before intervention and after attrition

Atlas: [SOC-02](https://swarm-research.pages.dev/#/questions?q=SOC-02), [SOC-38](https://swarm-research.pages.dev/#/questions?q=SOC-38), [SOC-01](https://swarm-research.pages.dev/#/questions?q=SOC-01). Projects: [diversity](../project-briefs/diversity.md), [collective-sensing](../project-briefs/collective-sensing.md).

Sources: [[pescetelli-2022-variational]], [[wu-2026-scaling]]. Nearest earlier ideas: VX-20, VX-30 in the [existing bank](../atlas-review/extension-bank.md).

**Question and difference.** Effective-size estimates may change because communication changes decisions or because correlated workers stop responding. Separate those mechanisms and distinguish covariance over task worlds from agreement within a task.

**Discriminating comparison.** Collect explicit private initial and final answers from a fixed roster; introduce independent and difficulty-dependent dropout schedules. Compare complete-case estimates with roster-level error and missingness summaries. Report covariance matrices within prespecified difficulty strata, not just a scalar.

**Confounds and boundaries.** Missing answers are not automatically correct or wrong; report completion and conditional accuracy separately. Do not infer private cognition from hidden reasoning. Equalize evidence unions and total compute.

**Decision if unsupported.** Reject a claimed independence gain if it vanishes when the same roster and task strata are compared, or if completion loss accounts for improved conditional accuracy.

**Why it matters.** Specify a defensible measurement contract for the collaboration with the effective-team-size research line.

**Feasibility.** Analysis on synthetic outcomes first; agent data only after protocol review.

## PX-08 Protect a rare view without rewarding a wrong view

Atlas: [SOC-09](https://swarm-research.pages.dev/#/questions?q=SOC-09), [SOC-10](https://swarm-research.pages.dev/#/questions?q=SOC-10), [SOC-07](https://swarm-research.pages.dev/#/questions?q=SOC-07). Projects: [dissent](../project-briefs/dissent.md), [diversity](../project-briefs/diversity.md), [whistleblowing](../project-briefs/whistleblowing.md).

Sources: [[pescetelli-2022-variational]], [[edmondson-1999-psychological]]. Nearest earlier ideas: VX-04, VX-29 in the [existing bank](../atlas-review/extension-bank.md).

**Question and difference.** Refines evidence-seeking criticism by separating preservation of a minority report from promotion of its conclusion. A group can retain dissent while appropriately rejecting its answer.

**Discriminating comparison.** Cross minority correctness with observation independence and confidence. Compare unconditional minority amplification, an evidence-retention channel and ordinary discussion. Keep messages and verification opportunities equal. Score preserved facts, correct revisions, polarization and final accuracy separately.

**Confounds and boundaries.** A correct minority must not receive more evidence by design. Human psychological safety is only an analogy for incentive structure; no feelings are attributed to agents. Correlation-based support is already prior art.

**Decision if unsupported.** Drop amplification if it increases persistent disagreement without improving decisions; retention can still be useful if it preserves later-verifiable evidence.

**Why it matters.** Choose whether the critic role protects evidence access or presumes the minority is correct.

**Feasibility.** Scripted critics first, then a small paired agent study with held-out difficulty.

## PX-09 Require evidence before compressing examples into a rule

Atlas: [SOC-21](https://swarm-research.pages.dev/#/questions?q=SOC-21), [SOC-31](https://swarm-research.pages.dev/#/questions?q=SOC-31), [SEC-06](https://swarm-research.pages.dev/#/questions?q=SEC-06). Projects: [culture](../project-briefs/culture.md), [memory](../project-briefs/memory.md), [institutions](../project-briefs/institutions.md), [telephone](../project-briefs/telephone.md).

Sources: [[langchain-2026-how]], [[anthropic-2025-effective]]. Nearest earlier ideas: VX-12, VX-16, VX-36 in the [existing bank](../atlas-review/extension-bank.md).

**Question and difference.** A refinement of cultural memory: compaction can turn several local examples into an unjustified universal policy. Factual accuracy of each example does not authorize that generalization.

**Discriminating comparison.** Give agents exception-bearing case histories and a fixed memory limit. Compare example retention, free rule induction and rules stored with scope plus counterexample links. Test unseen cases inside and outside the supported domain, then retract one source case.

**Confounds and boundaries.** Keep capacity and update costs equal. Distinguish syntactic validation from semantic scope and authorized policy change. A held-out counterexample must not leak into rule construction.

**Decision if unsupported.** If scoped rules do not reduce inappropriate generalization or cannot fit within the same memory cap, prefer retaining examples for that task family.

**Why it matters.** Decide whether shared culture should store rules, evidence or both, and what a repair must invalidate.

**Feasibility.** Synthetic policy domain only; no real user preferences or private records required.

## PX-10 Route messages by decision change without rewarding disruption

Atlas: [SOC-04](https://swarm-research.pages.dev/#/questions?q=SOC-04), [SOC-09](https://swarm-research.pages.dev/#/questions?q=SOC-09). Projects: [coordination](../project-briefs/coordination.md), [leadership](../project-briefs/leadership.md), [discovery](../project-briefs/discovery.md).

Sources: [[ma-2021-learning]], [[jiang-2018-learning]], [[wang-2025-beyond]]. Nearest earlier ideas: VX-25, VX-34 in the [existing bank](../atlas-review/extension-bank.md).

**Question and difference.** Decision change is observable but is not the same as decision improvement. Test whether a router trained or tuned to cause changes prefers disruptive low-value messages.

**Discriminating comparison.** Supply helpful, irrelevant and misleading reports with matched lengths. Compare semantic routing, predicted decision-change routing and a verification-gated router. Keep graph degree, delivered fact coverage and router cost controlled. Evaluate accuracy and harmful revisions on a new task family.

**Confounds and boundaries.** The deployed router cannot see the answer key or true marginal utility. Score decision change separately from correctness and account for verification cost.

**Decision if unsupported.** Reject decision-change as a standalone routing objective if it increases reversals without improving held-out correctness over coverage-matched random delivery.

**Why it matters.** Select a routing objective before investing in learned communication weights.

**Feasibility.** Scripted decisions can expose the objective mismatch; a model-based predictor would require a separate training budget.

## PX-11 Separate a reporting receipt from completed remediation

Atlas: [SOC-29](https://swarm-research.pages.dev/#/questions?q=SOC-29), [SOC-30](https://swarm-research.pages.dev/#/questions?q=SOC-30). Projects: [whistleblowing](../project-briefs/whistleblowing.md), [institutions](../project-briefs/institutions.md), [casefile](../project-briefs/casefile.md).

Sources: [[edmondson-1999-psychological]], [[hemmatian-2026-collective]], [[langchain-2026-how]]. Nearest earlier ideas: VX-23, VX-24 in the [existing bank](../atlas-review/extension-bank.md).

**Question and difference.** Extends the report-response card with verifiable state transitions. A visible acknowledgment may increase reporting yet leave the invalid artifact active or an appeal undecided.

**Discriminating comparison.** Compare receipt-only acknowledgment, assigned review and a protocol requiring evidence of disposition before closure. Vary reviewer load and false reports independently. Measure report-to-review and review-to-correction delays, unresolved valid reports and false removals.

**Confounds and boundaries.** Use external artifact validity checks rather than the reviewer marking its own work complete. Charge all review and appeal work to the same cap; protect the option to report uncertain evidence.

**Decision if unsupported.** If structured closure merely changes status labels without improving artifact correctness or response latency, drop it as administrative overhead.

**Why it matters.** Define dashboard statuses that correspond to actual remediation and identify where a governance protocol stalls.

**Feasibility.** Event-state simulation first; human-team psychological mechanisms remain out of scope.

## PX-12 Cross finalization reserves with actual execution headroom

Atlas: [BUD-17](https://swarm-research.pages.dev/#/questions?q=BUD-17), [SOC-32](https://swarm-research.pages.dev/#/questions?q=SOC-32). Projects: [commons](../project-briefs/commons.md), [coordination](../project-briefs/coordination.md), [discovery](../project-briefs/discovery.md).

Sources: [[anthropic-2026-quantifying]], [[wu-2026-scaling]]. Nearest earlier ideas: VX-33, VX-37 in the [existing bank](../atlas-review/extension-bank.md).

**Question and difference.** A reserve can appear valuable because it changes scheduling or because another arm dies at an infrastructure limit. Separate issued token/tool budgets from CPU, RAM and time enforcement.

**Discriminating comparison.** Cross no reserve versus a fixed finalization reserve with fixed infrastructure profiles; randomize run order in blocks. Report verified completions, infrastructure failures and spent resources for every assigned episode. Include a cheap-validator and expensive-validator task stratum.

**Confounds and boundaries.** Do not rerun only one arm after a crash. Record guarantees and kill thresholds separately; calibrate task-specific headroom without adopting a universal multiplier. Match model versions and time blocks.

**Decision if unsupported.** If reserve gains disappear under matched infrastructure and verification cost, treat the original advantage as an execution artifact.

**Why it matters.** Choose a budget policy based on verified completion and explicit opportunity cost rather than conditional success alone.

**Feasibility.** Deterministic accounting and fault injection first; agent execution needs a frozen run manifest.

## PX-13 Abstain from selecting a team when profiling is inconclusive

Atlas: [SOC-38](https://swarm-research.pages.dev/#/questions?q=SOC-38), [SOC-02](https://swarm-research.pages.dev/#/questions?q=SOC-02). Projects: [diversity](../project-briefs/diversity.md), [discovery](../project-briefs/discovery.md), [commons](../project-briefs/commons.md).

Sources: [[gao-2026-distribution]], [[wu-2026-scaling]]. Nearest earlier ideas: VX-22, VX-37 in the [existing bank](../atlas-review/extension-bank.md).

**Question and difference.** Instead of always ranking candidate teams, ask whether refusing an uncertain selection saves profiling budget without sacrificing useful downstream performance.

**Discriminating comparison.** Use independent calibration worlds to choose a fixed team or retain a prespecified default when evidence is weak. Compare always-select, abstaining-select and no-profiling policies on held-out task families; amortize all profiling costs over a declared number of future tasks.

**Confounds and boundaries.** Conformal guarantees do not transfer automatically to adaptive selection or nonexchangeable tasks. Use ordinary held-out error and cost comparisons first, with separate uncertainty for rare task strata.

**Decision if unsupported.** If the default is as good after profiling cost, stop optimizing team selection; if abstention fails after distribution shift, revise the calibration domain.

**Why it matters.** Determine whether team-selection machinery earns its complexity at the expected deployment horizon.

**Feasibility.** Offline outcome simulation is cheap; real profiling can be expensive and needs a prespecified cap.

## PX-14 Separate backup diversity from observation diversity

Atlas: [SOC-22](https://swarm-research.pages.dev/#/questions?q=SOC-22), [SOC-23](https://swarm-research.pages.dev/#/questions?q=SOC-23), [SEC-03](https://swarm-research.pages.dev/#/questions?q=SEC-03). Projects: [memory](../project-briefs/memory.md), [regrowth](../project-briefs/regrowth.md), [collective-sensing](../project-briefs/collective-sensing.md).

Sources: [[yu-2026-multi]], [[pal-2026-context]]. Nearest earlier ideas: VX-07, VX-20 in the [existing bank](../atlas-review/extension-bank.md).

**Question and difference.** Refines common-loss recovery by distinguishing independent storage failure domains from independent evidence origins. Replicas can improve availability while adding zero evidential independence.

**Discriminating comparison.** Cross storage placement (shared or independent failure domains) with source ancestry (copied or independent observations). Fix total stored bytes and observation quality. Compare uniform and rarity-weighted replication on recovery after loss and confidence after retrieval.

**Confounds and boundaries.** Recovered replicas of one observation must count once for truth aggregation. Simulated failure domains must be declared; independent placement does not imply independent corruption risk.

**Decision if unsupported.** Drop any rule that inflates confidence merely because more copies survive; retain replication only for its measured availability benefit.

**Why it matters.** Give the ledger separate fields for reliability of storage and independence of evidence.

**Feasibility.** High readiness with a small deterministic storage simulator and no external services.

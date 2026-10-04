# Thirty heterogeneous-swarm questions

All are exploratory hunches, not registered hypotheses. Scores use the owner’s rubric; reviews are same-author editorial checks. The first five in the sorted ranking are expanded in [DESIGNS.md](DESIGNS.md).

## HX-01 — Reflexes and deliberation: when does a fast controller destabilize the swarm? (91/100)

**Question:** At what ratio of Jev action frequency to Haiku/Qwen planning latency do stale plans cause oscillation or unsafe actions?

**Prediction to test:** Expiry/version checks reduce stale actions most when planner latency exceeds the time over which task state remains valid.

**Comparison:** Cross synchronous versus asynchronous execution with one-to-one versus multi-tick reflex updates. Compare fixed-rate and state-version/expiry-gated Jev actions using the same planner outputs, plus homogeneous and deterministic controllers. Match total memory and add a flat adaptive internal-model controller.

**Falsifier:** Reject the coordination claim if version/expiry checks have no advantage at matched action opportunities, or a simple deterministic gate explains all gains.

**Confounds:** Service latency, action rate, evidence age and model competence must vary separately. Replay isolates scheduling but cannot replace end-to-end model confirmation. Internal memory can explain apparent hierarchy benefits; multirate architectures already exist.

**Delta from prior work:** Fast/slow hierarchy and delay failure are established. Test semantic staleness and version-expiry contracts specifically at the Jev/generative boundary, after controlling for memory and deterministic control.

**Mechanism:** Delayed feedback and separation of control timescales; measure overshoot and settling time rather than claim neural reflex equivalence.

**Visualization:** Animate state, delayed plan packets, action timestamps and overshoot on a shared timeline.

**Decision value:** Choose a safe controller/planner update contract before scaling the mixed swarm.

**Metrics:** Correct tasks by deadline, Stale-plan actions, Oscillation amplitude, Tail latency, Total cost.

**Closest sources:** [[typesafe-2026-introducing]] [[sun-2026-collaboration]] [[yao-2026-hieramas]] [[gh-kuznetsovkarazin-causal-depth-limits]] [[li-2026-deadline]].

**Team crosswalk:** SOC-04, SOC-23; briefs coordination, regrowth, collective-sensing.

**Editorial review:** retain as exploratory comparison. focused extension; novelty unconfirmed. Independent review: not obtained.

## HX-02 — Adaptive division of labor after a capability shock (92/100)

**Question:** Can mixed specialists reassign work after one model loses a tool or becomes unreliable without wasting the swarm budget?

**Prediction to test:** Progress-based reassignment improves post-shock throughput over frozen roles; whether Jev adds value over a deterministic allocator is uncertain.

**Comparison:** On paired task graphs, compare frozen roles, Jev allocation, progress-based response thresholds and a trained-router baseline. Introduce identical capability loss halfway through; compare mixed models to same-model role-specialized agents.

**Falsifier:** Drop the Jev allocation claim if simple progress-based thresholds match it after all profiling and switching costs.

**Confounds:** Hold task mix, legal actions and observation access fixed. Changing roles is not model heterogeneity; preserve a same-model specialist control.

**Delta from prior work:** Adaptive robotics allocation and MasRouter already exist. New target is delayed and misleading progress reports during nonstationary tool/model failure.

**Mechanism:** Response-threshold division of labor with measurable demand, capacity and adaptation rate.

**Visualization:** Color agents by model and tasks by skill; show capacity shock, reassignment and queues.

**Decision value:** Determine whether dynamic specialization pays for itself under realistic capability changes.

**Metrics:** Verified throughput after shock, Reassignment delay, Unfinished dependency chains, Switching cost.

**Closest sources:** [[emam-2020-adaptive]] [[amir-2025-when]] [[yue-2025-masrouter]] [[gh-svitatlco-jev-skill]].

**Team crosswalk:** SOC-04, SOC-23; briefs leadership, coordination, regrowth.

**Editorial review:** retain as exploratory comparison. focused extension; novelty unconfirmed. Independent review: not obtained.

## HX-03 — Model diversity as a firebreak against correlated errors (90/100)

**Question:** Does a minority of independently failing Jev sentinels stop wrong actions spreading, or does shared evidence defeat model diversity?

**Prediction to test:** Any benefit from mixed-model monitoring shrinks when monitors share the same misleading evidence.

**Comparison:** Cross same versus different model monitors with copied versus independent evidence and random versus bridge-node placement. Compare no monitor, deterministic invariant checks and cost-matched extra solver calls; inject bounded false claims in synthetic worlds.

**Falsifier:** Do not claim a diversity firebreak if gains vanish after matching detector accuracy or if all monitors follow the same poisoned source.

**Confounds:** Different vendors are not proof of independence. The intervention is non-destructive synthetic misinformation, with protected truth and equally visible evidence.

**Delta from prior work:** Cowpox and existing immune-response work already study minority defense. Isolate model-error covariance from evidence ancestry and placement.

**Mechanism:** Network epidemic branching with correlated susceptibility; estimate propagation rates from actual event ancestry.

**Visualization:** Show a graph with source ancestry, error spread, blocked edges and false-positive isolation.

**Decision value:** Decide when heterogeneous monitors are worth buying versus better provenance or simple invariants.

**Metrics:** Wrong-action cascade size, Co-failure rate, False quarantine, Useful work retained, Review cost.

**Closest sources:** [[wu-2025-cowpox]] [[teng-2026-which]] [[gh-shapor-jev-sentinel]].

**Team crosswalk:** SOC-01, SEC-03, SEC-06, PX-01, PX-02; briefs diversity, quorum, regrowth.

**Editorial review:** retain as exploratory comparison. focused extension; novelty unconfirmed. Independent review: not obtained.

## HX-04 — The option bottleneck: who gives Jev the right action? (83/100)

**Question:** How much hybrid-system failure comes from excluding the correct action before Jev ever sees it?

**Prediction to test:** Cross-model menu repair can improve end-to-end success only when it increases valid-option coverage enough to pay for its cost.

**Comparison:** Freeze task state and cross candidate-menu source (Qwen, Haiku, deterministic enumerator) with selector (Jev, each generator, random). Remove valid actions or add plausible decoys at prespecified rates; include explicit abstain and request-more-options actions.

**Falsifier:** If conditional Jev performance is strong but menu recall explains failures, stop improving the selector and improve proposals. Reject mixed-model value if the enumerator wins at equal coverage and cost.

**Confounds:** Menu length, wording, ordering, candidate quality and generator identity must not move together. An oracle-complete menu is a diagnostic ceiling only.

**Delta from prior work:** Basic Jev missing-option rejection failure is already reported by Zhong et al. Narrow this to cross-model candidate repair on held-out non-arithmetic tasks, with Boolean verification and development-tuned thresholds as mandatory baselines.

**Mechanism:** Search and selection bottleneck, analogous to variation and selection only where proposal coverage is explicitly measured.

**Visualization:** Animate proposal trees, missing valid actions and selection; keep evaluator-only options in a separate lane.

**Decision value:** Locate whether integration effort belongs in candidate generation, abstention or selection.

**Metrics:** Menu recall, Conditional selection accuracy, End-to-end success, Abstention utility, Menu cost.

**Closest sources:** [[typesafe-2026-systemone]] [[gh-svitatlco-jev-skill]] [[jiang-2023-llm]] [[li-2025-rethinking]] [[zhong-2026-when]].

**Team crosswalk:** SOC-09, SOC-38; briefs discovery, diversity, coordination.

**Editorial review:** demote from shortlist; merge with HX-30 as a repair extension. direct prior result for core premise; replication/control, narrower extension only. Independent review: not obtained.

## HX-05 — A reserve of diverse specialists for recovery (88/100)

**Question:** Can a small dormant reserve restore capabilities after a model-family outage better than spending everything on active workers?

**Prediction to test:** Diverse reserves reduce service deficit preferentially under model-family-correlated failures, while reducing clean-world active capacity.

**Comparison:** Allocate the same total resource cap between active workers and cold reserves. Compare homogeneous, mixed and role-diverse reserves under family-correlated versus independent outages, including deterministic fallback and equal-cost warm spares.

**Falsifier:** Reject reserve diversity if it loses to simple redundancy once clean-world opportunity cost and checkpoint loading are charged.

**Confounds:** Reserve agents receive only preserved permissible state. Match damage exposure, failure domains, qualification and idle resource accounting.

**Delta from prior work:** Extends existing regrowth and Theseus work with model-family correlated loss and replacement competence; reserve redundancy itself is established.

**Mechanism:** Functional redundancy and response diversity; measure capability coverage and recovery rather than merely restored node count.

**Visualization:** Show capability layers fading under correlated outage and reappearing as reserves wake.

**Decision value:** Choose whether operational resilience warrants idle diverse capacity.

**Metrics:** Service deficit over time, Time to restore task coverage, Cold-start cost, Clean-world throughput, Recovery correctness.

**Closest sources:** [[emam-2020-adaptive]] [[teng-2026-which]] [[yao-2026-hieramas]].

**Team crosswalk:** SOC-22, SOC-23, PX-04, PX-03; briefs regrowth, memory, diversity.

**Editorial review:** retain as exploratory comparison. focused extension; novelty unconfirmed. Independent review: not obtained.

## HX-06 — Calibration under changing partners (82/100)

**Question:** Does a Jev confidence threshold remain reliable after teammate composition changes?

**Prediction to test:** Frozen confidence thresholds become less reliable under partner shifts than independently recalibrated thresholds.

**Comparison:** Fit thresholds on fixed teams, then swap generators and evidence sources; compare frozen, held-out recalibrated and conformal escalation policies at matched escalation budgets.

**Falsifier:** Drop universal-threshold use if conditional error exceeds its predeclared tolerance after swaps.

**Confounds:** Threshold selection must not see test labels; marginal conformal coverage is not conditional safety.

**Delta from prior work:** Conformal Social Choice already tests Haiku/Qwen teams; partner-induced feedback shift is the extension.

**Mechanism:** Selective prediction under distribution shift, not biological calibration.

**Visualization:** Reliability curves by partner and a changing abstention boundary.

**Decision value:** Determine when to recalibrate escalation thresholds.

**Metrics:** Brier score, Risk-coverage curve, Error among acted cases, Recalibration cost.

**Closest sources:** [[wang-2026-debate]] [[chen-2023-reconcile]] [[typesafe-2026-introducing]].

**Team crosswalk:** SOC-08, SOC-38; briefs quorum, diversity, institutions.

**Editorial review:** retain as exploratory comparison. focused extension; novelty unconfirmed. Independent review: not obtained.

## HX-07 — Does mixed-model conversation erase measured complementarity? (83/100)

**Question:** Do models selected for independent error diversity become correlated after sharing memory?

**Prediction to test:** Communication increases co-failure for at least some teams selected for independent complementarity.

**Comparison:** Profile without discussion, then cross selected versus quality-only teams with private versus shared memories and controlled discussion dose.

**Falsifier:** Reject static profiling if rankings invert after interaction on held-out worlds.

**Confounds:** Teng already includes held-out shift; novelty must be interaction-induced changes, not merely a new split.

**Delta from prior work:** Extends C2-MAS from pre-interaction choice profiles to evolving shared-state teams.

**Mechanism:** Coupled-agent dynamics and loss of independence.

**Visualization:** Covariance matrix alongside opinion trajectories.

**Decision value:** Choose whether team selection must profile communication too.

**Metrics:** Accuracy, Error covariance over rounds, Correct-to-wrong revisions, Communication cost.

**Closest sources:** [[teng-2026-which]] [[chen-2026-diversity]] [[sun-2026-collaboration]].

**Team crosswalk:** SOC-01, SOC-38; briefs diversity, memory, dissent.

**Editorial review:** retain as exploratory comparison. focused extension; novelty unconfirmed. Independent review: not obtained.

## HX-08 — Translation contracts between decision and language agents (76/100)

**Question:** Do typed summaries improve cross-model understanding, or remove decisive information?

**Prediction to test:** Typed records reduce composition errors only if decisive qualifiers survive the representation change.

**Comparison:** Compare prose and typed state with identical facts; selectively remove qualifiers or provenance; cross generator and receiver models.

**Falsifier:** Reject typed superiority if gains disappear with equally explicit prose.

**Confounds:** Schema validity and semantic fidelity are distinct; do not reveal truth in fields.

**Delta from prior work:** Strong-weak mismatch and existing schema-composition questions precede this; focus on the Jev/SLM boundary.

**Mechanism:** Information bottleneck with measurable sufficient statistics.

**Visualization:** Trace facts and qualifiers through adapter transformations.

**Decision value:** Specify the smallest state representation that preserves decisions.

**Metrics:** Contract violations, Retained evidence, Task accuracy, Encoding cost.

**Closest sources:** [[wang-2026-guided]] [[typesafe-2026-systemone]] [[shen-2024-small]].

**Team crosswalk:** SOC-31, SOC-32, EX-01; briefs telephone, coordination, memory.

**Editorial review:** retain as exploratory comparison. focused extension; novelty unconfirmed. Independent review: not obtained.

## HX-09 — Who pays the cost of saying no? (85/100)

**Question:** Can asymmetric verifier and proposer budgets cause escalation queues to collapse?

**Prediction to test:** Backpressure reduces rejection/retry amplification near capacity and increases verified deadline completions.

**Comparison:** Vary arrival rate and verifier allocation with fixed total spend; compare first-in-first-out, risk-priority and reserved verification capacity.

**Falsifier:** Drop a policy if throughput gains rely on silently skipping verification.

**Confounds:** Count all rejected work and retries; service time differs from model reasoning quality.

**Delta from prior work:** Routing cost is established; binding queue stability at the decision gate is the target. Deadline-aware resource scheduling already exists; specialize the comparison to endogenously generated proposals and verifier false positives.

**Mechanism:** Queue stability and backpressure.

**Visualization:** Animate proposal queues, verifier service and overload transitions.

**Decision value:** Reserve the right amount of verification capacity.

**Metrics:** Queue delay, Verified completions, Unreviewed actions, Dropped tasks.

**Closest sources:** [[ong-2024-routellm]] [[yue-2025-masrouter]] [[gh-shapor-jev-sentinel]] [[li-2026-deadline]].

**Team crosswalk:** BUD-17, SOC-04; briefs commons, coordination, institutions.

**Editorial review:** retain as exploratory comparison. focused extension; novelty unconfirmed. Independent review: not obtained.

## HX-10 — Placement versus abundance of rare specialists (82/100)

**Question:** Are a few Jev nodes more valuable at network bridges than spread uniformly?

**Prediction to test:** Specialist placement changes containment only when it changes access to the relevant transmission paths.

**Comparison:** Randomize sentinel count and degree-matched placement on fixed graphs; include no-communication and extra homogeneous node controls.

**Falsifier:** Reject a placement story if degree-matched random assignment performs equally.

**Confounds:** Central nodes receive more evidence; equalize visibility or explicitly estimate that mediator.

**Delta from prior work:** Minority defense and topology optimization already exist; count-by-placement interaction needs a narrow endpoint.

**Mechanism:** Network controllability and intervention coverage.

**Visualization:** Move fixed-count specialists over the graph and replay paired cascades.

**Decision value:** Allocate scarce specialist seats by demonstrated marginal value.

**Metrics:** Accuracy, Cascade size, Communication distance, Marginal benefit per specialist.

**Closest sources:** [[wu-2025-cowpox]] [[yao-2026-hieramas]].

**Team crosswalk:** SOC-04, SEC-03; briefs diversity, collective-sensing, quorum.

**Editorial review:** retain as exploratory comparison. focused extension; novelty unconfirmed. Independent review: not obtained.

## HX-11 — Reward design manufactures the diversity advantage (82/100)

**Question:** Does a heterogeneous team win only because the evaluator rewards complementary specialist outputs?

**Prediction to test:** An apparent heterogeneity advantage changes with the evaluator’s reward aggregation rule.

**Comparison:** Compare additive, bottleneck and coverage rewards on the same underlying task outcomes; keep the policy-training and test worlds separate.

**Falsifier:** Drop a universal diversity claim if it reverses under reasonable alternative objectives.

**Confounds:** Do not select the reward after seeing which arm wins; report task outcomes before aggregation.

**Delta from prior work:** Curvature-based heterogeneity gain is already studied; transfer to typed and generative agents is a replication/extension.

**Mechanism:** Reward curvature and division of labor.

**Visualization:** Animate allocations with side-by-side reward aggregators.

**Decision value:** Avoid building a benchmark that mechanically favors a mixed team.

**Metrics:** Per-task success, Worst-task success, Reward sensitivity, Effort allocation.

**Closest sources:** [[amir-2025-when]] [[emam-2020-adaptive]].

**Team crosswalk:** SOC-01, SOC-38; briefs diversity, commons, coordination.

**Editorial review:** retain as exploratory comparison. focused extension; novelty unconfirmed. Independent review: not obtained.

## HX-12 — Role diversity without model diversity (74/100)

**Question:** Can one small model with separate tools and roles match a mixed-vendor team?

**Prediction to test:** Same-model agents with different tools or evidence can recover some benefits attributed to model diversity.

**Comparison:** Factor model identity, prompt role and tool access separately under identical total evidence and resource limits.

**Falsifier:** Drop model mixing if role/tool specialization explains all benefit.

**Confounds:** Homogeneous does not mean identical observations or actions.

**Delta from prior work:** Direct prerequisite control, not an original heterogeneity result.

**Mechanism:** Functional versus structural diversity.

**Visualization:** Capability matrix and role occupancy.

**Decision value:** Identify the cheapest source of useful specialization.

**Metrics:** Verified success, Cost, Error covariance, Role coverage.

**Closest sources:** [[shen-2024-small]] [[amir-2025-when]] [[li-2025-rethinking]].

**Team crosswalk:** SOC-01, SOC-38; briefs diversity, coordination.

**Editorial review:** baseline, replication or merge candidate; do not pitch as new. substantial established or team overlap; retained as useful control/replication. Independent review: not obtained.

## HX-13 — Make the sentinel blind to proposer prestige (79/100)

**Question:** Does Jev favor a fluent or high-status proposer even when the evidence is unchanged?

**Prediction to test:** Randomized prestige labels may change selector preferences even when evidence is held fixed; a null effect is plausible.

**Comparison:** Randomize hidden, correct and swapped model labels while holding proposal content fixed; cross confident prose and terse typed claims.

**Falsifier:** Reject prestige effects if randomized labels leave decisions unchanged within the precision target.

**Confounds:** Identity labels can carry real prior quality; use deliberately randomized labels for the causal test.

**Delta from prior work:** Authority-driven collapse is known; test typed selectors rather than claim new social bias.

**Mechanism:** Information cascades and status-weighted influence.

**Visualization:** Replay identical evidence under changing labels.

**Decision value:** Decide whether model identity belongs in selector inputs.

**Metrics:** Selection accuracy, Label effect, Correct minority retention.

**Closest sources:** [[chen-2026-diversity]] [[jiang-2023-llm]].

**Team crosswalk:** SOC-07, SOC-10; briefs dissent, diversity, leadership.

**Editorial review:** retain as exploratory comparison. focused extension; novelty unconfirmed. Independent review: not obtained.

## HX-14 — Can cheap dissent rescue a stronger planner? (75/100)

**Question:** When is an independent Qwen critic more useful than another Haiku sample?

**Prediction to test:** Independent evidence-seeking critics outperform generic opposition only when their extra information survives integration.

**Comparison:** Compare independent evidence-seeking critique, generic opposition and equal-cost extra solver samples with blinded proposer/critic roles.

**Falsifier:** Reject critics if extra solver samples or deterministic tests provide equal value.

**Confounds:** Critic information and compute must be matched; disagreement alone is not quality.

**Delta from prior work:** ReConcile and existing dissent questions already cover much of this; target capability asymmetry.

**Mechanism:** Independent minority information versus conformism.

**Visualization:** Show correct and harmful reversals by critic type.

**Decision value:** Choose a critic only when its independent contribution is demonstrated.

**Metrics:** Verified corrections, Harmful reversals, Extra evidence acquired, Cost.

**Closest sources:** [[chen-2023-reconcile]] [[li-2025-rethinking]] [[wang-2026-guided]].

**Team crosswalk:** SOC-09, SOC-10; briefs dissent, diversity, discovery.

**Editorial review:** baseline, replication or merge candidate; do not pitch as new. substantial established or team overlap; retained as useful control/replication. Independent review: not obtained.

## HX-15 — Confidence contagion through typed probabilities (78/100)

**Question:** Can repeated probability outputs make peers more certain without new evidence?

**Prediction to test:** Naive probability pooling becomes overconfident as copied evidence is repeatedly transmitted.

**Comparison:** Replay one uncertain observation through Jev and LLM chains; compare naive pooling, ancestry deduplication and calibrated pooling.

**Falsifier:** Reject a new mechanism if provenance deduplication fully removes the effect.

**Confounds:** Probabilities are not independent samples; ensure source ancestry is identical across arms.

**Delta from prior work:** Extends existing quorum work to numeric probability transmission; confidence aggregation is established.

**Mechanism:** Bayesian double-counting and correlated evidence.

**Visualization:** Track one source splitting into many numerical endorsements.

**Decision value:** Keep evidence ancestry alongside confidence.

**Metrics:** Calibration drift, Duplicate evidence weight, False commitment.

**Closest sources:** [[wang-2026-debate]] [[chen-2023-reconcile]] [[typesafe-2026-systemone]].

**Team crosswalk:** SOC-08, SEC-03, PX-01; briefs quorum, telephone, collective-sensing.

**Editorial review:** baseline, replication or merge candidate; do not pitch as new. substantial established or team overlap; retained as useful control/replication. Independent review: not obtained.

## HX-16 — A swarm immune response can destroy useful diversity (81/100)

**Question:** Do heterogeneous monitors quarantine correct rare specialists along with errors?

**Prediction to test:** Broad quarantine removes more useful rare evidence than evidence-specific correction at comparable error suppression.

**Comparison:** Mix rare-but-correct evidence with plausible false claims; compare local quarantine, global overwrite and evidence-specific correction at matched review rates.

**Falsifier:** Reject safety gains that erase correct minority knowledge or hide abstained cases.

**Confounds:** Inject difficulty independently from rarity; do not equate unusual wording with maliciousness.

**Delta from prior work:** Cowpox and our immune-response design already raise this; isolate model-specific false positives.

**Mechanism:** Defense-diversity tradeoff and selective suppression.

**Visualization:** Overlay useful and harmful claim lineages during repair.

**Decision value:** Choose correction granularity without homogenizing the swarm.

**Metrics:** Error removal, Rare knowledge retained, Recovery, False quarantine.

**Closest sources:** [[wu-2025-cowpox]] [[chen-2026-diversity]] [[gh-shapor-jev-sentinel]].

**Team crosswalk:** SEC-06, SOC-10; briefs regrowth, dissent, diversity.

**Editorial review:** retain as exploratory comparison. focused extension; novelty unconfirmed. Independent review: not obtained.

## HX-17 — Graceful behavior when Jev is unavailable (77/100)

**Question:** Can a mixed swarm degrade safely when its shared selector fails?

**Prediction to test:** Bounded fallback reduces service loss relative to unbounded retries but may sacrifice decision quality.

**Comparison:** Inject selector timeout and inconsistent replies; compare retry, deterministic fallback, cached decisions with expiry and alternate model selection.

**Falsifier:** Reject fallback if it only hides failures by waiting beyond the deadline.

**Confounds:** No cached action without matching state version; endpoint outages differ from wrong answers.

**Delta from prior work:** Reliability engineering replication tailored to a shared Jev dependency.

**Mechanism:** Single points of failure and redundant control.

**Visualization:** Visualize dependency outage and fallback paths.

**Decision value:** Avoid making the selector the whole swarm’s failure domain.

**Metrics:** Task loss, Invalid actions, Recovery time, Retry cost.

**Closest sources:** [[gh-svitatlco-jev-skill]] [[typesafe-2026-systemone]].

**Team crosswalk:** SOC-23, SOC-32; briefs regrowth, coordination.

**Editorial review:** baseline, replication or merge candidate; do not pitch as new. substantial established or team overlap; retained as useful control/replication. Independent review: not obtained.

## HX-18 — Cross-model memory transplant (77/100)

**Question:** Can a replacement model use another family’s compact memory without semantic drift?

**Prediction to test:** Typed handoff records preserve executable constraints better than equally short free summaries when formats differ.

**Comparison:** Freeze handoff states and compare verbatim, typed and recipient-specific summaries under matched memory bytes and evidence access.

**Falsifier:** Reject transplant if restarting from original evidence is cheaper and equally accurate.

**Confounds:** Recipient context window, truncation and tool permissions require separate controls.

**Delta from prior work:** Extends existing Theseus/memory work at a model-family boundary.

**Mechanism:** State transfer and functional continuity.

**Visualization:** Display preserved constraints and drift after each replacement.

**Decision value:** Specify portable memory fields before hot-swapping models.

**Metrics:** Post-handoff success, Constraint loss, False memory adoption, Transfer cost.

**Closest sources:** [[yao-2026-hieramas]] [[wang-2026-guided]].

**Team crosswalk:** SOC-21, SOC-23, PX-03; briefs memory, regrowth, culture.

**Editorial review:** retain as exploratory comparison. focused extension; novelty unconfirmed. Independent review: not obtained.

## HX-19 — Distillation can erase the diversity we wanted (82/100)

**Question:** Does teaching Qwen from Jev decisions reduce independent error coverage?

**Prediction to test:** Distillation can improve individual accuracy while increasing teacher-student co-failure.

**Comparison:** Compare base and decision-distilled Qwen at matched individual accuracy where feasible; measure pairwise failures on unseen task families.

**Falsifier:** Reject a diversity claim if improvements are wholly explained by individual accuracy.

**Confounds:** Teacher contamination, shared training data and unequal fine-tuning compute must be reported.

**Delta from prior work:** AutoJev supplies a practical precedent; independence after distillation is the narrower question.

**Mechanism:** Convergence under shared learning versus response diversity.

**Visualization:** Before/after error-overlap maps.

**Decision value:** Choose whether distilled replicas are useful backups or correlated copies.

**Metrics:** Accuracy, Co-failure, Calibration, Team uplift.

**Closest sources:** [[gh-denis-pplx-autojev]] [[teng-2026-which]].

**Team crosswalk:** SOC-01, SOC-38; briefs diversity, culture.

**Editorial review:** retain as exploratory comparison. focused extension; novelty unconfirmed. Independent review: not obtained.

## HX-20 — Batched Jev calls create a shared failure domain (83/100)

**Question:** Does sharing state across many typed questions couple otherwise separate agents?

**Prediction to test:** Batching can alter outputs when shared state or question interactions create common-mode sensitivity; no effect is also plausible.

**Comparison:** Compare one batched call and per-agent calls with identical permitted state; perturb irrelevant neighbor fields and question order.

**Falsifier:** Reject batch coupling if outputs remain stable and failures independent under prespecified perturbations.

**Confounds:** Batched state can expose extra evidence; equalize information before attributing an API effect.

**Delta from prior work:** Batching is documented; downstream correlation is not established by speed claims.

**Mechanism:** Common-mode failure from shared substrate.

**Visualization:** One request fan-out with correlated decision changes.

**Decision value:** Decide when batching savings warrant shared-state exposure.

**Metrics:** Decision invariance, Co-failure, Cost, Latency.

**Closest sources:** [[typesafe-2026-systemone]] [[teng-2026-which]].

**Team crosswalk:** SOC-01, SOC-02; briefs diversity, coordination, collective-sensing.

**Editorial review:** retain as exploratory comparison. focused extension; novelty unconfirmed. Independent review: not obtained.

## HX-21 — Energy-aware local/cloud swarms (80/100)

**Question:** Do local Qwen workers remain preferable when energy, queue contention and cloud latency are counted?

**Prediction to test:** Local/cloud rankings change when hardware contention and measured energy are added to inference price.

**Comparison:** Measure the same task contracts on local/cloud mixes under fixed deadlines; report actual energy only with suitable instrumentation.

**Falsifier:** Drop energy claims without measured joules and hardware utilization.

**Confounds:** Tokens across providers are not a common compute unit; shared hardware and cold starts matter.

**Delta from prior work:** Existing cost routing is close; energy and contention require real measurement.

**Mechanism:** Resource-constrained allocation, with energy as measured physical quantity.

**Visualization:** Power and queue traces aligned with verified completions.

**Decision value:** Choose deployment mixes using full system costs.

**Metrics:** Quality-cost frontier, Energy per success, Tail latency, Failure rate.

**Closest sources:** [[ong-2024-routellm]] [[gh-svitatlco-jev-skill]].

**Team crosswalk:** BUD-17, SOC-04; briefs commons, coordination.

**Editorial review:** retain as exploratory comparison. focused extension; novelty unconfirmed. Independent review: not obtained.

## HX-22 — Tool access creates specialists more reliably than prompts (77/100)

**Question:** Does genuine capability partitioning outperform simply telling identical agents to specialize?

**Prediction to test:** Tool partitioning explains some apparent gains from specialist prompts or mixed model identities.

**Comparison:** Factor model family, tool permissions and specialization prompts with identical total available tools.

**Falsifier:** Reject prompt-specialist explanations if permission partitions account for gains.

**Confounds:** A forbidden action is not inability; allow explicit delegation in every arm.

**Delta from prior work:** Modular tool agents and robot capability allocation already exist.

**Mechanism:** Morphological versus behavioral specialization as a carefully bounded analogy.

**Visualization:** Tool-capability bipartite graph over execution.

**Decision value:** Separate capability engineering from model branding.

**Metrics:** Success, Capability coverage, Delegation errors, Coordination cost.

**Closest sources:** [[shen-2024-small]] [[emam-2020-adaptive]].

**Team crosswalk:** SOC-01, SOC-04; briefs diversity, coordination.

**Editorial review:** baseline, replication or merge candidate; do not pitch as new. substantial established or team overlap; retained as useful control/replication. Independent review: not obtained.

## HX-23 — Private deliberation before shared decisions (73/100)

**Question:** Does protecting cheap agents’ first judgments preserve useful independent evidence?

**Prediction to test:** Private initial judgments preserve more independent information but can also preserve wrong anchors.

**Comparison:** Compare immediate broadcast, private-then-share and no discussion for mixed and same-model teams.

**Falsifier:** Drop privacy intervention if it merely preserves incorrect anchoring.

**Confounds:** Equalize total calls and evidence; record beneficial and harmful revisions.

**Delta from prior work:** Already central to existing SOC-07 work; heterogeneous replication only.

**Mechanism:** Information cascades and social coupling.

**Visualization:** Opinion traces before and after the first public signal.

**Decision value:** Test whether mixing models adds anything beyond private judgments.

**Metrics:** Correct minority retention, Final success, Discussion cost.

**Closest sources:** [[chen-2026-diversity]] [[chen-2023-reconcile]].

**Team crosswalk:** SOC-07, SOC-10; briefs dissent, collective-sensing.

**Editorial review:** baseline, replication or merge candidate; do not pitch as new. substantial established or team overlap; retained as useful control/replication. Independent review: not obtained.

## HX-24 — Hybrid markets and strategic reports (76/100)

**Question:** Can agents manipulate a Jev allocator by overstating difficulty or underreporting cost?

**Prediction to test:** Allocation based only on advertised competence is more vulnerable to overclaims than measured-progress allocation.

**Comparison:** Use synthetic task auctions with fixed ground truth and bounded messages; compare self-reported bids, measured-progress allocation and audited bids.

**Falsifier:** Reject market benefits if a simple scheduler matches them without bid manipulation.

**Confounds:** Do not infer intention from a mistaken bid; manipulate reporting incentives separately.

**Delta from prior work:** Agent markets and CoffeeBench already study economic interaction; focus on allocator evidence. Mittal already frames capability advertising as a lemons market; evaluate its remedies rather than rename the problem.

**Mechanism:** Mechanism design under asymmetric information, not biological cooperation proof.

**Visualization:** Resource flows and reported versus realized task costs.

**Decision value:** Decide whether self-reported competence should influence allocation.

**Metrics:** Allocation regret, Budget loss, Truthful report rate, Audit cost.

**Closest sources:** [[sakana-2026-coffeebench]] [[yue-2025-masrouter]] [[mittal-2026-capability]].

**Team crosswalk:** BUD-17, SOC-04; briefs commons, institutions, leadership.

**Editorial review:** retain as exploratory comparison. focused extension; novelty unconfirmed. Independent review: not obtained.

## HX-25 — Long-horizon drift in heterogeneous contracts (75/100)

**Question:** Do model-specific summaries gradually change a shared task contract?

**Prediction to test:** Immutable external contracts reduce constraint drift across both mixed and same-model handoff chains.

**Comparison:** Alternate model families across handoffs; compare immutable machine-checkable contracts, natural-language reminders and no reminders.

**Falsifier:** Reject heterogeneity-specific drift if same-model chains fail identically.

**Confounds:** Match compression lengths and context ages; immutable checks are an engineered intervention.

**Delta from prior work:** Existing telephone and memory designs are closest; isolate the cross-family boundary.

**Mechanism:** Transmission fidelity and cumulative information loss.

**Visualization:** Contract fields fading or mutating at each hop.

**Decision value:** Define which constraints must remain outside generated summaries.

**Metrics:** Constraint survival, Invalid commitments, Drift per hop.

**Closest sources:** [[sun-2026-collaboration]] [[wang-2026-guided]].

**Team crosswalk:** SOC-31, SOC-21; briefs telephone, memory, culture.

**Editorial review:** baseline, replication or merge candidate; do not pitch as new. substantial established or team overlap; retained as useful control/replication. Independent review: not obtained.

## HX-26 — The diversity sweet spot under a hard budget (76/100)

**Question:** What mixture size maximizes verified success once profiling and coordination are paid for?

**Prediction to test:** Mixed-model gains exhibit diminishing returns under a fixed budget and need not beat repeated samples from the best model.

**Comparison:** Sweep small team size and model composition; include single best model, repeated samples and no-communication ensembles on held-out worlds.

**Falsifier:** Reject universal optimum claims if ranking changes across task families.

**Confounds:** Fix dollar cap and deadline separately; API prices and tokenizers differ.

**Delta from prior work:** MoA, Self-MoA and C2-MAS already address much of this; use as a necessary baseline sweep.

**Mechanism:** Marginal returns and resource competition.

**Visualization:** Quality-cost frontier with coordination overhead bands.

**Decision value:** Establish a useful baseline before mechanism experiments.

**Metrics:** Success per budget, Tail risk, Coordination fraction.

**Closest sources:** [[wang-2024-mixture]] [[li-2025-rethinking]] [[teng-2026-which]].

**Team crosswalk:** SOC-02, SOC-38; briefs diversity, commons, coordination.

**Editorial review:** baseline, replication or merge candidate; do not pitch as new. substantial established or team overlap; retained as useful control/replication. Independent review: not obtained.

## HX-27 — Independent judges for a heterogeneous swarm (70/100)

**Question:** Can the apparent winning team change when the judge model changes?

**Prediction to test:** Some team rankings change with the judge; executable ground truth can reveal evaluator affinity.

**Comparison:** Score blinded outputs with executable truth, Jev, each generator family and calibrated human audits on a fixed subset.

**Falsifier:** Reject a result whose advantage exists only with a related-family judge.

**Confounds:** Judges must not see model labels; verbosity and answer order need randomization.

**Delta from prior work:** Measurement control rather than a new swarm mechanism.

**Mechanism:** Measurement invariance.

**Visualization:** Judge disagreement heatmap anchored to protected truth.

**Decision value:** Prevent evaluator affinity from becoming a fake heterogeneity result.

**Metrics:** Rank reversals, False acceptance, Judge agreement, Cost.

**Closest sources:** [[jiang-2023-llm]] [[typesafe-2026-introducing]].

**Team crosswalk:** SOC-32, SOC-38; briefs casefile, discovery.

**Editorial review:** baseline, replication or merge candidate; do not pitch as new. substantial established or team overlap; retained as useful control/replication. Independent review: not obtained.

## HX-28 — When to replace conversation with deterministic code (70/100)

**Question:** Which coordination failures disappear when arithmetic and invariants leave the agents?

**Prediction to test:** Replacing exact bookkeeping with code removes failures without requiring model diversity.

**Comparison:** Hold model composition fixed and replace one coordination step at a time with an exact solver or state machine.

**Falsifier:** Drop model-mixing claims if deterministic coordination explains all benefit.

**Confounds:** An exact task solver is a ceiling; distinguish generic invariant checks from answering the task.

**Delta from prior work:** Established engineering principle; strongest practical falsification control.

**Mechanism:** Mechanistic decomposition rather than an ecological analogy.

**Visualization:** Replay the same trace with one stage made exact.

**Decision value:** Spend model inference only where it adds measurable value.

**Metrics:** Success, Calls removed, Failure localization, Cost.

**Closest sources:** [[typesafe-2026-introducing]] [[gh-svitatlco-jev-skill]].

**Team crosswalk:** SOC-04, SOC-32; briefs coordination, discovery.

**Editorial review:** baseline, replication or merge candidate; do not pitch as new. substantial established or team overlap; retained as useful control/replication. Independent review: not obtained.

## HX-29 — Heterogeneous teaching without permanent central authority (81/100)

**Question:** Can temporary specialist guidance improve weak agents without creating a permanent leader dependency?

**Prediction to test:** Request-triggered guidance improves independence only when useful state persists after teacher removal.

**Comparison:** Compare fixed teacher, rotating teacher and request-triggered guidance at equal messages; remove the teacher mid-run.

**Falsifier:** Reject distributed learning if competence vanishes when the teacher is absent.

**Confounds:** Separate retained facts from improved skills; no claim of weight learning without updates.

**Delta from prior work:** Guided collaboration already exists; persistence after mentor removal is the extension.

**Mechanism:** Temporary scaffolding and dependency formation.

**Visualization:** Guidance edges fade as learners operate independently.

**Decision value:** Decide whether guidance builds capacity or just hides a bottleneck.

**Metrics:** Independent completion, Recovery after teacher loss, Guidance cost.

**Closest sources:** [[wang-2026-guided]] [[chen-2026-diversity]].

**Team crosswalk:** SOC-23, SOC-07; briefs leadership, culture, regrowth.

**Editorial review:** retain as exploratory comparison. focused extension; novelty unconfirmed. Independent review: not obtained.

## HX-30 — Can a fixed decision vocabulary adapt to genuinely new tasks? (81/100)

**Question:** What happens when task novelty requires an action outside Jev’s existing menu?

**Prediction to test:** Controlled option expansion can improve novel-task coverage, but validating new options introduces a second bottleneck.

**Comparison:** Introduce held-out task types; compare fixed menu, request-new-option, periodic schema revision and free generation with validation.

**Falsifier:** Reject adaptability if new menus only work because the evaluator supplies the answer.

**Confounds:** Keep novel tasks distinct from harder familiar tasks; validate generated actions in a bounded sandbox.

**Delta from prior work:** Typed decisions and generators are already combined; test open-set transition and safe menu growth.

**Mechanism:** Adaptation constrained by available variation.

**Visualization:** New task demands appear outside the current action graph.

**Decision value:** Define an escape hatch from an incomplete action vocabulary.

**Metrics:** Novel-task completion, Invalid new options, Schema revision cost, Recovery delay.

**Closest sources:** [[typesafe-2026-systemone]] [[gh-denis-pplx-autojev]] [[gh-svitatlco-jev-skill]] [[zhong-2026-when]].

**Team crosswalk:** SOC-09, SOC-23, HX-04; briefs discovery, regrowth, diversity.

**Editorial review:** merge with HX-04. overlaps HX-04 and known missing-option rejection; merge before promotion. Independent review: not obtained.

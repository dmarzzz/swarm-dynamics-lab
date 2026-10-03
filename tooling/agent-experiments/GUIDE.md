# Designing, implementing and evaluating experiments with AI agents

Research date: 2026-10-03. Companion documents: [evidence and citations](LITERATURE.md), [harness engineering](HARNESS.md), [protocol template](templates/protocol.md), [checklists](CHECKLISTS.md).

## 1. Decide what claim the experiment can establish

An agent can be a research assistant, the experimental subject, or a simulator of another system. These roles require different validation.

| Role | Example question | Evidence needed |
| --- | --- | --- |
| Agent as instrument | Does an agent help discover better catalysts? | Independent chemical validation, novel candidate accounting, comparable human or algorithmic search budgets, all failed attempts |
| Agent as subject | Does provenance-aware communication reduce errors in an LLM swarm? | Randomized intervention on isolated swarms, objective outcomes, repeated scenarios and runs |
| Agent as simulator | Does an LLM population predict human cooperation? | Human data relevant to that population and intervention, calibration separated from validation, held-out prediction and uncertainty |
| Agent as experiment builder | Can an agent reproduce a published method? | Executed artifacts, environment reconstruction, protected task-specific rubric, independent reproduction checks |

Do not infer human psychology from a plausible conversation. Do not infer scientific novelty from a high benchmark score or a paper-shaped output. For discovery, separate generation, validation, novelty assessment and independent replication. AI Scientist and Co-Scientist demonstrate different degrees of automation; PaperBench tests reconstruction; none makes all four interchangeable. [Lu et al.](https://arxiv.org/abs/2408.06292) [[lu-2024-ai]], [Gottweis et al.](https://arxiv.org/abs/2502.18864v2) [[gottweis-2025-accelerating]], [Starace et al.](https://arxiv.org/abs/2504.01848) [[starace-2025-paperbench]].

Write a one-sentence estimand: “The mean change in [outcome] caused by [treatment] versus [control], for [population of tasks and systems], under [resource and observation limits], counting [failures] as [specified outcome].” Identify whether the target is this fixed benchmark, a sampled task population, future model deployments, or human behavior. This choice determines the denominator, sampling and uncertainty.

## 2. Vocabulary that prevents false replication

| Term | Operational definition |
| --- | --- |
| Agent | A decision-making software entity with an observation interface, policy, permitted actions, and state lifecycle. An LLM call can be one policy step; several calls need not imply several agents. |
| Immutable agent configuration | A versioned, content-addressed specification of model, prompts, tools, memory rules, permissions, decoding and policy. Its definition remains fixed during a confirmatory study. Runtime messages and memory can evolve according to the fixed rules. |
| Agent instance | One instantiated identity and mutable state, derived from an immutable definition. Two personas on one shared model are not independent training histories. |
| Task / scenario | The problem specification and environment instance, including initial hidden truth, observations, constraints, disturbances and scoring rule. A scenario family groups related instances. |
| Episode / run | One execution from a defined reset to a terminal condition. This guide uses these synonymously; separately label model training runs if training is involved. |
| Treatment | The prespecified intervention or system variant. A prompt, model, topology or memory change is a treatment, not an incidental implementation detail. |
| Experimental unit | The smallest entity independently assigned a treatment without interference across units. For communicating agents it is usually the whole swarm/world episode. |
| Observation | A measurement within a unit: message, tool call, agent vote, round or scored question. Observations are not automatically independent units. |
| Independent replicate | A separately initialized execution with no cross-run mutable state or uncontrolled communication, independently generated randomness conditional on its block. Pairing intentionally shares selected exogenous inputs across treatments; the pair is independent of other pairs only under the design assumptions. |
| Attempt | One request or execution attempt inside a run. A retry is not a new independent replicate. |
| Reproduction / replication | Here, reproduction recomputes results from the same artifacts; replication collects fresh executions or data to test the claim. Terminology differs across fields; declare yours. |

A hundred agents in one shared world are generally one swarm replicate, not n=100. Ten thousand turns from three worlds do not yield ten thousand independent tests. If persistent agents learn across episodes, the persistent lifecycle, cohort, or randomized deployment period may be the unit. If swarms share a database or message channel, isolation has failed or interference is part of the treatment and must be modeled.

## 3. Define the system before measuring it

Freeze the full system, not just its model name:

- Provider, exact model identifier or weight hash, revision, tokenizer, quantization, inference engine, reasoning setting, temperature, top-p, output limits, structured-output settings and seed support. Record requested and returned identifiers; aliases can drift.
- Every system/developer prompt, role, prompt renderer, examples, tool description, safety policy and truncation rule. Hash rendered initial messages after legitimate variable substitution. Store only public/sanitized prompts.
- Memory initialization, namespace, update, retrieval, summarization, eviction and reset policy. A new chat does not necessarily reset a vector store, browser cookies or shared files.
- Tools, schemas, code versions, allowlists, network destinations, access rights and tool-result filtering. Distinguish information agents may inspect from what is actually delivered.
- Population size, identities, roles, model diversity, communication graph, routing, bandwidth, message visibility, topology generation and failure behavior.
- Orchestration: scheduling, synchronous barriers or asynchronous delivery, tie-breaking, turn limits, deadline, termination, delegation and aggregation policy.
- System-wide budgets for input/output/reasoning tokens where observable, tool calls, money, wall time, GPU hours and human assistance. Count coordinator, critic, retriever and evaluator costs separately and in the full pipeline total.

An immutable definition may specify adaptation; record every resulting state transition. If weights or policies change across episodes, define a training phase, checkpoints, evaluation schedule and held-out population. Freeze evaluation checkpoints and prevent test feedback updating the policy.

## 4. From question to protocol

1. **Build a causal argument.** Name the intervention, primary endpoint, unit, task population and plausible confounders. A causal diagram can reveal that increasing agents also changes tokens and evidence. If both change, the estimand is a package effect.
2. **Review prior work and define novelty.** Record searches, versions and contrary findings. Keep literature retrieval separate from test answers. Save a novelty search date and evidence; absence in one search is not proof of novelty.
3. **Specify hypotheses.** Choose one primary contrast and a smallest effect of practical interest before observing confirmatory results. Separate mechanism hypotheses, secondary outcomes and exploratory analyses. State whether superiority, equivalence or noninferiority is intended; “not significant” cannot establish equivalence.
4. **Design controls and splits.** Include a credible single-agent baseline, a scripted heuristic, an independent-agent ensemble without communication and the specific architectural alternative of interest where appropriate. Tune baselines on development data with a documented comparable search allowance. Never deliberately weaken the baseline.
5. **Define measurement.** Prefer objective state changes, tests or externally checked artifacts. Specify a correct answer, valid action, failure, abstention and safety violation operationally. Use blinded scoring where possible. An agent's claim of completion is not completion.
6. **Pilot engineering and variance.** Use separate development scenarios to test initialization, logging, failure recovery, difficulty range, costs, outcome variance and evaluator agreement. Record all design changes. Pilot effect estimates are noisy and selection-biased; power for a scientifically useful effect, not the most favorable pilot effect.
7. **Preregister and freeze.** Time-stamp a local immutable protocol or use an appropriate registry when authorized. Include analysis code on synthetic data, exact allocation, exclusion and stopping rules. Hash data, configuration, grader and schedule. Keep exploratory changes in a new version.
8. **Execute and collect.** Start with a small smoke test; once its gate passes, run the frozen schedule. Monitor operational integrity without repeatedly testing the effect. Keep a ledger of planned, started, completed, failed, censored and scored units.
9. **Analyze under the design.** Preserve pairing, clustering and task weights. Report uncertainty, operational failures, costs and deviations alongside average outcomes.
10. **Report and replicate.** Provide artifacts and enough information for another researcher to reconstruct the claim. A new evaluator, model, task family or implementation is a valuable extension, but distinguish it from direct replication.

The distinctions between proposal, executable verification and valid result are particularly relevant to autonomous science: recent evaluations report execution and open-ended research limitations. [AgentActionBench](https://arxiv.org/abs/2609.11117) [[hong-2026-overview]], [SciAgentArena](https://arxiv.org/abs/2606.12736) [[liu-2026-benchmarking]].

## 5. Allocation, controls and fair comparisons

Randomize treatment order within blocks of scenario, model snapshot and time window. Interleave conditions to avoid putting all controls before an API update. Record the schedule before execution and actual starts. If a service changes mid-study, report the break and analyze a prespecified block or restart a new study version; do not silently pool incompatible systems.

Use paired designs when each treatment can receive the same underlying scenario, observations and exogenous disturbance schedule. Create those inputs once and clone them into isolated worlds. Do not copy post-treatment messages. Matching numerical seeds is insufficient if treatments consume a variable number of RNG draws; use independent keyed streams for environment, assignment, message delays, policy sampling and evaluation.

Communication is intended interference within a swarm. Between swarms, remove shared files, caches with generated content, package registries used as writable channels, retrieval updates and human feedback leakage. If evaluating a connected network with individual-level treatments, prespecify exposure mappings or cluster randomization; ordinary independent-arm tests will not identify direct and spillover effects separately.

Budget matching must reflect the question. At fixed **system** budget, additional agents divide resources and incur communication cost; at fixed **per-agent** budget, a larger swarm receives more compute. Report both only as separate estimands. Compare accuracy–cost and latency–cost frontiers where feasible. Token counts across different model tokenizers are imperfect compute proxies; document money, latency and model identities too. Realized consumption need not be equal even with equal caps. Do not pad useless calls to manufacture equality. [AI Agents That Matter](https://arxiv.org/abs/2407.01502) [[kapoor-2024-ai]], [Scaling Agent Systems, v3](https://arxiv.org/abs/2512.08296v3) [[kim-2025-towards]].

Ablate one mechanism at a time when seeking attribution: memory off, provenance removed, communication off, shuffled identities, alternative topology, no critic or independent verifier. Factorial designs estimate interactions more efficiently than unrelated experiments, but need sufficient replication per cell and a prespecified interaction analysis. If roles, prompts, evidence and budget all change, label the result a bundled comparison.

## 6. How many agents, scenarios and independent runs?

There is no universal run count. **Agent count is a treatment parameter; scenario count controls task coverage; repeats estimate execution variability.** More agents in one episode do not replace independent worlds. More seeds on one puzzle do not establish generalization to other puzzles.

For a first engineering pilot, a practical planning suggestion is 8–12 varied development scenarios, 3–5 fresh paired repetitions, and a small population such as 5 agents. These are debugging and variance-screening numbers, not a claim of adequate statistical power. Select sizes that distinguish the mechanisms: a three-node undirected ring is a complete graph, so it cannot distinguish local from global communication. For a scale study, a prespecified grid such as 1, 3, 5, 9 agents can reveal nonlinearity; verify that each topology is actually distinct at each size.

Let D_sr be a treatment-minus-control difference for scenario s and repetition r. A useful planning decomposition is D_sr = μ + u_s + ε_sr, with between-scenario variance σ²_b and within-scenario variance σ²_w. With S independently sampled scenarios and R independent paired repetitions per scenario, the variance of the mean is approximately:

`Var(mean D) = σ²_b / S + σ²_w / (S R)`.

Estimate both components from a pilot and vary them in sensitivity analyses. More scenarios help both terms; more repeats only reduce the second. Include scenario acquisition cost c_s and per-pair execution cost c_r in `cost = S(c_s + R c_r)` and compare feasible allocations. When σ²_b is large, prioritize scenarios; when within-scenario instability is the research target, allocate enough repetitions to characterize it. Two seeds cannot resolve tail reliability.

For independent approximately normal paired differences, a first planning approximation is:

`n_pairs ≈ ((z_(1−α/2) + z_power) × SD(D) / δ)²`.

At two-sided α=.05, 80% power, SD(D)=.25 and δ=.10, n≈49.1, rounded up to **50 independent pairs**. These assumptions are illustrative. Small-sample t inference, bounded/binary outcomes, clustering and multiple primary contrasts can require more. For a 95% CI half-width .05 with SD .25, precision planning gives approximately `(1.96 × .25 / .05)² = 96.04`, rounded up to **97 pairs**. Power and precision answer different questions.

For nested repetitions use the variance formula, not n=S×R in an independent-pair calculation. The worked example uses S=60, R=4, σ_b=.18 and σ_w=.20: SE≈.0266 and approximate 95% half-width .052. At δ=.08 the normal approximation gives roughly 85% power. This is a planning calculation with assumed variance, **not a pilot result**. Simulate the actual bounded outcome, scenario effects and planned analysis over plausible variance ranges before committing a costly confirmatory run. A 20% SD underestimate raises required independent sample size by 44%.

For binary success use paired discordance rates (McNemar design), an appropriate hierarchical logistic model, or simulation of paired Bernoulli outcomes. Avoid applying a normal continuous-outcome calculation without checking its approximation. With zero failures in n genuinely independent comparable trials, the one-sided 95% upper failure-probability bound is `1 − .05^(1/n)` (about 3/n). Zero failures in 30 trials still permits roughly 9.5% failure; clustered tasks weaken simple interpretation. [Lakens](https://doi.org/10.1525/collabra.33267) [[lakens-2022-sample]], [Patterson et al.](https://jmlr.org/papers/v25/23-0183.html) [[patterson-2024-empirical]], [Agarwal et al.](https://arxiv.org/abs/2108.13264) [[agarwal-2021-deep]].

If the available budget is insufficient, narrow the question or report a precision-limited exploratory study. Do not justify a preferred count with retrospective power calculated from the observed effect.

## 7. Outcomes, reliability and evaluators

Report a profile rather than one score:

| Dimension | Operational examples |
| --- | --- |
| Capability | Correct terminal state, task utility, independently validated discovery rate |
| Consistency | Per-scenario success distribution across resets; all-k success; variance in continuous scores |
| Robustness | Matched changes under irrelevant paraphrases, order changes, tool outages or observation noise |
| Predictability | Calibration of stated probabilities; failure prediction; abstention–coverage tradeoff |
| Safety | Severity-weighted violations, forbidden actions, oversight escalation, worst observed failure |
| Efficiency | Full system tokens, tool calls, dollars, elapsed time, GPU-hours and human minutes |

Define “success” and “reliability” once and use the same denominator throughout. A consistently wrong agent is consistent but unsuccessful. An all-k success metric asks whether all k fresh attempts succeed; pass@k asks whether at least one succeeds. They have different uses and generally assume a sampling model. Do not use best-of-k without charging for k attempts and the selection mechanism. [τ-bench](https://arxiv.org/abs/2406.12045) [[yao-2024-tau]], [Reliability, v3](https://arxiv.org/abs/2602.16666v3) [[rabanser-2026-towards]].

Calibrate an evaluator on a stratified sample spanning easy, hard, failed and ambiguous outputs. Have at least two domain-competent people independently annotate a calibration subset where feasible; report raw agreement, prevalence, confusion matrix and an appropriate agreement statistic with uncertainty. Adjudicate disagreements using a written rule. Measure scoring drift and lock the rubric before test scoring.

An LLM judge is a measurement instrument with its own model, prompt, context, randomness and errors. Blind treatment and model names; randomize answer order; test both orders for pairwise comparisons; include known-correct, known-wrong and adversarial judge-injection controls. Check style, verbosity, self-preference and reference leakage. Freeze judge versions, prevent agents editing rubrics, and sample human audits across conditions. Agreement on one dataset does not establish unbiased treatment comparisons elsewhere. Report judge-only versus adjudicated sensitivity analyses; include judge cost. For long reports validate document-level consistency and evidence coverage, not just fluency. [Zheng et al.](https://arxiv.org/abs/2306.05685) [[zheng-2023-judging]], [Soumik, v2](https://arxiv.org/abs/2604.23178v2) [[soumik-2026-judging]], [LongJudgeBench, v4](https://arxiv.org/abs/2606.01629v4) [[chen-2026-benchmarking]].

A read-only unit test is also fallible: check it verifies the intended semantic object. The research-swarm case study illustrates agents satisfying a flawed verifier while failing the intended proof task. Treat authors' governance remedies as hypotheses requiring interventions, not established causal fixes. [Paglieri et al.](https://arxiv.org/abs/2609.04170) [[paglieri-2026-case]].

## 8. Analysis without pseudoreplication

Analyze the randomized unit and preserve pairing. For equally weighted sampled scenarios, first compute each scenario's mean paired treatment difference, then average scenarios. A cluster bootstrap resamples whole scenarios with their paired repetitions intact; do not bootstrap individual messages. A hierarchical model can estimate scenario and model-family effects and interactions, with priors/assumptions and diagnostics disclosed. For a fixed benchmark, distinguish uncertainty from rerunning those exact tasks from uncertainty about a wider task population. Resampling scenarios implicitly changes the inferential target.

Use randomization inference consistent with the assignment scheme where suitable. Repeated seeds crossed with scenarios, shared task templates, common source documents and reused base models may require crossed effects or larger clusters. With few clusters, asymptotic standard errors can mislead; show scenario-level results and use an appropriate small-sample method. Report residual checks and sensitivity to outliers, weights and model specification. A model name is usually a fixed selected condition, not a random sample of all possible models.

Report raw denominators, absolute effect sizes and confidence intervals. Relative change alone can exaggerate small baselines. Show practical thresholds and costs next to p-values. For primary multiple comparisons, use a prespecified familywise procedure such as Holm; for a broad exploratory screen, control false discovery rate and label the results exploratory. Repeatedly searching prompts, topologies and outcome definitions is selection even if only the final comparison appears in the paper. Reserve untouched test scenarios after development.

Fix the sample size or preregister a valid sequential design. Ordinary 95% intervals and p<.05 at every peek do not preserve their advertised error rate. Group-sequential alpha spending or suitable confidence sequences can support interim decisions under their assumptions. Operational cost or safety stops are allowed, but disclose their timing, incomplete allocation and implications for inference. Stopping because the estimate “looks stable” is data-dependent stopping. [Howard et al.](https://arxiv.org/abs/1810.08240) [[howard-2018-time]].

Classify every noncompletion: model refusal, invalid action, timeout, budget exhaustion, tool outage, infrastructure crash, human stop or unavailable grade. For operational success, count prespecified noncompletions as failures in the assigned denominator. For time-to-success, a deadline may right-censor time; a timeout is still a failure for “success by deadline.” Informative censoring needs sensitivity analysis. Do not drop difficult runs. Missing outcomes can be bounded by assigning best and worst permissible scores; multiple imputation requires defensible missingness assumptions. Report complete-case analysis only as a labeled sensitivity result.

Infrastructure retries retain the original run ID and attempt lineage. Use a prespecified cap and backoff; classify retries that already consumed useful model output separately. A successful retry cannot erase the cost or first failure. Replacing a failed scenario with a new easy one changes the population. If reproducibility breaks, preserve evidence, quarantine affected blocks and record the protocol amendment.

## 9. Validity, security and scientific accountability

Prevent contamination at several levels: training overlap with public benchmarks; development access to hidden tests; retrieval containing solutions; shared memory between conditions; judge access to treatment labels; and human-assisted repairs guided by test outcomes. Record known overlap and unknown pretraining exposure. Use fresh synthetic instances, held-out generators, new task families and temporal holdouts where appropriate, while acknowledging that synthetic novelty alone does not ensure realism.

For social simulation, validate individual response distributions, interactions and aggregate dynamics separately. Match observations relevant to the proposed use, test competing mechanisms, assess parameter identifiability and run sensitivity analysis. Several rule systems can reproduce one macro-pattern; fitting that pattern does not prove the mechanism. Hold out interventions or contexts to test predictive validity. Biological analogies can inspire a mechanism but do not validate it. [ODD](https://www.jasss.org/23/2/7.html), [Validation Gap](https://proceedings.mlr.press/v306/puelma-touzel26a.html) [[puelma-touzel-2026-position]].

For AI-assisted science, maintain a claim-to-evidence ledger: proposed hypothesis → source data → generated candidate → execution → validator result → human review → replication. Include search failures and selection count; optimize on development evidence and validate the selected candidate on untouched data or a fresh physical experiment. Multiple candidate selection can overfit noisy validators. Report whether humans chose questions, supplied templates, repaired code, selected outputs or interpreted results. “Autonomous” needs a boundary and an intervention log.

Use least privilege, network allowlists and disposable environments. Keep graders, hidden truth, orchestration controls and source snapshots outside agent write access. Record manual interventions and safety stops as events. Public content may contain prompt injections; treat it as data, not an instruction source. Real laboratory, human-subject or field studies require the relevant domain oversight before execution. This package authorizes no external actions.

**Secrets never enter prompts, manifests, terminal output or trace payloads.** Reference only credential aliases; an approved local adapter consumes values from a secure store and returns sanitized status. Avoid logging headers, environment dumps, connection strings, raw exceptions or screenshots containing credentials. Filter at the collection boundary, before anything reaches the transcript. Prefer public synthetic data for shareable examples. For restricted records, preserve authorized encrypted artifacts locally with access controls and share de-identified derivatives only after review. Hash public artifact bytes; do not publish hashes of low-entropy secrets as a substitute for secrecy.

Track separate licenses for code, model weights, datasets, papers and generated/retrieved content. Access permission is not redistribution or training permission. A replication package should include license/attribution metadata and a retrieval recipe for restricted inputs. Do not silently assign a license to pre-existing owner material. Record consent, retention, deletion and ownership rules for human data.

## 10. What an independent researcher should receive

Deliver the frozen protocol and amendments; source archive and hashes; resolved configurations; prompts and access manifests; dataset versions/splits and generator; environment lockfile/container digest; planned and actual run ledger; raw sanitized events; evaluator and analysis code; scored outcomes; cost accounting; deviations; a reproduction command; expected outputs and tolerances; and a list of unavailable dependencies. Separate exact trace replay, fresh runs with the same specification, and independent reimplementation.

Hosted models may become unavailable. Save enough sanitized observations and outputs for analysis reproduction, and document that fresh behavioral replication depends on provider availability. Report model/version drift as a limitation rather than claiming that a seed reconstructs the service. A successful local smoke test validates the harness contract, not scientific effectiveness.

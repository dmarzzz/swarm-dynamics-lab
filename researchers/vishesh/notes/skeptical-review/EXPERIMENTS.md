# Experimental reasoning context

These are reviewer recommendations and mathematical checks, not a substitute for a chosen protocol's statistical analysis. Source codes resolve in [sources.md](sources.md).

## State the estimand before the mechanism

Write one sentence: “Across independently generated worlds from distribution D, policy A changes outcome Y relative to B under budget C.” Define what is randomized, what remains shared, and what information each arm can access. A larger discussion allowance estimates a joint effect of extra interaction, exposure and computation. To attribute it to social interaction, add equally funded private work. Do not quietly swap those estimands.

A fixed total budget and a fixed per-agent budget answer different questions. Report actual token, tool, latency and verification costs alongside resource ceilings. Treat an oracle's extra information as a ceiling, not a deployable method's fair advantage. Match access to fresh corrective evidence before praising a repair policy.

Keep all assigned episodes in the primary outcome denominator. Split wrong, valid abstention, invalid output, timeout and infrastructure failure. Completed-only accuracy is secondary. Infrastructure can matter operationally without diagnosing model intelligence. Pair worlds across conditions and randomize execution order; do not silently count recovered uploads or retries as new scientific replicates.

## Independence and effective size

For an average of N equal-variance quantities with common pairwise correlation rho, its variance is `sigma²[1+(N-1)rho]/N`. Matching that variance to an independent average motivates `N_eff = N/[1+(N-1)rho]`, when the covariance model is valid and the denominator is positive. This is a variance-equivalent size under explicit assumptions, not a count of truthful agents or a formula for majority-vote accuracy. It need not apply to heterogeneous tasks or correlated categorical errors without a defined estimator.

The citation participation ratio `(sum m_r)² / sum(m_r²)` instead measures concentration of citation mass across root labels. Four equally cited labels yield four even if all copied one observation. Empty evidence needs a separate state. Neither changing provider names nor hashing documents establishes independent evidence (E2). Independence is not an assumption of the classical Byzantine fault model (E11).

Inference should follow randomization. Agents, rounds, descendant branches and repeated seeds within a world are dependent. A shared checkpoint can improve pairing while not creating additional independent worlds. When generalizing beyond one template, reserve genuinely distinct task rules. A design-effect approximation can help planning, but it does not alone validate a clustered McNemar test or a confidence interval (E6).

## Baselines that can make a complicated idea unnecessary

Use the strongest feasible simple alternative: single solver with the same permitted fact union, independently sampled answers with a fixed aggregator, fixed-round or confidence stopping, indexed direct routing, append-only correction, full reset, ordinary transactions, or a fixed team. Charge its costs too. A “do nothing” arm identifies gross effect but rarely justifies complexity.

Qualify the benchmark with a simple correct solver, an intentionally wrong solver, answer-label permutation, metadata-only policy and blind policy. Mutate one input to ensure the scorer can recognize a consequential error. A test that cannot express the advertised failure cannot evaluate its defense. Absence of a found shortcut is not proof of benchmark validity (E10).

For recovery, score cumulative harm, restored task utility, correct knowledge retained, recurrence after a declared horizon, false quarantine and reacquisition cost. Include benign changes and a correct specialist. A defense that freezes every update may look safe but cannot serve a changing task. A finite re-entry test measures performance over its continuation distribution, not latent alignment (E4, E8).

## Stop and revise before spending

A deterministic counterexample is cheaper than a model sweep. Check empty inputs, ties, unanimity, inconsistent facts, duplicate retries, stale returns and exhausted budgets. The Scheme C counterexample in E12 must be resolved before treating the stopping rule as ready.

Choose a smallest practically worthwhile effect and a resource ceiling before confirmation. Use development worlds to establish task solvability and variance, then freeze prompts, thresholds, selection rules and exclusions. Report a null or a cheaper baseline win. Do not choose a flattering parameter sweep cell and present it as the preregistered primary test.

Useful first reductions are one task world, one failure surface, one intervention, one strong simple comparator and one negative control. Add a second world mechanism before adding more roles, visual ornament or model families. This is a sequencing recommendation, not permission to launch paid runs or bypass the lab's gates.

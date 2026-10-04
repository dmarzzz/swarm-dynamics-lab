# Experimental design and fork merge review

Review target: [experimental-design.md](../seo-poisoning/experimental-design.md) as published in commit `45b363a`, particularly Scheme C, the cheap-agent interface and the paired evaluation plan. This is an exploratory design review by vishesh/codex-methods, not the cross-researcher gate review required by AGENTS.md. Existing strengths include separating attack surfaces, retaining imperfect provenance, charging defense cost, and acknowledging that the biological brake is an analogy rather than a transferred theorem.

## Correct unanimity cannot pass the proposed ceiling

Scheme C defines `C = sum(p[o]^2)`, `C* = 1 - 1/(1 + kappa*N_eff)`, and permits commitment only when `theta <= C <= C*`. For every finite positive `kappa*N_eff`, `C* < 1`. If all votes put their mass on the same correct option, normalization yields `C = 1`, so commitment is forbidden irrespective of how many independent roots support it.

For example, `kappa=1`, `N_eff=5`, and `theta=0.6` give `C*=5/6`. Distribution `(0.8,0.1,0.1)` has `C=0.66` and passes the band; `(1,0,0)` fails. The existing check `theta <= C*` passes in both cases. It therefore does not catch this observation-dependent deadlock. These are arithmetic counterexamples, not measured agent outcomes.

Separate evidence admission from a lower confidence threshold and require explicit behavior for exhausted acquisition, empty evidence and correct unanimity. Compare the revised specification against confidence-only stopping and fixed rounds before choosing a functional form. This does not prove any alternative is safe; it makes the intended decision states reachable. See VX-03 and SOC-08.

## Source concentration is not established independent sample size

`(sum m_r)^2 / sum(m_r^2)` is an inverse concentration measure over citation counts. If five agents all cite the same four roots, it equals four. If four root labels copy a single upstream observation, it can still equal four. Calling it an effective *independent* evidence count requires a definition of independence and validation against error; domain, document and observation-level identity are not interchangeable. Correlated model errors are separately established prior, not removed by citation accounting. [[kim-2025-correlated]]

The draft already requires copying detection and imperfect-provenance controls. Extend those controls to **false splits versus false merges**, under-reported citations, and an honest rare specialist. Specify how empty root sets behave: Jaccard overlap of two empty sets and the concentration formula with no citations otherwise divide by zero. Missing evidence should remain a named state, not be assigned unjustified independence. See VX-01 and VX-02.

## Robust aggregation needs the right fault model

The attacker in this bundle changes external information consumed by otherwise legitimate agents. All agents can consequently share one error. That is different from a bounded number of arbitrary workers surrounded by honest gradient estimates. A bound such as `f/N < 1/3` does not by itself establish truth, availability or robustness for free-text judgments.

Bulyan's Section 4 requires `n >= 4f+3` received gradients. Thus a five-agent arm with `f=1` cannot use that guarantee: it requires at least seven. The paper's model assumes distributed stochastic gradients with specified statistical properties. Replacing them with weighted option probabilities does not inherit its theorem. [[el-mhamdi-2018-hidden]] [Primary PDF, Sections 2 and 4](https://arxiv.org/pdf/1802.07927).

Treat trimmed means, Multi-Krum and Bulyan as different candidate algorithms with explicit preconditions, not interchangeable robust-vector implementations. Define integer trimming at small N, retained coordinates, normalization and the behavior of a correct outlier. The nearest comparison includes a simple evidence ledger and ordinary independent voting, not only another robust aggregator. [[blanchard-2017-byzantine]]

## Exposure and propagation need distinct estimands

Keep all randomized task assignments in the primary end-to-end analysis. If the content treatment changes retrieval, comparing only episodes that retrieved it selects on a post-treatment event. Exposure, acceptance and later propagation are valuable descriptive stages, but their conditional rates do not automatically identify mediation effects.

A small local factorial can manipulate retrieval/ranking policy and peer communication independently, with the same generated truth and task resources. Add generic versus profiled material after that mechanism is understood. Match common external exposure before attributing similarity to peer influence. These are design inferences informed by work on interference and the difficulty of separating influence from shared causes. [[aronow-2013-estimating]] [[shalizi-2011-homophily]] See VX-26.

## Repeated seeds do not create independent task worlds

The proposed `35 tasks × 5 seeds` plan has 35 task clusters when generalizing over tasks, not 175 independent task draws. The draft appropriately mentions clustered analysis. Its McNemar component still needs an exact definition of the binary paired unit: a standard calculation on 175 dependent pairs would not automatically respect task clustering.

Freeze the estimand and use task-level paired differences with cluster-aware uncertainty or a randomization analysis faithful to assignment. Define how timeouts, invalid outputs and budget exhaustion enter every denominator. Pilot estimates can inform allocation between worlds and within-world seeds, but should not be counted as confirmation. These are reviewer recommendations; no power or coverage calculation for the final proposed experiment is claimed here. See MTH-01, MTH-04 and VX-33. [[aronow-2013-estimating]]

## Jev is a concrete component but its role still matters

The bundle's unresolved-name note can now be narrowed using public product documentation: TypeSafe's Choice interface selects among supplied options and returns probabilities and confidence; its examples name a Jev model. This establishes an interface to evaluate, not evidence of suitability or cheapness for this task. [TypeSafe Choice documentation](https://docs.typesafe.ai/primitives/choice).

For Choice, the documented confidence is `(p_max - 1/n)/(1 - 1/n)`. It is computed from the option distribution, not a separate observation of factual correctness. Holding `p_max=0.8` fixed gives confidence `0.6` for two options and approximately `0.7333` for four. Actual option changes may also change the model's probabilities. Pin the option set and model, retain raw probabilities, and evaluate calibration on held-out task truth. [TypeSafe confidence documentation](https://docs.typesafe.ai/confidence).

Distinguish raw retrieved text → Jev, cheap-LLM extracted state → Jev, and evaluator-provided factual state → Jev. The last is a diagnostic upper bound. Keep criteria and action authority in application-controlled configuration; retrieved content is evidence to evaluate. The classifier's use as response labeler, eligibility filter or collective adjudicator remains an explicit design choice. No provider calls or price claims were made in this review. See VX-28 and VX-36.

## Reduce the first implementation without losing the question

The bundle itself estimates 50–72 builder-hours and offers a smaller fallback. Treat those as planning estimates, not measured costs. The first useful slice is a deterministic evidence fixture with a simple baseline, an observable-provenance rule, an oracle-provenance upper bound and a budget-matched independent-check arm. Validate truth isolation, commit reachability, trace completeness and recovery semantics before adding a learned surrogate, adaptive attacker or larger model ladder.

The [published experiment toolkit](../../../../tooling/agent-experiments/README.md) supplies reusable discipline and examples; it is not a completed retrieval/provider experiment. The [simulation survey](../../../../surveys/sim-environments.md) records others' smoke checks; this review did not rerun them. These readiness limits are separate from whether the research question is interesting.

## Keep the fork merge regimes separate

The [nine setup families](../../../../src/fork-merge-setups/rigs.json), [source batches](../../../../src/fork-merge-setups/cards/) and [fork-merge questions](../../../../synthesis/fork-merge-questions.md) are useful inherited research context. Their aggregate claims were inspected as summaries, not independently re-audited source by source. In particular, statements that a mechanism was “never” tested should be read as limits of that scan, not global absence proofs.

| Setup families | Useful transfer | Boundary to retain | Relevant review links |
| --- | --- | --- | --- |
| R1 weight merging; R2 federated aggregation | Composition can defeat checks on individual parts; assumptions about honest inputs matter. | Weight-space attacks and SGD guarantees do not become text-memory guarantees. | SEC-09, SEC-12; VX-22 |
| R3 voting and debate | Correlated errors, fixed membership and evidence access shape aggregation. | More returning copies need not add independent evidence. | SOC-01, SEC-03; VX-01, VX-02 |
| R4 persistent memory; R5 channel contagion | Track admission, compaction, downstream use and correction separately. | A later single-agent session is not automatically a parallel returning fork. | SEC-05 through SEC-08; VX-06, VX-11 |
| R6 AI control; R7 deployed demonstrations | Audit the trusted monitor and tool boundary; retain useful-work measures. | A demonstrated exploit is not a prevalence estimate, and assumed monitor trust needs its own boundary. | SEC-04, SEC-12; VX-32, VX-38 |
| R8 classical systems | Commit, rollback, replay, capability and metadata models give concrete baselines. | Deterministic byte-comparable state differs from uncertain semantic evidence. | MTH-05, SEC-02, SEC-07; VX-11, VX-15 |
| R9 biological and human analogues | Identity admission, propagation and function after damage suggest useful contrasts. | Analogy supplies questions, not transferred theorem constants or LLM effect sizes. | PHY-17, SOC-24; VX-18, VX-27 |

MemTX already treats staged belief commitment and repair; MemLineage already treats provenance and derivation-based action enforcement. Those primary abstracts sharply narrow any generic “provenance plus repair” novelty claim. The promising remaining comparisons here concern wrong or incomplete lineage, stale returns, compaction and irrecoverable effects, subject to a full methods-level comparison before promotion. [[li-2026-memtx]] [[ouyang-2026-memlineage]]

# Focused prior-art review for qualification

vishesh/codex-idea-scores, 2026-10-04 UTC. This is an author-side focused review, not independent approval and not a completed lab survey. Source access below records the actual reading depth; inherited library full-read labels are not claims about this review.

## Closest work and consequences

**Kim et al., Towards a Science of Scaling Agent Systems, arXiv v3.** Opened the [versioned full text](https://arxiv.org/html/2512.08296v3); inspected research questions, task contrasts, regression predictors, token matching and limitations. Methods-targeted partial read. The study already compares architecture-dependent gains and losses and explores agent counts through nine. Its prediction model uses measured coordination quantities, which are unsuitable as uncharged inputs to our pre-launch rule. Our interpretation: a fixed architecture with a resource-conditioned choice of N is a narrower deployment question, not the first study of agent scaling. Preserve single-agent access to the same tools and aggregate allowance, and evaluate the selector with its own execution clock. [[kim-2025-towards]]

**Tran and Kiela, Single-Agent LLMs Outperform Multi-Agent Systems on Multi-Hop Reasoning Under Equal Thinking Token Budgets, arXiv v2.** Opened the [abstract](https://arxiv.org/abs/2604.02460) and [full-text landing page](https://arxiv.org/html/2604.02460v2); abstract-level conclusions only. Their matched-thinking-budget result and reported API-control artifacts directly challenge apparent swarm gains. Our consequence: both configured and actual consumption must be reported; unused allowance and early termination are outcomes, not reasons to silently give one arm more attempts. Our deadline and resource-envelope experiment does not by itself resolve their information-theoretic claim. [[tran-2026-single]]

**Liu, Kong and Pei, Phase Transition for Budgeted Multi-Agent Synergy, arXiv v2.** Opened the [abstract](https://arxiv.org/abs/2601.17311) and [full-text landing page](https://arxiv.org/html/2601.17311v2); abstract-level review, not a proof audit. Their theoretical model already treats finite context, lossy messages, correlated errors and budgeted team benefit; validation described in the abstract is synthetic. Our consequence: no “first optimal-size theory” claim. A crossover in our finite grid is not evidence of their phase transition without satisfying its aggregation and dependence assumptions. Our main study tests a centralized work protocol rather than majority aggregation on a deep tree. [[liu-2026-phase]]

**Kao and Couzin, Decision accuracy in complex environments is often maximized by small group sizes.** The repository's [[kao-2014-decision]] record is abstract-only. Publisher access returned 403 and the attempted PMC page returned a browser challenge in this pass. No new verification of its methods. Keep it as a biological reading lead, not a validated causal account of our software agents.

## Search and scope

One focused search used `multi-agent scaling budget single agent matched compute`, in addition to direct retrieval of the established closest sources. It surfaced the Tran and Liu studies already present in the shared library. This is not a saturation search, forward-citation survey, or independent source audit. It does not satisfy the repository's full survey gate. No library read-depth metadata was upgraded.

## Decision for this package

The generator/evaluator is worth qualifying as infrastructure for a narrow empirical comparison. Novelty remains provisional. The claim to test later is practical: whether a launch-time rule selecting N under a specified envelope improves verified on-time delivery over a frozen fixed-size baseline after charging decision overhead. Neither an aesthetic replay nor an author-side review counts as evidence for that claim.

Do not advance to a confirmatory core/transfer study on this note alone. The existing survey/review and hypothesis gates still apply. Exploratory S0/S1 work in owned notes follows the worker template's documented route, with public plan, independent package review, explicit budget and dedicated allocation still required for this design.

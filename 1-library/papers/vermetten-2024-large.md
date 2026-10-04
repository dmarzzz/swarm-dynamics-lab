---
id: vermetten-2024-large
type: paper
title: Large-Scale Benchmarking of Metaphor-Based Optimization Heuristics
authors:
- Diederick Vermetten
- Carola Doerr
- Hao Wang
- Anna V. Kononova
- Thomas Bäck
year: 2024
venue: Proceedings of the Genetic and Evolutionary Computation Conference (GECCO 2024)
url: https://arxiv.org/abs/2402.09800
doi: 10.1145/3638529.3654122
arxiv: '2402.09800'
cite: Vermetten, D., Doerr, C., Wang, H., Kononova, A. V., & Bäck, T. (2024). Large-scale benchmarking of metaphor-based optimization heuristics. In Proceedings of the Genetic and Evolutionary Computation Conference (GECCO '24) (pp. 41–49). ACM. https://doi.org/10.1145/3638529.3654122
topics:
- swarm-intelligence
- meta
added_by: dmarz/swarm-intelligence
accessed: '2026-10-03'
read_depth: full
relevance: 4
citations: 22 (OpenAlex, 2026-10-03)
code: []
---

## Summary

Benchmarks 294 publicly available optimiser implementations (14 EvoloPy, 53 NiaPy, 139 Mealpy, 76 Opytimizer, plus 12
baselines from Nevergrad, modCMA and modDE) on all 24 noiseless BBOB functions in d = 2, 5, 10, 20, 5 runs x 10
instances, budget 10,000 d (1,411,200 runs). Performance spreads widely; a sizeable fraction of metaphor-based
implementations lose to random search, only 45 algorithms ever reach a per-function top 3, and the overall best
is BIPOP-CMA-ES. Rankings change with budget and with the performance measure (anytime AOCC vs fixed budget).

## Contribution

Moves the metaphor critique from case studies ([[camacho-villalon-2023-exposing]]) to a portfolio-scale, reproducible
benchmark on a suite without the centre-bias flaw ([[kudela-2022-critical]]), and argues for judging algorithms by
complementarity (Shapley contribution to a portfolio) rather than average rank.

## Key results

- Measured: performance distribution of AOCC across the 294 implementations widens and drops off sharply with
  dimension; few algorithms scale to d = 20.
- Measured: on F11 RandomSearch beats more than 30% of the portfolio; several implementations lose to RandomSearch on
  all 2-D problems (likely broken implementations).
- Measured: of 96 (function, dimension) pairs, only 45 unique algorithms are top-3 anywhere, 20 of them once.
  multiBFGS is top-3 on 26 pairs but 14th on average loss (specialist); JADE is top-3 on 6 pairs but 3rd on loss.
- Measured: approximate Shapley values (250 subsets of size 1-20 per algorithm) show CMA-ES/BIPOP and DE variants
  gain value with budget, most metaphor algorithms only at low budget; ABC and GCO do well in low dimension only.
- Observed: two implementations of L-SHADE (modDE vs Mealpy) behave very differently, showing implementation
  underspecification.
- Observed: Cuckoo Search performs well here although it is known to be a reformulation of older ideas.

## Methods and models

IOHexperimenter on BBOB; metrics: normalised area over the convergence curve (AOCC, log-scaled precision bounds 1e-8
to 1e2, and a relaxed 1e8 variant) and fixed-budget precision at b in {10,...,10,000} x d; Shapley-style portfolio
contribution; UMAP of 96-dim AOCC vectors. Default parameters, no tuning. Data and code: Zenodo
doi:10.5281/zenodo.10561215, figures on Figshare doi:10.6084/m9.figshare.25060151. Libraries:
EvoloPy, NiaPy and Mealpy (GitHub URLs truncated in the text I extracted), https://github.com/gugarosa/opytimizer and
https://github.com/FacebookResearch/Nevergrad as printed in the paper.

## Limitations and open questions

Short conference paper; results depend on third-party implementations and default parameters (no HPO), which the
authors flag. Duplicate algorithms across libraries were kept. BBOB is one suite; the authors caution against
overfitting to it. Does not test whether algorithms are novel, only how they perform.

## Relevance to us

The practical benchmarking protocol we should copy if the hackathon compares a swarm optimiser against baselines:
BBOB via IOHexperimenter, RandomSearch and CMA-ES baselines, anytime metric. Complements
[[kudela-2023-evolutionary]] and [[sorensen-2015-metaheuristics]].

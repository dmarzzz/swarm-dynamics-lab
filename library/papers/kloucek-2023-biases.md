---
id: kloucek-2023-biases
type: paper
title: 'Biases in inverse Ising estimates of near-critical behavior'
authors: ['Maximilian B. Kloucek', 'Thomas Machon', 'Shogo Kajimura', 'C. Patrick Royall', 'Naoki Masuda', 'Francesco Turci']
year: 2023
venue: 'Physical Review E'
url: https://arxiv.org/abs/2301.05556
doi: 10.1103/PhysRevE.108.014109
arxiv: '2301.05556'
cite: 'Kloucek, M. B., Machon, T., Kajimura, S., Royall, C. P., Masuda, N., & Turci, F. (2023). Biases in inverse Ising estimates of near-critical behavior. Physical Review E, 108(1), 014109.'
topics: [criticality-measurement]
added_by: dmarz/criticality-measurement-audit
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: '6 (OpenAlex, 2026-10-03)'
code: []
---

## Summary

Inverse Ising inference by pseudo-likelihood maximisation (PLM) is the usual way to fit pairwise models to
binary data before asking whether the system is near critical. Using the Sherrington-Kirkpatrick spin glass as a
ground-truth benchmark, the authors show PLM estimates are biased, the bias is largest near phase boundaries, and
small sample sizes make inferred models look closer to criticality than the generating model. They test
data-driven bias corrections and apply them to an fMRI data set.

## Contribution

A quantitative, method-level version of the "inference makes things look critical" argument of
[[mastromatteo-2011-criticality]], with practical corrections.

## Key results

- PLM bias scales with 1/B (B = number of samples) with a prefactor that grows near criticality (analytic and simulation).
- Finite-sample bias shifts inferred models toward the critical region of the SK phase diagram (simulation).
- Two corrections: a self-consistency correction matching the second moment C2, and Firth's penalised logistic regression; both improve the reconstructed temperature in the SK benchmark (simulation).
- Single-participant resting-state fMRI (N = 399 regions, B = 9440 and 4248 samples): naive PLM gives different temperatures for meditation vs no-meditation sessions (T* = 0.98 vs 1.33), but after correction both look like the same state point, far from the transition in the paramagnetic phase (application).

## Methods and models

SK model at several temperature and field state points (for example T* = 1.40 and 2.00) sampled by Monte
Carlo; un-regularised PLM via logistic regressions; analysis of first-order bias; fMRI functional connectivity
data. Code: https://github.com/maxkloucek/pyplm.

## Limitations and open questions

Benchmark is a spin glass with all-to-all couplings, not a spatial swarm; only PLM is studied, not
Boltzmann-machine learning or mean-field inverse methods used in the flock literature.

## Relevance to us

If we fit maximum entropy models to swarm data, we need this check: compare the inferred distance to
criticality against sample size. Related: [[bialek-2012-statistical]], [[mora-2011-biological]],
[[nonnenmacher-2017-signatures]].

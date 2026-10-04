---
id: trelea-2003-particle
type: paper
title: 'The particle swarm optimization algorithm: convergence analysis and parameter selection'
authors:
- Ioan Cristian Trelea
year: 2003
venue: Information Processing Letters
url: https://doi.org/10.1016/S0020-0190(02)00447-7
doi: 10.1016/S0020-0190(02)00447-7
arxiv: null
cite: 'Trelea, I. C. (2003). The particle swarm optimization algorithm: Convergence analysis and parameter selection. Information Processing Letters, 85(6), 317–325. https://doi.org/10.1016/S0020-0190(02)00447-7'
topics:
- swarm-intelligence
added_by: dmarz/swarm-intelligence
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 2652 (OpenAlex, 2026-10-03)
code: []
---

## Summary

Analyses PSO with standard results from dynamic system theory, derives graphical parameter-selection guidelines,
discusses and illustrates the exploration-exploitation trade-off, and reports example parameter sets that outperform
previously published results on benchmark functions. (Abstract obtained from the CORE record of the paper.)

## Contribution

Widely used parameter-selection map for deterministic PSO dynamics, complementing [[clerc-2002-particle]].

## Key results

- Claimed in abstract: graphical stability/oscillation regions in parameter space; benchmark performance superior to
  earlier published settings (numbers not read).

## Methods and models

Linear dynamical-system analysis of the deterministic PSO recurrence; benchmark tests (abstract only).

## Limitations and open questions

Abstract-level reading; deterministic analysis ignores the random multipliers.

## Relevance to us

Background for choosing PSO baselines in experiments; see [[bonyadi-2017-particle]] for how later stability analyses
refined these regions.

---
id: levina-2022-tackling
type: paper
title: 'Tackling the subsampling problem to infer collective properties from limited data'
authors: ['Anna Levina', 'Viola Priesemann', 'Johannes Zierenberg']
year: 2022
venue: 'Nature Reviews Physics'
url: https://arxiv.org/abs/2209.05548
doi: 10.1038/s42254-022-00532-5
arxiv: '2209.05548'
cite: 'Levina, A., Priesemann, V., & Zierenberg, J. (2022). Tackling the subsampling problem to infer collective properties from limited data. Nature Reviews Physics, 4(12), 770-784.'
topics: [criticality-measurement, meta]
added_by: dmarz/criticality-measurement-audit
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: '31 (OpenAlex, 2026-10-03)'
code: []
---

## Summary

Perspective and review on spatial subsampling: observing only a small fraction of a system's units biases
estimates of its collective properties. It surveys how subsampling distorts graph statistics, avalanche
distributions, branching ratios and correlations, reviews correction methods for networks, animal collectives,
neural activity and epidemics, and lists open problems.

## Contribution

The map of the subsampling literature, written by the authors of the main correction tools
([[wilting-2018-inferring]]). It cites the flocking work ([[cavagna-2010-scale]] and the Physics Reports review)
as one of the application areas.

## Key results

- Naive inference from a subsample can systematically misclassify the dynamical state (review of prior results).
- Corrections exist for specific observables (branching ratio, degree distributions, avalanche statistics) but no general solution (claimed in abstract).
- Open challenges listed alongside large-scale recording developments.

## Methods and models

Review; boxes define spatial subsampling and show how incomplete sampling biases estimation.

## Limitations and open questions

Abstract-level read; mostly neuroscience-weighted examples.

## Relevance to us

Field-of-view and occlusion in swarm tracking are subsampling; any criticality claim from partly tracked groups
should address it. Related: [[nonnenmacher-2017-signatures]], [[priesemann-2014-spike]], [[attanasi-2014-finite]].

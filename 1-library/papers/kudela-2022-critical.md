---
id: kudela-2022-critical
type: paper
title: A critical problem in benchmarking and analysis of evolutionary computation methods
authors:
- Jakub Kudela
year: 2022
venue: Nature Machine Intelligence
url: https://www.nature.com/articles/s42256-022-00579-0
doi: 10.1038/s42256-022-00579-0
arxiv: null
cite: Kudela, J. (2022). A critical problem in benchmarking and analysis of evolutionary computation methods. Nature Machine Intelligence, 4(12), 1238–1245. https://doi.org/10.1038/s42256-022-00579-0
topics:
- swarm-intelligence
- meta
added_by: dmarz/swarm-intelligence
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 105 (OpenAlex, 2026-10-03)
code: []
---

## Summary

Shows that several frequently used benchmark functions have their optimum at the centre of the feasible set, and that
seven recently published methods contain a centre-bias operator that finds such optima easily, making comparisons
with unbiased methods meaningless. On shifted problems and harder benchmarks, compared with DE and PSO, only one of
the seven new methods was consistently better, three were on par, two performed very badly, and the worst barely beat
random search.

## Contribution

Identified the centre-bias artefact that inflates many recent swarm/evolutionary algorithms; extended to 90 methods in
[[kudela-2023-evolutionary]].

## Key results

- Measured (abstract): 7 new methods vs DE and PSO on shifted problems: 1 better, 3 on par, 2 very poor, 1 barely
  above random search.

## Methods and models

Shifted vs unshifted benchmark comparisons (abstract read on the publisher page).

## Limitations and open questions

Abstract-level reading; the full method is described in the follow-up I read.

## Relevance to us

Benchmarks for any swarm optimiser in the hackathon must be shifted/rotated; PSO and DE are the honest baselines.

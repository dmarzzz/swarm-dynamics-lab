---
id: eberhart-1995-new
type: paper
title: A new optimizer using particle swarm theory
authors:
- Russell Eberhart
- James Kennedy
year: 1995
venue: MHS'95. Proceedings of the Sixth International Symposium on Micro Machine and Human Science (IEEE)
url: https://doi.org/10.1109/MHS.1995.494215
doi: 10.1109/MHS.1995.494215
arxiv: null
cite: Eberhart, R., & Kennedy, J. (1995). A new optimizer using particle swarm theory. In MHS'95. Proceedings of the Sixth International Symposium on Micro Machine and Human Science (pp. 39–43). IEEE. https://doi.org/10.1109/MHS.1995.494215
topics:
- swarm-intelligence
added_by: dmarz/swarm-intelligence
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 14996 (OpenAlex, 2026-10-03)
code: []
---

## Summary

Companion to [[kennedy-1995-particle]] published the same year. Describes optimisation of nonlinear functions with
particle swarms and compares two paradigms, including a newly developed locally oriented version in which particles
follow the best of a local neighbourhood rather than the global best. Benchmark tests of both are described and
applications to neural-network training and robot task learning are proposed.

## Contribution

Introduces the local-best (lbest) neighbourhood variant, the origin of the topology question later studied in
[[kennedy-1999-small]] and [[mendes-2004-fully]].

## Key results

- Claimed in abstract: two paradigms (global and local) implemented and compared on benchmarks; numbers not read.

## Methods and models

Particle swarm update with global-best and local-neighbourhood-best attraction; benchmark testing (abstract only).

## Limitations and open questions

Abstract-level reading. Short conference paper; experimental detail limited by format.

## Relevance to us

Historical origin of interaction-topology effects in swarm optimisers, the algorithmic analogue of metric vs
topological neighbourhoods in flocking models.

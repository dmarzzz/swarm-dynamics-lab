---
id: niizato-2023-functional
type: paper
title: 'Functional duality in group criticality via ambiguous interactions'
authors: ['Takayuki Niizato', 'Hisashi Murakami', 'Takuya Musha']
year: 2023
venue: 'PLOS Computational Biology'
url: https://doi.org/10.1371/journal.pcbi.1010869
doi: 10.1371/journal.pcbi.1010869
arxiv: null
cite: 'Niizato, T., Murakami, H., & Musha, T. (2023). Functional duality in group criticality via ambiguous interactions. PLOS Computational Biology, 19(2), e1010869.'
topics: [criticality-measurement, collective-motion]
added_by: dmarz/criticality-measurement
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: '5 (OpenAlex, 2026-10-03)'
code: []
---

## Summary

Introduces an "ambiguous interaction" flocking model, a natural extension of Boids and Vicsek models,
that reproduces nested criticality across scales: scale-free correlation, super-diffusion, Levy walks and 1/f
fluctuations of relative velocity. Applying partial information decomposition to two scale-free-induced
subgroups shows that coupling of flock morphology and fluctuation power likely enables rapid group turns.

## Contribution

Links multi-scale critical signatures to function (turning) using PID-based information flows
between subgroups.

## Key results

- Model reproduces scale-free correlation, super-diffusion, Levy walks and 1/f fluctuation (simulation).
- PID information flows between subgroups relate group morphology and fluctuations to rapid turns.

## Methods and models

Agent-based ambiguous interaction model; PID on subgroup variables.

## Limitations and open questions

Abstract-level read.

## Relevance to us

Shows how to use PID on subgroups rather than individuals, which scales better. Related:
[[rosas-2020-reconciling]], [[niizato-2020-finding]].

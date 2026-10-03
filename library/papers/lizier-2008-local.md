---
id: lizier-2008-local
type: paper
title: 'Local information transfer as a spatiotemporal filter for complex systems'
authors: ['Joseph T. Lizier', 'Mikhail Prokopenko', 'Albert Y. Zomaya']
year: 2008
venue: 'Physical Review E'
url: https://arxiv.org/abs/0809.3275
doi: 10.1103/physreve.77.026110
arxiv: '0809.3275'
cite: 'Lizier, J. T., Prokopenko, M., & Zomaya, A. Y. (2008). Local information transfer as a spatiotemporal filter for complex systems. Physical Review E, 77(2), 026110.'
topics: [criticality-measurement]
added_by: dmarz/criticality-measurement
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: '293 (OpenAlex, 2026-10-03)'
code: []
---

## Summary

Defines local (pointwise) transfer entropy, the information a source's past adds about a target's
next state at each point in space and time, rather than the time-averaged quantity. Applied to elementary
cellular automata, it acts as a filter that highlights coherent structures, and it gives the first
quantitative evidence that gliders and domain walls are the dominant information-transfer agents.

## Contribution

The methodological foundation for spatiotemporal information-flow analysis in swarms used by
[[wang-2012-quantifying]], [[crosato-2018-informative]] and others.

## Key results

- Local transfer entropy profiles filter coherent structure in cellular automata.
- Particles (gliders, domain walls) are the dominant information-transfer agents (quantitative evidence in CA).

## Methods and models

t_{Y->X}(n) = log p(x_{n+1} | x_n^{(k)}, y_n) / p(x_{n+1} | x_n^{(k)}); apparent and complete
(conditional) variants; elementary CA rules. arXiv 0809.3275.

## Limitations and open questions

Demonstrated on discrete CA; continuous swarm data need estimators (see [[lizier-2014-jidt]]).

## Relevance to us

Core definition for measuring who informs whom, when, in a swarm. Local values can be negative
(misinformative), which [[crosato-2018-informative]] exploits.

---
id: marshall-2009-optimal
type: paper
title: "On optimal decision-making in brains and social insect colonies"
authors: ["James A. R. Marshall", "Rafal Bogacz", "Anna Dornhaus", "Robert Planqué", "Tim Kovacs", "Nigel R. Franks"]
year: 2009
venue: "Journal of The Royal Society Interface"
url: https://doi.org/10.1098/rsif.2008.0511
doi: "10.1098/rsif.2008.0511"
arxiv: null
cite: "Marshall, J. A. R., Bogacz, R., Dornhaus, A., Planqué, R., Kovacs, T., & Franks, N. R. (2009). On optimal decision-making in brains and social insect colonies. Journal of The Royal Society Interface, 6(40), 1065–1074. https://doi.org/10.1098/rsif.2008.0511"
topics: ["collective-decision", "swarm-intelligence"]
added_by: dmarz/collective-decision
accessed: 2026-10-03
read_depth: abstract
relevance: 5
citations: "237 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Adapts the analysis of neural evidence-accumulation models (in which competing populations integrate evidence until one hits a threshold) to models of house-hunting by social insects, and shows that colonies can in principle implement the statistically optimal sequential probability ratio test, minimising decision time for a given error rate, through direct competition between evidence-accumulating scout populations.

## Contribution

First explicit common theoretical framework for decision-making in brains and insect colonies; it set up the brain-colony analogy later tested in [[seeley-2012-stop]] and reframed by value-sensitivity in [[pais-2013-mechanism]].

## Key results

- Some colony decision models reduce to the drift-diffusion model and can achieve the optimal speed-accuracy compromise under particular parameterisations (analytical).
- Makes testable predictions about how recruitment and inhibition between scout populations should be organised.
- Abstract-level reading only; numbers beyond the abstract were not checked.

## Methods and models

Reduction of two-population colony models to one-dimensional drift-diffusion processes, following Bogacz et al. analyses of cortical models.

## Limitations and open questions

Optimality is for accuracy-based reward; later work argues value-based reward is the relevant criterion for nest choice ([[pais-2013-mechanism]], [[bose-2017-collective]]).

## Relevance to us

Key for any experiment that benchmarks a swarm's speed-accuracy curve against an optimal sequential test. Related: [[franks-2003-speed]], [[sumpter-2009-quorum]].

---
id: champneys-2023-pao
type: paper
title: 'PAO: A general particle swarm algorithm with exact dynamics and closed-form transition densities'
authors:
- Max D. Champneys
- Timothy J. Rogers
year: 2023
venue: arXiv preprint
url: https://arxiv.org/abs/2304.14956
doi: null
arxiv: '2304.14956'
cite: 'Champneys, M. D., & Rogers, T. J. (2023). PAO: A general particle swarm algorithm with exact dynamics and closed-form transition densities. arXiv preprint arXiv:2304.14956. https://doi.org/10.48550/arXiv.2304.14956'
topics:
- swarm-intelligence
added_by: dmarz/swarm-intelligence
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 0 (OpenAlex, 2026-10-03)
code: []
---

## Summary

Argues that new PSO variants can offer only marginal benchmark gains (citing no free lunch) and that research should
seek other useful properties. Proposes the particle attractor algorithm (PAO), a general, interpretable PSO variant
whose particle transition densities between generations are available exactly in closed form, which matters for
sequential Monte Carlo. Benchmarks against several state-of-the-art heuristics to show the properties do not cost
performance.

## Contribution

Designs a swarm optimiser for analysability (exact stochastic dynamics) rather than metaphor, a constructive response
in the spirit of [[camacho-villalon-2023-designing]], and links PSO to SMC.

## Key results

- Claimed (abstract): closed-form transition densities; competitive benchmark performance (numbers not read).

## Methods and models

Particle attractor dynamics with exactly computable generation-to-generation transition densities; benchmark
comparison against state-of-the-art heuristics (abstract only).

## Limitations and open questions

Abstract-level reading; preprint.

## Relevance to us

Exact transition densities would let us compute likelihoods of observed swarm trajectories, useful for inference on
swarm dynamics.

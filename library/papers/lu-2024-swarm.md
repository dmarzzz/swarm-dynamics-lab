---
id: lu-2024-swarm
type: paper
title: Swarm-based gradient descent method for non-convex optimization
authors:
- Jingcheng Lu
- Eitan Tadmor
- Anil Zenginoğlu
year: 2024
venue: Communications of the American Mathematical Society
url: https://arxiv.org/abs/2211.17157
doi: 10.1090/cams/42
arxiv: '2211.17157'
cite: Lu, J., Tadmor, E., & Zenginoğlu, A. (2024). Swarm-based gradient descent method for non-convex optimization. Communications of the American Mathematical Society, 4(17), 787–822. https://doi.org/10.1090/cams/42
topics:
- swarm-intelligence
- sync-consensus
added_by: dmarz/swarm-intelligence
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 6 (OpenAlex, 2026-10-03)
code: []
---

## Summary

Introduces swarm-based gradient descent (SBGD): each agent has a position and a mass; mass flows from agents on high
ground to the lowest agent, and step size depends on relative mass, so heavy "leaders" take small gradient steps
toward local minima while light "explorers" take large backtracking steps; an explorer that finds better ground
becomes a leader. Local convergence is proved and simulations on 1-, 2- and 20-dimensional benchmarks show improved
global behaviour.

## Contribution

A swarm optimiser designed by a collective-dynamics mathematician (Tadmor, of Cucker-Smale/Motsch-Tadmor flocking
models) in which the communication is mass transfer rather than attraction; a non-metaphor design that encodes a
leader/explorer division of labour.

## Key results

- Claimed in abstract: local convergence proof; numerical gains in global convergence on 1-, 2-, 20-D benchmarks
  (numbers not read).

## Methods and models

Gradient-based agents with mass-dependent step size and backtracking; mass transfer protocol (abstract only).

## Limitations and open questions

Abstract-level reading. Needs gradients. Global convergence not proved; benchmark breadth unknown from the abstract.

## Relevance to us

Example of explicit role differentiation (leaders vs explorers) emerging from a conserved quantity, relevant to
division-of-labour questions in swarms.

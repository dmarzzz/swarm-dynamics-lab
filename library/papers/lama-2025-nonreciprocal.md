---
id: lama-2025-nonreciprocal
type: paper
title: "Nonreciprocal field theory for decision-making in multi-agent control systems"
authors: ["Andrea Lama", "Mario di Bernardo", "Sabine H. L. Klapp"]
year: 2025
venue: "Nature Communications"
url: https://api.semanticscholar.org/graph/v1/paper/DOI:10.1038/s41467-025-63071-4?fields=title,abstract
doi: "10.1038/s41467-025-63071-4"
arxiv: "2503.01112"
cite: "Lama, A., di Bernardo, M., & Klapp, S. H. L. (2025). Nonreciprocal field theory for decision-making in multi-agent control systems. Nature Communications, 16(1), 8450."
topics: [swarm-robotics, active-matter, collective-decision]
added_by: dmarz/swarm-robotics
accessed: 2026-10-03
read_depth: abstract
relevance: 5
citations: "12 (Semantic Scholar, 2026-10-03)"
code: []
---
## Summary

Field theories of collective behaviour normally assume reciprocal pairwise interactions. Decision-making agents
break reciprocity and add many-body effects. Using the shepherding problem from swarm robotics (herders must
confine a group of targets in a region) as a paradigm, the authors build continuous approximations of target
selection and trajectory planning and derive field equations for the herder and target densities. The theory
shows how decision strategies at the agent level (from average attraction to highly selective choices, from
undirected to goal-oriented motion) become nonreciprocal couplings in the continuum that drive transitions
between homogeneous and confined configurations.

## Contribution

A recipe for putting decision-making into continuum (active-matter) theories of swarms, connecting multi-agent
control with nonreciprocal field theories ([[fruchart-2021-non]]).

## Key results

- Derived field equations; transitions between homogeneous and confined states controlled by decision
  strategies (from abstract; parameters not checked).

## Methods and models

Coarse-graining of herder-target agent dynamics with decision rules; linear stability and numerical solution of
field equations. Abstract read.

## Limitations and open questions

Theory and simulation; no robot experiments. Validity of the continuum approximation at small N not checked.

## Relevance to us

Strong candidate for a hackathon project that compares agent-based shepherding with its field theory.
Related to [[elamvazhuthi-2019-mean]] and [[valentini-2017-best]].

---
id: mehdizadeh-2026-exploring
type: paper
title: 'Exploring the Topology and Memory of Consensus: How LLM Agents Agree, Fragment, or Settle When Forming Conventions'
authors:
- Aliakbar Mehdizadeh
- Martin Hilbert
year: 2026
venue: arXiv preprint (submitted to JASSS)
url: https://arxiv.org/abs/2606.04197
doi: null
arxiv: '2606.04197'
cite: 'Mehdizadeh, A., & Hilbert, M. (2026). Exploring the topology and memory of consensus: How LLM agents agree, fragment, or settle when forming conventions. arXiv preprint arXiv:2606.04197.'
topics:
- llm-agent-swarms
- sync-consensus
added_by: dmarz/llm-agent-swarms
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 4 (Semantic Scholar, 2026-10-03; OpenAlex unavailable that day)
code: []
---

## Summary

Runs a networked naming game with LLM agents on eight fixed 16-agent topologies, varying memory depth (432 runs). Longer memory slows settling in decentralised networks but speeds it in centralised ones, so memory's effect flips sign with topology. "Faster settling" in centralised networks means locking into a fragmented plateau, not global consensus; centralised networks preserve more competing conventions. High-betweenness bridge agents suffer a brokerage penalty, while locally clustered agents coordinate better. Agents' choices are well fitted by fictitious play (belief-based, not reward-based adaptation).

## Contribution

Extends the well-mixed naming game of [[ashery-2024-emergent]] to structured networks and shows memory and topology must be co-designed.

## Key results

- Memory x topology interaction flips the sign of memory's effect on settling time (abstract).
- Centralised networks lock in fragmented conventions faster (abstract).
- Fictitious play describes agent choices (abstract).

## Methods and models

Networked naming game, 16 agents, 8 topologies, varied memory depth, 432 runs; agent-level network-centrality analysis. Code not checked.

## Limitations and open questions

Small N = 16; abstract-level read.

## Relevance to us

Network topology is a core swarm variable; this gives an LLM-specific result to contrast with classical naming-game results on networks.

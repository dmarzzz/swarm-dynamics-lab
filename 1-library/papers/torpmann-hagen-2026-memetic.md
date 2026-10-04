---
id: torpmann-hagen-2026-memetic
type: paper
title: 'Memetic Trojans: Social Contagions as Carriers of Adversarial Payloads in Agent Networks'
authors: [Birk Torpmann-Hagen, Finn Schwall, Leon Moonen]
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2610.00430
doi: null
arxiv: '2610.00430'
cite: 'Torpmann-Hagen, B., Schwall, F., & Moonen, L. (2026). Memetic Trojans: Social Contagions as Carriers of Adversarial Payloads in Agent Networks. arXiv preprint arXiv:2610.00430.'
topics: [llm-agent-swarms, criticality-measurement]
added_by: shadow/sol-1
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

Defines memetic trojans: adversarial payloads embedded in content that LLM agents already want to share (social contagions), so propagation is endogenous rather than induced by a self-replicating injection as in agent worms ([[lee-2024-prompt]], [[gu-2024-agent]]). The authors extract real social contagions from Moltbook, the agent-only social platform ([[de-marzo-2026-collective]]), and run controlled transmission experiments: the most effective contagion is retransmitted in about 50% of subsequent agent posts and upvoted at 2.5x the average post's rate, and its trojan counterpart largely inherits those properties. Monte Carlo attack simulations show memetic trojans amplify expected exposure by up to 3.19x, with network structure and amplification mechanisms producing heavy-tailed outcomes up to near network-wide exposure. Posted 2026-09-30, three days before the hackathon. Abstract only.

## Contribution

Connects information-cascade dynamics in agent populations to a security threat model and provides measured virality numbers for real agent-generated memes. The first paper I have seen that quantifies retransmission rates of content among LLM agents in the wild rather than in a designed game.

## Key results

- Reported: top contagion retransmitted in about 50% of subsequent posts, upvoted at 2.5x average (controlled transmission experiment, details not read).
- Reported: expected exposure amplification up to 3.19x for memetic trojans in Monte Carlo simulation.

## Methods and models

Contagion extraction from Moltbook data, controlled transmission experiments with LLM agents, Monte Carlo propagation over network structures. Models and network parameters not read.

## Limitations and open questions

- Abstract-level read; no detail on which models, how many agents, or how "retransmission" was scored.
- Whether the measured virality transfers from Moltbook-style feeds to task-oriented message boards (the incident setting) is untested.

## Relevance to us

The cascade and contagion face of swarm dynamics: a hackathon experiment could measure retransmission probability as a function of population size or board visibility, using Moltbook-derived memes as stimuli, and compare with the exploit-recipe spread in [[gh-killy-netsphere-sealed-swarm-transcripts]] (3 informed to 16 uninformed lineages via one post).

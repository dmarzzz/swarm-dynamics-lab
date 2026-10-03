---
id: chopra-2025-large
type: paper
title: "Large Population Models"
authors: ["Ayush Chopra"]
year: 2025
venue: "arXiv preprint"
url: https://arxiv.org/abs/2507.09901
doi: null
arxiv: '2507.09901'
cite: "Chopra, A. (2025). Large population models. arXiv:2507.09901."
topics: [llm-agent-swarms, meta]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: null
code: [gh-agenttorch-agenttorch]
---

## Summary

Position and synthesis paper aggregating the author's MIT PhD work on Large Population Models (LPMs): simulate whole populations (millions of agents) with three ingredients, namely compute methods for millions of simultaneous agents, frameworks that calibrate to diverse real-world data streams (differentiable simulation), and privacy-preserving protocols bridging virtual and physical populations. Implemented in AgentTorch.

## Contribution

Frames 'digital societies' as a complement to 'digital humans' and ties scale, calibration and privacy into one research programme.

## Key results

- No new experiments in the abstract; it summarises prior results (pandemic response, supply chains) implemented in AgentTorch.

## Methods and models

Tensorised ABM in PyTorch, LLM archetypes (cluster agents and query the LLM per archetype rather than per agent), gradient-based calibration.

## Limitations and open questions

Abstract only; a thesis aggregation, so claims rest on the underlying papers.

## Relevance to us

Borrow idea: LLM archetypes to keep LLM calls sublinear in population size when we need millions of agents. Code: [[gh-agenttorch-agenttorch]].

---
id: itkin-2026-poor
type: paper
title: "Poor Man's Agentic Modeling: Simulating Large LLM-Agent Societies on a Laptop"
authors: [Igor Itkin]
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2608.11215
doi: null
arxiv: '2608.11215'
cite: "Itkin, I. (2026). Poor Man's Agentic Modeling: Simulating Large LLM-Agent Societies on a Laptop. arXiv preprint arXiv:2608.11215."
topics: [llm-agent-swarms, criticality-measurement]
added_by: shadow/sol-1
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

A method paper for the compute problem that every LLM-society study hits. The observation: the questions asked of agent societies are macroscopic (phase behaviour, stylised facts, scaling with N), so each LLM agent can be replaced by a low-parameter surrogate fitted from a few hundred to a few thousand cheap queries, and the society then runs at any N on a laptop. The author proposes an [interaction order x memory] taxonomy that maps what an agent perceives and remembers to an effective theory and a predicted N-trend of the surrogate error, so whether the shortcut works is decided before running. Validated on a reimplementation of the EconAgent LLM macroeconomy and seven further named LLM simulations with decisions cloned from genuine LLM elicitations (mainly DeepSeek) for a few dollars; the predicted error trends hold cell by cell, and two refuted predictions are traced to curvature of a saturating response and matched by the theory with no free parameters. Abstract only.

## Contribution

Formalises the "extract the policy once, then simulate" move that [[flint-2026-group]] used for N up to 10^4 in the naming game and [[el-2026-physics]] used with a fitted kinetic-Ising model, and gives a rule for when it is valid.

## Key results

- Reported: surrogate error N-trends predicted by the taxonomy hold across eight LLM simulations (abstract; numbers not read).
- Reported: cloning cost a few dollars per simulation using DeepSeek elicitations.

## Methods and models

Fit low-parameter per-agent response models from LLM queries, classify the simulation by interaction order and memory, run the surrogate society at large N. Details not read.

## Limitations and open questions

- Abstract-level read; the taxonomy's exact cells and the failure cases need the full text.
- Surrogates by construction cannot show behaviours that depend on open-ended language (new conventions, invented tactics), which is exactly what the incident corpora show.

## Relevance to us

The practical recipe for a one-day hackathon experiment that wants an N-sweep: elicit the per-state policy from a small model a few hundred times, then sweep N in a surrogate. Pair with [[pavlova-2026-flag]] or [[ashery-2024-emergent]] as the game.

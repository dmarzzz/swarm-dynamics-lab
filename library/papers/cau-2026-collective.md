---
id: cau-2026-collective
type: paper
title: 'Collective Opinion Dynamics in Structured LLM Populations'
authors: [Erica Cau, Andrea Failla, Giulio Rossetti]
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2604.11312
doi: null
arxiv: '2604.11312'
cite: 'Cau, E., Failla, A., & Rossetti, G. (2026). Collective Opinion Dynamics in Structured LLM Populations. arXiv preprint arXiv:2604.11312.'
topics: [llm-agent-swarms, sync-consensus]
added_by: shadow/sol-1
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

Populations of LLM agents hold multi-round debates on networks generated with controlled homophily and varying relative group sizes, ten independent runs per configuration. Reported findings: opinion trajectories are highly sensitive to network structure, relative group size and the model used; low homophily speeds convergence by increasing cross-group exposure while high homophily preserves distinct opinion states (consistent with classical opinion-dynamics results); different LLMs show different opinion-updating patterns under identical network conditions; giving agents information about their local neighbourhood changes transition rates, with large model-to-model differences in sensitivity to local social context. Version 3 updated 2026-09-28. Abstract only; the models, N and update rule were not read.

## Contribution

A controlled homophily x group-size sweep for LLM opinion dynamics, which is the networked complement to the complete-graph naming-game line ([[ashery-2024-emergent]], [[flint-2026-group]]) and to the topology results of [[mehdizadeh-2026-exploring]] and [[saab-2026-graph]].

## Key results

- Reported: low homophily facilitates convergence, high homophily sustains fragmentation (abstract; numbers not read).
- Reported: substantial model-specific differences in updating under matched network conditions.

## Methods and models

Generated networks with controlled homophily, variable group sizes, multi-round debate, ten runs per configuration. Details not read.

## Limitations and open questions

- Abstract-level read. Without a ground truth, "convergence" cannot be scored as correct or wrong.
- The [[yang-2026-when]] diagnostic (randomised initial conditions, measured coupling gain) would tell whether the convergence is social or prior-driven; unknown whether applied.

## Relevance to us

Supports the choice of homophily or rewiring as the one-knob manipulation in a hackathon consensus experiment, and warns that results will not transfer across models.

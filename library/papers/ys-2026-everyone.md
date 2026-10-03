---
id: ys-2026-everyone
type: paper
title: 'Everyone Conforms, No One Believes: Pluralistic Ignorance in LLM Agent Populations'
authors:
- Yashwanth YS
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2608.02758
doi: null
arxiv: '2608.02758'
cite: 'YS, Y. (2026). Everyone Conforms, No One Believes: Pluralistic Ignorance in LLM Agent Populations. arXiv preprint arXiv:2608.02758.'
topics:
- llm-agent-swarms
- collective-decision
added_by: dmarz/llm-agent-swarms-recent
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 0 (OpenAlex, 2026-10-03); 2 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Tests whether LLM agent populations show pluralistic ignorance, where most members privately reject a norm but publicly conform, each believing they are alone. A benchmark of 100 scenarios across 10 domains and 5 authority levels is run on 8 models from 6 organisations. Agents publicly conform 64-94% of the time while privately opposing the norm. A single "norm entrepreneur" publicly dissenting rarely triggers a cascade: for 7 of 8 models cascades succeed less than 26% of the time (one model never), with GPT-4o an outlier at 48%. Removing the false-consensus framing and fit-in goal lowers but does not remove conformity (52-92%), so the author argues conformity is emergent rather than instructed.

## Contribution

Adds tipping-point (cascade) failure to the conformity literature on LLM collectives ([[weng-2025-do]], [[cho-2025-herd]]) and suggests LLM simulations may overstate norm stability, the opposite concern to the low critical masses in [[ashery-2024-emergent]].

## Key results

- Measured (per abstract): public conformity 64-94% despite private opposition.
- Measured: cascade success < 26% for 7 of 8 models; GPT-4o 48%; one model 0%.
- Measured: minimal-prompt condition still 52-92% conformity.

## Methods and models

100-scenario benchmark; private vs public responses; single dissenter intervention; prompt ablation; 8 models.

## Limitations and open questions

Abstract-level read; single-author preprint; populations and network structure not specified in the abstract.

## Relevance to us

A measurable tipping-point experiment; the gap between private and public states is a hidden variable worth tracking in swarm runs. Related: [[zhou-2025-pimmur]].

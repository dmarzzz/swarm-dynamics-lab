---
id: mordatch-2018-emergence
type: paper
title: Emergence of Grounded Compositional Language in Multi-Agent Populations
authors:
- Igor Mordatch
- Pieter Abbeel
year: 2018
venue: Proceedings of the AAAI Conference on Artificial Intelligence
url: https://arxiv.org/abs/1703.04908
doi: 10.1609/aaai.v32i1.11492
arxiv: '1703.04908'
cite: Mordatch, I., & Abbeel, P. (2018). Emergence of grounded compositional language in multi-agent populations. Proceedings of the AAAI Conference on Artificial Intelligence, 32(1). https://doi.org/10.1609/aaai.v32i1.11492
topics:
- marl-emergence
added_by: dmarz/marl-emergence
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 252 (Crossref, 2026-10-03); 442 for the AAAI record (OpenAlex, 2026-10-03)
code: []
---

## Summary

Agents in a 2D physical world must achieve goals (for example getting another agent to a landmark) and can emit discrete symbols. Trained jointly, the population develops a small grounded language with a defined vocabulary and syntax-like structure, and when verbal channels are removed agents fall back on non-verbal communication such as pointing and guiding. The abstract frames this as evidence that compositional language can emerge as a means to goals rather than from corpus statistics.

## Contribution

A founding paper of the deep emergent-communication line (with [[foerster-2016-learning]] and [[sukhbaatar-2016-learning]]), and the source of the particle world later packaged as MPE in [[lowe-2017-multi]]. Its end-to-end differentiable training through a model of the dynamics distinguishes it from model-free MARL.

## Key results

- Emergence of a discrete, compositional-looking symbol stream with vocabulary and word-order structure (claimed in the abstract; numbers not read).
- Non-verbal pointing and guiding emerge when symbols are unavailable (claimed).

## Methods and models

Particle-world agents with physical and symbolic actions, trained end to end through differentiable dynamics (per the description in [[huttenrauch-2019-deep]], which notes a softmax pooling over other agents). Only the abstract was read here.

## Limitations and open questions

Read at abstract level; how compositionality was measured was not checked. Later work (Lazaridou and Baroni's survey [[lazaridou-2020-emergent]]) questions whether such protocols are language-like.

## Relevance to us

Background for any communication-in-swarms idea; communication bandwidth is a natural control parameter for collective behaviour. Related: [[foerster-2016-learning]], [[zhu-2024-survey]].

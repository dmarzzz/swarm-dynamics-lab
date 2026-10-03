---
id: rahman-2025-llm-powered
type: paper
title: 'LLM-Powered Swarms: A New Frontier or a Conceptual Stretch?'
authors:
- Muhammad Atta Ur Rahman
- Melanie Schranz
- Samira Hayat
year: 2025
venue: arXiv preprint (author version of a paper submitted to IEEE Intelligent Systems)
url: https://arxiv.org/abs/2506.14496
doi: null
arxiv: '2506.14496'
cite: 'Rahman, M. A. U., Schranz, M., & Hayat, S. (2025). LLM-Powered Swarms: A New Frontier or a Conceptual Stretch? arXiv preprint arXiv:2506.14496 (author version submitted to IEEE Intelligent Systems).'
topics:
- llm-agent-swarms
- swarm-intelligence
- collective-motion
added_by: dmarz/llm-agent-swarms-recent
accessed: '2026-10-03'
read_depth: abstract
relevance: 5
citations: 5 (Semantic Scholar, 2026-10-03); not in OpenAlex as of 2026-10-03
code: []
---

## Summary

The paper checks whether systems marketed as LLM "swarms" (specifically OpenAI's Swarm framework, where agents coordinate through natural-language handoffs) satisfy the defining principles of classical swarm intelligence: decentralisation, simplicity of individuals, emergence and scalability. The authors implement classical and LLM-driven versions of Boids and Ant Colony Optimization in that framework and compare them. LLM-powered versions can emulate swarm-like dynamics, but at large computational overhead: the LLM-based Boids simulation took roughly 300 times the computation time of the classical implementation, which the authors argue limits LLM swarms for real-time systems.

## Contribution

A conceptual and empirical audit of the term "swarm" as used for LLM multi-agent frameworks, from swarm-robotics researchers. Provides the cost baseline every LLM-swarm proposal should report. Companion to [[jimenez-romero-2025-multi-agent]] and [[ruan-2025-benchmarking]].

## Key results

- Measured (per abstract): LLM Boids ~300x slower than classical Boids.
- Claimed: LLM swarms can emulate swarm-like dynamics but violate simplicity and scalability principles.

## Methods and models

OpenAI Swarm (OAS) framework; classical and LLM-based Boids and ACO; comparison of behaviour and computation time. Models and swarm sizes not checked.

## Limitations and open questions

Abstract-level read; only one framework; cost ratios depend on model and hardware.

## Relevance to us

Use as the reference for cost and for the definitional argument when we call anything an "LLM swarm". Related: [[zomer-2026-unraveling]], [[li-2025-swarmsys]], [[zou-2026-waggle]].

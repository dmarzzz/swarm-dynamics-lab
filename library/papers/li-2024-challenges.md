---
id: li-2024-challenges
type: paper
title: Challenges Faced by Large Language Models in Solving Multi-Agent Flocking
authors:
- Peihan Li
- Vishnu Menon
- Bhavanaraj Gudiguntla
- Daniel Ting
- Lifeng Zhou
year: 2024
venue: arXiv preprint
url: https://arxiv.org/abs/2404.04752
doi: null
arxiv: '2404.04752'
cite: Li, P., Menon, V., Gudiguntla, B., Ting, D., & Zhou, L. (2024). Challenges Faced by Large Language Models in Solving Multi-Agent Flocking. arXiv preprint arXiv:2404.04752.
topics:
- llm-agent-swarms
- collective-motion
- swarm-robotics
added_by: dmarz/llm-agent-swarms-recent
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 1 (OpenAlex, 2026-10-03); 8 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

The authors task LLM-powered agents, each acting as an individual decision-maker, with multi-agent flocking: staying close to neighbours, avoiding collisions and keeping a desired formation. The agents fall short. After extensive testing, LLM agents typically either converge onto the average of their initial positions or drift apart, rather than forming and maintaining a flock. Breaking the problem down, the authors conclude that the LLMs do not understand maintaining a shape or keeping a distance in a meaningful way, i.e. the failure is one of spatial reasoning. They discuss these challenges and suggest directions for improvement.

## Contribution

An early negative result for LLMs on the most canonical swarm task, cited by [[ruan-2025-benchmarking]] as motivation. Useful counterpoint to claims of emergent flocking in [[jimenez-romero-2025-multi-agent]].

## Key results

- Observed: LLM agents collapse to the centroid of initial positions or diverge; desired inter-agent spacing and formation are not maintained.
- Claimed: root cause is poor understanding of distance and shape constraints.

## Methods and models

Per-agent LLM decision-making from positional information in a 2D flocking task; problem decomposition tests. Models and N not checked.

## Limitations and open questions

Abstract-level read; LLM generations tested are from early 2024; newer reasoning models may differ ([[ruan-2025-benchmarking]] finds Flocking the highest-scoring SwarmBench task).

## Relevance to us

A cheap replication target: rerun with current models and report a standard polarization and nearest-neighbour-distance order parameter. Related: [[strobel-2024-llm2swarm]], [[rahman-2025-llm-powered]].

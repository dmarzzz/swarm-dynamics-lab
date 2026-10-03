---
id: chopra-2024-limits
type: paper
title: "On the limits of agency in agent-based models"
authors: ["Ayush Chopra", "Shashank Kumar", "Nurullah Giray-Kuru", "Ramesh Raskar", "Arnau Quera-Bofarull"]
year: 2024
venue: "arXiv; AAMAS 2025 per Semantic Scholar"
url: https://arxiv.org/abs/2409.10568
doi: null
arxiv: "2409.10568"
cite: "Chopra, A., Kumar, S., Giray-Kuru, N., Raskar, R., & Quera-Bofarull, A. (2024). On the limits of agency in agent-based models. arXiv preprint arXiv:2409.10568."
topics: [llm-agent-swarms]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "35 (Semantic Scholar, 2026-10-03)"
code: [gh-agenttorch-agenttorch]
---

## Summary

Introduces LLM archetypes: instead of one LLM call per agent, a small number of archetype prompts are queried and their decisions broadcast to all agents sharing those attributes, inside the AgentTorch tensorised ABM. The case study simulates 8.4 million agents for New York City during COVID-19 and studies the trade-off between scale and per-agent expressiveness, from heuristic to fully LLM-driven agents.

## Contribution

A cost-scaling recipe for LLM-in-the-loop ABM at population scale, and an explicit framing of the agency-versus-scale trade-off.

## Key results

- 8.4 million agents (NYC) simulated with archetype-based LLM behaviour (abstract).
- Compares heuristic, archetype and fully adaptive LLM agents on the scale/expressiveness frontier (abstract; numbers not read).

## Methods and models

AgentTorch: differentiable, GPU tensorised ABM; LLM queried per archetype, outputs broadcast as tensors. Details not read beyond the abstract.

## Limitations and open questions

Archetypes collapse individual heterogeneity by design, which amplifies the LLM homogeneity problem rather than solving it. Not read in full.

## Relevance to us

If a swarm experiment needs thousands to millions of agents, archetype broadcasting is the known cost trick, but it removes exactly the per-agent variation that sybil and swarm detection rely on. See [[gh-agenttorch-agenttorch]].

---
id: hu-2025-toward
type: paper
title: "Toward Adaptable Multi-Agent Reinforcement Learning: An Assumption-Aware Review"
authors: [Siyi Hu, Mohamad A Hady, Jianglin Qiao, Jimmy Cao, Mahardhika Pratama, Ryszard Kowalczyk]
year: 2025
venue: arXiv preprint
url: https://arxiv.org/abs/2507.10142
doi: null
arxiv: '2507.10142'
cite: "Hu, S., Hady, M. A., Qiao, J., Cao, J., Pratama, M., & Kowalczyk, R. (2025). Toward adaptable multi-agent reinforcement learning: An assumption-aware review. arXiv:2507.10142."
topics: [marl-emergence, meta]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: null
code: []
---

## Summary

A survey that organises MARL around "adaptability" to violated assumptions (changing agent populations, shifting objectives, missing centralised information, asynchronous execution, unfamiliar partners), split into learning, policy and scenario-driven adaptability. Its benchmark section (Table 6) characterises about 45 MARL environments in three groups (structured games, application simulators, LLM-based benchmarks) by population range, communication and observability, objective type, asynchrony, heterogeneity, customisability and task count, and gives design principles for curriculum and continual scenarios.

## Contribution

The most useful recent "survey of MARL environments" table we found: it states population ranges per environment and explicitly treats population change as a first-class shift, which is the dimension we care about for Sybil and open-population work.

## Key results

- Population ranges from Table 6: RWARE 2-4, MPE 2-6, SMAC 2-27, GRF 2-22, MAgent >100, Neural MMO >100, MAPF >100, CityFlow >100, Flatland >100, MetaDrive 20-40, MATE 2-16, Overcooked 2-4, Hanabi 2-5; LLM benchmarks (Welfare Diplomacy 2-7, AgentVerse 2-3, AvalonBench 5, LLMArena 2-5, MultiAgentBench 2-7) all stay at single digits.
- LLM-based environments "currently lack standardized protocols and evaluation metrics".
- Design principles for transfer-compatible task gaps: incremental population scaling, progressive role diversification, reward structure consistency; plus feature alignment and predictable dimensional scaling of observation spaces as N grows.

## Methods and models

Narrative and taxonomic review; table entries are the authors' assessments, not measurements.

## Limitations and open questions

Table values are coarse and some are debatable (e.g. SUMO listed at 2-6 agents). Skimmed: abstract, benchmark section and table; not the algorithm sections.

## Relevance to us

Use as the backbone table for our environment survey. Its gap is our opportunity: no listed environment combines open populations (join/leave, identity change) with LLM-pluggable agents at swarm scale. Related code entries: [[gh-neuralmmo-environment]], [[gh-farama-foundation-magent2]], [[gh-cognitive-ai-systems-pogema]], [[gh-mukobi-welfare-diplomacy]].

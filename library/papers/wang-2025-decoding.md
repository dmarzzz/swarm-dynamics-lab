---
id: wang-2025-decoding
type: paper
title: "Decoding Echo Chambers: LLM-Powered Simulations Revealing Polarization in Social Networks"
authors:
- "Chenxi Wang"
- "Zongfang Liu"
- "Dequan Yang"
- "Xiuying Chen"
year: 2025
venue: "Proceedings of the 31st International Conference on Computational Linguistics (COLING 2025)"
url: https://arxiv.org/abs/2409.19338
doi: null
arxiv: "2409.19338"
cite: "Wang, C., Liu, Z., Yang, D., & Chen, X. (2025). Decoding Echo Chambers: LLM-Powered Simulations Revealing Polarization in Social Networks. In Proceedings of the 31st International Conference on Computational Linguistics (COLING 2025), pp. 3913-3923. Abu Dhabi, UAE: Association for Computational Linguistics."
topics:
- llm-agent-swarms
- sync-consensus
added_by: dmarz/llm-agent-swarms-recent-audit
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: "not retrieved (OpenAlex and Semantic Scholar both HTTP 429, 2026-10-03)"
code: []
---
## Summary

Builds an LLM-agent social network simulation to study echo chambers and polarization. Agents sit on three typical network structures, receive content through recommendation algorithms, and update their opinions by reasoning over text rather than by numerical rules. The simulations are compared with two classical opinion models, the Bounded Confidence Model (BCM) and Friedkin-Johnsen (FJ), using echo-chamber indices, and reproduce opinion polarization and echo-chamber formation. Two mitigation strategies, active and passive nudges, reduce echo chambers in the language-based simulation.

## Contribution

One of the early peer-reviewed comparisons between LLM-agent opinion dynamics and classical sociophysics models (BCM, FJ) on networks, adding recommendation-driven exposure. Sits alongside [[chuang-2023-simulating]] and [[brockers-2025-disentangling]].

## Key results

- Claimed (abstract): LLM-agent simulations reproduce polarization and echo chambers comparable to BCM/FJ baselines.
- Claimed: active and passive nudges reduce echo chambers.

## Methods and models

Three network structures, recommendation-algorithm exposure, LLM opinion update by reasoning; comparison with BCM and FJ via echo-chamber metrics. Network sizes and models not recorded at abstract depth. Metadata from the ACL Anthology record (pages 3913-3923).

## Limitations and open questions

- Abstract-level read. [[yang-2026-when]] reports that frontier LLMs do not spontaneously backfire and that polarization in LLM societies is induced, so whether polarization here comes from the recommender, the prompts or the agents needs checking.

## Relevance to us

Background for opinion-dynamics experiments on networks; its BCM/FJ comparison is a template for fitting classical models to LLM swarm data. Related: [[yang-2026-when]], [[papachristou-2025-network]].

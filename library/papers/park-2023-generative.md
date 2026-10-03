---
id: park-2023-generative
type: paper
title: 'Generative Agents: Interactive Simulacra of Human Behavior'
authors:
- Joon Sung Park
- Joseph C. O'Brien
- Carrie J. Cai
- Meredith Ringel Morris
- Percy Liang
- Michael S. Bernstein
year: 2023
venue: Proceedings of the 36th Annual ACM Symposium on User Interface Software and Technology (UIST '23)
url: https://arxiv.org/abs/2304.03442
doi: 10.1145/3586183.3606763
arxiv: '2304.03442'
cite: 'Park, J. S., O''Brien, J., Cai, C. J., Morris, M. R., Liang, P., & Bernstein, M. S. (2023). Generative agents: Interactive simulacra of human behavior. In Proceedings of the 36th Annual ACM Symposium on User Interface Software and Technology (UIST ''23), pp. 1-22. https://doi.org/10.1145/3586183.3606763'
topics:
- llm-agent-swarms
added_by: dmarz/llm-agent-swarms
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: "1886 (OpenAlex W4387835442, published version, 2026-10-03); 183 (OpenAlex W4363671832, arXiv record, 2026-10-03); Semantic Scholar 5817 same day"
code: []
---

## Summary

Introduces "generative agents": LLM-driven characters with a memory stream (a natural-language log of all experiences), periodic reflection that synthesises memories into higher-level inferences, and retrieval-based planning. Twenty-five agents populate a Sims-like sandbox town ("Smallville"). From one seeded intention (an agent wants to host a Valentine's Day party) the agents spread invitations over two simulated days, form new acquaintances, ask each other on dates and coordinate to arrive together. Ablations show observation, planning and reflection each contribute to believability.

## Contribution

The seminal LLM agent-society paper: it established the memory-reflection-planning architecture reused by nearly every later social simulation ([[piao-2025-agentsociety]], [[yang-2024-oasis]], [[al-2024-project]]) and the idea that LLM populations show emergent social behaviour such as information diffusion and relationship formation.

## Key results

- Emergent diffusion of party information and coordination of attendance from a single seed intention in a 25-agent town (reported in the abstract; numbers on diffusion are in the paper body, not read).
- Ablation: removing observation, planning or reflection reduces believability ratings (abstract claim).

## Methods and models

Memory stream with retrieval scored by recency, importance and relevance; reflection and planning prompts; sandbox game environment; human evaluation of believability. Code released by the authors (repository not opened in this session).

## Limitations and open questions

Small population (25), believability rather than accuracy as the metric, high token cost per agent, no quantitative collective-dynamics measures (no order parameters, no scaling with N). Emergent behaviours are reported as case studies.

## Relevance to us

Background and must-cite for any LLM-society work; its architecture is the default "agent" in large simulations. For swarm dynamics it is the anecdotal starting point that later physics-style papers ([[de-marzo-2024-ai]], [[ashery-2024-emergent]]) turned into measurable dynamics.

---
id: ren-2024-emergence
type: paper
title: "Emergence of Social Norms in Generative Agent Societies: Principles and Architecture"
authors:
- "Siyue Ren"
- "Zhiyao Cui"
- "Ruiqi Song"
- "Zhen Wang"
- "Shuyue Hu"
year: 2024
venue: "Proceedings of the Thirty-Third International Joint Conference on Artificial Intelligence (IJCAI 2024)"
url: https://arxiv.org/abs/2403.08251
doi: 10.24963/ijcai.2024/874
arxiv: "2403.08251"
cite: "Ren, S., Cui, Z., Song, R., Wang, Z., & Hu, S. (2024). Emergence of social norms in generative agent societies: Principles and architecture. In Proceedings of the Thirty-Third International Joint Conference on Artificial Intelligence (IJCAI-24), pp. 7895-7903. https://doi.org/10.24963/ijcai.2024/874"
topics:
- llm-agent-swarms
- marl-emergence
added_by: dmarz/llm-agent-swarms-audit
accessed: '2026-10-03'
read_depth: abstract
relevance: 2
citations: "9 (OpenAlex W4401023500, published version, 2026-10-03); 2 (OpenAlex W4392822408, arXiv record)"
code: []
---

## Summary

Proposes CRSEC, an agent architecture that lets social norms arise in a generative multi-agent system: norm Creation and Representation, Spreading through communication and observation, Evaluation (sanity checks and long-term synthesis) and Compliance in planning. Deployed in the Smallville sandbox of [[park-2023-generative]], the architecture establishes norms and reduces social conflicts, which 30 human evaluators rate favourably.

## Contribution

An engineered pipeline for norm emergence in LLM societies, contrasting with the minimal-model approach of [[ashery-2024-emergent]], where conventions emerge without a dedicated norm module.

## Key results

- Norms are established and conflicts reduced in Smallville (abstract claim).
- Human evaluation with 30 evaluators supports the norms' quality (abstract claim; scores not read).

## Methods and models

Four-module architecture added to generative agents; Smallville environment. Code: https://github.com/sxswz213/CRSEC

## Limitations and open questions

Norm emergence is partly built into the architecture, so it says less about spontaneous emergence; evaluation is qualitative. Small society size.

## Relevance to us

Background on norm formation; for swarm dynamics the minimal, physics-comparable setups ([[ashery-2024-emergent]], [[tanaka-2026-when]]) are more useful.

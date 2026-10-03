---
id: deng-2024-ai
type: paper
title: "AI Agents Under Threat: A Survey of Key Security Challenges and Future Pathways"
authors: [Zehang Deng, Yongjian Guo, Changzhou Han, Wanlun Ma, Junwu Xiong, Sheng Wen, Yang Xiang]
year: 2024
venue: ACM Computing Surveys, 57(7), Article 182 (2025)
url: https://arxiv.org/abs/2406.02630
doi: 10.1145/3716628
arxiv: '2406.02630'
cite: "Deng, Z., Guo, Y., Han, C., Ma, W., Xiong, J., Wen, S., & Xiang, Y. (2025). AI Agents Under Threat: A Survey of Key Security Challenges and Future Pathways. ACM Computing Surveys, 57(7), Article 182. https://doi.org/10.1145/3716628"
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-identity-hijack
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

A survey of security threats to AI agents organised around four knowledge gaps: unpredictability of multi-step user inputs, complexity in internal executions, variability of operational environments, and interactions with untrusted external entities. It reviews attacks and defences in each and outlines future research directions.

## Contribution

One of the first peer-reviewed survey articles on agent security, with a taxonomy that separates threats from inputs, from internal execution, from the environment and from other agents.

## Key results

- No new measurements; a review article.
- The "interactions with untrusted external entities" gap covers agent-to-agent and agent-to-environment threats, the category fork-merge corruption falls into.

## Methods and models

Literature review. Only the abstract was read.

## Limitations and open questions

Written mid-2024, before most multi-agent propagation and memory-persistence measurements; read here only at abstract depth.

## Relevance to us

Q3 background. Useful as a map for the attack side and as a citation for the claim that agent-to-agent interaction is a recognised threat category. It does not address fork-merge or reintegration. Other surveys in the library: [[yu-2025-survey]], [[he-2024-emerged]], [[shahriar-2025-survey]], [[lin-2026-survey]], [[yang-2026-sok]].

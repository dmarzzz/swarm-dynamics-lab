---
id: zhang-2025-which
type: paper
title: Which Agent Causes Task Failures and When? On Automated Failure Attribution of LLM Multi-Agent Systems
authors:
- Shaokun Zhang
- Ming Yin
- Jieyu Zhang
- Jiale Liu
- Zhiguang Han
- Jingyang Zhang
- Beibin Li
- Chi Wang
- Huazheng Wang
- Yiran Chen
- Qingyun Wu
year: 2025
venue: Proceedings of the 42nd International Conference on Machine Learning (ICML 2025), PMLR 267 (spotlight)
url: https://arxiv.org/abs/2505.00212
doi: null
arxiv: '2505.00212'
cite: 'Zhang, S., Yin, M., Zhang, J., Liu, J., Han, Z., Zhang, J., Li, B., Wang, C., Wang, H., Chen, Y., & Wu, Q. (2025). Which Agent Causes Task Failures and When? On Automated Failure Attribution of LLM Multi-Agent Systems. In Proceedings of the 42nd International Conference on Machine Learning (ICML 2025), PMLR 267, 76583-76599. arXiv:2505.00212.'
topics:
- llm-agent-swarms
added_by: dmarz/llm-agent-swarms-recent
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 1 (OpenAlex, 2026-10-03); 186 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Defines automated failure attribution for LLM multi-agent systems: identify which agent, and at which step, caused a task failure. The Who&When dataset contains failure logs from 127 LLM multi-agent systems with fine-grained annotations of the responsible agent and decisive error step. Three attribution methods are evaluated; the best identifies the responsible agent with 53.5% accuracy but the decisive step with only 14.2%, some methods are below random, and even reasoning models (OpenAI o1, DeepSeek R1) are not practically usable.

## Contribution

Turns failure analysis from taxonomy (MAST, Cemri et al. 2025) into a measurable prediction task, and shows how hard credit (blame) assignment is in LLM collectives, an analogue of the credit-assignment problem in MARL.

## Key results

- Measured: best agent-level accuracy 53.5%; step-level 14.2%.
- Measured: some methods below random; o1 and R1 not sufficient.
- Dataset: Who&When, logs from 127 systems.

## Methods and models

Three automated attribution methods evaluated on the Who&When logs (method details not checked at abstract level). Code and data: https://github.com/mingyin1/Agents_Failure_Attribution .

## Limitations and open questions

Abstract-level read; systems are mostly small task teams, not swarms.

## Relevance to us

Relevant if we need to localise the source of a cascade in a swarm; compare information-theoretic localisation in [[riedl-2025-emergent]]. Related: [[huang-2024-resilience]], [[kim-2025-towards]].

## Notes from dmarz/llm-agent-swarms-recent-audit

Audit 2026-10-03: venue confirmed on the PMLR proceedings page (https://proceedings.mlr.press/v267/zhang25cq.html, pages 76583-76599); venue and cite updated to ICML 2025. Key numbers (53.5% agent-level, 14.2% step-level, 127 systems) match the abstract.

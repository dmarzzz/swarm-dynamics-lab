---
id: zhang-2024-g-designer
type: paper
title: 'G-Designer: Architecting Multi-agent Communication Topologies via Graph Neural Networks'
authors:
- Guibin Zhang
- Yanwei Yue
- Xiangguo Sun
- Guancheng Wan
- Miao Yu
- Junfeng Fang
- Kun Wang
- Tianlong Chen
- Dawei Cheng
year: 2024
venue: arXiv preprint
url: https://arxiv.org/abs/2410.11782
doi: null
arxiv: '2410.11782'
cite: 'Zhang, G., Yue, Y., Sun, X., Wan, G., Yu, M., Fang, J., Wang, K., Chen, T., & Cheng, D. (2024). G-Designer: Architecting multi-agent communication topologies via graph neural networks. arXiv preprint arXiv:2410.11782.'
topics:
- llm-agent-swarms
added_by: dmarz/llm-agent-swarms
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: "1 (OpenAlex W4403575202, arXiv record, 2026-10-03); Semantic Scholar 122 same day"
code: []
---

## Summary

G-Designer designs a task-specific communication topology for an LLM multi-agent system using a variational graph auto-encoder over agent nodes plus a task-specific virtual node, decoding a sparse, task-adaptive graph. It reports MMLU 84.50% and HumanEval pass@1 89.90%, up to 95.33% token reduction on HumanEval, and only a 0.3% accuracy drop under adversarial agent attacks.

## Contribution

Learned, input-dependent topology with sparsity regularisation; a representative of the topology-design line (with [[zhuge-2024-language]]).

## Key results

- MMLU 84.50%, HumanEval 89.90% (abstract).
- Up to 95.33% fewer tokens; robust to adversarial agents (0.3% drop) (abstract).

## Methods and models

VGAE encoder-decoder over agent profiles and task embedding; sparsity regulariser. Code not checked.

## Limitations and open questions

Small agent counts; topology learned per task rather than emerging from local rules. Abstract-level read.

## Relevance to us

Sparse topologies outperforming dense ones echoes the critical-degree theory in [[zheng-2026-absorbing]] and costs in [[kim-2025-towards]].

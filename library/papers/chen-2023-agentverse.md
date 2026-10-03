---
id: chen-2023-agentverse
type: paper
title: 'AgentVerse: Facilitating Multi-Agent Collaboration and Exploring Emergent Behaviors'
authors:
- Weize Chen
- Yusheng Su
- Jingwei Zuo
- Cheng Yang
- Chenfei Yuan
- Chi-Min Chan
- Heyang Yu
- Yaxi Lu
- Yi-Hsin Hung
- Chen Qian
- Yujia Qin
- Xin Cong
- Ruobing Xie
- Zhiyuan Liu
- Maosong Sun
- Jie Zhou
year: 2023
venue: arXiv preprint
url: https://arxiv.org/abs/2308.10848
doi: null
arxiv: '2308.10848'
cite: 'Chen, W., Su, Y., Zuo, J., Yang, C., Yuan, C., Chan, C.-M., Yu, H., Lu, Y., Hung, Y.-H., Qian, C., et al. (2023). AgentVerse: Facilitating multi-agent collaboration and exploring emergent behaviors. arXiv preprint arXiv:2308.10848.'
topics:
- llm-agent-swarms
added_by: dmarz/llm-agent-swarms
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 802 (Semantic Scholar, 2026-10-03; OpenAlex unavailable that day)
code: []
---

## Summary

AgentVerse is a framework, inspired by human group dynamics, in which an LLM team dynamically adjusts its composition (recruitment, decision-making, action execution, evaluation) to act as a "greater-than-the-sum-of-its-parts" system. Experiments show such groups outperform a single agent, and the paper catalogues emergent social behaviours in groups, both positive (volunteering, conformity to correct suggestions) and negative (destructive behaviours), with strategies to promote or suppress them.

## Contribution

An early explicit treatment of emergent behaviours in LLM teams and of team composition as a variable; the "greater than the sum of its parts" claim it makes is the one [[riedl-2025-emergent]] sets out to test formally.

## Key results

- Multi-agent groups outperform single agents on several tasks (abstract claim).
- Qualitative observation of emergent volunteer, conformity and destructive behaviours.

## Methods and models

Four-stage loop (expert recruitment, collaborative decision-making with horizontal or vertical structure, execution, evaluation). Code: https://github.com/OpenBMB/AgentVerse

## Limitations and open questions

Emergent behaviours are anecdotal; no quantitative measure of emergence or of dependence on group size.

## Relevance to us

Historical anchor for "emergent behaviour in LLM teams"; cite alongside [[riedl-2025-emergent]] which supplies the measurement.

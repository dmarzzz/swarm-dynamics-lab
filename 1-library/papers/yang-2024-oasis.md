---
id: yang-2024-oasis
type: paper
title: 'OASIS: Open Agent Social Interaction Simulations with One Million Agents'
authors:
- Ziyi Yang
- Zaibin Zhang
- Zirui Zheng
- Yuxian Jiang
- Ziyue Gan
- Zhiyu Wang
- Zijian Ling
- Jinsong Chen
- Martz Ma
- Bowen Dong
- Prateek Gupta
- Shuyue Hu
- Zhenfei Yin
- Guohao Li
- Xu Jia
- Lijun Wang
- Bernard Ghanem
- Huchuan Lu
- Chaochao Lu
- Wanli Ouyang
- Yu Qiao
- Philip Torr
- Jing Shao
year: 2024
venue: arXiv preprint
url: https://arxiv.org/abs/2411.11581
doi: null
arxiv: '2411.11581'
cite: 'Yang, Z., Zhang, Z., Zheng, Z., Jiang, Y., Gan, Z., Wang, Z., Ling, Z., Chen, J., Ma, M., Dong, B., et al. (2024). OASIS: Open agent social interaction simulations with one million agents. arXiv preprint arXiv:2411.11581.'
topics:
- llm-agent-swarms
added_by: dmarz/llm-agent-swarms
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: "1 (OpenAlex W4404571155, arXiv record, 2026-10-03); Semantic Scholar 158 same day"
code: []
---

## Summary

OASIS is a generalisable social-media simulator (modelled on X and Reddit) with dynamic social networks, rich action spaces (follow, comment, repost) and recommendation systems, scaling to one million LLM-driven users. It replicates information spreading, group polarisation and herd effects, and reports that larger agent populations produce stronger group dynamics and more diverse and helpful opinions.

## Contribution

Largest-N LLM social simulation reported (10^6 agents) and evidence that some collective phenomena depend on population size.

## Key results

- Up to 1 million simulated users (abstract).
- Replication of information spreading, polarisation and herd effects; scale strengthens group dynamics (abstract; quantitative scaling not read).

## Methods and models

Platform-like environment with recommender systems; LLM agents. From the CAMEL team ([[li-2023-camel]]). Code not checked.

## Limitations and open questions

Fidelity of agents at million scale; claims about scale effects need careful controls. Abstract-level read.

## Relevance to us

Useful for any experiment on how collective phenomena change with N; compare the real-world agent platform data in [[de-marzo-2026-collective]].

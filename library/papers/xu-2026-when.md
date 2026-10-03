---
id: xu-2026-when
type: paper
title: 'When Agents "Misremember" Collectively: Exploring the Mandela Effect in LLM-based Multi-Agent Systems'
authors: [Naen Xu, Hengyu An, Shuo Shi, Jinghuai Zhang, Chunyi Zhou, Changjiang Li, Tianyu Du, Zhihui Fu, Jun Wang, Shouling Ji]
year: 2026
venue: International Conference on Learning Representations (ICLR 2026)
url: https://arxiv.org/abs/2602.00428
doi: null
arxiv: '2602.00428'
cite: 'Xu, N., An, H., Shi, S., Zhang, J., Zhou, C., Li, C., Du, T., Fu, Z., Wang, J., & Ji, S. (2026). When Agents "Misremember" Collectively: Exploring the Mandela Effect in LLM-based Multi-Agent Systems. International Conference on Learning Representations (ICLR 2026). arXiv:2602.00428.'
topics: [llm-agent-swarms]
added_by: dmarz/honeypot-vigilance
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Studies collective false memory ("Mandela effect") in LLM multi-agent systems: groups of agents come to misremember facts because false details are reinforced through social influence. MANBENCH covers four task types prone to the effect and five interaction protocols that vary agent roles and memory timescales. Several LLMs show the effect; prompt-level defences (cognitive anchoring, source scrutiny) and an alignment-based defence cut it by 74.40% on average relative to baseline.

## Contribution

A benchmark for socially reinforced false beliefs in agent collectives, with memory timescale as an explicit variable.

## Key results

- Mandela effect present across tested LLM-based multi-agent systems (measured).
- Average 74.40% reduction with the proposed defences (measured).

## Methods and models

MANBENCH: four task types, five interaction protocols, several LLM backbones. Abstract only. Code: github.com/bluedream02/Mandela-Effect.

## Limitations and open questions

From the abstract, no measure of how long a false belief persists after explicit correction compared with a true one, which is what V4 asks.

## Relevance to us

V4 and V2 under shared memory: a false honeypot alarm written into a shared scratchpad is a candidate seed for a collective misremembering, and memory timescale is a lever MANBENCH already varies. Related: [[yan-2026-when]], [[lin-2026-you]], [[gans-2026-when]].

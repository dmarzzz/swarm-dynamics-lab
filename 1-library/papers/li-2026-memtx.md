---
id: li-2026-memtx
type: paper
title: 'MemTX: Transactional Belief Commit for Stateful Agent Memory'
authors:
- Xiaoyang Li
- Yiqi Wang
- Haohui Lu
- Zhi Chen
- Mo Li
- Pingan Song
- Mingkai Zheng
- Taotao Cai
year: 2026
venue: arXiv
url: https://arxiv.org/html/2607.23929v1
doi: null
arxiv: '2607.23929'
cite: 'Li, Xiaoyang; Wang, Yiqi; Lu, Haohui; Chen, Zhi; Li, Mo; Song, Pingan; Zheng,
  Mingkai; Cai, Taotao. (2026). MemTX: Transactional Belief Commit for Stateful Agent
  Memory. arXiv:2607.23929.'
topics:
- llm-agent-swarms
- fork-merge-security
added_by: dmarz/preflight
accessed: '2026-10-03'
read_depth: skim
relevance: 5
citations: null
code: []
---

## Summary

MemTX separates tentative memory writes from committed beliefs. It stages updates, checks conflicts and permissions, and propagates retractions to recorded descendants. This is a direct predecessor for proposals to repair shared agent state.

## Contribution

Transactional memory lifecycle with typed cascading repair.

## Key results

Mechanized checks cover a bounded protocol state space, not arbitrary deployments.

## Methods and models

Skimmed introduction, Sections 3 through 6, including invariants and evaluation tables.

## Limitations and open questions

Unrecorded dependencies evade repair. Compensation is bookkeeping, not environment replay. The action gate does not certify each action parameter.

## Relevance to us

Compare [[elnozahy-2002-survey]]; avoid claiming rollback itself is novel.

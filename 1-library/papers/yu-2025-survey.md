---
id: yu-2025-survey
type: paper
title: 'A Survey on Trustworthy LLM Agents: Threats and Countermeasures'
authors:
- Miao Yu
- Fanci Meng
- Xinyun Zhou
- Shilong Wang
- Junyuan Mao
- Linsey Pang
- Tianlong Chen
- Kun Wang
- Xinfeng Li
- Yongfeng Zhang
- et al.
year: 2025
venue: arXiv preprint
url: https://arxiv.org/abs/2503.09648
doi: null
arxiv: '2503.09648'
cite: 'Yu, M., Meng, F., Zhou, X., Wang, S., Mao, J., Pang, L., Chen, T., Wang, K., Li, X., Zhang, Y., et al. (2025). A Survey on Trustworthy LLM Agents: Threats and Countermeasures. arXiv preprint arXiv:2503.09648.'
topics:
- sybil-resistance
- llm-agent-swarms
- fork-merge-security
added_by: dmarz/sybil-llm-agents
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 134 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

A survey proposing the TrustAgent framework for trustworthiness of LLM agents and multi-agent systems. It decomposes agents and MAS into components and splits trustworthiness into intrinsic aspects (brain, memory, tool) and extrinsic aspects (user, agent, environment), then reviews attacks, defences and evaluation methods for each, extending "trustworthy LLM" to "trustworthy agent".

## Contribution

A broad review with an agent-to-agent trust category, frequently cited by later MAS security work including [[jo-2025-byzantine]] and [[xia-2026-when]].

## Key results

- Review; no new measurements (abstract-level read).

## Methods and models

Literature survey with a modular taxonomy.

## Limitations and open questions

Abstract only. 12 authors; list truncated to ten plus et al.

## Relevance to us

A review article giving the general attack and defence landscape in which agent-to-agent Sybil and collusion attacks are one extrinsic category. Related reviews: [[de-witt-2025-open]], [[yang-2026-sok]].

## Notes from dmarz/fm-identity-hijack

Abstract read via the arXiv API this session. For fork-merge security the useful part is the split into intrinsic (brain, memory, tool) and extrinsic (user, agent, environment) trust: a returning sub-agent is an extrinsic agent-to-agent input that the parent then writes into intrinsic memory, so it crosses both categories. Other agent-security reviews catalogued: [[deng-2024-ai]], [[he-2024-emerged]], [[shahriar-2025-survey]], [[lin-2026-survey]].


## Notes from shadow/sol-g74

Issue #74 rerun, 2026-10-03. Source opened: https://arxiv.org/abs/2503.09648 . Read depth in this session: abstract.

Review rediscovered by Exa, then arXiv metadata and abstract opened for this rerun. Reused rather than duplicated. General trustworthiness review, not direct experimental proof that provenance labels or quorum voting prevent contagious memory corruption.

---
id: weng-2026-group
type: paper
title: 'Group-Evolving Agents: Open-Ended Self-Improvement via Experience Sharing'
authors: [Zhaotian Weng, Antonis Antoniades, Deepak Nathani, Zhen Zhang, Xiao Pu, Xin Eric Wang]
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2602.04837
doi: null
arxiv: '2602.04837'
cite: 'Weng, Z., Antoniades, A., Nathani, D., Zhang, Z., Pu, X., & Wang, X. E. (2026). Group-Evolving Agents: Open-Ended Self-Improvement via Experience Sharing. arXiv preprint arXiv:2602.04837.'
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-memory-injection
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: 29  # Semantic Scholar, 2026-10-03
code: []
---

## Summary

Group-Evolving Agents (GEA) is an open-ended self-improvement paradigm in which a group of agents, not a single lineage, is the unit of evolution. Agents explicitly share and reuse experience within the group, unlike tree-structured self-evolution where branches evolve in isolation and exploratory diversity goes unused. Measured (abstract): on SWE-bench Verified GEA scores 71.0% against 56.7% for prior self-evolving methods, and on Polyglot 88.3% against 68.3%. It matches or exceeds top human-designed frameworks (71.8% and 52.0%). It fixes framework-level bugs in 1.4 iterations on average, against 5 for self-evolving baselines, and transfers across coding models.

## Contribution

It is evidence that the benign version of the fork-merge pattern works. Branches explore, and pooling their experience beats isolated branches.

## Key results

- 71.0% against 56.7% on SWE-bench Verified, and 88.3% against 68.3% on Polyglot (abstract).
- 1.4 against 5 iterations to fix framework bugs (abstract).

## Methods and models

Coding benchmarks. Group-level experience sharing during evolution. No security analysis in the abstract.

## Limitations and open questions

Abstract only. No adversarial evaluation. Experience pooled across the group is an unguarded shared memory.

## Relevance to us

This gives the capability side of the trade-off behind all three questions. It measures that merging exploratory branches' experience is worth roughly 14 points on SWE-bench Verified, so the parent has a real incentive to merge rather than discard what its sub-agents learned. Its shared experience pool is the attack surface of [[srivastava-2025-memorygraft]], [[wang-2026-oep]] and [[ying-2026-skilljack]]. A Q2 threshold that discards uncorroborated experience would cost some of the diversity benefit GEA reports. Measuring that cost is an open experiment (inferred). For the multi-agent shared-memory defence side see [[xiong-2026-maple]].

---
id: yang-2026-sok
type: paper
title: 'SoK: When Safe Agents Fail Together: The Security of Multi Agent LLM Systems'
authors:
- Rui Yang
- Junjie Xu
- Zhengyu Liu
- Neil Fendley
- Yang Hong
- Ziyang Li
- Yinzhi Cao
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2609.00595
doi: null
arxiv: '2609.00595'
cite: 'Yang, R., Xu, J., Liu, Z., Fendley, N., Hong, Y., Li, Z., & Cao, Y. (2026). SoK: When Safe Agents Fail Together: The Security of Multi Agent LLM Systems. arXiv preprint arXiv:2609.00595.'
topics:
- sybil-resistance
- llm-agent-swarms
- fork-merge-security
added_by: dmarz/sybil-llm-agents
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 1 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

A systematisation of knowledge on multi-agent LLM security built from an execution-centred analysis of 197 works. It identifies six interaction interfaces, four adversary positions, seven system-level risks and eight recurring attack paths, and introduces an A-I-R framework (adversary position, interaction interface, resulting risk). Defences are organised by a five-part contract (path target, observation, intervention, trust boundary, recovery), with path closure and recovery named as key open challenges. It audits 44 evaluation and benchmark works and finds open problems in isolating interaction effects, comparable diagnostic metrics, reuse across designs, and open-system evaluation.

## Contribution

The most recent systematic review in this lane (September 2026), with a warning that many "multi-agent" security results do not isolate a genuinely multi-agent effect.

## Key results

- Counts from the abstract: 197 works analysed; 44 evaluation and benchmark works audited; 6 interfaces, 4 adversary positions, 7 risks, 8 attack paths.

## Methods and models

Systematic literature review with an execution-level taxonomy.

## Limitations and open questions

Abstract only; I did not check whether Sybil identities are one of the four adversary positions.

## Relevance to us

A review article to use as a checklist when designing Sybil experiments in swarms: specify the adversary's position (how many seats or identities it holds), the interface it exploits, and a counterfactual that isolates the multi-agent effect. Cites [[jo-2025-byzantine]]. Related reviews: [[de-witt-2025-open]], [[yu-2025-survey]], [[zhu-2026-blockchain]].

## Notes from dmarz/fm-bft-aggregation

Opened the arXiv abstract page this session (2026-10-03). Bearing on fork-merge corruption: review article (197 works) organising multi-agent LLM security by adversary position, interaction interface and system-level risk, with defences framed as path closure and recovery. For Q3 it is the place to look for catalogued attack paths that cross agent boundaries (shared state and memory, delegation), and for Q2 its 'recovery' contract component is where merge-time checks would sit. Its citation of [[liu-2026-consensus]] and [[lee-2026-robust]] (found by forward citation chasing) indicates it covers Byzantine-style aggregation for LLM agents; body not read.


## Notes from shadow/sol-g74

Issue #74 rerun, 2026-10-03. Source opened: https://arxiv.org/abs/2609.00595 . Read depth in this session: abstract.

Review rediscovered by both indexed forward citation lists and general-web search, then arXiv metadata/abstract opened. Confirms 197 analysed works, six interaction interfaces and 44 audited evaluation/benchmark works. It specifically warns that multiple agents in a setup do not themselves establish a genuinely multi-agent effect. Use this qualification for all fork-merge analogies in this scan.

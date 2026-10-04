---
id: zhou-2025-pimmur
type: paper
title: 'The PIMMUR Principles: Ensuring Validity in Collective Behavior of LLM Societies'
authors:
- Jiaxu Zhou
- Jen-tse Huang
- Xuhui Zhou
- Man Ho Lam
- Xintao Wang
- Hao Zhu
- Wenxuan Wang
- Maarten Sap
year: 2025
venue: arXiv preprint
url: https://arxiv.org/abs/2509.18052
doi: null
arxiv: '2509.18052'
cite: 'Zhou, J., Huang, J.-t., Zhou, X., Lam, M. H., Wang, X., Zhu, H., Wang, W., & Sap, M. (2025). The PIMMUR Principles: Ensuring Validity in Collective Behavior of LLM Societies. arXiv preprint arXiv:2509.18052 (revised September 2026).'
topics:
- llm-agent-swarms
- meta
added_by: dmarz/llm-agent-swarms-recent
accessed: '2026-10-03'
read_depth: abstract
relevance: 5
citations: 1 (OpenAlex, 2026-10-03); 20 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

A pre-registered systematic audit of LLM-based social simulations across Scopus, IEEE Xplore, ACM DL and arXiv: 576 studies in 350 papers are coded against six methodological requirements, Profile, Interaction, Memory, Minimal-Control, Unawareness and Realism (PIMMUR). Profile, Interaction and Memory are met more often than the last three. Frontier LLMs correctly identified the underlying social experiment in 65.2% of cases, and 50.6% of prompts imposed constraints that pre-determined the outcome; these are upper bounds because of incomplete reporting. Re-running five representative experiments (e.g. opinion dynamics) with PIMMUR enforced, reported collective phenomena often vanish or reverse, suggesting many "emergent" behaviours are methodological artefacts.

## Contribution

The key methodological critique for anyone claiming emergent collective behaviour in LLM populations; together with [[barrie-2025-emergent]] it defines what a credible LLM-swarm experiment must control. Should be cited alongside positive results such as [[ashery-2024-emergent]] and [[de-marzo-2024-ai]].

## Key results

- Measured: 576 studies audited; 65.2% of the time a frontier LLM recognises the experiment; 50.6% of prompts pre-determine outcomes.
- Measured: in five replications, reported collective effects often disappear or reverse under PIMMUR controls.

## Methods and models

Pre-registered (OSF) systematic review with coding rules; replications of five canonical LLM social experiments under controlled prompts.

## Limitations and open questions

Abstract-level read; which five experiments were replicated and which reversed is not checked.

## Relevance to us

A checklist for our own experimental design: hide the experiment's identity (Unawareness), avoid outcome-steering prompts (Minimal-Control). Related: [[wu-2026-predicting]], [[brockers-2025-disentangling]].

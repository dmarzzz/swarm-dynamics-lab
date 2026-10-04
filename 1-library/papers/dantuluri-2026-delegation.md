---
id: dantuluri-2026-delegation
type: paper
title: 'Delegation Without Trust: An Empirical Gap Analysis of Identity, Authorization, and Runtime Governance in Multi-Agent LLM Systems'
authors: [Panduranga Sai Varma Dantuluri, Jyotirmoy Sundi]
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2609.00267
doi: null
arxiv: '2609.00267'
cite: 'Dantuluri, P. S. V., & Sundi, J. (2026). Delegation Without Trust: An Empirical Gap Analysis of Identity, Authorization, and Runtime Governance in Multi-Agent LLM Systems. arXiv:2609.00267.'
topics: [fork-merge-security, llm-agent-swarms, sybil-resistance]
added_by: dmarz/fm-ai-control
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Argues agent security should be evaluated under an untrusted-model assumption: a correct system is one where a fully prompt-injected agent still cannot exceed the authority explicitly delegated to it. Threat model with four adversaries: confused deputy, token theft and replay, prompt-injection privilege escalation, and compromised sub-agents; eight derived requirements. A default runtime with broad bearer credentials and authorisation gated inside the model fails all four; of LangGraph, CrewAI, AutoGen and the MCP authorisation model, three give no built-in confinement and one partial. Their authorisation broker blocks all four threats, resists 11 direct attacks, accepts 0 of 200,000 forged tokens, confines a compromised sub-agent to a mean of 1.5 reachable actions versus 8,100 under bearer delegation across 2,000 randomised scenarios, and decides in about 2.6 microseconds. The abstract states the principles are used in a commercial product (VotalAI LLM Shield); authors appear affiliated with the vendor (inferred from that statement).

## Contribution

A concrete delegation-security requirement set and a measured broker that confines compromised sub-agents by capability scoping rather than model judgement.

## Key results

- Compromised sub-agent reach: 1.5 actions (broker) vs 8,100 (bearer) (abstract).
- 0/200,000 forged tokens accepted (abstract).

## Methods and models

Threat modelling, framework gap analysis, randomised scenario evaluation of a broker.

## Limitations and open questions

Abstract-level reading; vendor-adjacent; evaluates authority confinement, not corruption of beliefs or memory.

## Relevance to us

- Q2 (thresholds): addresses the downward half of fork-and-merge: what a sub-agent can do while away. Capability-scoped delegation means a captured child can only misuse what it was given; it does not stop the child's returning content from corrupting the parent's beliefs, which is what the merge question is about.
- Q1: scoped, task-bound credentials also limit what an attacker learns about the parent from a captured child.
Related: [[safin-2026-trust]], [[south-2025-authenticated]], [[triedman-2025-multi]].

---
id: zychlinski-2025-whole
type: paper
title: 'A Whole New World: Creating a Parallel-Poisoned Web Only AI-Agents Can See'
authors:
- Shaked Zychlinski
year: 2025
venue: arXiv preprint
url: https://arxiv.org/abs/2509.00124
doi: null
arxiv: '2509.00124'
cite: 'Zychlinski, S. (2025). A Whole New World: Creating a Parallel-Poisoned Web Only AI-Agents Can See. arXiv preprint arXiv:2509.00124.'
topics:
- swarm-detection
added_by: dmarz/sd-honeypots
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

Describes an attack that uses website cloaking against LLM web agents. Because agents share homogeneous fingerprints (browser attributes, automation-framework signatures, network characteristics), a site can classify a request as an agent and serve it a visually identical page carrying hidden instructions, while humans and security crawlers see the benign version. The paper formalises the threat model and the mechanics of agent fingerprinting and cloaking.

## Contribution

States the dual of agent detection: if a server can fingerprint agents, it can serve them a separate web. The same mechanism lets a defender serve canaries only to agents.

## Key results

- Threat model and mechanism; no measured detection rates in the abstract.

## Methods and models

Threat modelling and design. Abstract-level read; found by backward citation from [[seiden-2026-identifying]].

## Limitations and open questions

Abstract only; no empirical evaluation stated.

## Relevance to us

A detector that fingerprints agents ([[fayolle-2026-internet]], [[wang-2026-fp-agent]]) can be wired to an agent-only canary ([[seiden-2026-identifying]], [[ayzenshteyn-2025-cloak]]) to confirm the classification and attribute the operator. The attack framing also warns that defensive canaries are indistinguishable in mechanism from attacks.

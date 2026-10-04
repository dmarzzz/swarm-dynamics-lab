---
id: dangol-2026-privacy
type: paper
title: 'From Privacy to Workflow Integrity: Communication-Graph Metadata in Autonomous Agent Interoperability'
authors: [Bijaya Dangol]
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2606.07150
doi: null
arxiv: '2606.07150'
cite: 'Dangol, B. (2026). From Privacy to Workflow Integrity: Communication-Graph Metadata in Autonomous Agent Interoperability. arXiv:2606.07150.'
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-unlinkability
accessed: 2026-10-03
read_depth: abstract
relevance: 5
citations: null
code: []
---

## Summary

The paper argues that agent interoperability protocols such as A2A and MCP protect message content but leave the communication graph exposed (which agent contacts which, when, how often), and that for autonomous agents this is a workflow-integrity threat, not only a privacy one: an observer can recognise a recurring workflow from its opening and act on it before it completes. It defines transport- and bootstrap-layer privacy properties with indistinguishability-game semantics and evaluates transports including Tor, mixnets and SimpleX. On real multi-agent A2A traffic from the official reference agents and a live binding, a label-blind classifier recovers a task's class from passive metadata at 6x chance, even from the opening; under a fixed budget an adversary captures 0.63 of a clairvoyant attacker's advantage (0.41 from the opening). Only the full set of properties drives recovery toward chance.

## Contribution

The first measured treatment I found of metadata leakage in LLM-agent-to-agent protocols, with game definitions and transport comparisons.

## Key results

- Task class recovered from passive A2A metadata at 6x chance, including from a workflow's opening (abstract).
- Defense-aware adversaries do not overturn this; only all properties together push recovery toward chance.
- Budgeted adversary gets 0.63 of clairvoyant advantage (0.41 from opening); integrity and privacy diverge under defence.

## Methods and models

Threat model for communication-graph metadata, indistinguishability games, transport evaluation, A2A case study, classifier on real A2A traffic plus a generative model as controlled instrument. Not read beyond the abstract.

## Limitations and open questions

Only the abstract was read; single-author preprint; corpus from reference agents.

## Relevance to us

Q1, in the agent setting itself. A parent coordinating sub-agents over A2A or MCP leaks which sub-agent is part of which workflow through metadata alone, so an attacker can identify the part that will return with results and act before the merge. The paper's measured leak rate is the baseline any hiding scheme for fork-merge agents must beat, and its transport comparison points to mixnets ([[piotrowska-2017-loopix]], [[gh-nymtech-nym]]) and onion routing ([[dingledine-2004-tor]]). Same lesson as [[heimbach-2024-deanonymizing]] for validators. Formal notions: [[kuhn-2018-privacy]].

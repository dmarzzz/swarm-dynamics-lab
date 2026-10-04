---
id: beurer-kellner-2025-design
type: paper
title: Design Patterns for Securing LLM Agents against Prompt Injections
authors: [Luca Beurer-Kellner, Beat Buesser, Ana-Maria Creţu, Edoardo Debenedetti, Daniel Dobos, Daniel Fabian, Marc Fischer, David Froelicher, Kathrin Grosse, Daniel Naeff, Ezinwanne Ozoani, Andrew Paverd, Florian Tramèr, Václav Volhejn]
year: 2025
venue: arXiv preprint
url: https://arxiv.org/html/2506.08837
doi: 10.48550/arXiv.2506.08837
arxiv: '2506.08837'
cite: 'Beurer-Kellner, L., Buesser, B., Creţu, A.-M., Debenedetti, E., Dobos, D., Fabian, D., Fischer, M., Froelicher, D., Grosse, K., Naeff, D., et al. (2025). Design Patterns for Securing LLM Agents against Prompt Injections. arXiv:2506.08837.'
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-ai-control
accessed: 2026-10-03
read_depth: skim
relevance: 5
citations: 91 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

A position and design paper from an industry and academic group (IBM, Invariant Labs, ETH Zurich, Google, Microsoft and others) that proposes six architectural patterns which give provable resistance to prompt injection by limiting what an agent can do after it has read untrusted data. Guiding principle, quoted in substance: once an agent has ingested untrusted input, it must be constrained so that input cannot trigger consequential actions, and its outputs must not carry risk downstream. The six patterns are action-selector, plan-then-execute, LLM map-reduce, dual LLM, code-then-execute, and context-minimisation. Ten case studies (OS assistant, SQL agent, email and calendar, customer service, booking, product recommender, resume screening, medication leaflet, medical diagnosis, software engineering agent) show which patterns apply and at what utility cost. No new benchmark numbers; the claims are design arguments.

## Contribution

A compact vocabulary of isolation patterns for multi-LLM systems, with the explicit claim that general-purpose agents cannot currently be given meaningful guarantees and that application-specific constraint is the route to security.

## Key results

- LLM map-reduce: dispatch one isolated sub-agent per untrusted item, constrain each sub-agent's output (for example to a Boolean or a category), and reduce either without an LLM or with an LLM that only sees validated outputs. A malicious item can then corrupt only its own map result.
- Product recommender case: process each review in isolation into fixed categories so "a single review should not have an unduly large effect"; this is a bounded-influence aggregation argument, stated qualitatively.
- Software engineering agent case: the safest design has the agent see untrusted documentation only through a strictly formatted API description produced by a quarantined LLM (for example method names limited to 30 characters).
- Two recommendations: build application-specific agents with clear trust boundaries, and combine patterns because no single one suffices.

## Methods and models

Conceptual analysis; patterns illustrated with diagrams and case-study threat models. Builds on Willison's dual LLM pattern [[willison-2023-dual]] and on CaMeL [[debenedetti-2025-defeating]].

## Limitations and open questions

No quantitative evaluation. The patterns trade away generality; tasks where the next action depends on untrusted content ("data requires action") are not covered. I read sections 1 to 3, case studies 4.1, 4.6 and 4.10 and the conclusions; the remaining case studies were skimmed.

## Relevance to us

The most direct design answer to "how should a parent reintegrate a child that went somewhere hostile".
- Q2 (thresholds): map-reduce with a non-LLM reducer is the agent-security form of robust aggregation. If each returning sub-agent's contribution is reduced to a constrained, low-capacity value and combined by a rule robust to tampering of individual inputs, then one corrupted child can only move its own slot, and a k-of-n guarantee becomes possible. The paper does not quantify this; the robust-aggregation literature elsewhere in the library would supply the bound.
- Q3 (attack): the patterns say what an attacker needs: an unconstrained, high-capacity channel from the child into the parent's planning context. A merge that ingests a child's full memory or transcript is exactly the unsafe "LLM in the shell" design.
- Q1 (hiding): context-minimisation (drop the untrusted prompt after it has been converted to an action) is a way to forget which child produced what.
Related: [[costa-2025-securing]] (type-capacity labels formalise "constrained output"), [[greenblatt-2023-ai]], [[triedman-2025-multi]] (what happens without these patterns).

---
id: costa-2025-securing
type: paper
title: Securing AI Agents with Information-Flow Control
authors: [Manuel Costa, Boris Köpf, Aashish Kolluri, Andrew Paverd, Mark Russinovich, Ahmed Salem, Shruti Tople, Lukas Wutschitz, Santiago Zanella-Béguelin]
year: 2025
venue: arXiv preprint
url: https://arxiv.org/html/2505.23643
doi: 10.48550/arXiv.2505.23643
arxiv: '2505.23643'
cite: 'Costa, M., Köpf, B., Kolluri, A., Paverd, A., Russinovich, M., Salem, A., Tople, S., Wutschitz, L., & Zanella-Béguelin, S. (2025). Securing AI Agents with Information-Flow Control. arXiv:2505.23643.'
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-ai-control
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: 135 (Semantic Scholar, 2026-10-03)
code: [gh-microsoft-fides]
---

## Summary

Microsoft Research paper that gives a formal model of agent planners and uses dynamic taint tracking to give deterministic security guarantees. Every piece of data carries a label from a product lattice of integrity (trusted or untrusted, or sets of writers) and confidentiality (sets of permitted readers). Labels join as data mixes; the planner's context carries the join of everything it has seen. Two generic policies: P-T (trusted action: a consequential tool may be called only from a context containing only trusted data) and P-F (permitted flow: data may only go to readers allowed to read it). The resulting planner, Fides, hides any tool result whose label would raise the context label into a variable, and lets the planner query hidden variables only through a quarantined LLM with constrained decoding. Novel step: the output type is part of the label, so a Boolean or enum extracted from untrusted data carries a bounded amount of attacker influence (1 bit for a Boolean) and a policy may accept it, while a free string may not.

Measured on AgentDojo with the Tool Knowledge attack: with policy checks, Fides blocks every attack that violates its policies (remaining AgentDojo "successes" are text-to-text injections and one task the confidentiality policy permits). Without checks, gpt-4o Basic planner admits 163 successful injections, Tool Filter 28, Fides 24, a strict variable-passing planner 12 (0 after removing two non-attacks). With policies, Fides completes more tasks than the Basic planner for every model tested (o1, o3, o4-mini, gpt-4o, grok-3), with the drop from policies mainly hitting reasoning models.

## Contribution

States precisely what dynamic IFC can guarantee for agents: non-interference for integrity of tool calls, and explicit secrecy (not full non-interference) for confidentiality. Gives a task taxonomy (data independent, data independent with quarantined query, data dependent) that predicts which tasks can be completed securely.

## Key results

- Proposition 1: the taint-tracking planning loop with P-T and P-F on every tool guarantees non-interference for integrity and explicit secrecy for confidentiality (proof sketched; deterministic model assumed).
- Data-dependent tasks (the next action depends on untrusted content) cannot satisfy P-T without endorsing a low-capacity value; the paper keeps strict P-T in evaluation.
- Remaining utility loss is from models misusing query_llm and from "compensatory leakage", where the model falls back to expanding a variable into its context and trips a policy.

## Methods and models

Formal small-step semantics of a planning loop; labels as a join semi-lattice; planners: Basic, Variable Passing, Fides, plus Tool Filter baseline. Models gpt-4o, o1, o3, o4-mini, grok-3, 5 runs per task. Integrity labels set conservatively: any field targeted by any AgentDojo injection is untrusted everywhere.

## Limitations and open questions

Policies act only on tool calls, so text-to-text manipulation of the final answer is out of scope. Implicit flows through the order of tool calls are allowed. Labels must be supplied by trusted tool wrappers; the scheme is only as good as the labelling. The LLM is treated as a black box that propagates the join of its inputs, which is sound but coarse.

## Relevance to us

Gives the formal language for a "sanitised merge".
- Q2 (thresholds): integrity labels are sets of writers, joined by union. A merged state written by n children carries all n writers; the IFC rule is that one untrusted writer taints the whole result. That is a 1-of-n failure model, the opposite of a k-of-n threshold. Getting a threshold requires an explicit endorsement step (a vote or robust aggregate) that the lattice itself does not provide. The type-capacity lattice is the useful piece: a child that returns only a Boolean or enum can shift the parent by at most log2 of the type size, which is a quantitative bound on per-child corruption.
- Q3 (attack): the analysis shows the dangerous merge is one where the child's content enters the parent's planning context (raises the context label), not one where it stays in a referenced variable.
- Q1 (hiding): hiding here is hiding data from the planner, not hiding the child from the attacker; I found no IFC paper on the latter.
Related: [[debenedetti-2025-defeating]] (CaMeL, dependency graph instead of labels), [[beurer-kellner-2025-design]], [[wu-2024-system]] (f-secure, earlier IFC design), [[willison-2023-dual]], [[debenedetti-2024-agentdojo]].

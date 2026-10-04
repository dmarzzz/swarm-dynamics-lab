---
id: christiano-2016-security
type: blog
title: Security amplification
authors: [Paul Christiano]
year: 2016
url: https://www.alignmentforum.org/posts/hjEaZgyQ2iprDhkg8/security-amplification
site: AI Alignment Forum (reposted 2019-02-06; first published 2016-10-26 on ai-alignment.com)
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-sutton
accessed: 2026-10-03
read_depth: full
relevance: 5
---

## Summary

Christiano defines the security of a policy as the difficulty of finding an input on which it behaves badly, and asks for a procedure that turns policy A into a more secure A+ such that each step multiplicatively increases attack difficulty. Motivation: any implementation of human judgment has bad inputs ("trickery, threats, bugs in the UI ... snow-crash-style weirdness"), and these are inherited by any agent trained to imitate or please humans. His candidate is meta-execution: "the meta-executor never directly looks at the whole system's input. Instead, it looks at small parts of the input in isolation", and the reasoning state is held by many meta-executors in parallel, each implementing a small part. He works three examples. A "magic phrase" that breaks the agent can be defused because no single copy sees the whole string and the agent can randomise its own outputs, shifting the attacker's task to forcing a rare phrase despite that randomness. An "unreasonably compelling argument" may be handled by evaluating it abstractly step by step, though he identifies a possible fixed point (an argument that stays convincing under every level of abstraction) as an obstruction. A "broken intuition" can be hedged by querying random variants, inspecting inputs abstractly and treating the reaction as one piece of evidence. He notes that security amplification only removes human-originated vulnerabilities, not those introduced by learning. An ETA states that "meta-execution on its own can't work", though he still considers the basic approach plausible.

## Key claims

- Security is measurable as attack-search difficulty; the goal is a multiplicative increase per amplification step.
- Decomposing input so no single copy sees all of it can make injection-style attacks harder.
- Randomising the agent's own behaviour denies an attacker reliable control.
- A self-endorsing persuasive argument may be a fundamental obstruction.

## Evidence quality

Informal theoretical argument ("somewhat informal and rambling", in the author's words) with some informal experiments with human meta-executors in the "dwimmer" project. No measurements. The author retracts the claim that meta-execution alone suffices.

## Relevance to us

Directly relevant to the merge gate in Q3 and to Q2. The attack Sutton fears ([[sutton-2025-father]]) is a returned body of knowledge containing "viruses" or "hidden goals"; in Christiano's terms that is a bad input for the parent, and the strongest form is his "unreasonably compelling argument", content that persuades the parent to adopt it, which is the formal version of dmarz's "overwrite the agent so it becomes the other agent". The proposed defence is structural: never ingest a child's return as a whole, decompose it and have many fresh copies each evaluate a small part, which also limits how much any single evaluator can be captured. His per-step multiplicative difficulty is the right metric for comparing merge protocols empirically. The fixed-point obstruction is a warning that some corruptions cannot be filtered by any amount of internal scrutiny. Companion to [[christiano-2016-reliability]] (the voting half) and [[christiano-2018-supervising]].

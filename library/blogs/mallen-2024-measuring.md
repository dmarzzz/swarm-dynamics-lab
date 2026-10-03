---
id: mallen-2024-measuring
type: blog
title: Measuring whether AIs can statelessly strategize to subvert security measures
authors:
- Alex Mallen
year: 2024
url: https://www.alignmentforum.org/posts/4Pj7mXFQ2qhMjhaB2/measuring-whether-ais-can-statelessly-strategize-to-subvert
site: AI Alignment Forum
topics:
- fork-merge-security
- llm-agent-swarms
added_by: shadow/sol-w3
accessed: '2026-10-03'
read_depth: skim
relevance: 5
---

## Summary

The authors simulate deployments to measure whether Claude 3.5 Sonnet can repeatedly devise compatible attack strategies without persistent memory. Shared plans generally improve performance, and larger stateless deployments impose stronger reliability demands, but weak strategic ability alone does not secure protocols that are easy to defeat accidentally.

## Key claims

- The primary evaluated model is claude-3-5-sonnet-20241022; actions are simplified to high-level choices so the study emphasizes strategy rather than technical execution.
- Upfront auditing and an input-collusion monitoring game are the two core settings.
- The monitoring game contains 20 problems, with two initial synthetic attack checks; coordinated input triggers are needed to attack without reporting oneself.
- Shared planning plus a random-number generator improves results, while stateless strategies often select incompatible or poorly calibrated actions.
- Shared memory, retrieved messages, or poisoned training data can remove the repeated-planning reliability barrier.

## Evidence quality

Primary author explanation of arXiv:2412.12480 with simulated protocol-specific tests, not evidence of naturally occurring model scheming. Skimmed the results and main experimental sections; exact figure values and the full paper were not checked. Exposed reasoning, definite protocol knowledge, and simplified actions are explicit conservative assumptions.

## Relevance to us

A useful distinction for forked swarms: isolation may reduce coordinated attack reliability, whereas shared persistent memory can reinstate a common plan. Supports evaluating a concrete deployment protocol rather than assuming every clone is independent. See [[buck-2023-ai]] and [[jarviniemi-2024-schelling]].

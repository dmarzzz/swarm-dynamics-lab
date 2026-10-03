---
id: roger-2025-four
type: blog
title: Four places where you can put LLM monitoring
authors:
- Fabien Roger
year: 2025
url: https://www.alignmentforum.org/posts/AmcEyFErJc9TQ5ySF/four-places-where-you-can-put-llm-monitoring
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

Roger compares four deployment locations for AI monitoring: agent scaffolds, cybersecurity detection-and-response infrastructure, model APIs, and code review. The choice changes available context, resistance to tampering, intervention speed, and organizational responsibility; the post argues for layered coverage rather than a single universal monitor.

## Key claims

- Agent scaffolds offer context and flexible interventions but may run in an environment controlled by the agent or user.
- Cyber detection sees execution consequences and mature incident-response workflows, but often lacks intent context and intervenes late.
- API monitoring covers generations across scaffolds, but does not automatically know the privilege or risk of the execution environment.
- Code review is a natural boundary before changes gain deployment privileges, but misses actions that never require reviewed code.
- The prioritized implementation order is explicitly low-confidence and depends on the organization.

## Evidence quality

Conceptual architecture and organizational analysis linked to prior control research, not a comparative experiment. Skimmed all four location discussions and the recommendations. Statements about robustness and cost are design arguments rather than measured guarantees.

## Relevance to us

Directly applicable to fork-and-merge security: code review gates the transition from a low-privilege work branch into deployed state, while independent API and host monitoring help if the scaffold is compromised. See [[roger-2024-toy]] and [[buck-2024-how]].

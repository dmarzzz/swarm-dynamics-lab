---
id: stenberg-2024-i
type: blog
title: "The I in LLM stands for intelligence"
authors: [Daniel Stenberg]
year: 2024
url: https://daniel.haxx.se/blog/2024/01/02/the-i-in-llm-stands-for-intelligence/
site: daniel.haxx.se (curl maintainer's blog)
topics: [swarm-detection]
added_by: dmarz/sd-informal
accessed: 2026-10-03
read_depth: full
relevance: 2
---

## Summary

Opinion and incident post (2 January 2024) by curl's lead maintainer on LLM-generated bug-bounty reports on HackerOne. At the time curl's bounty had paid over $70,000 across 415 reports, of which 64 were confirmed security problems and 77 informative, so 66% were neither. He describes two examples: a report (which admitted using Google Bard) claiming the fix for CVE-2023-38545 had leaked, which mixed details from older issues; and a well-written "buffer overflow in WebSocket handling" report from a reporter with decent HackerOne reputation that turned out, after repeated hallucinated follow-ups, to be false. His point is that better-written AI reports cost more maintainer time to reject, and that AI-text signals cannot be used alone because many honest reporters use AI for translation.

## Key claims

- LLM slop is harder to detect when users mix their own words with model output.
- Reputation on the bounty platform did not filter the hallucinated report.
- A human check before submission would fix most of it (opinion).

## Evidence quality

Practitioner opinion with two linked HackerOne reports and bounty statistics from the project's own records. These are human-submitted LLM outputs, not autonomous agents.

## Relevance to us

An early dated record of the cost asymmetry that agent swarms exploit in open-source triage (cheap to generate, expensive to reject), and of why content-based AI detection is a poor gate where legitimate users also use AI. The 2026 autonomous-agent escalation is documented in [[shambaugh-2026-ai]].

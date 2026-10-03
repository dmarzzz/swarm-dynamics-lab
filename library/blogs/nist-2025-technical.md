---
id: nist-2025-technical
type: blog
title: "Technical Blog: Strengthening AI Agent Hijacking Evaluations"
authors: [Technical Staff of the U.S. AI Safety Institute / Center for AI Standards and Innovation (CAISI), NIST]
year: 2025
url: https://www.nist.gov/news-events/news/2025/01/technical-blog-strengthening-ai-agent-hijacking-evaluations
site: nist.gov
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-identity-hijack
accessed: 2026-10-03
read_depth: full
relevance: 4
---

## Summary

A government evaluation note dated 17 January 2025. NIST staff ran agent hijacking evaluations on Claude 3.5 Sonnet (October 2024 upgrade) using AgentDojo, added new injection tasks (remote code execution, mass database exfiltration, automated phishing, a ransomware-style sequence), and red-teamed new attacks with the UK AI Security Institute. The point is methodological: baseline benchmark numbers understate hijacking risk.

## Key claims

- Measured: on Workspace tasks, with attacks developed on one subset of user tasks and tested on held-out tasks, the strongest baseline attack succeeded 11% of the time and the strongest new red-team attack 81%.
- Measured: across five new high-impact injection tasks, average single-attempt success was 57%, with large per-task spread.
- Measured: attempting each attack 25 times raised average success from 57% to 80%. An attacker who can retry cheaply should be evaluated at pass@k, not pass@1.
- Lessons stated: shared frameworks need continual extension; evaluations must be adaptive; report per-task, not only aggregate, success; test multiple attempts.
- Released improvements as usnistgov/agentdojo-inspect (not opened).

## Evidence quality

Empirical, single model, single framework, attacks not published in full. Numbers are first-party measurements by an evaluator with no stake in the model, which makes them more credible than vendor claims, but there are no confidence intervals in the post.

## Relevance to us

Q3, on how strong the attacker can be. The jump from 11% to 81% with adaptive red-teaming, and from 57% to 80% with 25 retries, says that a static benchmark rate is a floor. In the fork-merge setting the adversary in a foreign information domain may get many attempts at each exploring sub-agent over a long excursion, so the relevant number is closer to the repeated-attempt rate. For Q2 this matters because Byzantine thresholds assume a bound on how many parts fall; if per-part compromise probability is high and attempts are cheap, the k-of-n bound has to be sized for near-certain compromise of exposed parts. Builds on [[debenedetti-2024-agentdojo]]; compare static rates in [[zhan-2024-injecagent]] and [[zhang-2024-agent]].

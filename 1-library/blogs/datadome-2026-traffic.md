---
id: datadome-2026-traffic
type: blog
title: 'The AI Traffic Report Q2 2026: Agentic Traffic Surged 45%, With Meta Taking
  the Lead'
authors:
- Jerome Segura
year: 2026
url: https://datadome.co/threat-research/ai-traffic-report-q2-2026/
site: DataDome
topics:
- swarm-detection
- llm-agent-swarms
read_depth: skim
relevance: 5
added_by: shadow/sol-g49
accessed: '2026-10-03'
---

## Summary

DataDome's second-quarter traffic report documents increasing AI crawler requests and a detectable MCP discovery layer on its customer network. Its use of 'agent' includes model-training and indexing crawlers, so aggregate volume should not be interpreted as a population of autonomous coordinating actors.

## Key claims

- Last updated 2026-07-16, window April to June 2026: 17.7 billion AI requests versus 12.2 billion in Q1, reported 45% growth. Monthly counts 4.77, 6.29 and 6.60 billion.
- Method: network telemetry across 400+ enterprises, with 5 trillion signals analyzed daily, assigned to AI identities and request categories. No independently verified agent-intent label set is exposed.
- Meta-ExternalAgent rose 74% QoQ to 5.3 billion; Meta-WebIndexer 163% to 3.75 billion. ChatGPT-User declined 6%, while AI-driven referrals from ChatGPT grew 17%.
- MCP peaks approach 500,000 requests/day. Request mix: initialize 20.3%, tools/list 19.7%, prompts/list 20.1%, notifications/initialized 19.1%. Capability discovery is measured; malicious intent is not.
- Recommends behavioral session analysis and IP validation/Web Bot Auth rather than trusting user-agent strings alone.

## Evidence quality

Primary commercial telemetry report read through Exa text retrieval after the initial DataDome path returned a CAPTCHA shell. Public report accessible through this route, no mitigation bypass attempted. Data definitions differ from [[human-2026-measuring]].

## Relevance to us

Adds measurable protocol and session features, a dated denominator, and evidence for operator-disjoint splits. It is not itself a runnable labelled request dataset.

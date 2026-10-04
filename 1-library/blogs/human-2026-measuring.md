---
id: human-2026-measuring
type: blog
title: Measuring the AI-Driven Internet with The 2026 State of AI Traffic & Cyberthreat
  Benchmark Report
authors:
- Jeff Edwards
year: 2026
url: https://www.humansecurity.com/learn/blog/ai-traffic-growth-2025-key-findings/
site: HUMAN Security
topics:
- swarm-detection
- llm-agent-swarms
read_depth: full
relevance: 5
added_by: shadow/sol-g49
accessed: '2026-10-03'
---

## Summary

HUMAN reports a shift from crawler collection to agent interaction in customer traffic during 2025. Its telemetry separates broad AI-driven activity from agentic browsing and finds concentrated operators and destinations, but it does not release independently labelled individual sessions for detector training.

## Key claims

- Published 2026-03-26; observation period calendar 2025. Monthly AI-driven volume rose 187% January to December, peaking at 3.61x January in October. Agentic systems' traffic grew 7,851% year over year.
- Method: Human Defense Platform customer-interaction telemetry and vendor categorization of crawlers versus navigating/acting agents. More than 95% of AI-driven traffic targets retail/e-commerce, media/streaming and travel/hospitality.
- OpenAI identities contribute approximately 69% of observed AI traffic, Meta-ExternalAgent 16%, Anthropic identities 11%. Checkout pages receive 2.3% of agentic activity. These are vendor-network shares, not global shares or proof of completed autonomous purchases.
- Publication advertises AgenticTrust, launched late 2025, for recognizing actions, intent and trust levels. No confusion matrix or labelled public traffic corpus is provided here.

## Evidence quality

Primary vendor telemetry with dates and explicit identity categories. Model-release causation for the October spike is conjectural. Bot families sharing an operator must not be treated as independent swarms.

## Relevance to us

Provides operator concentration and task-stage observables for leave-one-operator-out evaluation; compare [[cloudflare-2025-radar]] and [[datadome-2026-traffic]].

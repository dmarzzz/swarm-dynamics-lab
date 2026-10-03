---
id: humansecurity-2025-examining
type: blog
title: "Examining AI Agent Traffic: What Early Traffic Patterns Tell us About Agentic Commerce"
authors: [Jeff Edwards]
year: 2025
url: https://www.humansecurity.com/learn/blog/ai-agent-statistics-agentic-commerce/
site: HUMAN Security blog (bot-mitigation vendor)
topics: [swarm-detection]
added_by: dmarz/sd-informal
accessed: 2026-10-03
read_depth: full
relevance: 3
---

## Summary

Vendor blog (6 October 2025) with telemetry on autonomous AI agents and agentic browsers, as distinct from LLM crawlers and RAG fetchers, across HUMAN-verified interactions (HUMAN says it verifies over 20 trillion interactions a week). Agentic traffic grew more than 1,300% from January to August 2025, to nearly 4.5 million requests a month, which is tiny next to crawler and scraper volumes. It rose 131.15% month over month from August to September 2025 and more than tripled from July to September, driven by the July launches of ChatGPT Agent and Perplexity Comet. ChatGPT Agent was 90% of agent activity in July and 82.5% in August; by September Comet led with 52.5% versus 42%. From January to August, about 87% of pages browsed by agents were product pages, 2.2% checkout or payment, 3.9% account pages (mostly logins), and 0.10% account registration attempts. HUMAN says it detects and attributes agent traffic and has released open-source infrastructure for cryptographically verified agent identity.

## Key claims

- Most third-party analytics cannot distinguish agent traffic from human traffic.
- Blocking agents wholesale costs sales because most act for real users; the post argues for per-agent policy (allow trusted agents, block spoofed ones).

## Evidence quality

Vendor marketing blog; the telemetry is from HUMAN's customer base only (the post says so), and the detection and attribution method is not described. Numbers are useful as dated orders of magnitude, not as population estimates.

## Relevance to us

One of the few published time series for browser-using AI agents (as opposed to crawlers) in the wild, with a market-share split showing how quickly one product launch changes the population. It suggests that in late 2025 agent traffic was dominated by a handful of declared commercial agents, so the detection problem for swarms of undeclared agents sits inside a much larger stream of benign declared ones. Related identity schemes: [[cloudflare-2025-forget]].

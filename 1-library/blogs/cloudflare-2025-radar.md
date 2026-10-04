---
id: cloudflare-2025-radar
type: blog
title: The 2025 Cloudflare Radar Year in Review- the rise of AI, post-quantum, and
  record-breaking DDoS attacks
authors:
- Cloudflare
year: 2025
url: https://blog.cloudflare.com/radar-2025-year-in-review/
site: Cloudflare Blog
topics:
- swarm-detection
- llm-agent-swarms
read_depth: skim
relevance: 5
added_by: shadow/sol-g49
accessed: '2026-10-03'
---

## Summary

Cloudflare measures crawler traffic on its own network, distinguishing identified AI crawlers from dual-purpose Googlebot. The commonly repeated 8.7% figure combines two categories rather than measuring autonomous agent swarms: 4.2% AI bots and 4.5% Googlebot among HTML requests.

## Key claims

- Published 2025-12-15; observation window 2025-01-01 to 2025-12-02. AI bots average 4.2% of HTML requests, with weekly extremes of 2.4% in early April and 6.4% in late June. Googlebot alone averages 4.5%. Their sum is 8.7%, calculated here, not a count of user-directed agents.
- Method: request telemetry and bot classification on Cloudflare customer properties, filtered to HTML requests to remove API, mobile-app and IoT traffic. Denominator is not all Internet traffic. Network handles over 81 million HTTP requests/s on average.
- User-action crawling grew over 15x during 2025; classifier categories depend on declared crawler purpose.

## Evidence quality

Primary vendor telemetry with explicit window and denominator, not independently labelled swarm ground truth. No per-request labelled dataset released here. The aggregate combines legitimate search indexing and AI collection.

## Relevance to us

Baseline prevalence with proper denominators. Compare request authentication in [[cloudflare-2025-forget]] and signed-agent policy in [[cloudflare-2025-age]]. Do not conflate content collection with coordinated malicious operators.

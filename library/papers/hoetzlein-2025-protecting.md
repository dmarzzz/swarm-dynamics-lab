---
id: hoetzlein-2025-protecting
type: paper
title: "Protecting Small Organizations from AI Bots with Logrip: Hierarchical IP Hashing"
authors: ["Rama Carl Hoetzlein"]
year: 2025
venue: "arXiv preprint"
url: https://arxiv.org/abs/2508.03130
doi: "10.48550/arXiv.2508.03130"
arxiv: "2508.03130"
cite: "Hoetzlein, R. C. (2025). Protecting Small Organizations from AI Bots with Logrip: Hierarchical IP Hashing. arXiv preprint arXiv:2508.03130."
topics: ["swarm-detection"]
added_by: dmarz/sd-web-agents
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Hoetzlein proposes Logrip, which aggregates server-log IP activity hierarchically across subnet classes (hierarchical IP hashing) and visualises it to separate human visitors from automated, coordinated crawling that per-IP throttling misses. In a real deployment for a small organisation, he estimates that 80 to 95 percent of traffic came from AI crawlers.

## Contribution

A cheap, log-only method that looks for coordination at the subnet level rather than per IP, aimed at operators who cannot buy commercial bot management.

## Key results

- Estimated (abstract): 80 to 95 percent of a small organisation's traffic came from AI crawlers.
- Claimed (abstract): subnet-level aggregation detects distributed crawling that conventional tools miss; no detection accuracy figures in the abstract.

## Methods and models

Server event logs, hierarchical hashing of IPs by subnet class, statistical measures and visualisation. Abstract only.

## Limitations and open questions

Single real-world example; the AI-crawler share is an estimate, not ground-truthed.

## Relevance to us

Subnet-level aggregation is a coordination signal: many low-rate IPs in the same blocks acting together. Directly reusable as a swarm feature alongside the per-session agent flags from [[wang-2026-fp-agent]]. Compare [[van-boxem-2026-shy]] (log-only, user-agent and favicon heuristics).

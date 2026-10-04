---
id: pangram-2026-feed
type: blog
title: AI Content Is Everywhere on Social Media, Especially LinkedIn
authors:
- Max Spero
year: 2026
url: https://www.pangram.com/blog/ai-in-your-feed
site: Pangram
topics:
- swarm-detection
read_depth: full
relevance: 4
added_by: shadow/sol-g49
accessed: '2026-10-03'
---

## Summary

Pangram uses opt-in browser-extension scans to measure the AI authorship its users inspect, covering LinkedIn, Medium, Substack, X and Reddit. This selected-user sample offers a different denominator from platform enforcement and random post sampling.

## Key claims

- Published 2026-07-09; scans accumulated since extension launch 2026-04-24. Dataset 1,002,627 unique posts/items, all >50 words; Pangram 3.3 classifier. Precise end date not stated beyond publication.
- Overall fully AI rate 13.8%; items >250 words 25.72% fully AI. X articles 23.9% fully AI and 22.9% mixed, total 46.8%; ordinary scanned X posts 10.0% AI-saturation as reported.
- Reddit scanned content 4.4% combined AI, top-level posts 11.6%, replies 98.1% human; replies are 72% of scanned Reddit items. Platform/category mix strongly changes overall rates.
- Method: users opt in to share anonymous scan statistics, each post counted once. Self-selected user requests and a >50-word filter are not random platform sampling. Vendor claims model FPR 0.01%, no independent in-sample audit included.
- Bluesky and Yelp are not platforms in the dataset. No public per-post release or reuse licence established.

## Evidence quality

Primary vendor classifier study with transparent selection process and counts, not population ground truth. Do not contrast its X 10.0% with [[originality-2026-social]] 56.9% as if both sampled the same texts.

## Relevance to us

Demonstrates selection/length bias and top-level/reply distinctions. Agent-operator detection still requires behavior and provenance rather than detector text labels.

---
id: he-2026-degentweb
type: paper
title: 'DeGenTWeb: A First Look at LLM-dominant Websites'
authors:
- Sichang Steven He
- Calvin Ardi
- Ramesh Govindan
- Harsha V. Madhyastha
year: 2026
venue: arXiv preprint (in submission)
url: https://arxiv.org/abs/2605.00087
doi: null
arxiv: '2605.00087'
cite: 'He, S. S., Ardi, C., Govindan, R., & Madhyastha, H. V. (2026). DeGenTWeb: A First Look at LLM-dominant Websites. arXiv:2605.00087.'
topics:
- swarm-detection
added_by: dmarz/sd-ai-content
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 1 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Argues that claims of LLM text taking over the web rest on unrepresentative samples and opaque methods, and that text detectors perform much worse than advertised when tuned for very low false-attribution rates. DeGenTWeb adapts detectors to web pages and aggregates page-level scores into a site-level verdict to find LLM-dominant websites (content generated with little human input). Such sites are highly prevalent in Common Crawl and in Bing results and their share is growing.

## Contribution

Moves the unit of detection from the page to the site, aggregating many weak per-page verdicts into a confident operator-level call.

## Key results

- Measured (abstract): detectors degrade sharply at low false-positive operating points on web pages.
- Measured (abstract): LLM-dominant sites are highly prevalent in Common Crawl and Bing results and growing (numbers not in abstract).
- Claimed (abstract): identifying such sites appears increasingly hard with the latest LLMs.

## Methods and models

Detector adaptation to web pages; multi-page aggregation for site-level classification; sampling from Common Crawl and Bing. Abstract read only.

## Limitations and open questions

Abstract gives no prevalence numbers. Abstract depth.

## Relevance to us

The aggregation idea is the direct analogue of account- or operator-level swarm detection: many low-confidence item scores combined over everything one operator controls. Compare [[chen-2024-online]] (sequential testing of a source) and [[dolezal-2026-impact]] (page-level web prevalence).

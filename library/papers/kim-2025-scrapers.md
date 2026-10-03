---
id: kim-2025-scrapers
type: paper
title: 'Scrapers selectively respect robots.txt directives: evidence from a large-scale empirical study'
authors:
- Taein Kim
- Karstan Bock
- Claire Luo
- Amanda Liswood
- Chloe Poroslay
- Emily Wenger
year: 2025
venue: ACM Internet Measurement Conference (IMC 2025); arXiv preprint
url: https://arxiv.org/abs/2505.21733
doi: null
arxiv: '2505.21733'
cite: 'Kim, T., Bock, K., Luo, C., Liswood, A., Poroslay, C., & Wenger, E. (2025). Scrapers selectively respect robots.txt directives: evidence from a large-scale empirical study. In Proceedings of the ACM Internet Measurement Conference (IMC 2025), pp. 541–557. arXiv:2505.21733.'
topics:
- swarm-detection
added_by: dmarz/sd-honeypots
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Uses anonymised web logs from the authors' institution and a series of controlled robots.txt changes to measure compliance by 130 self-declared bots, and many anonymous ones, over 40 days. Bots comply less as directives get stricter, and some categories, including AI search crawlers, rarely fetch robots.txt at all.

## Contribution

The first large-scale controlled compliance study of the Robots Exclusion Protocol. Changing robots.txt and watching who obeys works as a behavioural probe that separates bot categories.

## Key results

- 130 self-declared bots over 40 days; compliance falls with stricter directives; AI search crawlers rarely check robots.txt (measured, abstract).

## Methods and models

Controlled robots.txt experiments on institutional sites; log analysis. Abstract-level read; found by backward citation from [[seiden-2026-identifying]] and [[fayolle-2026-internet]]. IMC pages 541-557 are taken from the reference list of [[fayolle-2026-internet]].

## Limitations and open questions

Abstract only; one institution's logs.

## Relevance to us

A robots.txt change is a zero-cost trap: a disallowed path that only non-compliant bots visit labels them. Same group as [[seiden-2026-identifying]]; context in [[liu-2024-somesite]].

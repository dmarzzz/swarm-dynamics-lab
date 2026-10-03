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

## Notes from dmarz/sd-web-agents

This lane catalogued the same source independently (added_by dmarz/sd-web-agents, accessed 2026-10-03). Its distinct content:

- Frontmatter `venue` in this lane's version: ACM Internet Measurement Conference (IMC 2025)
- Frontmatter `doi` in this lane's version: 10.1145/3730567.3764471
- Frontmatter `cite` in this lane's version: 'Kim, T., Bock, K., Luo, C., Liswood, A., Poroslay, C., & Wenger, E. (2025). Scrapers selectively respect robots.txt directives: evidence from a large-scale empirical study. In Proceedings of the 2025 ACM Internet Measurement Conference (IMC ''25), pp. 541-557. https://doi.org/10.1145/3730567.3764471. arXiv:2505.21733.'
- Frontmatter `read_depth` in this lane's version: skim
- Frontmatter `relevance` in this lane's version: 4
- Frontmatter `citations` in this lane's version: 17 (Semantic Scholar, 2026-10-03)

### Summary

Kim, Bock, Luo, Liswood, Poroslay and Wenger (Duke) analyse 40 days of anonymised web logs from their university's sites, covering 130 self-declared bots and many anonymous ones, and run a controlled experiment that swaps in four increasingly strict robots.txt files for two weeks each on one high-traffic site. Bots comply most with crawl-delay and less as directives tighten to endpoint and full disallow. AI search crawlers and AI assistants rarely fetch robots.txt at all and have the lowest re-check rates. They also flag likely User-Agent spoofing by looking for bots whose traffic mostly comes from one ASN but sometimes from others.

### Contribution

First rigorous, controlled measurement of robots.txt compliance by category, including AI-specific bots, and a simple ASN-consistency heuristic for spotting spoofed bot identities.

### Key results

- Measured: 130 self-declared bots over 40 days; YisouSpider and AppleBot dominate traffic.
- Measured: average compliance is highest for crawl-delay, nearly 2x that of endpoint restrictions; compliance falls as robots.txt tightens.
- Measured: AI assistants and AI search crawlers have the lowest robots.txt re-check rates of any category.
- Measured: several well-known bot User-Agents, including Googlebot, also appear from minority ASNs, which the authors read as probable spoofing (not proven).

### Methods and models

Institutional web logs, Dark Visitors bot categories, weighted per-category compliance ratios, statistical tests on shifts between robots.txt versions, ASN-dominance spoofing heuristic. I skimmed the HTML; many numeric values were lost in conversion so I cite only those I could read.

### Limitations and open questions

Single institution's sites; SEO bots exempted at the institution's request; the spoofing analysis cannot confirm spoofing; the authors suggest honeypots for that.

### Relevance to us

Measured base rate that AI-related bots ignore the cooperative channel. The ASN-consistency check is a cheap Sybil-ish signal: one declared identity seen from many networks. Compare [[cui-2025-odyssey]], [[lopez-fonseca-2026-do]], [[seiden-2026-identifying]].

---
id: kim-2025-scrapers
type: paper
title: "Scrapers selectively respect robots.txt directives: evidence from a large-scale empirical study"
authors: ["Taein Kim", "Karstan Bock", "Claire Luo", "Amanda Liswood", "Chloe Poroslay", "Emily Wenger"]
year: 2025
venue: "ACM Internet Measurement Conference (IMC 2025)"
url: https://arxiv.org/abs/2505.21733
doi: "10.1145/3730567.3764471"
arxiv: "2505.21733"
cite: "Kim, T., Bock, K., Luo, C., Liswood, A., Poroslay, C., & Wenger, E. (2025). Scrapers selectively respect robots.txt directives: evidence from a large-scale empirical study. In Proceedings of the 2025 ACM Internet Measurement Conference (IMC '25), pp. 541-557. https://doi.org/10.1145/3730567.3764471. arXiv:2505.21733."
topics: ["swarm-detection"]
added_by: dmarz/sd-web-agents
accessed: '2026-10-03'
read_depth: skim
relevance: 4
citations: "17 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

Kim, Bock, Luo, Liswood, Poroslay and Wenger (Duke) analyse 40 days of anonymised web logs from their university's sites, covering 130 self-declared bots and many anonymous ones, and run a controlled experiment that swaps in four increasingly strict robots.txt files for two weeks each on one high-traffic site. Bots comply most with crawl-delay and less as directives tighten to endpoint and full disallow. AI search crawlers and AI assistants rarely fetch robots.txt at all and have the lowest re-check rates. They also flag likely User-Agent spoofing by looking for bots whose traffic mostly comes from one ASN but sometimes from others.

## Contribution

First rigorous, controlled measurement of robots.txt compliance by category, including AI-specific bots, and a simple ASN-consistency heuristic for spotting spoofed bot identities.

## Key results

- Measured: 130 self-declared bots over 40 days; YisouSpider and AppleBot dominate traffic.
- Measured: average compliance is highest for crawl-delay, nearly 2x that of endpoint restrictions; compliance falls as robots.txt tightens.
- Measured: AI assistants and AI search crawlers have the lowest robots.txt re-check rates of any category.
- Measured: several well-known bot User-Agents, including Googlebot, also appear from minority ASNs, which the authors read as probable spoofing (not proven).

## Methods and models

Institutional web logs, Dark Visitors bot categories, weighted per-category compliance ratios, statistical tests on shifts between robots.txt versions, ASN-dominance spoofing heuristic. I skimmed the HTML; many numeric values were lost in conversion so I cite only those I could read.

## Limitations and open questions

Single institution's sites; SEO bots exempted at the institution's request; the spoofing analysis cannot confirm spoofing; the authors suggest honeypots for that.

## Relevance to us

Measured base rate that AI-related bots ignore the cooperative channel. The ASN-consistency check is a cheap Sybil-ish signal: one declared identity seen from many networks. Compare [[cui-2025-odyssey]], [[lopez-fonseca-2026-do]], [[seiden-2026-identifying]].

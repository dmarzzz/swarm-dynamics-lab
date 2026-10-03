---
id: li-2021-good
type: paper
title: 'Good Bot, Bad Bot: Characterizing Automated Browsing Activity'
authors:
- Xigao Li
- Babak Amin Azad
- Amir Rahmati
- Nick Nikiforakis
year: 2021
venue: 2021 IEEE Symposium on Security and Privacy (SP)
url: https://api.openalex.org/works/W3152517439?mailto=sol@shad0w.xyz
doi: 10.1109/sp40001.2021.00079
arxiv: null
cite: 'Xigao Li; Babak Amin Azad; Amir Rahmati; Nick Nikiforakis. (2021). Good Bot,
  Bad Bot: Characterizing Automated Browsing Activity. 2021 IEEE Symposium on Security
  and Privacy (SP), 1589-1605. https://doi.org/10.1109/sp40001.2021.00079'
topics:
- swarm-detection
added_by: shadow/sol-g51
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

Aristaeus deploys honeysites to characterize automated browsing and malicious bots. Its abstract reports a seven-month experiment across one hundred sites, collecting 26.4 million requests from more than 287,000 addresses, and uses mismatches between claimed browsers, TLS handshakes, and headers to reveal automation.

## Contribution

Honeysite deployment and request, TLS, and HTTP-header comparison.

## Key results

- 26.4M requests; over 287K IPs; 76,396 malicious-bot IPs; more than 86.2% of bots claiming Firefox or Chrome used simple HTTP tools.

## Methods and models

Honeysite deployment and request, TLS, and HTTP-header comparison.

## Limitations and open questions

IP addresses are not unique operators, and findings about simple libraries may not transfer to browser-native LLM agents.

## Relevance to us

A comparison source for coordinated automation and security measurement. Full-text methods and replication have not been checked.

## Access provenance

Crossref metadata and the abstract at the recorded URL were opened directly or through Exa content extraction on 2026-10-03. Any non-null citation count is OpenAlex cited_by_count on that date. Abstract depth is deliberate even where an open PDF was found.

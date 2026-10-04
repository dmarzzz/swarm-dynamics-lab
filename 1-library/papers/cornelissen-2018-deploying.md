---
id: cornelissen-2018-deploying
type: paper
title: Deploying South African Social Honeypots on Twitter
authors:
- Laurenz A. Cornelissen
- Richard J. Barnett
- Morakane A. M. Kepa
- Daniel Loebenberg-Novitzkas
- Jacques Jordaan
year: 2018
venue: Proceedings of the Annual Conference of the South African Institute of Computer Scientists and Information Technologists (SAICSIT 2018)
url: https://arxiv.org/abs/1809.06185
doi: 10.1145/3278681.3278703
arxiv: '1809.06185'
cite: Cornelissen, L. A., Barnett, R. J., Kepa, M. A. M., Loebenberg-Novitzkas, D., & Jordaan, J. (2018). Deploying South African Social Honeypots on Twitter. In Proceedings of SAICSIT 2018, pp. 179–187. https://doi.org/10.1145/3278681.3278703
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

Building on the observation that tweeting gibberish attracts automated accounts, the authors combined several honeypot techniques to draw interactions from users in the South African political context on Twitter. They argue honeypots should not be confused with bot detection: they capture 'low-quality users', not necessarily bots. They produced a list of 288 local low-quality users active in political discussion.

## Contribution

A politically targeted social-honeypot replication with an explicit negative claim: a honeypot hit is evidence of low quality, not of automation.

## Key results

- 288 local low-quality users captured in the South African political context (abstract).
- Conceptual claim: honeypots capture low-quality users rather than detect bots (argument).

## Methods and models

Combination of defined lure techniques on Twitter. Abstract-level read. Venue and pages 179-187 confirmed via the Crossref record for the DOI.

## Limitations and open questions

Abstract only; small catch.

## Relevance to us

A caution for interpreting trap hits in the LLM era: an engaged account may be a human engagement-farmer, not an agent. Pair passive traps with an active discriminator such as [[ayzenshteyn-2025-cloak]] or [[reworr-2024-llm]]. Classic predecessors: [[lee-2011-seven]], [[lee-2010-uncovering]].

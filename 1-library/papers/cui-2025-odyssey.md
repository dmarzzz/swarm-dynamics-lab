---
id: cui-2025-odyssey
type: paper
title: "The Odyssey of robots.txt Governance: Measuring Convention Implications of Web Bots in Large Language Model Services"
authors: ["Jian Cui", "Mingming Zha", "XiaoFeng Wang", "Xiaojing Liao"]
year: 2025
venue: "ACM SIGSAC Conference on Computer and Communications Security (CCS 2025)"
url: https://www.semanticscholar.org/paper/7efc75f584fd571dff0e348198f2f0f6acb089e5
doi: "10.1145/3719027.3765063"
arxiv: null
cite: "Cui, J., Zha, M., Wang, X., & Liao, X. (2025). The Odyssey of robots.txt Governance: Measuring Convention Implications of Web Bots in Large Language Model Services. In Proceedings of the 2025 ACM SIGSAC Conference on Computer and Communications Security (CCS '25), pp. 21-35. https://doi.org/10.1145/3719027.3765063."
topics: ["swarm-detection"]
added_by: dmarz/sd-web-agents
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: "9 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

Cui, Zha, Wang and Liao study 18 LLM-vendor bots (such as ChatGPT-User and Google-Extended) across 582,281 robots.txt files. Rules naming LLM bots rose sharply, most in finance and news domains. Publishers struggle to configure robots.txt correctly given the number of bots and third-party brokers. The authors document violations, including LLMs that memorised content from restricted domains and ChatGPT-User fetching restricted content.

## Contribution

Large-scale census of LLM-bot rules in robots.txt plus case evidence of non-compliance by user-triggered fetchers. Abstract read via the Semantic Scholar record; the ACM page returned 403.

## Key results

- Measured (abstract): 18 LLM bots, 582,281 robots.txt files.
- Measured (abstract): significant growth in LLM-bot rules, concentrated in finance and news.
- Observed (abstract): ChatGPT-User ignored robots.txt and accessed restricted content; models memorised content from restricted domains.

## Methods and models

robots.txt crawling and parsing at scale, case studies of bot behaviour and model memorisation. Not read beyond the abstract.

## Limitations and open questions

Abstract only; violation counts and methods not checked.

## Relevance to us

Another measured negative for cooperative self-identification, and evidence that user-triggered agent fetches behave differently from training crawlers. Pairs with [[kim-2025-scrapers]] and [[lopez-fonseca-2026-do]].

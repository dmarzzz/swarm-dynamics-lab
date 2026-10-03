---
id: farooqi-2020-canarytrap
type: paper
title: 'CanaryTrap: Detecting Data Misuse by Third-Party Apps on Online Social Networks'
authors:
- Shehroze Farooqi
- Maaz Musa
- Zubair Shafiq
- Fareed Zaffar
year: 2020
venue: arXiv preprint
url: https://arxiv.org/abs/2006.15794
doi: null
arxiv: '2006.15794'
cite: 'Farooqi, S., Musa, M., Shafiq, Z., & Zaffar, F. (2020). CanaryTrap: Detecting Data Misuse by Third-Party Apps on Online Social Networks. arXiv preprint arXiv:2006.15794.'
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

Attaches a unique honeytoken (the email address of a Facebook account) to each third-party app it installs, then watches for unrecognised use of that token through the mailbox and through Facebook's ad-transparency tool. Deployed against 1,024 Facebook apps, it found multiple cases of data misuse including ransomware, spam and targeted advertising.

## Contribution

A large-scale, platform-side honeytoken methodology: one token per counterparty, misuse detected out-of-band. This is the pre-LLM ancestor of per-scraper canaries.

## Key results

- 1,024 Facebook apps monitored; multiple cases of misuse found (ransomware, spam, targeted ads) (abstract; exact counts not in abstract).

## Methods and models

Per-app unique email honeytokens; monitoring of inbound email and ad targeting. Abstract-level read.

## Limitations and open questions

Abstract only; detection depends on the misuser using the token in an observable channel.

## Relevance to us

The "one token per counterparty, watch where it surfaces" design transfers directly to agent marketplaces and APIs: give each agent or API key a distinct canary and attribute leaks. Modern descendant: [[seiden-2026-identifying]]. Survey context: [[zhang-2021-three]].

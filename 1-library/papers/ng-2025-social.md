---
id: ng-2025-social
type: paper
title: Social Cyber Geographical Worldwide Inventory of Bots
authors:
- Lynnette Hui Xian Ng
- Kathleen M. Carley
year: 2025
venue: arXiv preprint
url: https://arxiv.org/abs/2501.18839
doi: null
arxiv: '2501.18839'
cite: Ng, L. H. X., & Carley, K. M. (2025). Social Cyber Geographical Worldwide Inventory of Bots. arXiv preprint arXiv:2501.18839.
topics:
- swarm-detection
added_by: dmarz/sd-bots
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

A multilingual, geolocated census of bots in about 100 million COVID-19 posts by about 31 million X users in 2021. The authors built Multilingual BotBuster and a profile-based country identifier, found only 47% of bots write in English, and estimate a bot share of roughly 20% per country despite very different bot locations.

## Contribution

A global, non-English prevalence estimate from the CMU social-cybersecurity group, whose estimate (about 20%) is far above platform claims and above [[varol-2017-online]].

## Key results

- About 100M posts by about 31M users; 47% of detected bots write in English.
- Bot proportion per country about 20%.
- Bots appear to move between self-declared countries while keeping their language.

## Methods and models

Multilingual BotBuster (mixture-of-experts bot detector) plus a geolocation identifier over a 2021 X COVID dataset. Abstract-level read.

## Limitations and open questions

Prevalence comes from a classifier threshold without published audit, the exact pattern criticised in [[gallwitz-2022-investigating]]. Preprint.

## Relevance to us

Shows how far apart bot-share estimates sit (under 5% platform claim, 9-15%, about 20%), which is the measurement problem any agent-swarm census inherits. Compare [[tan-2023-botpercent]].

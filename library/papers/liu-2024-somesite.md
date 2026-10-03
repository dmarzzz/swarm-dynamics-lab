---
id: liu-2024-somesite
type: paper
title: 'Somesite I Used To Crawl: Awareness, Agency and Efficacy in Protecting Content Creators From AI Crawlers'
authors:
- Enze Liu
- Elisa Luo
- Shawn Shan
- Geoffrey M. Voelker
- Ben Y. Zhao
- Stefan Savage
year: 2024
venue: ACM Internet Measurement Conference (IMC 2025); arXiv preprint 2024
url: https://arxiv.org/abs/2411.15091
doi: 10.1145/3730567.3732913
arxiv: '2411.15091'
cite: 'Liu, E., Luo, E., Shan, S., Voelker, G. M., Zhao, B. Y., & Savage, S. (2025). Somesite I Used To Crawl: Awareness, Agency and Efficacy in Protecting Content Creators From AI Crawlers. In Proceedings of the ACM Internet Measurement Conference (IMC 2025), pp. 78–99. https://doi.org/10.1145/3730567.3732913'
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

Large-scale measurement plus a user study of 203 professional artists on whether creators can keep AI crawlers away using robots.txt, NoAI meta tags and reverse-proxy crawler blocking. Artists want such tools but face hurdles in awareness and in the ability to deploy them (hosting restrictions), and robots.txt has limited efficacy against crawlers that do not respond to it. Network-level blockers in reverse proxies give stronger protection but are not widely deployed and have their own limits.

## Contribution

Establishes that self-declared crawler identity plus voluntary compliance is a weak basis for controlling AI agents on the web. This motivates identity inference from behaviour or traps ([[seiden-2026-identifying]], [[fayolle-2026-internet]]).

## Key results

- 203 professional artists surveyed; strong demand but low awareness and agency (abstract).
- robots.txt has limited efficacy against unresponsive crawlers; reverse-proxy blockers are stronger (abstract).

## Methods and models

Web measurement of robots.txt and blocker deployment; active crawler tests; user study. Abstract-level read. Note: arXiv year 2024, conference version IMC 2025 (authors ask to cite the conference version).

## Limitations and open questions

Abstract only.

## Relevance to us

Background for the web-crawler slice of swarm detection: declared identity fails, so traps and fingerprints are needed. Shares an author (Enze Liu) with [[seiden-2026-identifying]]. Related: [[hoetzlein-2025-protecting]].

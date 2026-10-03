---
id: vastel-2020-fp-crawlers
type: paper
title: "FP-Crawlers: Studying the Resilience of Browser Fingerprinting to Block Crawlers"
authors: ["Antoine Vastel", "Walter Rudametkin", "Romain Rouvoy", "Xavier Blanc"]
year: 2020
venue: "NDSS Workshop on Measurements, Attacks, and Defenses for the Web (MADWeb 2020)"
url: https://www.semanticscholar.org/paper/d02f2b52eabb7025953847bb722a4c66d4d9f274
doi: "10.14722/madweb.2020.23010"
arxiv: null
cite: "Vastel, A., Rudametkin, W., Rouvoy, R., & Blanc, X. (2020). FP-Crawlers: Studying the Resilience of Browser Fingerprinting to Block Crawlers. In Proceedings 2020 Workshop on Measurements, Attacks, and Defenses for the Web (MADWeb 2020). https://doi.org/10.14722/madweb.2020.23010."
topics: ["swarm-detection"]
added_by: dmarz/sd-web-agents
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: "65 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

Vastel, Rudametkin, Rouvoy and Blanc crawled the Alexa top 10K, found 291 sites that block crawlers, and showed that 93 of them (31.96%) use browser fingerprinting to do so. They reverse-engineer the detection checks of the major fingerprinting vendors and test crawlers that try to hide: fingerprinting detects crawlers well but an adversary who knows which attributes are collected can bypass it with little effort.

## Contribution

Early measurement of fingerprinting as deployed crawler detection, and of its weakness to informed spoofing. Co-author Rudametkin is also on [[fayolle-2026-internet]].

## Key results

- Measured (abstract): 291 of Alexa top 10K block crawlers; 93 (31.96%) of those use browser fingerprinting.
- Measured (abstract): fingerprinting is bypassable with little effort by an adversary who knows the collected attributes.

## Methods and models

Large crawl, script analysis of fingerprinting vendors, evasion experiments. Abstract read from the Semantic Scholar record.

## Limitations and open questions

Abstract only; 2020 crawler stacks, no LLM agents.

## Relevance to us

Sets the expectation that any fixed fingerprint rule set will be spoofed once known; the same arms race applies to agent fingerprints. See [[amin-azad-2020-web]].

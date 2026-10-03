---
id: wang-2026-fp
type: paper
title: "FP-Agent: Fingerprinting AI Browsing Agents"
authors: ["Ethan Wang", "Zubair Shafiq", "Yash Vekaria"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2605.01247
doi: null
arxiv: "2605.01247"
cite: "Wang, E., Shafiq, Z., & Vekaria, Y. (2026). FP-Agent: Fingerprinting AI Browsing Agents. arXiv:2605.01247."
topics: [swarm-detection]
added_by: dmarz/sd-attribution
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

First controlled measurement of seven AI browsing agents and humans on an instrumented honey website performing flight booking, shopping and forum tasks. Browser fingerprints discriminate poorly when several agents share them, but behavioural fingerprints (typing, scrolling, mouse) separate agents from humans and from one another. In a case study FP-Agent detects all seven agents while Cloudflare's bot detection detects one.

## Contribution

Shows commercial bot detection largely misses AI browsing agents and that behavioural features close the gap.

## Key results

- FP-Agent detects 7 of 7 agents; Cloudflare detects 1 of 7 (abstract).
- Browser fingerprints have limited power when shared; behavioural fingerprints are distinctive (abstract).

## Methods and models

Honey website, three tasks, multi-class classifier over browser and behavioural features.

## Limitations and open questions

Abstract-only reading; seven agents.

## Relevance to us

Measured gap between deployed bot defences and agents, relevant to base rates: agent traffic counted by Cloudflare-style tools is likely an undercount. Related: [[choudhary-2026-what]], [[lugoloobi-2026-known]].

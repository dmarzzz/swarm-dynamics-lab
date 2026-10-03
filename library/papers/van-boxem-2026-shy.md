---
id: van-boxem-2026-shy
type: paper
title: "Shy Guys: A Light-Weight Approach to Detecting Robots on Websites"
authors: ["Rémi Van Boxem", "Tom Barbette", "Cristel Pelsser", "Ramin Sadre"]
year: 2026
venue: "arXiv preprint (submitted to IFIP TMA 2026)"
url: https://arxiv.org/abs/2603.28546
doi: "10.48550/arXiv.2603.28546"
arxiv: "2603.28546"
cite: "Van Boxem, R., Barbette, T., Pelsser, C., & Sadre, R. (2026). Shy Guys: A Light-Weight Approach to Detecting Robots on Websites. arXiv preprint arXiv:2603.28546."
topics: ["swarm-detection"]
added_by: dmarz/sd-web-agents
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Van Boxem, Barbette, Pelsser and Sadre propose a passive bot detector that uses only standard web server logs: User-Agent string analysis plus heuristics around favicon requests, which real browsers fetch and many bots do not. On 4.6 million requests with 54,945 unique User-Agents from sites worldwide, it flags 67.7% of bot traffic at a 3% false-positive rate, against under 20% for the prior state of the art. They frame it as a first filter that routes only ambiguous traffic to active challenges.

## Contribution

A near-zero-cost passive detector that needs no client JavaScript, useful as a first stage before fingerprinting.

## Key results

- Measured (abstract): 67.7% bot detection at 3% false-positive rate on 4.6M requests.
- Measured (abstract): prior state of the art under 20% on the same data.
- Context (abstract): bots are roughly half of web requests.

## Methods and models

Server-log features: User-Agent parsing and favicon-request behaviour. Abstract only.

## Limitations and open questions

Abstract only. Browser-based agents load favicons like real browsers, so this likely misses them (inference, not tested in the abstract).

## Relevance to us

Cheap first-stage filter; its blind spot is exactly the full-browser LLM agent studied in [[fayolle-2026-internet]] and [[wang-2026-fp-agent]].

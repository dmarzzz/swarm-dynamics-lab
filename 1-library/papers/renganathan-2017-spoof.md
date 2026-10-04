---
id: renganathan-2017-spoof
type: paper
title: "Spoof resilient coordination for distributed multi-robot systems"
authors: ["Venkatraman Renganathan", "Tyler Summers"]
year: 2017
venue: "2017 International Symposium on Multi-Robot and Multi-Agent Systems (MRS)"
url: https://api.openalex.org/works/doi:10.1109/mrs.2017.8250942
doi: "10.1109/mrs.2017.8250942"
arxiv: null
cite: "Renganathan, V., & Summers, T. (2017). Spoof resilient coordination for distributed multi-robot systems. In 2017 International Symposium on Multi-Robot and Multi-Agent Systems (MRS), 135-141."
topics: [sybil-resistance, sync-consensus, swarm-robotics]
added_by: dmarz/sybil-robotics
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "29 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Points out that spoofing, where one malicious agent spawns identities or impersonates legitimate ones, breaks resilient algorithms that assume an upper bound on the number of malicious agents. Generalises W-MSR consensus [[leblanc-2013-resilient]] by adding physical fingerprint comparison of received signals so legitimate agents can isolate spoofers, and quantifies the effect of detection delay and noisy, inexact detection. Numerical simulations only.

## Contribution

The first explicit merge of W-MSR outlier trimming with physical-layer Sybil detection; cited by [[wardega-2023-byzantine]] as the way to bolt Sybil prevention onto W-MSR.

## Key results

- Spoof-resilient W-MSR variant with analysis of detection delay and inexact detection (abstract).
- Applicable to coverage, distributed estimation and formation control (claimed).

## Methods and models

W-MSR plus fingerprint-based isolation. Abstract read only; details beyond the abstract not checked.

## Limitations and open questions

Assumes a fingerprinting capability like [[gil-2015-guaranteeing]]; simulation only.

## Relevance to us

Makes explicit the key structural point for any swarm: an F-bounded Byzantine guarantee is meaningless without a bound on identities per adversary, so Sybil resistance must sit underneath Byzantine resilience.

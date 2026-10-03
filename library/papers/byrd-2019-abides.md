---
id: byrd-2019-abides
type: paper
title: "ABIDES: Towards High-Fidelity Market Simulation for AI Research"
authors: ["David Byrd", "Maria Hybinette", "Tucker Hybinette Balch"]
year: 2019
venue: "arXiv preprint"
url: https://arxiv.org/abs/1904.12066
doi: null
arxiv: "1904.12066"
cite: "Byrd, D., Hybinette, M., & Balch, T. H. (2019). ABIDES: Towards High-Fidelity Market Simulation for AI Research. arXiv preprint arXiv:1904.12066."
topics: [meta]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "82 (Semantic Scholar, 2026-10-03)"
code: [gh-abides-sim-abides, gh-jpmorganchase-abides-jpmc-public]
---

## Summary

Introduces ABIDES, an agent-based interactive discrete-event simulator built for AI research on markets, motivated by the lack of broadly available high-fidelity market simulators outside trading firms. It supports tens of thousands of trading agents interacting with an exchange agent, configurable pairwise network latency between every agent and the exchange, and a message design modelled on NASDAQ's ITCH and OUCH protocols; the paper validates it with example trading scenarios and a market-impact experiment.

## Contribution

A general latency-aware message-passing kernel for agent markets, released open source; later extended into ABIDES-Markets and ABIDES-Gym.

## Key results

- Tens of thousands of trading agents supported (abstract).
- Market-impact model experiment used as an illustration (abstract; details not read).

## Methods and models

Not read beyond the abstract and the repository README.

## Limitations and open questions

Only the abstract was read. The original repository's last commit is 2020-11-19.

## Relevance to us

The kernel design (explicit per-pair latency, messages only) is what an MEV builder or relay race simulator needs; we ran its successor [[gh-jpmorganchase-abides-jpmc-public]].

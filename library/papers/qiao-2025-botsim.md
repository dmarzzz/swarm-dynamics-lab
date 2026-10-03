---
id: qiao-2025-botsim
type: paper
title: "BotSim: LLM-Powered Malicious Social Botnet Simulation"
authors: ["Boyu Qiao", "Kun Li", "Wei Zhou", "Shilong Li", "Qianqian Lu", "Songlin Hu"]
year: 2025
venue: "Proceedings of the AAAI Conference on Artificial Intelligence"
url: https://arxiv.org/abs/2412.13420
doi: "10.1609/aaai.v39i13.33575"
arxiv: "2412.13420"
cite: "Qiao, B., Li, K., Zhou, W., Li, S., Lu, Q., & Hu, S. (2025). BotSim: LLM-Powered Malicious Social Botnet Simulation. Proceedings of the AAAI Conference on Artificial Intelligence, 39(13), 14377–14385."
topics: [swarm-detection, llm-agent-swarms]
added_by: dmarz/sd-coordination
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "47 (Semantic Scholar, 2026-10-03)"
code: []
---
## Summary

BotSim simulates a social network of LLM-driven agent bots alongside real human users, with temporal posting and commenting that mimics real information spread. From it the authors build BotSim-24, a dataset of highly human-like LLM bots, and benchmark existing bot detection methods on it. Methods that work on traditional bot datasets perform worse on BotSim-24.

## Contribution

A synthetic benchmark of LLM botnets embedded among real users, with the measured result that pre-LLM detectors lose accuracy against them.

## Key results

- Detection methods effective on traditional bot datasets perform worse on BotSim-24 (abstract; per-method numbers not in the abstract).

## Methods and models

LLM agent bots with personas acting in a timed simulation over a graph seeded with real users; benchmarking of feature-, text- and graph-based detectors.

## Limitations and open questions

Abstract only. The bots are designed by the authors, so the benchmark measures detector robustness to one design, not to real operators. [[mukherjee-2026-moltgraph]] cites a BotSim-25 successor dataset I did not open.

## Relevance to us

The main synthetic LLM-botnet benchmark. Contrast with [[ng-2025-are]], which finds LLM bot networks differ from wild bots, and [[orlando-2026-emergent]], where LLM agents still leave co-retweet signatures. Existing entry [[yang-2023-anatomy]] is the in-the-wild counterpart.

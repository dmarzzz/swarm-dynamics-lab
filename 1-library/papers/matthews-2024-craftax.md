---
id: matthews-2024-craftax
type: paper
title: "Craftax: A Lightning-Fast Benchmark for Open-Ended Reinforcement Learning"
authors: ["Michael Matthews", "Michael Beukman", "Benjamin Ellis", "Mikayel Samvelyan", "Matthew Jackson", "Samuel Coward", "Jakob Foerster"]
year: 2024
venue: "arXiv preprint"
url: https://arxiv.org/abs/2402.16801
doi: null
arxiv: "2402.16801"
cite: "Matthews, M., Beukman, M., Ellis, B., Samvelyan, M., Jackson, M., Coward, S., & Foerster, J. (2024). Craftax: A Lightning-Fast Benchmark for Open-Ended Reinforcement Learning. arXiv preprint arXiv:2402.16801."
topics: [marl-emergence]
added_by: dmarz/factory-scan
accessed: 2026-10-03
read_depth: abstract
relevance: 2
citations: null
code: []
---

## Summary

Craftax-Classic rewrites the Crafter survival-crafting game in JAX and runs up to 250x faster than the Python original; PPO with 1 billion environment interactions finishes in under an hour on one GPU and averages 90% of optimal reward. The main Craftax benchmark extends Crafter with NetHack-like mechanics; existing exploration and unsupervised-environment-design methods make little progress on it.

## Contribution

A cheap, open-ended crafting benchmark with a tech tree, which made large-sample RL on crafting tasks practical. Its multi-agent descendant is [[al-omari-2025-multi]].

## Key results

- Measured (abstract): 250x speed-up over Crafter; PPO reaches 90% of optimal on Craftax-Classic in under an hour with 1B steps.
- Measured (abstract): global and episodic exploration and UED fail to make material progress on full Craftax.

## Methods and models

JAX environment, PPO and exploration baselines. Abstract read only. The repo MichaelTMatthews/Craftax had 456 stars and MIT licence on 2026-10-03 (checked via GitHub API, not catalogued separately).

## Limitations and open questions

Single-agent, RL-oriented; no market or pricing. Abstract only.

## Relevance to us

A fast crafting substrate if we want RL or scripted baselines next to LLM firms. Too simple on its own for multi-firm markets; see [[al-omari-2025-multi]] for the trading variant and [[hopkins-2025-factorio]] for LLM-native production.

---
id: li-2023-are
type: paper
title: Are you in a Masquerade? Exploring the Behavior and Impact of Large Language Model Driven Social Bots in Online Social Networks
authors:
- Siyu Li
- Jin Yang
- Kui Zhao
year: 2023
venue: arXiv preprint
url: https://arxiv.org/abs/2307.10337
doi: null
arxiv: '2307.10337'
cite: Li, S., Yang, J., & Zhao, K. (2023). Are you in a Masquerade? Exploring the Behavior and Impact of Large Language Model Driven Social Bots in Online Social Networks. arXiv preprint arXiv:2307.10337.
topics:
- swarm-detection
- llm-agent-swarms
added_by: dmarz/sd-bots
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

An exploratory study of Chirper, a Twitter-like network populated by LLM-driven bots. The authors find these bots camouflage well individually but show collective regularities, can push toxic behaviour into communities, and that existing bot detection methods still apply but with reduced effectiveness. They release the collected data as the Masquerade-23 dataset.

## Contribution

One of the first behavioural datasets of LLM-driven social agents living in a shared network, as opposed to single generated posts.

## Key results

- LLM-driven bots show stronger individual-level camouflage but some collective characteristics (abstract).
- Bots can influence communities through toxic behaviour.
- Existing detection methods are applicable but limited in effectiveness on this population.
- Masquerade-23 dataset released.

## Methods and models

Data collection from Chirper; behavioural and network analysis; evaluation of existing detectors. Abstract-level read.

## Limitations and open questions

Chirper is an all-bot platform, so 'detection' is not tested against a realistic human background; preprint.

## Relevance to us

Direct evidence for the hypothesis that LLM agents look human one by one but leave group-level signatures. Synthetic counterparts: [[qiao-2024-botsim]], [[ng-2025-are]].

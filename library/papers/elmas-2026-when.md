---
id: elmas-2026-when
type: paper
title: When Does the Public Become Suspicious of Bots? Demand-Side Evidence from Botometer Query Logs
authors:
- Tuğrulcan Elmas
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2609.20661
doi: null
arxiv: '2609.20661'
cite: Elmas, T. (2026). When Does the Public Become Suspicious of Bots? Demand-Side Evidence from Botometer Query Logs. arXiv preprint arXiv:2609.20661.
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

Treats each Botometer lookup as a trace of public suspicion and analyses more than 1 million public checks of Twitter accounts from 2020 to 2023, joined with 3.2 billion tweets from the 1% stream. Suspicion spikes with platform crises, above all the 2022 Musk-Twitter bot dispute; checked accounts are older, more prolific and promotional, political or crypto, and accounts drawing collective suspicion have higher bot scores and are more often suspended.

## Contribution

Uses detector query logs as a distributed crowd-auditing signal, a new data source for where people think bots are.

## Key results

- Over 1M public Botometer checks (2020-2023) and 3.2B stream tweets.
- Accounts with collective suspicion have higher bot scores and higher suspension rates.
- Public arguments for 'bot' cite posting rate, political content and cross-account coordination.

## Methods and models

Log analysis joined with stream data; suspension follow-up. Abstract-level read.

## Limitations and open questions

Suspicion is not ground truth; bot scores and suspensions share biases with the tool being queried. Preprint.

## Relevance to us

Suggests crowd reports as a cheap sensor for swarm detection (compare the human-plus-AI ensembles in [[la-gatta-2026-human]]). Tool background: [[yang-2019-arming]].

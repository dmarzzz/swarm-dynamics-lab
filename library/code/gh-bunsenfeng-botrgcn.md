---
id: gh-bunsenfeng-botrgcn
type: code
title: "BotRGCN: relational graph convolutional network for Twitter bot detection (TwiBot-20)"
repo: BunsenFeng/BotRGCN
url: https://github.com/BunsenFeng/BotRGCN
authors: ["Shangbin Feng (BunsenFeng)"]
year: 2021
language: Python
license: "MIT"
stars: 44
last_commit: 2022-11-07
topics: [swarm-detection, sybil-resistance]
added_by: dmarz/sd-code-data
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: []
---

## Summary

Reference implementation of BotRGCN (ASONAM 2021, arXiv 2106.13092): users are nodes with description, tweet, numerical and categorical property embeddings, following and follower edges are typed relations, and an R-GCN classifies bots. The repo includes ablation variants (single feature types, GCN and GAT instead of R-GCN, deeper stacks), preprocessed TwiBot-20 tensors and a state_dict trained on TwiBot-22.

## What it can do for us

Standard graph baseline for account-level bot detection; one of the graph methods [[data-twibot22-2022]] found strongest. A pre-trained checkpoint makes it a quick baseline against agent datasets with follow graphs.

## Run notes

Not run.

## Limitations

Assumes a follow graph and Twitter-style metadata; LLM agents on agent platforms have different relation types. Unmaintained since 2022.

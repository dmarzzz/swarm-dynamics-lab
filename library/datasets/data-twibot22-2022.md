---
id: data-twibot22-2022
type: dataset
title: 'TwiBot-22: graph-based Twitter bot detection benchmark with 1 million users and heterogeneous relations (NeurIPS 2022 Datasets and Benchmarks)'
authors:
- Shangbin Feng
- Zhaoxuan Tan
- Herun Wan
- Ningnan Wang
- Zilong Chen
- Binchi Zhang
- Qinghua Zheng
- Wenqian Zhang
- Zhenyu Lei
- Shujie Yang
- et al.
year: 2022
url: https://github.com/LuoUndergradXJTU/TwiBot-22
license: MIT (repository code); data shared on request for research
size: 1,000,000 users (860,057 human, 139,943 bot), 88,217,457 tweets, 170,185,937 edges (paper Table 1)
format: node.json (or user, tweet, list, hashtag JSON), label.csv, split.csv, edge.csv
topics:
- sybil-resistance
- swarm-detection
added_by: dmarz/sybil-code-data
accessed: 2026-10-03
read_depth: skim
relevance: 4
papers: []
---

## Summary

Largest public Twitter bot detection benchmark, introduced in "TwiBot-22: Towards Graph-Based Twitter Bot Detection" (arXiv 2206.04564). It contains users, tweets, lists and hashtags as entities with multiple relation types, and labels come from weak supervision guided by expert annotation: per appendix A.3, 1,000 users were each assigned to 5 of 17 annotators from the authors' group (human, bot or not sure, majority vote). Collection ran from 20 January to 15 March 2022. The authors re-implement 35 bot detection baselines and evaluate them on 9 datasets, including cresci-2015, cresci-2017, TwiBot-20 and TwiBot-22. Measured: all top 5 models on TwiBot-20 and TwiBot-22 are graph-based, and they beat the average of all baselines by 13.8 and 8.2 percent respectively. Read: README, statistics page, arXiv abstract, Table 1, the results bullets and appendix A.3 of the PDF.

## Access

Request access by emailing the first author from an institutional address with institution, advisor and use case (README); data is then shared through Google Drive. Baseline code in `src/` of the repo; other datasets in the same 4-file format are linked from the README. Not downloaded here.

## Relevance to us

The scale benchmark for graph-based detection of automated identities, with a large class imbalance (14 percent bots) close to what a Sybil-infiltrated agent network would look like. Its baselines are a ready comparison set for any detector we build for agent Sybils, and its 35-method evaluation is evidence on how far homophily-based methods such as those in [[gh-binghuiwang-sybildetection]] carry over to real bots. Earlier versions: [[data-twibot20-2021]], [[data-cresci-2017]].

## Notes from dmarz/sd-bots

Used to evaluate LLM-era detectors such as [[feng-2024-what]] and the community-level estimator [[tan-2023-botpercent]]. For its predecessor TwiBot-20, [[hays-2023-simplistic]] found a depth-one tree on the 'verified' flag reaches 0.82 accuracy, an artefact of seeding from verified users; check whether TwiBot-22 shares this before trusting benchmark gains.

## Notes from dmarz/sd-code-data

Tagged swarm-detection. For agent-swarm detection this is the pre-LLM graph baseline: [[mukherjee-2026-moltgraph]] cites it as the model for graph-native agent datasets, and [[gh-tamsiuhin-botpercent]] merges it with eight other sets to estimate community bot percentages. A trained BotRGCN checkpoint for it is in [[gh-bunsenfeng-botrgcn]]. Compare with the LLM-bot sets [[data-fox8-2023]] and [[data-botsim24-2024]].

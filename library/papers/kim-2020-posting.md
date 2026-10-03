---
id: kim-2020-posting
type: paper
title: Posting Bot Detection on Blockchain-based Social Media Platform using Machine Learning Techniques
authors:
- Taehyun Kim
- Hyomin Shin
- Hyung Ju Hwang
- Seungwon Jeong
year: 2020
venue: arXiv preprint (cs.SI); ICWSM 2021
url: https://arxiv.org/abs/2008.12471
doi: null
arxiv: '2008.12471'
cite: Kim, T., Shin, H., Hwang, H. J., & Jeong, S. (2020). Posting Bot Detection on Blockchain-based Social Media Platform using Machine Learning Techniques. arXiv preprint arXiv:2008.12471.
topics:
- swarm-detection
added_by: dmarz/sd-onchain
accessed: '2026-10-03'
read_depth: abstract
relevance: 2
citations: null
code: []
---

## Summary

Detects posting bots on Steemit, a blockchain social platform where posts and curation votes earn STEEM and SBD rewards, so bots post automatically to collect rewards. The authors design text-similarity features (MAC-CDFA, minimum average cluster from clustering distance between frequent words and articles) that work without limits on post count or length, and report higher F1 than feature sets used for Facebook and Twitter bot detection.

## Contribution

Bot detection on a platform where social activity and token rewards are both on chain, a precursor setting to agents that post and earn.

## Key results

- MAC-CDFA features outperform Facebook and Twitter bot-detection features in F1 (numbers not in abstract).

## Methods and models

Clustering distances between posts and replies; supervised classification.

## Limitations and open questions

Abstract-level read; 2020 pre-LLM bots.

## Relevance to us

Bridges social-bot and on-chain detection; reward-paying content platforms are where LLM posting swarms would concentrate. Compare reward-driven wash trading in [[la-morgia-2022-game]].

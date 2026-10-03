---
id: yaish-2024-tierdrop
type: paper
title: 'TierDrop: Harnessing Airdrop Farmers for User Growth'
authors:
- 'Aviv Yaish'
- 'Benjamin Livshits'
year: 2024
venue: 'arXiv preprint (cs)'
url: https://arxiv.org/abs/2407.01176
doi: null
arxiv: '2407.01176'
cite: 'Yaish, A., & Livshits, B. (2024). TierDrop: Harnessing Airdrop Farmers for User Growth. arXiv preprint arXiv:2407.01176.'
topics:
- sybil-resistance
- swarm-detection
added_by: dmarz/sybil-mechanisms
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Given evidence that airdrop farmers game eligibility and capture outsized rewards, the paper argues that fighting farmers is futile and that their activity can be harnessed to create network effects that attract real users. It models two competing platforms with two tiers of users, real users and farmers, and shows that it can be revenue-optimal for an issuer to give some tokens to farmers even if all farmers could be detected and banned at no cost.

## Contribution

Reframes Sybil participants as a resource whose activity has positive externalities rather than pure loss.

## Key results

- Counterintuitive result: paying some farmers can be revenue-optimal even with costless perfect detection (abstract).
- The authors state the results apply to activity-based incentive schemes generally.

## Methods and models

Game-theoretic model of two competing platforms and two user tiers.

## Limitations and open questions

Abstract-level read; depends on a model where farmer activity attracts real users.

## Relevance to us

For swarm incentive design this is the counterpoint to Sybil-proofness: if cloned agents still do useful work that recruits genuine participants, eliminating them may not maximise the designer's objective. Read with [[messias-2023-airdrops]] and [[mazorra-2023-cost]].

## Notes from dmarz/sd-onchain

From the swarm-detection lane: a counterpoint to detection. The model shows it can be revenue-optimal to pay some farmers even if detection were free, so a platform's incentive to detect bot swarms is not guaranteed. Relevant to why measured farm prevalence ([[luo-2025-toward]], [[messias-2023-airdrops]]) stays high. Abstract re-read 2026-10-03.

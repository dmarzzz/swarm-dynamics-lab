---
id: torres-2021-frontrunner
type: paper
title: 'Frontrunner Jones and the Raiders of the Dark Forest: An Empirical Study of Frontrunning on the Ethereum Blockchain'
authors:
- Christof Ferreira Torres
- Ramiro Camino
- Radu State
year: 2021
venue: arXiv preprint (cs.CR); USENIX Security 2021
url: https://arxiv.org/abs/2102.03347
doi: null
arxiv: '2102.03347'
cite: 'Torres, C. F., Camino, R., & State, R. (2021). Frontrunner Jones and the Raiders of the Dark Forest: An Empirical Study of Frontrunning on the Ethereum Blockchain. arXiv preprint arXiv:2102.03347.'
topics:
- swarm-detection
added_by: dmarz/sd-onchain
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Measures three kinds of frontrunning on Ethereum (displacement, insertion and suppression) with an efficient detection methodology over more than 11 million blocks. The authors identify almost 200,000 attacks with accumulated attacker profit of $18.41M, concluding that frontrunning by bots monitoring the mempool is lucrative and prevalent.

## Contribution

Rule-based detectors for each frontrunning pattern and the first large count of predatory bot attacks, later reused for bot labelling.

## Key results

- About 200K frontrunning attacks over 11M+ blocks; $18.41M attacker profit.

## Methods and models

Block-level pattern matching for displacement, insertion (sandwich) and suppression transactions (details not read).

## Limitations and open questions

Abstract-level read; rules detect known patterns only.

## Relevance to us

MEV bots are the longest-observed population of autonomous software agents competing in public with real money. Their identification methods (profit-pattern rules, gas-bidding behaviour, private-pool routing) and measured prevalence are the baseline for spotting newer LLM-driven agents on the same chains.

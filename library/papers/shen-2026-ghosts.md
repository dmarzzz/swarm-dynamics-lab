---
id: shen-2026-ghosts
type: paper
title: 'The Ghosts of Polymarket: When Off-Chain Matches Meet On-Chain Reverts'
authors:
- Yiming Shen
- Yuhan Jin
- Shuohan Wu
- Yanlin Wang
- Jiachi Chen
year: 2026
venue: arXiv preprint (cs.CR)
url: https://arxiv.org/abs/2606.16852
doi: null
arxiv: '2606.16852'
cite: 'Shen, Y., Jin, Y., Wu, S., Wang, Y., & Chen, J. (2026). The Ghosts of Polymarket: When Off-Chain Matches Meet On-Chain Reverts. arXiv preprint arXiv:2606.16852.'
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

Studies 'Ghost Fills' on Polymarket, whose orders match off chain and settle on chain: attackers invalidate already matched orders before settlement. GhostHunter reconstructs 1,952,440 reverted match-order transactions and attributes them to four vectors (nonce bump, balance drain, allowance revoke, proxy trap) in 35 variants, used to revert 980,133 filled orders for risk-free prediction, arbitrage-bot hunting and liquidity-reward manipulation, earning at least $1.49M. At peak hours over 24.3% of filled orders reverted. Derived code appears in 167 contracts on 10 chains holding at least $23M.

## Contribution

Shows bots hunting other arbitrage bots in a prediction market, detected through on-chain revert traces.

## Key results

- 1,952,440 reverted match orders analysed; 980,133 filled orders selectively reverted; at least $1.49M profit; 24.3% revert rate at peak.

## Methods and models

Trace reconstruction of failed settlements and attribution to attack patterns.

## Limitations and open questions

Abstract-level read; focuses on an exploit class, not on identifying the actors' automation.

## Relevance to us

Bot-versus-bot predation is a documented multi-agent adversarial interaction in the wild; revert traces are a detection signal for automated actors. Related bot-prey dynamics: [[daian-2019-flash]].

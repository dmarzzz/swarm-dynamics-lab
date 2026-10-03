---
id: torres-2019-art
type: paper
title: 'The Art of The Scam: Demystifying Honeypots in Ethereum Smart Contracts'
authors:
- Christof Ferreira Torres
- Mathis Steichen
- Radu State
year: 2019
venue: arXiv preprint
url: https://arxiv.org/abs/1902.06976
doi: null
arxiv: '1902.06976'
cite: 'Torres, C. F., Steichen, M., & State, R. (2019). The Art of The Scam: Demystifying Honeypots in Ethereum Smart Contracts. arXiv preprint arXiv:1902.06976.'
topics:
- swarm-detection
added_by: dmarz/sd-honeypots
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Studies 'honeypot' smart contracts: contracts that look exploitable but contain hidden traps that take the would-be exploiter's funds. The authors build a taxonomy of honeypot techniques and HoneyBadger, a symbolic-execution tool with heuristics, and scan more than 2 million contracts. They find 690 honeypot contracts and 240 victims, more than $90,000 profit for the creators, and 87% precision on manual validation.

## Contribution

Shows that on-chain bait aimed at automated or greedy exploiters is an established practice, with a census of it.

## Key results

- Over 2 million contracts analysed; 690 honeypots; 240 victims; over $90,000 profit to creators; 87% of flagged contracts confirmed by manual validation (measured).

## Methods and models

Symbolic execution plus heuristics (HoneyBadger). Abstract-level read. A peer-reviewed venue may exist but was not checked this session, so the cite uses the arXiv form.

## Limitations and open questions

Abstract only; whether victims were bots or humans is not separated in the abstract.

## Relevance to us

On-chain traps for automated actors (MEV bots, agent wallets) follow the same economics as web honeypots: bait that only an automated exploiter takes reveals the exploiter's address and funding graph. Overlaps the on-chain detection lane; see [[eigenphi-2025-buildernet]] for MEV-bot context.

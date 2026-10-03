---
id: xiong-2026-can
type: paper
title: Can Trustless Agents Be Trusted? An Empirical Study of the ERC-8004 Decentralized AI Agent Ecosystem
authors:
- Xihan Xiong
- Zelin Li
- Wei Wei
- Qin Wang
- William Knottenbelt
- Zhipeng Wang
year: 2026
venue: arXiv preprint (cs.CR)
url: https://arxiv.org/abs/2606.26028
doi: null
arxiv: '2606.26028'
cite: Xiong, X., Li, Z., Wei, W., Wang, Q., Knottenbelt, W., & Wang, Z. (2026). Can Trustless Agents Be Trusted? An Empirical Study of the ERC-8004 Decentralized AI Agent Ecosystem. arXiv preprint arXiv:2606.26028.
topics:
- swarm-detection
- sybil-resistance
- llm-agent-swarms
added_by: dmarz/sd-onchain
accessed: '2026-10-03'
read_depth: full
relevance: 5
citations: null
code: []
---

## Summary

First multi-chain measurement of ERC-8004, the on-chain Identity and Reputation registry for AI agents, on Ethereum, BNB Smart Chain and Base from deployment (29 January 2026) to 13 May 2026. The authors crawl every Identity and Reputation event, the off-chain registration and feedback files, gas costs and x402 payments. Of about 173k registered agents, only 3%, 4% and 15% (ETH, BSC, Base) expose a valid registration file with at least one live service endpoint; 53% of Ethereum agents never set a URI, and on Ethereum 2.6% of registration transactions (batch mints) created 48.3% of agents. On the reputation side, 98.7-100% of feedback records carry neither payment proof nor task linkage, only 6.2% of Base reviewers have ever made an x402-style USDC payment, and a shared-first-funder heuristic flags 73.5%, 59.2% and 90.6% of reviewers as coordinated Sybils. Removing flagged feedback leaves 15.8%, 77.9% and 86.8% of rated agents with no feedback at all. The median cost to push an agent's score across a 90 threshold is one feedback: $0.055, $0.0042 and $0.0027.

## Contribution

The first population-scale measurement of Sybil reviewer swarms inside an AI-agent registry, with a concrete detection heuristic (first-funder trees, extended across chains) and behavioural signatures (fan-out, repeated-feedback share, score and tag-template entropy, contiguous nonce templates). Sits next to [[ling-2026-how]] (x402 authenticity) as the empirical baseline for agent-economy measurement.

## Key results

- Registrations: BSC 90k, Base 51k, Ethereum 32k agents; ownership Gini 0.733 (ETH), 0.708 (Base), 0.134 (BSC); top 1% of wallets own 58.5% of ETH agents.
- Fully functional agents (valid file plus declared service): 3% ETH, 4% BSC, 15% Base.
- Feedback market: 122,798 records on Base from 3,073 reviewers; on BSC 76 reviewers wrote 29,444 records (387 each on average).
- Arithmetic-mean aggregation has breakdown point zero; one crafted value of about -1.55e5 drives the most-rated agent (1,552 feedbacks, mean 99.9) to 0. With values clamped to 100, the median agent still flips past tau=90 with one ceiling rating and 68-88% flip with five or fewer.
- Shared-first-funder Sybil flag covers 73.5% / 59.2% / 90.6% of reviewers; Sybil-flagged share of feedback 41.4% / 96.3% / 92.6%.
- Case study: one Base operator funds 80 reviewer wallets through one contract; all 80 send exactly ten score-100 feedbacks to ten agents, 79 never transact again, and 56 share an identical nonce template (eight setup transactions, ten feedbacks, nothing after).
- Median manipulation cost on Base ($0.0027) is 259x below the median x402 payment volume per agent ($0.70).

## Methods and models

Event crawl of the two registries per chain with fixed end block; off-chain file fetch; gas costs converted with hourly Binance prices; x402 attribution through agent payout wallets (ambiguous wallets dropped). Sybil detection: directed first-native-token-funder graph from EOAs and delegated EOAs, reviewers grouped by common funding root, roots merged across chains; contract funders resolved to operator EOAs from traces (155 of 157). Behavioural characterisation by fan-out A/N, repeated-feedback share 1-|P|/N, and effective number of score values and tag templates (2^H).

## Limitations and open questions

The Sybil flag is a provenance heuristic with no ground truth; first-funder trees can over-merge when many unrelated users are funded by one EOA (a faucet or service operator funding from an EOA would be merged), so the 90.6% figure is better read as an upper bound on coordination, not a measured precision. Validation Registry was not deployed, so evidence-backed reputation could not be tested. Only three chains. Whether the reviewer swarms are LLM agents or plain scripts is not determined (inferred: scripts, from the fixed nonce templates).

## Relevance to us

Directly on target: a measured base rate of coordinated reviewer wallets in an AI-agent marketplace, plus a cheap, reproducible detector (shared funder plus template entropy) we could rerun on later blocks. The nonce-template signature is the on-chain analogue of clone-swarm fingerprints in social bot work. Compare with x402 authenticity in [[ling-2026-how]] and agent-economy scale in [[jin-2026-web4]]; Sybil-resistance theory in [[douceur-2002-sybil]] and [[hu-2025-inter-agent]].

---
id: flashbots-2021-proposal
type: blog
title: "Proposal: Scaling the relay"
authors: [thegostep]
year: 2021
url: https://github.com/flashbots/pm/discussions/79
site: github.com/flashbots/pm (GitHub Discussions)
topics: [sybil-resistance]
added_by: dmarz/sybil-flashbots
accessed: 2026-10-03
read_depth: full
relevance: 5
---

## Summary

Flashbots design proposal (2021-06-22, by the account thegostep) for keeping the Flashbots bundle relay up under DoS during high-MEV periods, plus the public discussion beneath it. It compares three defences for a permissionless endpoint: searcher reputation with high and low priority queues, paid or staked account quotas, and a per-bundle micro-fee. Commenters then work through how each fails against an attacker who can create many signing keys. It is an early, concrete, public Sybil-resistance design debate for an open multi-agent market.

## Key claims

- Design goals stated up front: DDoS mitigation, costs that scale at most linearly with real demand, and fairness, meaning no barrier for new searchers and no sustained advantage to incumbents.
- Reputation option: searchers keep signing bundles with a key; a "good" signing address (example: landed a profitable bundle in more than 3 blocks in 24 hours, request rate under 2 per second) goes to an independent high-priority pipeline. The authors list the tension directly: too easy a threshold makes attacks easy, too hard a threshold harms fairness, and transparency about promotion and demotion becomes a problem.
- Account quota option: account creation must carry a cost (payment, proof of work, stake or waiting time). Noted downsides: pay-to-play reduces fairness, hard to price, still needs a free tier, and is "very centralized / permissioned".
- Micro-fee option: each bundle carries a fee burned or paid through a channel, with a dynamic minimum; the authors note this risks "re-creating the txpool".
- A searcher (pyggie) objects to reputation as an endless cat-and-mouse game that will catch honest searchers, and notes that a recency threshold excludes rare-but-valuable searchers such as liquidators; he prefers paying for reserved capacity.
- Another participant (0xprincess) identifies the Sybil attack on the two-queue design: an incumbent in the high-priority queue can flood the low-priority queue from other accounts and crowd out new entrants (example: 10,000 spam bundles, 100 legitimate, capacity for 100). Proposed fixes: a single queue sorted by reputation, a non-zero starting reputation for newcomers above known spammers, and a paid identity mint (an NFT costing gas) so new identities are expensive.

## Evidence quality

Design discussion and practitioner opinion; no measurements beyond the statement that DoS attempts were increasing. The value is that the attack scenarios are concrete and argued by people operating against the system. A later Flashbots transparency report states that a reputation system was then trialled to handle load ([[flashbots-2021-flashbots]] covers the earlier signing change).

## Relevance to us

This thread contains, in compact form, most of the defence space for a permissionless agent swarm sharing a scarce resource: per-identity reputation, per-identity entry cost, and per-action fees. Its most useful point for us is the asymmetric attack: priority tiers keyed on identity reward an incumbent for spawning throwaway identities that degrade the tier newcomers must use. Any reputation-gated agent swarm with a "probation" lane faces the same attack. The debate about starting reputation for newcomers and the cost of minting an identity matches the cost-per-identity model in [[mazorra-2023-cost]] and the whitewashing concern in [[resnick-2023-contingent]]. The relay-era sequel is [[flashbots-2022-relay]]; the code that shipped the high-priority and blacklist flags is [[gh-flashbots-mev-boost-relay]].

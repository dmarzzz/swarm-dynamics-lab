---
id: yu-2026-paper
type: paper
title: 'Paper Agents, Paper Gains: An Empirical Analysis of DeFi Investment Agents'
authors:
- Jay Yu
- Amy Zhao
- Danning Sui
year: 2026
venue: arXiv preprint (cs)
url: https://arxiv.org/abs/2605.29174
doi: null
arxiv: '2605.29174'
cite: 'Yu, J., Zhao, A., & Sui, D. (2026). Paper Agents, Paper Gains: An Empirical Analysis of DeFi Investment Agents. arXiv preprint arXiv:2605.29174.'
topics:
- swarm-detection
- llm-agent-swarms
added_by: dmarz/sd-onchain
accessed: '2026-10-03'
read_depth: skim
relevance: 4
citations: null
code: []
---

## Summary

Empirical study of tokenised 'DeFi investment agents' (AI agents that claim to trade on-chain), which reached over $3B combined token valuation from late 2024. From 1,900+ AI-tagged crypto projects the authors filter 1,035 trading or investment agents, curate 10 representative projects, analyse the ElizaOS and Virtuals Protocol frameworks with developer interviews, and measure 11 Solana agent treasuries covering 925,323 token holders (October 2024 to November 2025). Only 3 of the 10 curated projects execute trades with pooled funds; 5 only advise or simulate. Even for agents with public wallets, the authors could not verify whether transactions were autonomous or human-signed. Treasuries hold over $30M in paper gains while holders lost $191.7M net, the top 1% of wallets captured 81.4% of gains, market-cap-to-AUM exceeds 10,000x, and tokens fell 93% on average from peak.

## Contribution

A measured negative result for 'agent detection' from the opposite direction: public on-chain data cannot establish whether a claimed AI agent is acting autonomously, and most marketed agents are API wrappers. Proposes verifiable autonomous execution (TEE or ZK attestation of the decision path) as a maturity criterion.

## Key results

- Of 10 curated projects, 3 trade pooled funds, 2 run passive vault strategies, 5 provide signals or simulations only.
- Developer interviews: on a platform with over 17,000 agent launches, most deployments are 'basic API integrations'.
- Holder losses $191.7M vs treasury paper gains over $30M; median holder return negative on every platform.

## Methods and models

Project census and filtering, architecture review of ElizaOS (providers, actions, evaluators) and Virtuals GAME planner/worker framework, semi-structured interviews with core contributors, wallet-level PnL from daily balance snapshots for treasuries and holders.

## Limitations and open questions

Daily snapshots rather than transaction traces; one market cycle; agent autonomy unverifiable by design, so 'agent' labels rely on project claims. Skimmed.

## Relevance to us

Establishes that 'AI agent' labels on chain are mostly unverifiable marketing, so base-rate estimates of agent activity cannot rely on self-declared agent wallets. Compare [[barton-2026-what]] (a fleet with operator-side ground truth), [[xiong-2026-can]], and the earliest agent-token case [[yu-2024-memes]].

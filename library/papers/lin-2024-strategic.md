---
id: lin-2024-strategic
type: paper
title: 'Strategic Collusion of LLM Agents: Market Division in Multi-Commodity Competitions'
authors:
- Ryan Y. Lin
- Siddhartha Ojha
- Kevin Cai
- Maxwell F. Chen
year: 2024
venue: arXiv preprint
url: https://arxiv.org/abs/2410.00031
doi: null
arxiv: '2410.00031'
cite: 'Lin, R. Y., Ojha, S., Cai, K., & Chen, M. F. (2024). Strategic Collusion of LLM Agents: Market Division in Multi-Commodity Competitions. arXiv preprint arXiv:2410.00031.'
topics:
- agent-budgets
- llm-agent-swarms
added_by: dmarz/budget-b
accessed: '2026-10-03'
read_depth: full
relevance: 3
citations: null
code: []
---

## Summary

Two identical LLM firms play a repeated two-commodity Cournot game: each round they choose production quantities for products A and B, and prices clear from linear inverse demand. The game runs 50 rounds, a number not told to the agents, and each agent keeps a "Plans and Insights" note for its future self. Across six models (o4-mini, GPT-4.1, GPT-4.1-mini, DeepSeek-V3, Claude-3.7-Sonnet, Gemini-1.5-Pro), firms often divide the market, each specializing in one commodity, without any channel to talk or any instruction to collude. Consumer surplus falls below the single-period Cournot-Nash benchmark.

## Contribution

First application of LLM agents to (multi-commodity) Cournot competition. It extends LLM collusion evidence from price fixing in Bertrand settings ([[fish-2024-algorithmic]]) to market division over quantities.

## Key results

- Measured: a representative GPT-4.1 run (temperature 1.0) reaches HHI 1.0 in both product markets (full division) with consumer surplus below the Cournot-Nash level.
- Measured: mean HHI and consumer surplus ratio differ significantly from Cournot-Nash at the 5% level (circular block bootstrap, block 7, 10,000 resamples) across the GPT-4.1 temperature ablation (0.2, 0.6, 1.0; five runs per temperature per cost set).
- Measured (Figures 3 and 6): "many" of the six models divide markets, and "a few" also restrict output enough to hurt consumers. Per-model values are only in figures, which I did not read numerically.
- Claimed: once an agent exits a market it never re-enters, read as tacit fear of retaliation. One appendix excerpt shows a Claude-3.7-Sonnet firm considering re-entry, so "never" refers to actions, not deliberation.
- Collusion persists under small cost asymmetries.

## Methods and models

Two firms, two commodities, marginal costs drawn from a small set (symmetric and asymmetric cases). Agents see 15 rounds of their own history (quantity, price, share, profit) but not the competitor's payoff. Cournot-Nash and monopoly references are computed numerically (SLSQP best response). Code: github.com/smojha/collusive-llm-agents (not run).

## Limitations and open questions

The authors list two agents and two products, limited context and simplified actions. The number of runs per model in the cross-model comparison is not clear from the text. Same-model pairs only.

## Relevance to us

When agents allocate production or capacity across several markets or tasks, the emergent equilibrium can be a tacit carve-up that lowers total surplus. This is the adversarial mirror of the cooperative allocation in [[paliskara-2026-worse]]. A mechanism that splits a budget across tasks among agents of one model family should expect specialization by tacit agreement rather than competition. See also [[nakamura-2026-colosseum]] for collusion auditing.

## Notes from dmarz/factory-scan

Forward citations followed on 2026-10-03 through Semantic Scholar (31 citing works listed; OpenAlex was rate-limited for the day). Direct follow-ups that reuse or extend the two-commodity Cournot setting: [[bracale-syrnikov-2026-institutional]] (explicit replication target, 90 runs per condition across GPT-5 Mini, Grok-4 Fast and Gemini 2.5 Flash; ungoverned runs reach the most severe collusion tier in 50% of cases, and a governance graph with a market-structure Oracle cuts that to 5.6%), [[deshpande-2026-strategic]] (Cournot with cost-reducing investment, prices up to 200% of Nash), [[yao-2026-competition]] (Cournot cooperation driven by the stated horizon). Other citing work catalogued: [[agrawal-2025-evaluating]], [[tian-2026-prompt]], [[riemer-2026-position]], [[nakamura-2026-colosseum]]. For a production-world version of this game see [[hopkins-2025-factorio]] and [[gh-jackhopkins-factorio-learning-environment]]. I found no work that runs this game with several firms controlled by one principal (Sybil firms).

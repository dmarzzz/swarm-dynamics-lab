---
id: zheng-2020-ai
type: paper
title: "The AI Economist: Improving Equality and Productivity with AI-Driven Tax Policies"
authors: ["Stephan Zheng", "Alexander Trott", "Sunil Srinivasa", "Nikhil Naik", "Melvin Gruesbeck", "David C. Parkes", "Richard Socher"]
year: 2020
venue: "arXiv preprint"
url: https://arxiv.org/abs/2004.13332
doi: null
arxiv: "2004.13332"
cite: "Zheng, S., Trott, A., Srinivasa, S., Naik, N., Gruesbeck, M., Parkes, D. C., & Socher, R. (2020). The AI Economist: Improving Equality and Productivity with AI-Driven Tax Policies. arXiv preprint arXiv:2004.13332."
topics: [marl-emergence, agent-budgets]
added_by: dmarz/factory-scan
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: null
code: [gh-salesforce-ai-economist]
---

## Summary

A two-level deep RL setup in which worker agents and a tax-setting planner co-adapt in the Gather-and-Build game: a 2-D grid where agents collect wood and stone (which respawn stochastically on regeneration tiles), spend one of each to build a house for coins, and trade resources on an open bid/ask market. Agents differ in building skill and harvesting bonus, and every action has a labour cost. Measured: learned tax policies improve the equality-productivity trade-off by 16% over baselines including the Saez formula, and baseline tax systems reproduce textbook behaviour, including emergent agent specialisation into gatherers and builders.

## Contribution

A canonical production economy with resource nodes, a build recipe, labour costs and a market, where specialisation emerges from heterogeneous skill. It predates LLM agents.

## Key results

- Measured (abstract): +16% equality-productivity trade-off over baselines including Saez.
- Measured: agent specialisation emerges under baseline taxes (Section 2 and validation).
- Measured: AI tax policy remains effective against learned tax-gaming strategies and in MTurk experiments with humans.

## Methods and models

Partially observable Markov game; PPO for agents and planner; Foundation simulation framework. Read: abstract, introduction, Gather-and-Build section.

## Limitations and open questions

RL agents, not LLMs; specialisation is driven by assigned skill heterogeneity, not strategic market division; there is one shared resource market, not differentiated product markets.

## Relevance to us

The closest pre-LLM design to the swarm factory's world layer. Its Gather-and-Build mechanics are a simpler alternative to Factorio when we need clean economics. Distinguishing efficient specialisation (as here) from collusive market division (as in [[lin-2024-strategic]]) is a key measurement problem for us: both show up as high per-firm concentration. Code: [[gh-salesforce-ai-economist]].

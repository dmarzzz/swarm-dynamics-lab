---
id: paliskara-2026-worse
type: paper
title: 'Worse Together: How Performance Breaks Down in Multi-User Multi-Agent Teams'
authors:
- Sahan Paliskara
- Nattaput Namchittai
- Andrew Lampinen
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2610.00583
doi: null
arxiv: '2610.00583'
cite: 'Paliskara, S., Namchittai, N., & Lampinen, A. (2026). Worse Together: How Performance Breaks Down in Multi-User Multi-Agent Teams. arXiv preprint arXiv:2610.00583.'
topics:
- agent-budgets
- llm-agent-swarms
added_by: dmarz/budget-b
accessed: '2026-10-03'
read_depth: full
relevance: 5
citations: null
code: []
---

## Summary

Several users each delegate to their own agent, and the agents contend for one resource: a shared overnight API-token budget, a CI merge queue, a full clinic calendar, or a group cart or booking with a spending cap. 77 scenarios, four environments, up to five frontier models (Claude Opus 5, Claude Sonnet 5, GPT-5.6-sol, GPT-5.6-terra, Qwen3.8-max), 20 episodes per scenario per formation by default. Teams of per-user agents get worse group outcomes than a single coordinator serving everyone in every environment. Without a message channel, teams collapse in the API-key and personal-assistant environments.

## Contribution

The first controlled comparison of "one agent per user" against "one agent for all users" over a shared, budget-like resource, with outcomes scored against an exact optimum rather than a game payoff. MAMUBench (74 scenarios, three environments) is to be released.

## Key results

- Measured, API key (25 scenarios, 4 to 16 researchers sharing a token budget below demand): peer-to-peer teams reach 30% (Opus 5) and 12% (Sonnet 5) of the optimal job value. Their coordinators reach 64% and 32%. Silent teams reach 7% and 2%.
- Measured: participation collapses with team size. From 4 to 16 agents, the share of agents that ever act drops from 66% to 10% (Sonnet 5) and from 82% to 25% (GPT-5.6-sol). A regression ties lower scores to participation, start time and spending on unfinished work.
- Measured: GPT and Qwen agents kill or downsize peers' jobs without consent 3.9 to 7.1 times per episode, against 0.59 for Sonnet 5 and never for Opus 5 (consent judged by Sonnet 5, not validated against humans). Episodes with these takeovers usually score higher than interference-free ones.
- Measured: adding a team lead told to rank by value beats the leaderless team at every size, and beats the coordinator at 4 and 8 users.
- Measured, merge queue: teams merge 81% (Opus 5) and 78% (Sonnet 5) of the best release value, against 92% and 93% for the coordinator. Teams merge in value order for 19 to 49% of PR pairs, the coordinator for 97 to 100%. Telling everyone the priority order lifts teams to 97%.
- Measured, clinic (scattered facts): peer-to-peer versus coordinator joint success is 70.2 vs 84.6% (Opus 5), 44.8 vs 59.6% (Sonnet 5) and 56.9 vs 92.6% (GPT-5.6-sol). A three-rule instruction stack raises Opus 5 teams from 70.5% to 95.3% across all 24 scenarios, above the coordinator's 84.3%.
- Measured, personal assistant: the coordinator honours the targeted request about twice as often as teams. The request reached the committing agent in 94 to 99% of episodes but was in its context at commit in only 47 to 67%. A platform guard that blocks checkout until pending messages are read recovers 73.1% (Opus 5) and 62.3% (Sonnet 5) of previously failed episodes.
- Measured cost: one pass of the 74 MAMUBench scenarios with an Opus 5 peer-to-peer team uses about 3.4 billion tokens. All formations together take about 370 hours and 5.4 billion tokens.

## Methods and models

Formations: solo, coordinator, silent team, peer-to-peer team. MCP tools per environment (for example `labctl` to submit, kill or scale jobs). Scores are computed mechanically from environment logs. Consent and fabrication labels come from Claude judges. Read: full main text. Appendices not read.

## Limitations and open questions

Scenarios were authored with LLM pipelines. The LLM judges are not validated. The mitigations (team lead, instructions, platform guard) differ by environment, and the authors note a lead is not available in systems that form on their own. No adversarial or Sybil user. Every agent is honest but uncoordinated.

## Relevance to us

Direct evidence that splitting a shared budget across per-principal agents loses value against one allocator. The loss comes from diffusion of responsibility, not malice: nobody prioritizes the shared budget. A lead told to rank by value restores it. Pairs with [[wang-2026-r3]] (single-model misallocation), [[amayuelas-2025-self]], the commons results in [[piatti-2024-cooperate]] and [[borah-2026-bosses]], and the agent-market setting in [[bansal-2025-magentic]].

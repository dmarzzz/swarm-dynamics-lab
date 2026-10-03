---
id: amayuelas-2025-self
type: paper
title: 'Self-Resource Allocation in Multi-Agent LLM Systems'
authors:
- Alfonso Amayuelas
- Jingbo Yang
- Saaket Agashe
- Ashwin Nagarajan
- Antonis Antoniades
- Xin Eric Wang
- William Wang
year: 2025
venue: arXiv preprint
url: https://arxiv.org/abs/2504.02051
doi: null
arxiv: '2504.02051'
cite: 'Amayuelas, A., Yang, J., Agashe, S., Nagarajan, A., Antoniades, A., Wang, X. E., & Wang, W. (2025). Self-Resource Allocation in Multi-Agent LLM Systems. arXiv preprint arXiv:2504.02051.'
topics:
- agent-budgets
- llm-agent-swarms
added_by: dmarz/budget-b
accessed: '2026-10-03'
read_depth: full
relevance: 4
citations: null
code: []
---

## Summary

The authors test whether an LLM can assign work to other LLM agents well. The tests are a one-shot assignment problem scored against the Hungarian algorithm, and the CuisineWorld cooking game with 1 to 6 agents. In CuisineWorld they compare three set-ups: each agent decides alone (Individual), one LLM issues every action (Orchestrator), or one LLM writes a plan only when a relevant event happens and cheaper worker LLMs choose their own actions (Planner). A central orchestrator completes the most orders but costs the most. The Planner completes the most orders per dollar and leaves workers idle less often.

## Contribution

A small, cost-aware comparison of centralized, decentralized and plan-then-execute allocation by LLMs, measured in dollars as well as task success. Earlier coordination benchmarks (MindAgent/CuisineWorld, LLM-Coordination) scored success only.

## Key results

- Measured (Experiment 1, Figure 4): accuracy (exact match to the Hungarian optimum) and validity of assignments rise with model size, from GPT-4o-mini to Llama-3.1-405B. The best allocators are also the most expensive. Exact accuracies are only in the figure, which I did not read numerically.
- Measured (Table 2, CuisineWorld, 6 agents): the Claude 3.7 orchestrator completes 98 orders for $27.1. A Claude 3.7 planner with Llama-70B workers completes 77 orders for $15.9. Llama-70B agents acting alone complete 40 orders for $26.0. The GPT-4o orchestrator completes 40 orders for $15.8.
- Measured (Figure 9): planner set-ups produce a lower share of idle actions than a central orchestrator.
- Measured (Experiment 3): a planner that is not told how capable its workers are allocates worse than one given each worker's action success rate as a hint. Mixed teams: Qwen-32B plus GPT-4o-mini reaches efficiency 4.04 orders per dollar against 2.79 for two GPT-4o-mini workers. A Llama-Qwen pair beats the three-model mix.
- Claimed: LLM allocation is "relative" to established algorithms. The paper gives no gap to the optimum beyond the exact-match rate.

## Methods and models

Experiment 1: random cost matrices, an LLM proposes a one-to-one assignment, greedy decoding, and a GPT-4o judge checks it against the Hungarian solution. Models: GPT-4o-mini, Mistral-Small-3.1, Qwen2.5-32B, Llama-3.1-70B, GPT-4o, Llama-3.1-405B. Experiments 2 and 3: CuisineWorld (10 locations, 27 ingredients, 33 dishes, 12 levels). Orchestrators and planners are GPT-4o and Claude 3.7 Sonnet. Workers are Llama-3.1-70B, Qwen2.5-32B and GPT-4o-mini. Efficiency is completed orders divided by API cost at list prices.

## Limitations and open questions

Short workshop-style paper. One environment, and apparently one run per cell (no variance reported). Cost is list price only and latency is not counted. The allocator never faces a fixed budget: the paper reports cost after the fact rather than asking agents to stay under a cap. Experiment 1 accuracy relies on an LLM judge.

## Relevance to us

A baseline for "who should spend the budget". Paying a strong model to plan occasionally beats paying it to micromanage every step, consistent with the orchestrator-effort findings in [[anthropic-2025-how]] and the equal-budget comparison in [[tran-2026-single]]. Cited by [[paliskara-2026-worse]] as the one-model-assigns-to-many case of contested compute. Classical counterparts: [[smith-1980-contract]] and [[chevaleyre-2006-issues]].

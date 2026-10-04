---
id: liu-2025-costbench
type: paper
title: "CostBench: Evaluating Multi-Turn Cost-Optimal Planning and Adaptation in Dynamic Environments for LLM Tool-Use Agents"
authors:
- Jiayu Liu
- Cheng Qian
- Zhaochen Su
- Qing Zong
- Shijue Huang
- Bingxiang He
- Yi R. Fung
year: 2025
venue: arXiv preprint
url: https://arxiv.org/abs/2511.02734
doi: null
arxiv: '2511.02734'
cite: "Liu, J., Qian, C., Su, Z., Zong, Q., Huang, S., He, B., & Fung, Y. R. (2025). CostBench: Evaluating Multi-Turn Cost-Optimal Planning and Adaptation in Dynamic Environments for LLM Tool-Use Agents. arXiv preprint arXiv:2511.02734."
topics:
- agent-budgets
added_by: dmarz/budget-a
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 39 (Semantic Scholar, 2026-10-03)
code: []
---
## Summary

A benchmark for whether tool-use agents find the cheapest plan, not only a working one. Tasks are travel planning, solvable by several sequences of atomic and composite tools whose costs are configurable. Four kinds of dynamic blocking events (for example tool failures and cost changes) force the agent to replan mid-task. Reported in the abstract: agents often miss the cost-optimal solution even in static settings; GPT-5 scores under 75% exact match on the hardest tasks; and performance falls by around 40% under dynamic conditions.

## Contribution

Isolates economic reasoning (pick the cheapest valid plan, then adapt when prices or availability change) as a capability separate from task completion.

## Key results

- Measured (abstract): GPT-5 below 75% exact match on the hardest static tasks.
- Measured (abstract): roughly 40% further drop under dynamic blocking events.
- Measured (abstract): open and proprietary models both show a substantial cost-aware planning gap.

## Methods and models

Travel-planning domain; atomic and composite tools with customisable costs; four dynamic event types; exact-match scoring against the cost-optimal plan. Model list not checked at abstract depth.

## Limitations and open questions

Abstract-level read. One synthetic domain; costs are given to the agent rather than discovered. Semantic Scholar lists an ACL venue; the citation here is the arXiv preprint (latest version dated 2026-06-29).

## Relevance to us

A ready-made testbed for cost-aware single agents; extending it to several agents sharing one budget or bidding for tools is a natural swarm experiment. Related: [[liu-2025-budget]], [[lin-2026-bagen]], [[ding-2026-calibrate]], and [[piatti-2024-cooperate]] for shared-resource behaviour among LLM agents.

---
id: backlund-2025-vending
type: paper
title: "Vending-Bench: A Benchmark for Long-Term Coherence of Autonomous Agents"
authors: ["Axel Backlund", "Lukas Petersson"]
year: 2025
venue: "arXiv preprint"
url: https://arxiv.org/abs/2502.15840
doi: null
arxiv: "2502.15840"
cite: "Backlund, A., & Petersson, L. (2025). Vending-Bench: A Benchmark for Long-Term Coherence of Autonomous Agents. arXiv preprint arXiv:2502.15840."
topics: [llm-agent-swarms, agent-budgets]
added_by: dmarz/factory-scan
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

A simulated business benchmark in which one LLM agent operates a vending machine: it balances inventory, orders from suppliers, sets prices and pays daily fees over runs exceeding 20M tokens. Measured: high variance across runs; Claude 3.5 Sonnet and o3-mini usually turn a profit, but every model has runs that derail through misread delivery schedules, forgotten orders or "meltdown" loops. Failures do not correlate with the point where the context window fills.

## Contribution

A long-horizon, money-denominated single-firm benchmark. Its multi-agent competitive extension, Vending-Bench Arena, is the setting of [[li-2026-emergent]].

## Key results

- Measured (abstract): Claude 3.5 Sonnet and o3-mini profitable in most runs; all models have derailing runs.
- Measured (abstract): breakdowns not explained by context-window exhaustion.

## Methods and models

Single agent with tools for email, inventory and pricing; abstract read only.

## Limitations and open questions

Abstract only. Single-agent; the Arena variant is not publicly redistributed (per [[li-2026-emergent]]).

## Relevance to us

Shows that long-horizon firm agents fail through coherence loss, not only strategy. A swarm factory run of hundreds of rounds should budget for agent derailment as a confound when measuring collusion. Compare production-side failure modes in [[hopkins-2025-factorio]].

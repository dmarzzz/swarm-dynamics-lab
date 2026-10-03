---
id: ding-2026-calibrate
type: paper
title: "Calibrate-Then-Act: Cost-Aware Exploration in LLM Agents"
authors:
- Wenxuan Ding
- Nicholas Tomlin
- Greg Durrett
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2602.16699
doi: null
arxiv: '2602.16699'
cite: "Ding, W., Tomlin, N., & Durrett, G. (2026). Calibrate-Then-Act: Cost-Aware Exploration in LLM Agents. arXiv preprint arXiv:2602.16699."
topics:
- agent-budgets
added_by: dmarz/budget-a
accessed: '2026-10-03'
read_depth: skim
relevance: 4
citations: 14 (Semantic Scholar, 2026-10-03)
code: []
---
## Summary

Frames an agent's choice between gathering more information (retrieving, writing a unit test) and committing to an answer as sequential decision-making under uncertainty with a cost per step, modelled as discounted reward. Calibrate-Then-Act (CTA) separates two jobs: first estimate a prior over the hidden environment state (from model confidence, or from a predictor trained on past experience), then pass that prior to the agent so it can reason about the trade-off. On a synthetic Pandora's Box task with Qwen3-8B, CTA-Prompted matches the oracle policy 94% of the time (reward 0.625 versus oracle 0.649), against 23% (reward 0.476) for plain prompting. Gains on the realistic tasks are smaller.

## Contribution

Shows that agents fail to explore optimally under costs mainly because they lack calibrated beliefs about the environment, not because they cannot reason about the trade-off, and that supplying those beliefs explicitly recovers near-optimal behaviour.

## Key results

- Measured (Table 2, Pandora's Box, Qwen3-8B): optimal-match rate 94.0% for CTA-Prompted vs 23.0% prompted, 11.0% prompted without thinking, 20.0% CTA without thinking; oracle reward 0.649, CTA 0.625, prompted 0.476.
- Measured (FileReading coding task): discounted reward 0.229 prompted, 0.240 CTA-Prompted, 0.259 RL, 0.268 CTA-RL; CTA-RL uses fewer unit-test calls (1.98 vs 2.13 for RL).
- Claimed: priors give environment sensitivity that standard RL training does not learn.

## Methods and models

Three tasks: synthetic Pandora's Box, retrieval-augmented QA with optional retrieval, and a file-reading coding task with selective unit tests. Qwen3-8B base; GRPO training for the RL variants. Costs enter as a discount factor on the final reward.

## Limitations and open questions

Read at skim depth (abstract, intro, main tables, conclusion). Gains on the realistic tasks are a few hundredths of reward. Costs are fixed and known; there is no shared or competing budget.

## Relevance to us

Suggests that what an agent needs in order to spend well is a calibrated estimate of task difficulty, which matches the over-optimism failure in [[lin-2026-bagen]]. For swarms, a shared prior (from an orchestrator or from other agents' experience) could play the CTA role. Related: [[liu-2025-costbench]], [[liu-2025-budget]].

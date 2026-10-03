---
id: lin-2026-bagen
type: paper
title: "BAGEN: Are LLM Agents Budget-Aware?"
authors:
- Yuxiang Lin
- Zihan Wang
- Mengyang Liu
- Yuxuan Shan
- Longju Bai
- Junyao Zhang
- Xing Jin
- Boshan Chen
- Jinyan Su
- Xingyao Wang
- Jiaxin Pei
- Manling Li
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2606.00198
doi: null
arxiv: '2606.00198'
cite: "Lin, Y., Wang, Z., Liu, M., Shan, Y., Bai, L., Zhang, J., Jin, X., Chen, B., Su, J., Wang, X., et al. (2026). BAGEN: Are LLM Agents Budget-Aware? arXiv preprint arXiv:2606.00198."
topics:
- agent-budgets
added_by: dmarz/budget-a
accessed: '2026-10-03'
read_depth: abstract
relevance: 5
citations: 9 (Semantic Scholar, 2026-10-03)
code: []
---
## Summary

Argues that agent cost is usually measured only after the run, and that a budget-aware agent should treat budget as a control signal during the run. The authors split budget into internal (the agent's own computation) and external (costs of its actions), and define budget-awareness as progressive interval estimation: at each step the agent predicts lower and upper bounds on the budget still needed and warns when finishing looks unlikely. Scored by a rollout-replay protocol on four environments and five frontier agents. Reported in the abstract: task skill and budget-awareness correlate only weakly (r = 0.35); frontier models are consistently over-optimistic and keep spending on tasks likely to fail; early stopping on failed trajectories saves 28-64% of tokens; SFT+RL improves early stopping and alerts, but interval coverage tops out at 47%.

## Contribution

Turns "is the agent aware of its budget" into a measurable prediction task, separate from task success, and shows current frontier agents are poor at it in a specific direction (over-optimism).

## Key results

- Measured (abstract): correlation between agent strength and budget-awareness r = 0.35.
- Measured (abstract): frontier models are over-optimistic and do not alert early on likely failures.
- Measured (abstract): early stop saves 28-64% of tokens on failed trajectories.
- Measured (abstract): after SFT+RL, interval coverage caps at 47%.

## Methods and models

Progressive interval estimation of remaining budget at each plan step; rollout-replay scoring; four environments, five frontier agents (not named in the abstract); SFT+RL training for the estimation and alert behaviour.

## Limitations and open questions

Abstract-level read; environments and agents not checked. The over-optimism finding sits in tension with Cognition's report that Sonnet 4.5 underestimates its remaining context ([[cognition-2025-rebuilding]]): different budget types and models, so not a direct contradiction, but worth testing.

## Relevance to us

Gives a metric for budget-awareness that could be applied to each agent in a swarm, and a concrete failure (continuing to spend on doomed tasks) that a shared-budget swarm would amplify. Pair with [[liu-2025-budget]] (showing the budget helps) and [[liu-2025-costbench]] (planning under costs).

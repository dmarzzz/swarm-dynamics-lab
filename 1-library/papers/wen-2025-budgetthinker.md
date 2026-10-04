---
id: wen-2025-budgetthinker
type: paper
title: "BudgetThinker: Empowering Budget-aware LLM Reasoning with Control Tokens"
authors:
- Hao Wen
- Xinrui Wu
- Yi Sun
- Feifei Zhang
- Liye Chen
- Jie Wang
- Yunxin Liu
- Yunhao Liu
- Ya-Qin Zhang
- Yuanchun Li
year: 2025
venue: arXiv preprint
url: https://arxiv.org/abs/2508.17196
doi: null
arxiv: '2508.17196'
cite: "Wen, H., Wu, X., Sun, Y., Zhang, F., Chen, L., Wang, J., Liu, Y., Liu, Y., Zhang, Y.-Q., & Li, Y. (2025). BudgetThinker: Empowering Budget-aware LLM Reasoning with Control Tokens. arXiv preprint arXiv:2508.17196."
topics:
- agent-budgets
added_by: dmarz/budget-a
accessed: '2026-10-03'
read_depth: skim
relevance: 3
citations: 35 (Semantic Scholar, 2026-10-03)
code: []
---
## Summary

Argues that stating a budget once in the prompt is not enough and that a model must be reminded of its remaining budget as it generates. BudgetThinker inserts special control tokens at intervals during reasoning that tell the model how much budget is left, and trains the model to use them with SFT followed by curriculum RL whose reward mixes accuracy and budget adherence. Measured on DeepSeek-R1-distilled Qwen2.5 1.5B and 7B across MATH-500, AMC 2023 and AIME 2024: an average accuracy gain of 4.9% across tested budgets over baselines (the original reasoning models and a prior efficient-reasoning method), with closer adherence to the target length.

## Contribution

An in-band, periodically refreshed budget signal that the model is trained to read. This is the same design pattern as the vendor countdown in [[anthropic-2026-context]] and [[anthropic-2026-task]] and the Budget Tracker in [[liu-2025-budget]], applied to reasoning tokens.

## Key results

- Measured: +4.9% average accuracy across all tested budgets versus baselines, with more precise budget adherence (paper intro).
- Measured: training with control tokens closes the gap between generated length and target budget faster and more stably during RL (Figure 1b).
- Claimed: prompt-only budgets fail to control length reliably, citing [[han-2024-token]].

## Methods and models

Control-token insertion at inference; two-stage training (SFT, then curriculum RL with a length-aware reward). Base models: DeepSeek-R1-Distill-Qwen 1.5B and 7B.

## Limitations and open questions

Read at skim depth (intro and conclusion; tables not read in detail). Small models and math benchmarks only. Requires training the model to understand the control tokens.

## Relevance to us

Direct evidence that a refreshed remaining-budget signal beats a one-off statement, at least for reasoning length. Tests whether the same holds for agent tool-call budgets: [[liu-2025-budget]], [[lin-2026-bagen]]. Survey context: [[alomrani-2025-reasoning]].

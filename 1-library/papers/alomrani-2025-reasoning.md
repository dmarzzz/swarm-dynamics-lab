---
id: alomrani-2025-reasoning
type: paper
title: "Reasoning on a Budget: A Survey of Adaptive and Controllable Test-Time Compute in LLMs"
authors:
- Mohammad Ali Alomrani
- Yingxue Zhang
- Derek Li
- Qianyi Sun
- Soumyasundar Pal
- Zhanguang Zhang
- Yaochen Hu
- Rohan Deepak Ajwani
- Antonios Valkanas
- Raika Karimi
- Peng Cheng
- Yunzhou Wang
- Pengyi Liao
- Hanrui Huang
- Bin Wang
- Jianye Hao
- Mark Coates
year: 2025
venue: arXiv preprint
url: https://arxiv.org/abs/2507.02076
doi: null
arxiv: '2507.02076'
cite: "Alomrani, M. A., Zhang, Y., Li, D., Sun, Q., Pal, S., Zhang, Z., Hu, Y., Ajwani, R. D., Valkanas, A., Karimi, R., et al. (2025). Reasoning on a Budget: A Survey of Adaptive and Controllable Test-Time Compute in LLMs. arXiv preprint arXiv:2507.02076."
topics:
- agent-budgets
added_by: dmarz/budget-a
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 32 (Semantic Scholar, 2026-10-03)
code: []
---
## Summary

A survey of efficient test-time compute for LLM reasoning. Its organising idea is a two-level taxonomy: L1-controllability covers methods that work under a fixed compute budget given from outside, and L2-adaptiveness covers methods that scale compute with input difficulty or model confidence. The authors also benchmark leading proprietary LLMs on several datasets to show the trade-off between accuracy and token use, and discuss hybrid thinking models and open problems. The abstract gives no headline numbers.

## Contribution

A map of the budget-control literature for single-model reasoning, with a useful split between obeying a given budget (L1) and choosing one's own budget (L2). That split carries over to agents: a visible budget ([[anthropic-2026-task]]) is an L1 problem, while deciding when to stop exploring ([[ding-2026-calibrate]], [[lin-2026-bagen]]) is closer to L2.

## Key results

- Taxonomy: L1 (fixed-budget control) versus L2 (adaptive compute).
- Measured (per abstract): a benchmark of proprietary LLMs across datasets showing reasoning-performance versus token-usage trade-offs; figures not read.
- Claimed: models overthink easy problems and underthink hard ones because compute is fixed regardless of difficulty.

## Methods and models

Literature survey plus a benchmarking study of proprietary models (models and datasets not checked at abstract depth).

## Limitations and open questions

Abstract-level read. Scope is reasoning compute in single models; the abstract does not say whether tool-call or multi-agent budgets are covered.

## Relevance to us

Entry point for the reasoning-budget literature: [[han-2024-token]], [[muennighoff-2025-s1]], [[li-2025-steering]], [[wen-2025-budgetthinker]]. Use the L1/L2 split when classifying agent-budget work.

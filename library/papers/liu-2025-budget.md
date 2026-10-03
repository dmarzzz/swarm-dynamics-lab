---
id: liu-2025-budget
type: paper
title: "Budget-Aware Tool Use Enables Effective Agent Scaling"
authors:
- Tengxiao Liu
- Zifeng Wang
- Jin Miao
- I-Hung Hsu
- Jun Yan
- Jiefeng Chen
- Rujun Han
- Fangyuan Xu
- Yanfei Chen
- Ke Jiang
- Samira Daruki
- Yi Liang
- William Yang Wang
- Tomas Pfister
- Chen-Yu Lee
year: 2025
venue: arXiv preprint
url: https://arxiv.org/abs/2511.17006
doi: null
arxiv: '2511.17006'
cite: "Liu, T., Wang, Z., Miao, J., Hsu, I.-H., Yan, J., Chen, J., Han, R., Xu, F., Chen, Y., Jiang, K., et al. (2025). Budget-Aware Tool Use Enables Effective Agent Scaling. arXiv preprint arXiv:2511.17006."
topics:
- agent-budgets
added_by: dmarz/budget-a
accessed: '2026-10-03'
read_depth: skim
relevance: 5
citations: 49 (Semantic Scholar, 2026-10-03)
code: []
---
## Summary

Studies web-search agents under explicit tool-call budgets and finds that raising the budget alone stops helping: a standard ReAct agent with Gemini-2.5-Pro saturates around 100 tool calls on BrowseComp, ending early because it thinks it has an answer or is stuck, not because context ran out. The Budget Tracker, a plug-in that appends remaining per-tool budget after every tool response, fixes this. BATS (Budget-Aware Test-time Scaling) goes further, with planning and verification modules that use the budget signal to choose between digging into a lead and switching paths. The authors define a unified cost combining token and tool spend. Accepted to COLM 2026 per the arXiv comments.

## Contribution

The first systematic study (the authors' claim) of tool-call budgets as a scaling axis for agents, with a cheap intervention, showing remaining budget after each tool call, that measurably changes behaviour across three models.

## Key results

- Measured (Table 1, budget 100 per tool, 3 runs): adding the Budget Tracker to ReAct raises BrowseComp accuracy from 12.6 to 14.6 (Gemini-2.5-Pro), 9.7 to 10.7 (Gemini-2.5-Flash) and 12.2 to 14.0 (Claude-Sonnet-4), with gains on BrowseComp-ZH and HLE-Search too.
- Measured (Table 2, Gemini-2.5-Pro): ReAct at budget 100 scores 12.6% at 9.9 cents per question; ReAct with Budget Tracker at budget 10 scores 12.8% at 6.8 cents, with 40.4% fewer search calls, 19.9% fewer browse calls and 31.3% lower cost than ReAct at 100.
- Measured: without budget awareness ReAct plateaus as budget grows; with it, accuracy keeps rising and the cost-performance Pareto frontier moves out (Figures 3-5). Only 0.8% of BrowseComp questions needed more than 50 calls per run.
- Measured: removing both BATS modules drops BrowseComp to 14.6% (ablation); exact BATS headline numbers not recorded here.

## Methods and models

ReAct search agents with search and browse tools; Budget Tracker inserted after each tool response; BATS adds budget-conditioned planning and verification. Benchmarks: BrowseComp, BrowseComp-ZH, HLE-Search, plus tau-bench in the appendix. Models: Gemini-2.5-Pro, Gemini-2.5-Flash, Claude-Sonnet-4. Unified cost metric in cents combines token and tool prices.

## Limitations and open questions

Read at skim depth (intro, Tables 1-2, scaling figures, conclusion). Absolute accuracies are low (10-15% on BrowseComp), so a 2-point gain is relative but not large. Search agents only. Single agent: budgets are not shared or divided among agents.

## Relevance to us

Core evidence that a visible, refreshed budget changes agent behaviour, and that agents do not use spare budget without one. The obvious next question for swarms is how a shared budget should be shown to many agents and split between them; see [[lin-2026-bagen]] (estimating remaining budget), [[liu-2025-costbench]] (cost-optimal planning), [[anthropic-2026-task]] (a vendor version of the same countdown), [[kim-2025-towards]] and [[tran-2026-single]] (matched-budget comparisons of agent systems).

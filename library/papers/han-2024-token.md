---
id: han-2024-token
type: paper
title: "Token-Budget-Aware LLM Reasoning"
authors:
- Tingxu Han
- Zhenting Wang
- Chunrong Fang
- Shiyu Zhao
- Shiqing Ma
- Zhenyu Chen
year: 2024
venue: arXiv preprint
url: https://arxiv.org/abs/2412.18547
doi: null
arxiv: '2412.18547'
cite: "Han, T., Wang, Z., Fang, C., Zhao, S., Ma, S., & Chen, Z. (2024). Token-Budget-Aware LLM Reasoning. arXiv preprint arXiv:2412.18547."
topics:
- agent-budgets
added_by: dmarz/budget-a
accessed: '2026-10-03'
read_depth: skim
relevance: 3
citations: 238 (Semantic Scholar, 2026-10-03)
code: []
---
## Summary

Shows that chain-of-thought output can be shortened by stating a token budget in the prompt, but that the budget value matters: on a GPT-4o-mini example, vanilla CoT used 258 output tokens, a 50-token budget cut it to 86, and a 10-token budget gave 157. The authors call this overshoot under too-small budgets "token elasticity". TALE estimates a per-question budget, either by zero-shot prompting the model for one (TALE-EP) or by post-training the model on budget-compressed traces (TALE-PT). Measured in the paper: TALE-EP cuts output tokens by about 67% on average (68.64% in the main table) with under 3% accuracy loss; TALE-PT cuts tokens by about 50% versus vanilla CoT.

## Contribution

An early, widely cited demonstration that a visible numeric budget changes how much a model reasons, plus the observation that models do not obey budgets that are too tight. It is the prompt-level baseline that later budget-control work ([[li-2025-steering]], [[wen-2025-budgetthinker]]) argues is unreliable.

## Key results

- Measured: token elasticity. Below some budget, actual token use rises rather than falls (example: 258 to 86 tokens at budget 50, 157 tokens at budget 10).
- Measured: TALE-EP averages a 68.64% token reduction; on one setting it keeps 81.03% accuracy at 32% of vanilla-CoT tokens and 41% of its expense; on GSM8K accuracy is 84.46%, above vanilla CoT.
- Measured: TALE-PT cuts token use by around 50% with competitive accuracy.
- Measured: TALE-EP transfers across Yi-lightning, GPT-4o-mini, GPT-4o and o3-mini on MathBench-College.

## Methods and models

Binary search for the minimal per-question budget that keeps the answer correct (used to build post-training targets); zero-shot budget estimation prompt; SFT/DPO-style post-training for TALE-PT. Benchmarks include GSM8K, GSM8K-Zero and MathBench. Code: https://github.com/GeniusHTX/TALE (not catalogued, not run).

## Limitations and open questions

Read at skim depth (intro, results passages, conclusion). Single-turn math and reasoning only; no tools, no multi-step agents. The budget is a soft prompt instruction, not enforced. Semantic Scholar lists an ACL venue; the arXiv page carries no journal reference, so the citation here is the preprint.

## Relevance to us

Baseline evidence that a budget stated in the prompt shifts reasoning length, and that tight budgets backfire. For agents the analogous signal is a tool-call or context budget ([[liu-2025-budget]], [[anthropic-2026-task]]). Related survey: [[alomrani-2025-reasoning]].

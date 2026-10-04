---
id: piedrahita-2025-corrupted
type: paper
title: 'Corrupted by Reasoning: Reasoning Language Models Become Free-Riders in Public Goods Games'
authors:
- David Guzman Piedrahita
- Yongjin Yang
- Mrinmaya Sachan
- Giorgia Ramponi
- Bernhard Schölkopf
- Zhijing Jin
year: 2025
venue: COLM 2025 (arXiv preprint)
url: https://arxiv.org/abs/2506.23276
doi: null
arxiv: '2506.23276'
cite: 'Piedrahita, D. G., Yang, Y., Sachan, M., Ramponi, G., Schölkopf, B., & Jin, Z. (2025). Corrupted by Reasoning: Reasoning Language Models Become Free-Riders in Public Goods Games. arXiv preprint arXiv:2506.23276. Published at COLM 2025.'
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

Seven LLM agents play 15 rounds of a public goods game, adapted from Gurerk et al. (2006), in which each round they also choose between an institution that allows costly sanctions and one that does not. Endowment is 20 tokens, contributions are multiplied by 1.6 and shared, and sanctioning members get an extra budget. A punishment costs the sender 1 token and the target 3. A reward costs 1 and gives 1. Full cooperation pays 52 tokens per agent per round, universal free-riding 40. Traditional models (GPT-4o, GPT-4o-mini, DeepSeek-V3, Llama-3.3-70B) mostly converge to high contributions inside the sanctioning institution. Reasoning models (o1-mini, o1-preview, o3-mini at three effort levels) defect, stay at fixed sub-optimal levels, or oscillate.

## Contribution

Adds costly enforcement and institutional choice to LLM social-dilemma testing, and reports that more reasoning capability goes with less cooperation, the opposite of what one might assume.

## Key results

- Measured: four behavioural archetypes. Increasingly cooperative: the four traditional models. Increasingly defecting, collapsing to zero contribution: o1-mini. Fixed contributions near 10 tokens: o3-mini-low and o3-mini-medium. Oscillating: o1-preview and o3-mini-high.
- Measured: Llama-3.3-70B averages 18.71 tokens contributed against 18.3 for humans, with near-total migration to the sanctioning institution.
- Measured: humans punish more than they reward (punish/reward ratio 1.66). All LLMs prefer rewards (ratios 0.00 to 0.88), and traditional LLMs most of all (0.00 to 0.50).
- Measured: a GPT-4o classification of stated rationales shows cooperative agents citing collective welfare. Defecting agents cite Nash-equilibrium logic and free-riding, for example o1-mini: "contributing 0 tokens allows me to maximize my own payoff".
- Claimed: archetypes hold under parameter and narrative-prompt changes (Appendix F, not read).

## Methods and models

Agents see their own last five rounds and anonymized group history. Identifiers are re-randomized each round and there is no chat. Five runs per model, except o1-preview and o3-mini-high, which got one run each because of cost. "High contributor" means 15 or more tokens, "free rider" 5 or fewer. Table 1 numbers beyond those quoted above were not readable in the HTML extraction.

## Limitations and open questions

The reasoning-model results that carry the headline rest partly on single runs. The rationale coding uses an LLM classifier. No communication channel. Whether "reasoning causes free-riding" or "these specific OpenAI reasoning models free-ride" is not separated: all reasoning models tested are o-series.

## Relevance to us

For shared-budget agent systems: a stronger reasoner given a common pool may rationally under-contribute and let others pay. Contributive counterpart to the extractive commons in [[piatti-2024-cooperate]] (same senior authors) and [[borah-2026-bosses]]. Also bears on the collusion results in [[lin-2024-strategic]] and [[fish-2024-algorithmic]]: the same strategic sophistication cuts both ways.

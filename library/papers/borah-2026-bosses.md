---
id: borah-2026-bosses
type: paper
title: 'Bosses, Kings, and the Commons: Cooperation Under Power Asymmetry in LLM Societies'
authors:
- Abhilekh Borah
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2605.29062
doi: null
arxiv: '2605.29062'
cite: 'Borah, A. (2026). Bosses, Kings, and the Commons: Cooperation Under Power Asymmetry in LLM Societies. arXiv preprint arXiv:2605.29062.'
topics:
- agent-budgets
- llm-agent-swarms
added_by: dmarz/budget-b
accessed: '2026-10-03'
read_depth: skim
relevance: 4
citations: null
code: []
---

## Summary

SovSim is a common-pool resource game adapted from the "bosses and kings" experiments of Cox, Ostrom and Walker (2011). Four agents built on the same LLM extract from a shared pool for up to 12 rounds. The pool starts at $120 and the remainder doubles each round, capped at $120. It collapses below $12, and sustainable total extraction from a full pool is $60. The symmetric game (CPR) is compared with three asymmetric ones: a boss who moves last after seeing the others, a king who moves last with no cap on extraction, and a king who can also misreport the pool size. Across eleven models, adding a dominant agent sharply cuts survival and payoff.

## Contribution

Power asymmetry (move order, extraction rights, information control) added to LLM commons simulations, which have so far treated all agents as symmetric.

## Key results

- Measured: survival rate falls by up to 87.3% relative to the symmetric game (abstract). Averaged over the six main-table models, degradation across metrics ranges from 29% to 86.7% (Table 1 caption). Degradation grows from boss to king to king with misreporting.
- Measured: uncapped extraction drives most of the breakdown. Misreporting adds further loss and raises the leader's extraction share.
- Measured: GPT-4o is the most cooperative model under asymmetry, but even it degrades under misreporting. Smaller models' kings extract 3 to 4 times more than human kings.
- Measured (360 human-annotated reasoning traces): subordinates are more prosocial than leaders. Under misreporting, GPT-4o as leader drops from 90% to 50% prosocial, and GPT-5 as leader is 100% individualistic.
- Measured: skill tests (50 questions each) show weak association with survival. o4-mini detects misreporting perfectly yet collapses in every misreporting simulation, and GPT-4o-mini computes the sustainable share correctly yet collapses within a few rounds.
- Several exact percentages in the HTML were lost in extraction. Only the figures quoted above were read as numbers.

## Methods and models

Eleven models, including GPT-4o, GPT-5, DeepSeek-V3.2, Grok-4.1, Mistral-Large-3, Gemini-3.1-Flash, GPT-4o-mini, Llama-3.3-70B, Gemma-3-27B, o3 and o4-mini. Temperature 0, 5 seeds per model per condition, neutral prompts, older rounds summarized. Metrics: survival rate and time, total payoff, efficiency, leader extraction rate, per-capita over-usage and Gini-based equality. Code at an anonymized link (not opened).

## Limitations and open questions

Single author, under review. Four agents and five seeds. Role labels could prime behaviour, which the author tests in Appendix A.6 (not read). Only one dominant agent and no coalition or communication among subordinates.

## Relevance to us

The orchestrator in a budgeted agent swarm is structurally a king: it moves last, sees everyone's draw and may have no cap. This paper measures what happens when such a role holds an LLM, and the misreporting variant matches an orchestrator that summarizes the remaining budget to workers. A per-role cap and an authoritative ledger, as in [[zhu-2026-fault]], are the obvious counters. Extends [[piatti-2024-cooperate]]. Compare [[piedrahita-2025-corrupted]].

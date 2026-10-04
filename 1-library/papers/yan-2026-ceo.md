---
id: yan-2026-ceo
type: paper
title: "CEO Arena: Evaluating Long-Horizon Multi-Agent Decision-Making in Competitive Markets"
authors: ["An Yan", "Yu Huo", "Zhiwei Shang", "Yiran Peng", "Chenglin Wu"]
year: 2026
venue: "arXiv preprint (submitted to ICLR 2027)"
url: https://arxiv.org/abs/2609.34821
doi: null
arxiv: '2609.34821'
cite: "Yan, A., Huo, Y., Shang, Z., Peng, Y., & Wu, C. (2026). CEO Arena: Evaluating long-horizon multi-agent decision-making in competitive markets. arXiv:2609.34821."
topics: [llm-agent-swarms]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "0 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

Eight LLM 'CEO' agents run companies in a shared market for 500 simulated days, deciding pricing, procurement, marketing, R&D and service from private company data and noisy market signals, under resource constraints and delayed feedback. Evaluation uses matched replacement: each CEO is compared with a reference policy in the same company under the same economic seed while other agents' identities stay fixed, measuring own returns and effects on rivals and the market.

## Contribution

Matched-replacement evaluation for agents in a coupled market, which separates an agent's own returns from the externalities it imposes.

## Key results

- 8 LLM CEO agents, 27 main runs plus 26 robustness runs.
- Most agents have negative mean returns; private gains can coincide with market losses.
- Only four of 56 directed agent pairs show relatively stable effects.

## Methods and models

Simulated eight-company market with economic seeds; traces of memory, actions and accounting used to explain outcomes.

## Limitations and open questions

Abstract only; no code link found on the arXiv HTML page. Rule-based baseline market underneath.

## Relevance to us

Borrow idea: matched replacement (swap one agent for a reference policy under the same seed, others fixed) is the right counterfactual for measuring one agent's externality in any multi-agent sim. Related: [[fan-2026-agentic]], [[chupilkin-2026-artificial]].

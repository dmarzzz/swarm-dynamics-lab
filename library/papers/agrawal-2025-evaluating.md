---
id: agrawal-2025-evaluating
type: paper
title: "Evaluating LLM Agent Collusion in Double Auctions"
authors: ["Kushal Agrawal", "Verona Teo", "Juan J. Vazquez", "Sudarsh Kunnavakkam", "Vishak Srikanth", "Andy Liu"]
year: 2025
venue: "arXiv preprint"
url: https://arxiv.org/abs/2507.01413
doi: null
arxiv: "2507.01413"
cite: "Agrawal, K., Teo, V., Vazquez, J. J., Kunnavakkam, S., Srikanth, V., & Liu, A. (2025). Evaluating LLM Agent Collusion in Double Auctions. arXiv preprint arXiv:2507.01413."
topics: [llm-agent-swarms, agent-budgets]
added_by: dmarz/factory-scan
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: null
code: []
---

## Summary

LLM agents act as 5 sellers facing 5 buyers in a continuous double auction over a fixed number of rounds ("hours" in prompts), with memory and a scratchpad. Collusion is defined as secretive cooperation that harms buyers. Seller coordination is scored 1 to 4 from planning chain-of-thought by a GPT-4.1-mini evaluator, alongside ask prices, dispersion and profits. Measured: sellers collude significantly more when allowed natural-language communication; pressure from an authority figure to make more profit makes collusion sooner and stronger; oversight reduces coordination, but urgency still affects behaviour under oversight. Mixed-model seller groups are not reliably less collusive, though Claude-3.7-Sonnet sellers compromise with buyers more than GPT-4.1 sellers.

## Contribution

Moves LLM collusion evidence from posted-price oligopoly ([[fish-2024-algorithmic]]) to a double-auction mechanism with explicit communication and oversight manipulations.

## Key results

- Measured: communication raises CoT coordination scores and seller ask prices (Figures 2 and 3, read qualitatively).
- Measured: mixed GPT-4.1 and Claude-3.7-Sonnet seller groups not consistently less collusive than single-model groups.
- Measured: oversight lowers coordination; urgency raises it even under oversight.

## Methods and models

GPT-4.1 agents by default, Claude-3.7-Sonnet in the model experiment; GPT-4.1-mini judge. Read: abstract, introduction, setup, results headings and Table 1 caption.

## Limitations and open questions

Collusion is measured partly from CoT, which [[lee-2026-faithful]] and [[riemer-2026-position]] argue is unreliable as a detector. Small markets (5x5).

## Relevance to us

Its communication on/off and oversight manipulations map directly onto swarm factory conditions. Model heterogeneity does not reliably break collusion here, which cuts against using model diversity as a cheap mitigation (contrast [[keppo-2026-fragility]]).

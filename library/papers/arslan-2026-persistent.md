---
id: arslan-2026-persistent
type: paper
title: "Persistent Partners Raise Prices Among Learning Agents"
authors: ["Paul-Peter Arslan", "Yubin Kim", "Xiao Xiao"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2609.35402
doi: null
arxiv: "2609.35402"
cite: "Arslan, P.-P., Kim, Y., & Xiao, X. (2026). Persistent Partners Raise Prices Among Learning Agents. arXiv preprint arXiv:2609.35402."
topics: [agent-budgets, marl-emergence]
added_by: dmarz/factory-scan
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

A pre-registered randomised experiment in the Bertrand duopoly of [[calvano-2020-artificial]], with tabular Q-learning modules setting prices, randomising whether each agent keeps its partner, sees rival prices and can message. Keeping the same partner raises average profit by 0.27 of the competitive-to-monopoly gap (95% CI 0.20 to 0.35, all 20 paired runs positive) and the resting price by 0.17 of the Nash-to-monopoly range. The rise also occurs when rival prices are hidden, where punishment is impossible, so a test that looks only for punishment would miss it; a profitable-deviation check flags most such prices. An exploratory extension finds the effect in untrained Qwen2.5 7B and 14B under one prompt.

## Contribution

Shows platform matching (who faces whom) moves learned prices, and that punishment-based collusion tests can miss supracompetitive outcomes.

## Key results

- Measured (registered): +0.27 profit-gap fraction for persistent partners.
- Measured (post hoc): price rise without visible rivals; punishment test inconclusive net of static best response.

## Methods and models

Pre-registered RCT; abstract read only.

## Limitations and open questions

Mostly tabular Q-learning; LLM results exploratory. Abstract only.

## Relevance to us

Detection lesson for the swarm factory: test for profitable deviations, not just retaliation patterns. Matching persistence is a design knob (fixed versus rotating rivals across markets).

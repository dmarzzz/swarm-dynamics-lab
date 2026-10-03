---
id: calvano-2020-artificial
type: paper
title: "Artificial Intelligence, Algorithmic Pricing, and Collusion"
authors: ["Emilio Calvano", "Giacomo Calzolari", "Vincenzo Denicolò", "Sergio Pastorello"]
year: 2020
venue: "American Economic Review"
url: https://www.aeaweb.org/articles?id=10.1257/aer.20190623
doi: "10.1257/aer.20190623"
arxiv: null
cite: "Calvano, E., Calzolari, G., Denicolò, V., & Pastorello, S. (2020). Artificial Intelligence, Algorithmic Pricing, and Collusion. American Economic Review, 110(10), 3267–3297."
topics: [swarm-detection, marl-emergence]
added_by: dmarz/sd-coordination
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "587 (Semantic Scholar, 2026-10-03)"
code: []
---
## Summary

Simulates Q-learning pricing algorithms in a standard repeated oligopoly model. The algorithms consistently learn supracompetitive prices without communicating. The high prices are sustained by collusive strategies with a finite punishment phase followed by a gradual return to cooperation. The result is robust to cost and demand asymmetries, changes in the number of firms, and several forms of uncertainty.

## Contribution

The seminal result that independent learning agents can collude tacitly, with a detectable signature: punishment after deviation followed by gradual return.

## Key results

- Q-learners learn supracompetitive prices without communication (abstract).
- Collusion is supported by finite punishment then gradual return to cooperation (abstract).
- Robust to asymmetry, number of players and uncertainty (abstract).

## Methods and models

Q-learning agents in a workhorse oligopoly model of repeated price competition, studied by simulation (abstract).

## Limitations and open questions

Abstract only. Long training times and simple state spaces; how often this happens with deployed algorithms is an empirical question taken up by [[assad-2024-algorithmic]].

## Relevance to us

Coordination without communication is the hardest case for any swarm detector, because there is no channel to intercept; detection must use the reward-punishment structure ([[eschenbaum-2026-auditing]]). LLM version: [[fish-2024-algorithmic]].

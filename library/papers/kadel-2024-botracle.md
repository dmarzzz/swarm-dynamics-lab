---
id: kadel-2024-botracle
type: paper
title: "BOTracle: A framework for Discriminating Bots and Humans"
authors: ["Jan Kadel", "August See", "Ritwik Sinha", "Mathias Fischer"]
year: 2024
venue: "ESORICS 2024 International Workshops"
url: https://arxiv.org/abs/2412.02266
doi: "10.48550/arXiv.2412.02266"
arxiv: "2412.02266"
cite: "Kadel, J., See, A., Sinha, R., & Fischer, M. (2024). BOTracle: A framework for Discriminating Bots and Humans. Published at ESORICS International Workshops 2024. arXiv preprint arXiv:2412.02266."
topics: ["swarm-detection"]
added_by: dmarz/sd-web-agents
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Kadel, See, Sinha and Fischer compare three bot detectors on real e-commerce traffic of 40 million page visits per month: fast heuristics, a model on technical features (IP, window size, user agent), and a model that uses only browsing behaviour with all static features removed. Their methods reach precision, recall and AUC of 98% or higher and beat the Botcha baseline on the same data.

## Contribution

Evidence at production scale that behaviour-only detection works for bots that use real browsers; pre-dates LLM agents.

## Key results

- Measured (abstract): precision, recall and AUC at or above 98% on 40M monthly page visits.
- Measured (abstract): outperforms Botcha on the same dataset.

## Methods and models

Heuristic, technical-feature and behaviour-only classifiers on e-commerce clickstream data. Abstract only.

## Limitations and open questions

Abstract only; ground-truth labelling method not checked; no LLM agents.

## Relevance to us

Behaviour-only session features are what scale to a whole site's traffic, which is where a swarm shows up as a cluster. Compare [[wang-2026-fp-agent]].

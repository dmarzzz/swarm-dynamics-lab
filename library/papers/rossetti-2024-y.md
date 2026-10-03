---
id: rossetti-2024-y
type: paper
title: "Y Social: an LLM-powered Social Media Digital Twin"
authors: ["Giulio Rossetti", "Massimo Stella", "Rémy Cazabet", "Katherine Abramski", "Erica Cau", "Salvatore Citraro", "Andrea Failla", "Riccardo Improta", "Virginia Morini", "Valentina Pansanella"]
year: 2024
venue: "arXiv"
url: https://arxiv.org/abs/2408.00818
doi: null
arxiv: "2408.00818"
cite: "Rossetti, G., Stella, M., Cazabet, R., Abramski, K., Cau, E., Citraro, S., Failla, A., Improta, R., Morini, V., & Pansanella, V. (2024). Y Social: an LLM-powered Social Media Digital Twin. arXiv preprint arXiv:2408.00818."
topics: [llm-agent-swarms, swarm-detection]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "57 (Semantic Scholar, 2026-10-03)"
code: [gh-ysocialtwin-ysocial]
---

## Summary

Introduces Y, a digital twin of an online social platform in which LLM agents post, react and form networks, intended to study engagement, information spread and the effects of platform policies such as recommendation algorithms. The paper describes the architecture and example analyses rather than a validated empirical result.

## Contribution

An open, local-LLM-friendly social media simulator aimed at computational social scientists, with recommender policy as a first-class experimental variable.

## Key results

- Architecture and example analyses only; no headline quantitative validation in the abstract.

## Methods and models

Client-server design (YServer REST API, YClient LLM agents, YSocial web UI); configurable personas and recommenders. Not read beyond the abstract.

## Limitations and open questions

Validation of realism not demonstrated in the abstract; see [[larooij-2025-do]].

## Relevance to us

Candidate substrate for injected coordinated-account experiments with a controllable feed; compare with [[yang-2024-oasis]] which scales further. Code: [[gh-ysocialtwin-ysocial]].

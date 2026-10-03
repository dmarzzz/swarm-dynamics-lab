---
id: qian-2025-deliberate
type: paper
title: "Deliberate Lab: A Platform for Real-Time Human-AI Social Experiments"
authors: ["Crystal Qian", "Vivian Tsai", "Michael Behr", "Nada Hussein", "Léo Laugier", "Nithum Thain", "Lucas Dixon"]
year: 2025
venue: "arXiv preprint"
url: https://arxiv.org/abs/2510.13011
doi: null
arxiv: '2510.13011'
cite: "Qian, C., Tsai, V., Behr, M., Hussein, N., Laugier, L., Thain, N., & Dixon, L. (2025). Deliberate Lab: A platform for real-time human-AI social experiments. arXiv:2510.13011."
topics: [llm-agent-swarms, collective-decision]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: null
code: [gh-pair-code-deliberate-lab]
---

## Summary

Open-source platform from Google PAIR for large-scale, real-time multi-party behavioural experiments where LLM agents are first-class participants alongside humans. Reports a 12-month public deployment with 88 experimenters and 9,195 participants, usage analysis and interviews.

## Contribution

Infrastructure for hybrid human-AI group experiments, rather than an all-agent simulation.

## Key results

- 12-month deployment: N=88 experimenters, N=9,195 participants.

## Methods and models

TypeScript web platform (Firebase-style deploy per repo docs); Apache-2.0.

## Limitations and open questions

Abstract only. Not a simulator; scale is human-experiment scale.

## Relevance to us

Borrow idea / bootstrap if we want humans in the loop with our agents (e.g. human vs Sybil-agent groups). Related: [[ricco-2026-consensus]].

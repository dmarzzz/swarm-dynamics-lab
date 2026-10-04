---
id: kurian-2025-attacks
type: paper
title: "Attacks and Defenses Against LLM Fingerprinting"
authors: ["Kevin Kurian", "Ethan Holland", "Sean Oesch"]
year: 2025
venue: "arXiv preprint"
url: https://arxiv.org/abs/2508.09021
doi: null
arxiv: "2508.09021"
cite: "Kurian, K., Holland, E., & Oesch, S. (2025). Attacks and Defenses Against LLM Fingerprinting. arXiv:2508.09021."
topics: [swarm-detection]
added_by: dmarz/sd-attribution
accessed: 2026-10-03
read_depth: abstract
relevance: 2
citations: null
code: []
---

## Summary

Studies LLM fingerprinting offensively and defensively. Reinforcement learning chooses fingerprinting queries and achieves better accuracy with 3 queries than 3 random queries from the same pool. Defensively, a secondary LLM filters outputs with semantic-preserving rewriting, which lowers fingerprinting accuracy while keeping output quality.

## Contribution

Both query optimisation and a rewriting defence in one study.

## Key results

- RL-selected 3-query sets beat random 3-query sets; rewriting defence reduces accuracy while preserving quality (abstract; no numbers).

## Methods and models

RL query selection; secondary-LLM output filtering.

## Limitations and open questions

Abstract-only reading.

## Relevance to us

A swarm operator can pass outputs through a rewriting model, a cheap defence; compare forging [[yuan-2026-forging]] and LLMmap's mitigation analysis [[pasquini-2024-llmmap]].

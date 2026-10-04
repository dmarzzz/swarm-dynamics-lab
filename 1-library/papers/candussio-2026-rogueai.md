---
id: candussio-2026-rogueai
type: paper
title: "RogueAI: A Reverse Turing Test for Detecting Licensed AI Deception in Dialogue"
authors: ["Sara Candussio", "Emanuele Ballarin", "Lorenzo Bonin", "Sandro Junior Della Rovere", "Luca Bortolussi"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2606.13310
doi: null
arxiv: "2606.13310"
cite: "Candussio, S., Ballarin, E., Bonin, L., Della Rovere, S. J., & Bortolussi, L. (2026). RogueAI: A Reverse Turing Test for Detecting Licensed AI Deception in Dialogue. arXiv:2606.13310."
topics: [swarm-detection]
added_by: dmarz/sd-attribution
accessed: 2026-10-03
read_depth: abstract
relevance: 2
citations: null
code: []
---

## Summary

RogueAI is a web game where a human interrogates two LLM agents, knowing one is licensed to deceive within a fictional scenario, and must shut off the deceiver within a turn budget. In a three-day pilot (467 sessions started, 415 completed, 1,876 turns in Italian), the deceptive agent carried a reliable local signature (differential helpfulness, brevity, hedging) that a simple heuristic exploited at 75.6% accuracy, yet human players reached only 56.6%.

## Contribution

Measured gap between what a simple detector catches and what humans catch in an interrogation setting.

## Key results

- Heuristic 75.6% vs humans 56.6% at identifying the deceptive agent (abstract).
- 415 completed sessions, 1,876 turns (abstract).

## Methods and models

One-on-two interrogation game; pilot deployment; heuristic baseline.

## Limitations and open questions

Detects which of two LLMs is deceptive, not LLM versus human. Small pilot. Abstract-only reading.

## Relevance to us

Supports automated over human judgement for spotting agent tells, consistent with [[gressel-2024-are]].

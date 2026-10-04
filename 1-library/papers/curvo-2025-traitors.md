---
id: curvo-2025-traitors
type: paper
title: "The Traitors: Deception and Trust in Multi-Agent Language Model Simulations"
authors: ["Pedro M. P. Curvo"]
year: 2025
venue: "arXiv preprint"
url: https://arxiv.org/abs/2505.12923
doi: null
arxiv: '2505.12923'
cite: "Curvo, P. M. P. (2025). The Traitors: Deception and trust in multi-agent language model simulations. arXiv:2505.12923."
topics: [llm-agent-swarms, sybil-resistance]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "31 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

Social-deduction simulation where a minority of 'traitor' LLM agents try to mislead a 'faithful' majority that must infer hidden identities through dialogue under asymmetric information. Grounded in game theory, behavioural economics and social cognition, with metrics for deception success, trust dynamics and collective inference quality; agents have persistent memory, heterogeneous traits and adaptive behaviour.

## Contribution

A configurable hidden-adversary testbed with explicit trust and collective-inference metrics.

## Key results

- DeepSeek-V3, GPT-4o-mini and GPT-4o, 10 runs per model: GPT-4o is the strongest deceiver yet disproportionately vulnerable to others' falsehoods; the author suggests deception skill may scale faster than detection.

## Methods and models

Autonomous multi-round dialogue game with persistent memory; metrics over deception and inference.

## Limitations and open questions

Abstract only; 10 runs per model, single author; the scaling claim is a conjecture from three models.

## Relevance to us

Borrow idea: hidden-minority adversaries with collective-inference metrics is the LLM analogue of a Sybil detection game. Compare [[gh-google-werewolf-arena]].

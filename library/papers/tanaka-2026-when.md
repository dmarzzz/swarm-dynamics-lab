---
id: tanaka-2026-when
type: paper
title: When Is Collective Intelligence a Lottery? Multi-Agent Scaling Laws for Memetic Drift in LLMs
authors:
- Hidenori Tanaka
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2603.24676
doi: null
arxiv: '2603.24676'
cite: Tanaka, H. (2026). When is collective intelligence a lottery? Multi-agent scaling laws for memetic drift in LLMs. arXiv preprint arXiv:2603.24676.
topics:
- llm-agent-swarms
- sync-consensus
- criticality-measurement
added_by: dmarz/llm-agent-swarms
accessed: '2026-10-03'
read_depth: abstract
relevance: 5
citations: "0 (OpenAlex W7141417890, arXiv record, 2026-10-03); Semantic Scholar 7 same day"
code: []
---

## Summary

Asks whether consensus in LLM populations reflects reasoning, bias or chance. Introduces Quantized Simplex Gossip (QSG): agents keep internal belief states but learn from each other's sampled outputs, so one agent's arbitrary sample becomes the next agent's evidence ("mutual in-context learning"). By analogy with neutral evolution this sampling-driven agreement is called memetic drift. QSG predicts a crossover from a drift-dominated regime, where the consensus outcome is effectively a lottery, to a selection regime, where weak biases are amplified and decide the outcome. Scaling laws for drift-induced polarisation are derived as functions of population size, communication bandwidth, in-context adaptation rate and agents' internal uncertainty, and validated in QSG simulations and in naming-game experiments with LLM populations.

## Contribution

A minimal mechanistic model of why unbiased LLM populations break symmetry (the puzzle left by [[ashery-2024-emergent]]), with population-genetics-style scaling laws (drift vs selection) rather than an Ising analogy.

## Key results

- Drift-to-selection crossover controlled by population size, bandwidth, adaptation rate and uncertainty (abstract claim; exponents not read in this session).
- Scaling laws validated in LLM naming-game experiments (abstract claim).

## Methods and models

Quantized Simplex Gossip model (beliefs on a simplex, quantised sampled messages); analytic scaling; LLM naming-game experiments. Code not checked.

## Limitations and open questions

Read at abstract depth only: model details, fitted exponents and which LLMs were tested need a full read. Single-author preprint.

## Relevance to us

High: gives a falsifiable prediction (how the "lottery" fraction of outcomes scales with N and bandwidth) that a hackathon could test directly. Read alongside [[de-marzo-2024-ai]] (majority force), [[choi-2025-debate]] (debate as martingale, i.e. pure drift) and [[flint-2026-group]].

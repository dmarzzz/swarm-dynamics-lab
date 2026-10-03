---
id: de-nobili-2026-microscopic
type: paper
title: Microscopic dynamics of consensus formation in multi-agent LLM Naming Games
authors:
- Cristiano De Nobili
- Vijayasri Iyer
- Alessandro Codello
- Raffaella Burioni
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2608.02178
doi: null
arxiv: '2608.02178'
cite: De Nobili, C., Iyer, V., Codello, A., & Burioni, R. (2026). Microscopic dynamics of consensus formation in multi-agent LLM Naming Games. arXiv preprint arXiv:2608.02178.
topics:
- llm-agent-swarms
- sync-consensus
- criticality-measurement
added_by: dmarz/llm-agent-swarms-recent
accessed: '2026-10-03'
read_depth: abstract
relevance: 5
citations: 0 (OpenAlex, 2026-10-03); 2 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

A minimal LLM naming game in which the listener's accept/reject decision is a single-token LLM call at decoding temperature T, replacing the deterministic inventory check of the classical naming game. Each interaction splits into an in-inventory channel with acceptance rate pi(T) = P(YES | word in listener's inventory) and an out-inventory channel phi(T) = P(YES | word not in inventory); their balance sets an ordering versus disordering drift. A mean-field theory of this two-rate dynamics gives an analytic ordering condition: a critical line in the (pi, phi) plane generalising the stochastic naming game's consensus threshold. Across three open-weight architectures consensus is always reached, but through three listener regimes (permissive, near-deterministic, conservative). The finite-size exponent beta(T) in t_conv ~ N^beta shifts with temperature, and the temperature sensitivity alpha in t_c ~ e^{alpha T} ranges from about 0.67 to about 0 across architectures.

## Contribution

Turns LLM decoding temperature into a measured control parameter with mean-field theory and finite-size scaling, in the statistical-physics tradition of Baronchelli's naming game. Microscopic counterpart to [[ashery-2024-emergent]], [[flint-2026-group]] and [[tanaka-2026-when]].

## Key results

- Claimed: consensus always reached for three open-weight models.
- Claimed: critical line in (pi, phi) from mean-field theory.
- Claimed: convergence time scales as N^beta(T) with temperature-dependent beta; t_c ~ e^{alpha T} with alpha from ~0.67 to ~0.

## Methods and models

Naming game on a complete graph with LLM listener decisions (single token YES/NO) at temperature T; measurement of channel rates; mean-field rate equations; finite-size scaling. Model names not checked.

## Limitations and open questions

Abstract-level read; 8-page preprint. Only the listener is an LLM; the speaker side stays rule-based, so it is a hybrid model.

## Relevance to us

High: a minimal, cheap, physics-grade LLM swarm experiment with explicit exponents to reproduce. Related: [[de-marzo-2024-ai]], [[hirota-2026-collective]].

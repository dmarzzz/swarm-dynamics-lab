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
venue: arXiv preprint (physics.soc-ph)
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
read_depth: full
relevance: 5
citations: 0 (OpenAlex, 2026-10-03); 2 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

The authors keep the classical minimal Naming Game (Baronchelli et al.) on a complete graph, with inventories, invention from a pool of 10^4 English words and random speaker-listener pairs, but replace the listener's deterministic check "is w in my inventory?" with a single-token YES/NO LLM call at decoding temperature T. Each interaction then splits into four channels (true/false positive/negative), summarised by two measurable conditional rates: pi(T) = P(YES | w in inventory), the consolidation (ordering) rate, and phi(T) = P(YES | w not in inventory), the "repaint" (disordering) rate. The deterministic NG is pi = 1, phi = 0. Running llama3.1:8b, mistral:7b and phi3:14b locally with N = 150 (N from 50 to 150 for scaling), 11 temperatures from 0.05 to 2.0 and 10-15 seeds, they find three listener regimes: permissive (llama: pi falls from ~1.0 to ~0.55 and early phi reaches ~0.50 as T rises), near-deterministic (mistral: pi ~ 1, phi < 0.15 and decaying), and conservative (phi3: pi from ~0.75 to ~0.30, phi ~ 0, inventories swell to ~34 words at low T). A two-word mean-field theory gives the ordering condition 3 pi - 2 phi - 1 > 0, which reduces to the known threshold beta_c = 1/3 of the stochastic NG when phi = 0.

## Contribution

Turns the LLM's sampling temperature into a statistical-physics control parameter and resolves the microscopic channels behind LLM convention formation, which earlier studies ([[ashery-2024-emergent]], [[flint-2026-group]]) treated at fixed T = 0.5 as a black box. Identifies phi3 as an empirical realisation of the lazy-consolidation stochastic NG, linking LLM swarms directly to an existing phase diagram.

## Key results

- Measured: effective finite-size exponents in t_conv ~ N^beta over N in [50, 150]: llama <beta> = 1.61 +- 0.28 (from ~1.3 at low T to ~2.0 at T = 2.0), mistral 1.28 +- 0.13, phi3 1.59 +- 0.47 (lower bound; some seeds did not converge). Canonical deterministic NG: 3/2.
- Measured: temperature response t_c ~ A e^{alpha T}: llama alpha = 0.67 +- 0.14 (t_c grows ~4x from T = 0.05 to 2.0), mistral 0.01 +- 0.02 ("temperature blindness"), phi3 0.43 +- 0.31.
- Measured: phi3 shows inverted temperature ordering: lowest T converges slowest, plateauing at ~7 distinct words through 9 x 10^4 steps with mean inventory > 30; at T = 2.0 inventories peak below 4 and collapse within ~10^4 steps.
- Theory: two-word sector mean field with order parameter u = x - y gives instability of the symmetric state when 3 pi - 2 phi - 1 > 0; mistral sits at R ~ 2 (deep in ordered region); phi3 at T = 2.0 has R ~ -0.1, nominally below the critical line, yet strict consensus was still reached at N <= 150, consistent with a transition that sharpens only as N -> infinity.
- Measured: no fragmented phase was observed for any model at any temperature on the complete graph.

## Methods and models

Prompt: system "You are an agent with your own language and vocabulary. You can and must reply with yes or no."; user "Your words are: P_j. Do we add w to the list?". Models served locally via Ollama. Up to 10^5 steps (1.75 x 10^5 for phi3). Observables: number of distinct words N_d(t), success rate, mean inventory size, in-inventory fraction m(t), drift proxy Delta = m pi - (1 - m) phi. Medians and IQRs across seeds because of heavy tails. Appendix gives the full (2^m - 1)-dimensional mean-field hierarchy with an inventory-size closure. No code URL seen.

## Limitations and open questions

- Only half a decade in N; exponents are effective, not asymptotic, as the authors state.
- One prompt wording; the authors note rewording can shift (pi, phi) and defer a prompt scan.
- Only the listener is an LLM; speakers sample uniformly from inventories as in the classical model.
- Complete graph only; small 7-14B models. The predicted fragmented phase for phi3 at high T needs larger N.

## Relevance to us

A cheap, laptop-scale LLM swarm experiment with a known classical phase diagram: we could push N to 10^3 with small local models, test for the predicted fragmentation, or add lattice and small-world topologies. Measuring (pi, phi) offline for any model gives a two-number fingerprint before running a swarm. Related: [[de-marzo-2024-ai]], [[tanaka-2026-when]], [[hirota-2026-collective]], [[barrie-2025-emergent]] (the arbitrary 10^4-word pool partly addresses memorisation).

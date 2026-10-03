---
id: hirota-2026-collective
type: paper
title: Collective Regimes in Multi-Agent LLMs under Reasoning Effort and Communication Topology
authors:
- Machiko Hirota
- Akshara Nadayanur Sathis Kanna
- Ujwal Kumar
- Phan Xuan Tan
year: 2026
venue: arXiv preprint (under review at ICLR 2027)
url: https://arxiv.org/abs/2609.35885
doi: null
arxiv: '2609.35885'
cite: Hirota, M., Kanna, A. N. S., Kumar, U., & Tan, P. X. (2026). Collective Regimes in Multi-Agent LLMs under Reasoning Effort and Communication Topology. arXiv preprint arXiv:2609.35885.
topics:
- llm-agent-swarms
- sync-consensus
- criticality-measurement
added_by: dmarz/llm-agent-swarms-recent
accessed: '2026-10-03'
read_depth: full
relevance: 5
citations: 0 (OpenAlex, 2026-10-03)
code: []
---

## Summary

Panels of N = 50 stateless LLM agents sit on a communication graph and, every turn, see their own previous estimate plus those of their fixed neighbours and return an updated estimate (temperature 0, no chat history). The main task is circular: each agent predicts an event's peak time of day (HH:MM), so answers map to phases theta_i in [0, 2 pi) and the Kuramoto order parameters apply directly: global order r = |mean e^{i theta}| and local order Z_i over each agent's self-inclusive neighbourhood. Priors are assigned in agent order around a ring C_N^R (each agent sees R neighbours per side, degree 2R), so the start is already a one-twist configuration. The authors classify panels as synchronised (r > 0.9), twisted (r < 0.1, mean Z > 0.7), chimera-like (not collapsed, max Z_i > 0.9 and min Z_i < 0.7) or incoherent. Raising gpt-5-mini's reasoning effort increases fitted neighbour coupling from beta = 0.221 to 0.468-0.489 and lowers spatial heterogeneity by about 0.42, but all 20 higher-effort trials end twisted (r ~ 0.01), not synchronised; minimal-effort trials from the same start end chimera-like. Degree-preserving rewiring of the ring (double-edge swaps) makes every panel synchronise. The lifetime of fragmented states scales with 1/lambda_2 (algebraic connectivity) across eight graph instances (Spearman rho = 0.889 over 35 collapsed trials; graph-level rho = 0.929, p = 0.0067).

## Contribution

The most direct transfer so far of coupled-oscillator theory (twisted states, chimeras, Laplacian spectral contraction) to LLM agent swarms, with a fitted microscopic update rule and a spectral prediction for how fast disagreement dies. It shows two control knobs act on different parts of the dynamics: model-side reasoning effort sets coupling strength (local order), while topology sets global synchronisation. Complements the mean-field (all-to-all) picture of [[de-marzo-2024-ai]] and the information-theoretic emergence measures of [[riedl-2025-emergent]].

## Key results

- Measured (calibration): uniform-random agents give Delta Z = 0.162 (R = 5) and 0.140 (R = 7); copy-a-neighbour agents give 0.414 and 0.247, so spatial heterogeneity alone cannot identify chimeras.
- Measured: across 14 model/effort conditions from six providers, chimera-like, twisted, incoherent and synchronised outcomes all occur; spatial heterogeneity peaks at intermediate radius R = 6 in exploratory sweeps (n = 3 per radius) with Qwen-2.5-72b and gpt-5-nano.
- Measured: gpt-5-mini effort raises beta 0.221 -> 0.468-0.489; Gemini-3.1-Flash-Lite raises beta from ~0 (R^2 = 0.002, no measurable neighbour response at default) to 0.411 and 0.589, lowering Delta Z from 0.219 to 0.118 and 0.070.
- Measured: every degree-preserving rewired control synchronises; matched rings stay heterogeneous. Judges task (scores 1-100): ring vs rewired heterogeneity difference 0.128 (p < 0.0001); the effort effect is not monotonic there.
- Measured: permuted (unwound) priors still produced twisted states with opposite winding numbers (k = +1 and k = -1) in both medium-effort trials (n = 2), none in five minimal-effort trials.
- Measured: predicted vs observed lifetime rank correlation rho = 0.964 (graph level) but the linear theory overpredicts absolute lifetimes by 1.13-3.18x.
- Measured: of trials with Delta Z < 0.03, 40.0% remain fragmented (twisted) at the horizon; 13.4% of trials with steady r >= 0.9 contain a transient minority.
- Theory: k-twisted states are fixed points of circular averaging on C_N^R when S_k = 1 + 2 sum_{m=1}^R cos(2 pi k m / N) > 0; the one-twist state on C_50^R is stable for R <= 16 and loses stability at R = 17 (R/N ~ 0.34), consistent with Wiley, Strogatz and Girvan (2006). Disagreement mode m contracts by 1 - beta lambda_m/(d + 1), so the slowest decay rate is gamma = beta lambda_2/(d + 1).
- Simulation of the fitted map: chimera-like cells appear only when the copy probability q > 0.

## Methods and models

Fitted update map: with probability 1 - q, x_i(t+1) = x_i(t) + beta (m_i(t) - x_i(t)) + eta_i(t) (m_i the self-inclusive local circular or arithmetic mean, eta noise of scale sigma); with probability q, copy a random neighbour. (beta, sigma) estimated by OLS on observed transitions per model/effort condition. Topologies: rings C_N^R (R in {5, 7}), degree-preserving double-edge-swap rewiring, Watts-Strogatz p in {0.1, 0.5}, directed random with out-degree 2R. Dataset: 340 LLM trials (228 clock, 112 judging) plus 20 baselines and 12 permuted-initialisation trials; T = 30 turns (60 and 120 for rewiring and lifetime runs); OpenRouter API; base seed 20251109; bootstrap CIs (20,000 resamples) and permutation tests. Models include gpt-5-mini, gpt-5-nano, Qwen-2.5-72b and Gemini-3.1-Flash-Lite. Agents are instructed to weight their previous estimate and neighbours equally in the clock task, which roughly encodes beta = 0.5. No code URL seen in the main text.

## Limitations and open questions

- Small cells (n = 2-20 per condition; radius sweep n = 3) and one circular task; the judging task does not reproduce the monotone effort effect.
- The equal-weighting instruction in the clock task partly imposes the coupling the paper then measures.
- Ordered initial priors already form a one-twist state, so twisted outcomes may be survival rather than formation; the permuted-prior follow-up (n = 2) bounds but does not settle this.
- The linear spectral model explains collapse ordering but not absolute times and has R^2 = 0.09 at minimal effort.
- Temperature 0 throughout; noise comes from the model, not sampling.

## Relevance to us

Must-read for a swarm-dynamics hackathon: it provides a fully specified, cheap protocol (50 agents, 30 turns, circular estimate), Kuramoto order parameters, and quantitative predictions (lifetime ~ 1/(beta lambda_2)) we can re-test with other models, temperatures, larger N, or swarmalator-style spatial motion. Natural extensions: sweep Watts-Strogatz p continuously (cf. [[wang-2025-rethinking]]), vary temperature (cf. [[de-nobili-2026-microscopic]]), or measure synergy as in [[riedl-2025-emergent]]. Related: [[ricco-2026-consensus]], [[flint-2026-group]], [[grotschla-2025-agentsnet]].

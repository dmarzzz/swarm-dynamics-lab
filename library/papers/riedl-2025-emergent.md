---
id: riedl-2025-emergent
type: paper
title: Emergent Coordination in Multi-Agent Language Models
authors:
- Christoph Riedl
year: 2025
venue: International Conference on Learning Representations (ICLR 2026); arXiv preprint
url: https://arxiv.org/abs/2510.05174
doi: null
arxiv: '2510.05174'
cite: Riedl, C. (2025). Emergent coordination in multi-agent language models. International Conference on Learning Representations (ICLR 2026). arXiv:2510.05174.
topics:
- llm-agent-swarms
- criticality-measurement
- collective-decision
added_by: dmarz/llm-agent-swarms
accessed: '2026-10-03'
read_depth: full
relevance: 5
citations: "3 (OpenAlex W4414973927, arXiv record, 2026-10-03); Semantic Scholar 25 same day"
code: []
---

## Summary

Riedl asks when a group of LLM agents is a genuine collective with higher-order structure rather than a bag of independent agents, and answers it with information theory instead of win rates. Groups of GPT-4.1 agents (plus Llama-3.1-8B/70B, Gemini 2.0 Flash and Qwen3 as robustness checks) play the "group binary search" game of Goldstone et al. (2024): each agent guesses an integer, only the sum is compared with a hidden target, and the only feedback is a group-level "too high/too low". Agents cannot see each other or know the group size, so identical strategies oscillate and only complementary (differentiated) strategies succeed. Three prompt interventions are compared: Plain, Persona (each agent gets a persona), and ToM (persona plus "think about what other agents might do"). Using partial information decomposition (PID) of time-delayed mutual information, the paper finds dynamical synergy in all conditions, but only the ToM condition produces identity-linked differentiation plus goal-directed complementarity, i.e. a stable, integrated collective. Performance improves when synergy and redundancy co-occur.

## Contribution

A falsifiable, data-driven test for emergence in LLM collectives, imported from the Rosas/Mediano causal-emergence framework (PID of time-delayed mutual information) and paired with surrogate null models that localise where synergy lives (row-shuffles break agent identity, column/time-shift shuffles break cross-agent alignment). It is the first paper I found that measures emergence in an LLM collective with the same tools used for neural and animal collectives, and it frames prompting as a control parameter that moves the system between a disordered ("gaseous") regime and a stable attractor.

## Key results

- Preliminary grid (GPT-4.1, 7,150 groups: N = 3..15 agents x temperature 0..1 in 0.1 steps x 50 groups): each extra member lowers the odds of success by about 8% (logistic OR = 0.92); each unit of temperature raises odds by about 50% (OR = 1.50). Measured.
- Main experiment: N = 10 agents, T = 1, 200 groups per condition (600 total). Success rate does not differ significantly across Plain/Persona/ToM. Measured.
- Practical emergence criterion: only about 3.5% of individual groups are significant at p < 0.05, but Fisher-combined p-values are highly significant overall and within each condition; bias-corrected values are above 0 in all conditions. Emergence capacity (pairwise PID synergy) is significant in all conditions; about 32% of groups individually significant (Plain 37%, Persona 44%, ToM 18%). Measured.
- Under the stricter functional-null (coordination-free baseline) only ToM retains significant cross-agent structure (Wilcoxon p = 0.025 vs 0.999 Plain, 0.896 Persona). Measured.
- Total Stability (triplet TDMI normalised by macro-signal entropy, a proxy for Lyapunov stability) is indistinguishable from zero in Plain and Persona and rises sharply under ToM. Triadic information gain over the best pair is about 0, so coordination is pairwise alignment to the global "mean field", not irreducible triplet synergy. Measured; the "mean field" and "basin of attraction" readings are the author's interpretation.
- Agent differentiation (mixed-model likelihood-ratio tests on agent intercepts/slopes): more groups with differentiated agents in Persona, most in ToM. Measured.
- Synergy alone and redundancy alone do not predict success; their interaction does (each amplifies the other's log-odds benefit by 27%). Causal mediation: ToM raises performance indirectly via synergy, only marginally significant. Measured, but correlational with IPW corrections.
- Other models: success Plain/Persona/ToM = Llama-8B 11/14/5.5%, Llama-70B 53/59/61%, Gemini 2.0 Flash 60/75/71%, Qwen3 51/71/58%. Llama-8B is stuck in oscillation; Qwen3 shows "paralysis under coordination ambiguity" (endless chain-of-thought loops), fixed by one prompt line ("repeat your last guess"). Measured.

## Methods and models

Microstate of agent i at round t: deviation of its guess from the equal-share contribution (target/N); macro signal: group error. Three criteria: (1) emergence capacity, pairwise Williams-Beer PID (I_min redundancy) of I(X_t^i, X_t^j ; X_{t+1}^i, X_{t+1}^j) taking the synergy atom; (2) practical criterion Psi = I(V_t; V_{t+1}) - sum_i I(X_t^i; V_{t+1}); (3) coalition test G3 = I_3 - max pair information about the future macro. Two-bin quantile discretisation, Jeffreys-prior and Miller-Madow bias corrections, MMI redundancy as a robustness check, permutation nulls combined across groups with Fisher's method. Agent differentiation via hierarchical mixed models with agent random intercepts/slopes. Prompts and personas in the appendix. Code: https://github.com/riedlc/AI-GBS (replication code).

## Limitations and open questions

Single minimalist task with no direct communication; only global feedback, so the "mean-field" coupling is built into the design. Small-sample entropy estimation forces two-bin discretisation and order-2/3 measures, which can miss higher-order synergy. Synergy and redundancy co-evolve with performance, so their causal role is hard to isolate (mediation only marginal). The ToM effect on success rate is not significant in the main GPT-4.1 runs. Open: does the framework carry over to spatial swarm tasks and larger N, and does the same PID signature appear in [[ruan-2025-benchmarking]]-style local-interaction swarms?

## Relevance to us

This is the measurement toolkit we would most directly reuse: it gives an operational, falsifiable definition of "emergence" for an LLM swarm with nulls that a reviewer will accept, and connects LLM collectives to the criticality and integrated-information literature (topic criticality-measurement). Pairs with the physics-style order-parameter work of [[de-marzo-2024-ai]], [[el-2026-physics]] and [[de-nobili-2026-collective]], and with the group-size and scaling results in [[kim-2025-towards]] and [[flint-2026-group]]. A hackathon experiment could compute Riedl's Psi and G3 on SwarmBench trajectories.

## Notes from dmarz/llm-agent-swarms-recent

Independent full read (arXiv v4, 28 Apr 2026; JREF lists ICLR 2026). Numbers to keep: preliminary sweep of 7,150 GPT-4.1 groups (N = 3-15, T = 0-1 in 0.1 steps, 50 groups per cell): each extra member lowers success odds by ~8% (OR = 0.92), each unit of temperature raises odds ~50% (OR = 1.50). Main runs: N = 10, T = 1, 200 groups per condition. I_3 is ~0 in Plain (p = 0.974) and Persona (p = 0.846) but positive under ToM (p = 3.5e-14); G_3 ~ 0 under Persona/ToM, so the stable regime is pairwise alignment to the mean-field signal rather than irreducible triadic synergy. Synergy x redundancy interaction beta = 0.24 (p = 0.014). Qwen3 shows "paralysis under coordination ambiguity". For swarm work this is a measurement toolkit (PID of time-delayed MI with row/column-shuffle surrogates) applicable to any agent-trajectory data, e.g. SwarmBench logs [[ruan-2025-benchmarking]]. Code: https://github.com/riedlc/AI-GBS

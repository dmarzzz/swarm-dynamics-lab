---
id: zomer-2026-unraveling
type: paper
title: Unraveling the emergence of collective behavior in networks of cognitive agents
authors:
- Nicola Zomer
- Manlio De Domenico
year: 2026
venue: npj Artificial Intelligence
url: https://www.nature.com/articles/s44387-026-00091-5
doi: 10.1038/s44387-026-00091-5
arxiv: null
cite: Zomer, N., & De Domenico, M. (2026). Unraveling the emergence of collective behavior in networks of cognitive agents. npj Artificial Intelligence, 2(1), 36. https://doi.org/10.1038/s44387-026-00091-5
topics:
- llm-agent-swarms
- swarm-intelligence
- collective-decision
added_by: dmarz/llm-agent-swarms-recent
accessed: '2026-10-03'
read_depth: full
relevance: 5
citations: 1 (OpenAlex, 2026-10-03); 7 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

The authors compare LLM-driven "cognitive agents" with classical rule-following particles on two canonical collective tasks, holding everything else fixed. (1) Optimisation: LLM Agent Swarm Optimization (llmASO) extends OPRO (a single LLM proposing new solutions from a sorted list of past solution-value pairs) to a swarm of 20 LLM agents that, each step, share suggestions and best previous solutions with their network neighbours (a multi-agent debate) before proposing new points. It is compared with Clerc-Kennedy constriction PSO (c1 = c2 = 2.05, chi = 0.729) on 2D Ackley, Rastrigin and Rosenbrock functions (randomly shifted each run so agents cannot guess the origin), up to 9,000 function evaluations. A lone LLM agent (OPRO) beats a lone particle and sometimes converges very fast (Ackley: 3 of 5 runs under 1,500 evaluations) but gets trapped in local minima on multimodal landscapes; llmASO on a ring network reliably reaches the global optimum but more slowly than PSO. Denser, shorter-path networks (Barabasi-Albert, random geometric graphs) made llmASO fail on Rastrigin in about 50% of trials, attributed to fast LLM consensus causing premature convergence. (2) A Schelling segregation variant with 100 agents on a 100 x 100 grid, neighbourhood radius 15 and tolerance T from 0.1 to 0.9: with a complete communication network, LLM agents reproduce the particle model's three phases (mixed, segregated, frozen) almost exactly; with BA or local (RGG) communication networks, segregation decreases and convergence slows; homophilic communication (h = 1) removes the mixed phase and makes all agents happy in every run, while heterophilic communication (h = 0) shifts the transition to higher tolerances yet still produces strong segregation at T in [0.4, 0.6].

## Contribution

The most controlled "LLM swarm vs particle swarm" comparison in a peer-reviewed venue, with the classical baselines (PSO, Schelling) implemented identically. Its main finding is that individual cognitive ability does not translate into better collective performance, and that communication topology, not agent intelligence, is the dominant control parameter, with the sign of the effect opposite to human collective problem-solving experiments (Mason and Watts) where efficient networks help. Complements [[jimenez-romero-2025-multi-agent]], [[rahman-2025-llm-powered]] and [[ruan-2025-benchmarking]].

## Key results

- Measured: OPRO single agents outperform single particles; llmASO reaches the global minimum on all three functions but converges more slowly than CF-PSO (20 runs each for swarms, 5 for single agents).
- Measured: llmASO final swarm diameter ~2 in a 20-wide search space, described as an emergent shared convention.
- Measured (SI): BA and RGG networks lead to convergence failure on Rastrigin in ~50% of trials; ring topology preserves diversity. BA dominates on Rosenbrock (problem-dependent optimal topology).
- Measured: Schelling with complete network: segregation coefficient, iterations and unhappy fraction nearly identical to particles across T; LLM agents end with more nearest neighbours in mixed and diluted phases.
- Measured: homophily (h = 1) gives zero unhappy agents in all runs and all T; heterophily (h = 0) needs many more iterations and shifts transitions upward.
- Observed: agents tend to probe the origin or the domain centre without evidence (hence random shifts), and "Let's think step by step" increased hallucinations in the Schelling task.

## Methods and models

Starling-LM-7B-alpha (4-bit) via llama.cpp and LangChain, chosen to be feasible on small robots. llmASO: synchronous neighbour message exchange, 3-digit float precision (a 20,000 x 20,000 effective grid), best solutions sorted with best last. Schelling: segregation coefficient s = (2/N^2) sum_c n_c^2, unhappy fraction, iterations to stationarity (cap 100 Monte Carlo steps), stationarity by slope thresholds (window 20, threshold 0.001); agents converse pairwise with a random connected peer before relocating; homophilic BA networks after Karimi et al. Code: https://github.com/CoMuNeLab/LLM-Agents (stated as to be released upon acceptance; not checked).

## Limitations and open questions

- One small 7B model; the authors note hyperparameters were varied one at a time only, and model, prompt and incentive choices remain untested.
- 2D functions and 100-agent Schelling only; LLM cost limits runs (5-20 per condition).
- Prompt order (own info before social info) may over-weight social cues (herding), which the authors flag as a possible cause of premature convergence.
- No explicit order parameter for llmASO beyond diameter and best value.

## Relevance to us

Directly reusable design for a hackathon: a PSO-vs-LLM-swarm comparison with topology as the control knob, using a small local model. The result that sparse (ring) networks are needed to prevent premature consensus connects to [[hirota-2026-collective]] (ring vs rewired), [[de-marzo-2024-ai]] (fast consensus in small groups) and [[weng-2025-do]] (conformity). A natural extension is to add PSO-style explicit weighting of individual vs social information.

## Notes from dmarz/llm-agent-swarms-recent-audit

Audit 2026-10-03: spot-checked against the Nature (npj AI) full text and Crossref (2(1), article 36). Confirmed: Starling-LM-7B-alpha 4-bit, LangChain, c1 = c2 = 2.05 and chi = 0.729, max 9000 evaluations, 20 swarm runs and 5 single-agent runs, 100-agent Schelling, code to be released at github.com/CoMuNeLab/LLM-Agents. The ~50% Rastrigin failure figure is attributed to the SI and was not re-checked. No corrections.

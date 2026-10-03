---
id: el-2026-physics
type: paper
title: 'Physics of Agents: Statistical Mechanics Predicts Collective Behavior of AI Agents'
authors:
- Batu El
- Jinhee Paeng
- Fatih Dinc
- Shiye Su
- Mete Erdogan
- Aneesh Pappu
- Haotian Ye
- Wanjia Zhao
- Surya Ganguli
- James Zou
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2608.16578
doi: null
arxiv: '2608.16578'
cite: 'El, B., Paeng, J., Dinc, F., Su, S., Erdogan, M., Pappu, A., Ye, H., Zhao, W., Ganguli, S., & Zou, J. (2026). Physics of agents: Statistical mechanics predicts collective behavior of AI agents. arXiv preprint arXiv:2608.16578.'
topics:
- llm-agent-swarms
- sync-consensus
- criticality-measurement
added_by: dmarz/llm-agent-swarms
accessed: '2026-10-03'
read_depth: full
relevance: 5
citations: "0 (OpenAlex W7203684476, arXiv record, 2026-10-03); Semantic Scholar 8 same day"
code: []
---

## Summary

The authors simulate about 10,000 communities of N = 32 persona-conditioned LLM agents (GPT-4o-mini, Gemma-3n-E4B, Qwen3.5-9B, Llama-3.1-8B) that hold a binary opinion on a shared question, exchange short messages over a fixed signed network J in {-1, 0, +1} (friendly vs unfriendly ties) for T = 8 synchronous rounds, and revise their opinions. Questions are either objective (MATH problems recast as binary choice, personas encode expertise) or subjective (political statements, personas from TWIN-2K-500). Groups start indifferent and build conviction, ending in consensus or polarisation; communication improves accuracy on objective questions but drifts subjective opinions rightward for three of four models. A kinetic-Ising (Glauber) model with three couplings and a learned intrinsic field predicts individual and group trajectories from initial opinions alone and generalises to unseen graph families.

## Contribution

Shows that a compact, interpretable energy-based model, E(s) = -1/2 sum J_ij s_i s_j - sum g_i s_i with logistic Glauber updates, is a predictive dynamical law for LLM collectives on networks, not just a descriptive analogy. It also measures where real LLM communities sit relative to a critical social temperature, and explains truth-seeking and consensus through fitted coupling asymmetries.

## Key results

- Individual archetypes (frozen, switcher, intermittent, oscillator) and five group archetypes; "divergence" and "majority switch" groups reach 11-12% for GPT-4o-mini and Qwen3.5-9B. Measured.
- Conviction c(t) = mean of squared opinions rises in all settings; indifference falls and consensus rises monotonically. On objective questions incorrect-to-correct majority switches outnumber the reverse for all models. Measured.
- Prediction (balanced accuracy on held-out questions): three-coupling discrete rule 75-86% one-step and 61-77% rollout, best in every column; single-coupling version can fall to chance (53.9 Llama subjective, 50.6 Qwen objective); mean-field baseline mid-50s to low-70s. In- vs out-of-distribution graphs differ by at most 2.4 points; on unseen families (low-rank, square and triangular lattices) one-step accuracy is 85.0-97.8%. Measured.
- A 64-agent mixed community (32 GPT-5.6-sol + 32 DeepSeek-V4-Flash) is predicted at 81.9 (subjective) and 80.0 (objective) one-step balanced accuracy. Measured.
- Rollouts reproduce group-archetype shares within about 3 points (objective) and 5 points (subjective) mean absolute deviation; individual oscillators are over-predicted. Measured.
- Criticality: sweeping a temperature over 41 values (0.05-20) and locating the peak of chi = N Var(|n|) places every fitted community below its critical temperature, explaining conviction build-up. Model-derived.
- Fitted couplings: effective concordant coupling (beta+ + beta0) 0.99-3.03 vs discordant (beta0 - beta-) at most 0.73 (negative for GPT-4o-mini subjective), so attraction dominates and favours consensus. A five-coupling fit shows correct neighbours pull harder (beta+_T > beta+_F) and incorrect neighbours push harder, a statistical account of truth seeking. Measured parameters, mechanistic reading is the authors'.
- Asynchronous updates (rate 0.5 per round): continuous-time rule reaches 80.4/78.5 rollout accuracy (subjective). Measured.

## Methods and models

Opinions averaged over K = 5 samples per agent per round (values on a 6-point grid); messages routed to separate friendly/unfriendly inboxes; Markovian updates (only latest messages). Update rule P(s_i = +1) = sigma(beta+ sum J+_ij s_j + beta- sum J-_ij s_j + beta0 sum |J_ij| s_j + g_i), with g_i = w . phi_i from persona and question embeddings; two-stage gradient-descent fit on one-step transitions; mean-field ODE from the master equation for the asynchronous case. Four graph families (signed random, low-rank, square lattice, triangular lattice). No code repository linked on the arXiv page as of 2026-10-03.

## Limitations and open questions

Binary opinions, fixed symmetric networks, no memory beyond the last inbox, and message content is discarded by the model (only stance signs enter). Group trajectories are only partly reproducible across sampling seeds, so prediction is evaluated at the distribution level. The authors propose Potts extensions, message-embedding fields and time-varying graphs, including agents situated in physical space with proximity-based communication, which is exactly the swarm setting.

## Relevance to us

The most complete statistical-physics treatment of LLM collectives I found: it supplies a fitted Hamiltonian, a critical temperature and archetype classification that a hackathon could reuse as an analysis pipeline. Extends [[de-marzo-2024-ai]] from all-to-all Curie-Weiss to signed sparse networks, complements [[de-nobili-2026-collective]] (2D lattice exponents) and [[brockers-2025-disentangling]] (bias vs interaction), and offers a mechanistic reading of debate results in [[du-2023-improving]] and [[choi-2025-debate]].

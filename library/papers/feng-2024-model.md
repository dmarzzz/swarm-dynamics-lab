---
id: feng-2024-model
type: paper
title: 'Model Swarms: Collaborative Search to Adapt LLM Experts via Swarm Intelligence'
authors:
- Shangbin Feng
- Zifeng Wang
- Yike Wang
- Sayna Ebrahimi
- Hamid Palangi
- Lesly Miculicich
- Achin Kulshrestha
- Nathalie Rauschmayr
- Yejin Choi
- Yulia Tsvetkov
- Chen-Yu Lee
- Tomas Pfister
year: 2024
venue: International Conference on Machine Learning (ICML 2025)
url: https://arxiv.org/abs/2410.11163
doi: null
arxiv: '2410.11163'
cite: 'Feng, S., Wang, Z., Wang, Y., Ebrahimi, S., Palangi, H., Miculicich, L., Kulshrestha, A., Rauschmayr, N., Choi, Y., Tsvetkov, Y., et al. (2025). Model swarms: Collaborative search to adapt LLM experts via swarm intelligence. International Conference on Machine Learning (ICML 2025). arXiv:2410.11163.'
topics:
- llm-agent-swarms
- swarm-intelligence
added_by: dmarz/llm-agent-swarms
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: "2 (OpenAlex W4403573463, arXiv record, 2026-10-03); Semantic Scholar 34 same day"
code: []
---

## Summary

Model Swarms treats a pool of LLM expert checkpoints as particles that move collaboratively in weight space, guided by the best-found checkpoints (a particle-swarm-optimisation-style search), to optimise a utility function for adaptation. It is tuning-free, works with as few as 200 examples, and improves over 12 model-composition baselines by up to 21.0% across single tasks, multi-task domains, reward models and human interests; experts can discover capabilities absent from the initial checkpoints (weak-to-strong transitions).

## Contribution

Uses swarm intelligence (PSO) on LLM weights rather than LLM agents in a swarm, an inversion worth distinguishing.

## Key results

- Up to 21.0% over 12 baselines (abstract).
- Works with about 200 examples (abstract).

## Methods and models

PSO-like velocity updates over model parameter vectors with personal-best and global-best guidance. Code not checked.

## Limitations and open questions

Requires same-architecture checkpoints; compute for weight-space search. Abstract-level read.

## Relevance to us

Relevant to topic swarm-intelligence as an application of PSO to LLMs; not about agent interaction dynamics.

## Notes from dmarz/swarm-intelligence

Read in full (arXiv v2, 31 May 2025; ICML 2025, PMLR 267). Details the entry above does not record:

- Algorithm (measured setup): N = 20 particles grown from n = 10 Gemma-7B LoRA experts (one per Tulu-v2 SFT domain) by
  random pairwise linear interpolation. Velocity update v_i <- (1/C)[r_v phi_v v_i + r_p phi_p (p_i - x_i) +
  r_g phi_g (g - x_i) - r_w phi_w (g_w - x_i)], with C the sum of the four weighted terms, r ~ U(0,1), and a repulsion
  from the global worst g_w added to standard PSO; step x_i <- x_i + lambda v_i with lambda decayed by 0.95 per
  iteration; restart a particle at its personal best if it has not improved for c_r iterations; K = 50 max iterations.
  The utility f is validation performance on as few as 200 examples, a reward-model score, or an LLM-as-judge score.
- Results (measured): +13.3% over the second-best of 12 composition baselines averaged over 9 single-task datasets,
  +21.0% on the three reasoning tasks, up to +29.7% on GSM8k; +5.7% on multi-task domains; +6.7% average over 14
  baselines (including PPO and DPO) on reward models, with steerability to both verbose and concise RMs; human
  evaluation 70.8% average win rate over the initial experts across 16 interest domains.
- Swarm-dynamics observations (measured): only 10.4% of best-ending particles started as best, and 56.9% started in
  the bottom half ("weak-to-strong"); 36.0-53.5% of questions no initial expert solved were solved by at least one
  expert afterwards; with the number of particles fixed, a more diverse initial pool (10 x 1 vs 1 x 10) gave +35.3%.
- Token-swarm variant runs the same update on mixing weights over next-token distributions of experts with different
  architectures (4 Gemma + 4 Mistral): global best +5.7% and +11.9% on two datasets.
- Limitations stated: can stall in local optima; all experts must share an architecture for weight swarms; per-step
  cost scales with N full model evaluations; perplexity could not be reliably optimised; dual-use risk with
  adversarial utility functions.
- Code: https://github.com/BunsenFeng/model_swarm
- Relevance from the swarm-intelligence angle: a high-dimensional PSO in weight space where diversity of the
  initial swarm matters more than its quality, which matches the exploration-diversity arguments in PSO theory
  ([[huang-2023-global]], [[pinnau-2017-consensus]]); the global-worst repulsion term is a new interaction rule worth
  testing in dynamics experiments.

---
id: yu-2019-multi
type: paper
title: Multi-Agent Adversarial Inverse Reinforcement Learning
authors:
- Lantao Yu
- Jiaming Song
- Stefano Ermon
year: 2019
venue: 'Proceedings of the 36th International Conference on Machine Learning (ICML), PMLR 97'
url: https://proceedings.mlr.press/v97/yu19e.html
doi: null
arxiv: '1907.13220'
cite: 'Yu, L., Song, J., & Ermon, S. (2019). Multi-Agent Adversarial Inverse Reinforcement Learning. In K. Chaudhuri & R. Salakhutdinov (Eds.), Proceedings of the 36th International Conference on Machine Learning, PMLR 97:7194-7201.'
topics:
- marl-emergence
added_by: vishesh/senku-1
accessed: '2026-10-03'
read_depth: full
relevance: 3
citations: '171 (Semantic Scholar, 2026-10-03)'
code: []
---

## Summary

MA-AIRL recovers each agent's reward function from demonstrations of a multi-agent interaction, where single-agent inverse RL does not apply because one agent's optimal policy depends on the others. The authors introduce a solution concept, logistic stochastic best response equilibrium (LSBRE), built from a Gibbs-sampling-style process in which each agent repeatedly best-responds with entropy regularisation while the others are held fixed; the stationary distribution of that chain is the joint policy. Theorem 1 characterises the trajectory distribution induced by LSBRE as an energy-based model, and Theorem 2 shows that maximum pseudolikelihood estimation over the per-agent conditionals is asymptotically consistent for the intractable joint likelihood. The practical algorithm trains one discriminator and one adaptive importance sampler per agent, with the reward split into an estimator and a potential shaping term. Experiments use three particle environments and compare against MA-GAIL.

## Contribution

The first MaxEnt inverse RL framework for Markov games that scales to high-dimensional continuous state-action spaces with unknown dynamics, obtained by replacing Nash or correlated equilibrium with LSBRE, which tolerates bounded rationality, and by making the resulting likelihood tractable through pseudolikelihood.

## Key results

- Measured (Table 3, cooperative tasks, correlation between learned and ground-truth rewards, mean and variance over N independently learned reward functions): cooperative navigation SCC 0.934 +/- 0.015 for MA-AIRL against 0.792 +/- 0.085 for MA-GAIL, PCC 0.882 +/- 0.028 against 0.556 +/- 0.081; cooperative communication SCC 0.936 +/- 0.080 against 0.879 +/- 0.059, PCC 0.848 +/- 0.099 against 0.612 +/- 0.093.
- Measured (Table 4, competitive keep-away): average SCC 0.721 for MA-AIRL against 0.538 for MA-GAIL, average PCC 0.694 against 0.445.
- Measured (Table 1, expected returns, cooperative): navigation expert -43.195 +/- 2.659, random -391.314 +/- 10.092, MA-AIRL -47.515 +/- 2.549, MA-GAIL -52.810 +/- 2.981; communication expert -12.712 +/- 1.613, random -125.825 +/- 3.4906, MA-AIRL -12.727 +/- 1.557, MA-GAIL -12.811 +/- 1.604.
- Measured (Table 2, competitive keep-away, agent 1 is the seeker and agent 2 the adversary): expert against expert -6.804 +/- 0.316; MA-AIRL against expert -6.785 +/- 0.312 and MA-GAIL against expert -6.978 +/- 0.305; expert against MA-AIRL -7.367 +/- 0.311 and expert against MA-GAIL -6.919 +/- 0.298.
- Measured (Figure 1): MA-GAIL's reward-ground-truth PCC starts high and degrades over roughly 12,000 training epochs toward 0.5-0.6, while MA-AIRL stays near 0.85-0.9, consistent with the argument that a GAIL discriminator converges to 0.5 everywhere and so stops carrying reward information.

## Methods and models

Three simulated particle environments from Lowe et al.: cooperative navigation (three agents, three landmarks), cooperative communication (a speaker and a listener), and competitive keep-away. Experts are trained with a multi-agent version of ACKTR on the ground-truth rewards; 200 demonstration episodes of 50 time steps each are used, with behaviour-cloning pretraining for both methods. Learning is decentralised and uses no prior knowledge of whether a task is cooperative or competitive; the reward parameters carry an l2 penalty. Metrics are Pearson and Spearman correlation against ground-truth rewards, and expected return. Code is at github.com/ermongroup/MA-AIRL; the environments are the suite catalogued as [[gh-openai-multiagent-particle-envs]].

## Limitations and open questions

Everything is measured on three small particle tasks with two or three agents, so nothing here speaks to large populations. Reward shaping ambiguity is handled by restricting the learned function to an estimator plus a state-only potential, which mitigates rather than removes the identifiability problem; the formal version of that gap is the subject of [[kim-2021-reward]]. The discussion section names reward regularisation and exploiting known task structure as future work.

## Relevance to us

If the hackathon question is whether a preference inferred from one agent predicts a collective's choices, this is the method that does the inferring: it is the standard way to recover a per-agent reward from observed joint behaviour, and its measured correlations (PCC 0.88 cooperative, 0.69 competitive) are a realistic ceiling on how well such an inferred preference can be expected to match the real one in a small group. Its honest reading for us is cautionary as much as enabling: inference quality is already well below 1.0 at three agents, so a pipeline that infers a preference and then uses it to steer a collective inherits that error before any influence step runs. The LSBRE idea of agents best-responding in scan order is also a usable model of a debate round. Pairs with [[kim-2021-reward]] on when the recovered reward is unique at all, with [[lowe-2017-multi]] for the environments and the MARL baseline, and with the other inverse-modelling entries [[sosic-2017-inverse]] and [[schafer-2022-bayesian]].

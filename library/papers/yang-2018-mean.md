---
id: yang-2018-mean
type: paper
title: Mean Field Multi-Agent Reinforcement Learning
authors: [Yaodong Yang, Rui Luo, Minne Li, Ming Zhou, Weinan Zhang, Jun Wang]
year: 2018
venue: Proceedings of the 35th International Conference on Machine Learning (ICML), PMLR 80
url: https://arxiv.org/abs/1802.05438
doi: null
arxiv: '1802.05438'
cite: Yang, Y., Luo, R., Li, M., Zhou, M., Zhang, W., & Wang, J. (2018). Mean field multi-agent reinforcement learning. In Proceedings of the 35th International Conference on Machine Learning (ICML), PMLR 80, 5571–5580.
topics: [marl-emergence]
added_by: dmarz/marl-emergence
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: "313 for the arXiv record (OpenAlex, 2026-10-03); undercounts the ICML version"
code: []
---

## Summary

MARL methods with joint-action critics do not scale past tens of agents because the joint action grows with N
and other agents' exploration noise swamps the learning signal. The authors factor each agent's Q-function into
pairwise interactions with its neighbours and then apply a mean-field approximation: agent j's Q depends only
on its own action and the mean (empirical distribution) of its neighbours' one-hot actions. This turns a
many-body problem into a two-body problem between an agent and a "mean agent". They derive MF-Q and MF-AC,
prove convergence of MF-Q to a Nash Q-value under strong assumptions, and show learning with up to 1000 agents
on a resource-allocation game, recovery of the 2D Ising phase transition without an energy function, and wins
in a 64 versus 64 MAgent battle.

## Contribution

The founding paper of "mean-field MARL" in the ML community: it brings the physics mean-field approximation into
model-free Q-learning so that critic size is independent of N. It is distinct from mean-field games
([[lasry-2007-mean]]), which solve coupled HJB and Fokker-Planck equations with known dynamics; the paper itself
draws that contrast.

## Key results

- Gaussian Squeeze (agents pick integers 0-9 whose sum x is scored by x exp(-(x - mu)^2 / sigma^2), mu = 400,
  sigma = 200): with N = 100 all methods do well; with N = 500 and N = 1000, MF-Q and MF-AC learn the optimum
  while independent Q-learning, FMQ, Rec-FMQ and a MADDPG-style MAAC all fail (measured).
- Ising model on a 20x20 grid, reward r_j = h_j a_j + (lambda/2) sum over neighbours of a_j a_k, agents not told
  the energy function: the equilibrium order parameter versus temperature from MF-Q nearly matches MCMC,
  including a critical temperature near tau = 1.2 (measured). Claimed as the first model-free RL solution of
  the Ising model.
- MAgent battle, 64 v 64: MF-Q beats IL, AC and MF-AC on win rate and total reward after 2000 self-play rounds;
  the authors say results hold at 8, 144 and 256 agents but do not show them.
- Theory: with Assumptions 1-3 (every stage game's Nash equilibrium is a global optimum or a saddle point) and a
  low enough Boltzmann temperature, MF-Q converges to the Nash Q-value. The authors note Assumption 3 is very
  strong and appears unnecessary in practice.

## Methods and models

Stochastic game with N agents. Q_j(s, a) ~ (1/N_j) sum_k Q_j(s, a_j, a_k) over neighbours, then Taylor-expand
around abar_j = (1/N_j) sum_k a_k so Q_j(s, a) ~ Q_j(s, a_j, abar_j) with a bounded second-order remainder.
Update Q_j <- (1 - alpha) Q_j + alpha [r_j + gamma v_j(s')], with v_j the expectation under a Boltzmann policy
pi_j(a_j | s, abar_j) proportional to exp(beta Q_j(s, a_j, abar_j)); mean actions and policies are iterated to
a fixed point. MF-Q uses DQN-style training; MF-AC uses a policy-gradient actor with the MF critic.
Environments: Gaussian Squeeze, Ising (validated against MCMC), MAgent battle (Zheng et al. 2018). Main text read
in full; appendices (proof details, hyperparameters) skimmed.

## Limitations and open questions

Requires homogeneous, exchangeable neighbours and an action-mean summary, so it cannot represent who did what;
heterogeneous or role-differentiated swarms break the approximation. The convergence proof rests on an
assumption that rarely holds. The Ising experiment is a stateless stage game, so it shows that MARL can find
a mean-field equilibrium, not that it reproduces dynamics. Baselines in the battle game exclude centralised
critics because agents die. Later work (Laurière et al., Guo et al.) puts mean-field RL on firmer ground.

## Relevance to us

The bridge between statistical physics and MARL: an Ising phase transition recovered by learning agents is
exactly the kind of experiment a swarm-dynamics hackathon could extend (does a learned flock show a Vicsek-like
transition?). Pairs with [[huttenrauch-2019-deep]] (mean of observations rather than actions), [[durve-2020-learning]]
(alignment rule learned by Q-learning), [[zheng-2018-magent]] (the battle environment) and [[lasry-2007-mean]].

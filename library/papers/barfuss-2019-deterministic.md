---
id: barfuss-2019-deterministic
type: paper
title: Deterministic limit of temporal difference reinforcement learning for stochastic games
authors: [Wolfram Barfuss, Jonathan F. Donges, Jürgen Kurths]
year: 2019
venue: Physical Review E
url: https://arxiv.org/abs/1809.07225
doi: 10.1103/PhysRevE.99.043305
arxiv: '1809.07225'
cite: Barfuss, W., Donges, J. F., & Kurths, J. (2019). Deterministic limit of temporal difference reinforcement learning for stochastic games. Physical Review E, 99(4), 043305.
topics: [marl-emergence]
added_by: dmarz/marl-emergence-audit
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "58 (Crossref is-referenced-by-count, 2026-10-03)"
code: []
---

## Summary

Analytical work on learning dynamics (replicator equations and their relatives) had been confined to stateless
repeated games. The authors separate the fast interaction timescale from the slow adaptation timescale, average
over interactions, and obtain deterministic ordinary maps for Q-learning, SARSA and actor-critic learners in
multi-state stochastic games. Iterating these maps on two-agent, two-action, two-state environments (a two-state
Matching Pennies and a risk-reward dilemma) reveals fixed points, limit cycles and deterministic chaos, with
largest Lyapunov exponents and bifurcation diagrams in learning rate alpha and discount gamma.

## Contribution

Extends the evolutionary-game-theory view of multi-agent learning, surveyed in [[bloembergen-2015-evolutionary]],
from normal-form games to environments with state, and gives a physicist's toolset (deterministic limit,
bifurcations, Lyapunov exponents) for the dynamics of learning agents themselves.

## Key results

- Deterministic learning equations for Q, SARSA and AC learners in stochastic games, derived and validated
  against stochastic simulations.
- Two-state Matching Pennies with gamma = 0.1, beta = 5: Q and SARSA learners converge to the mixed fixed point
  (reward 0.5, about 600 steps at alpha = 0.02), while actor-critic learners behave qualitatively differently.
- Across alpha and gamma the dynamics show fixed points, periodic orbits and chaotic motion with positive largest
  Lyapunov exponent (measured numerically).

## Methods and models

Multi-agent Markov environments; Boltzmann (softmax) action selection with intensity of choice beta; TD errors
replaced by their expectation over the current joint policy and stationary state distribution (batch / infinite
memory limit). Bifurcation diagrams and Lyapunov exponents computed from the resulting maps.

## Limitations and open questions

Only two agents, two actions and two states; the deterministic limit assumes slow learning and ignores sampling
noise. Whether chaos persists for many agents in spatial environments is open (see [[sanders-2018-prevalence]]
for many-player normal-form games).

## Relevance to us

If a learned swarm fails to settle, this is the framework for asking whether the learning dynamics themselves are
chaotic. Related: [[galla-2013-complex]], [[sanders-2018-prevalence]], [[bloembergen-2015-evolutionary]].

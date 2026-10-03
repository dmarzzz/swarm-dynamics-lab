---
id: galla-2013-complex
type: paper
title: Complex dynamics in learning complicated games
authors: [Tobias Galla, J. Doyne Farmer]
year: 2013
venue: Proceedings of the National Academy of Sciences
url: https://pmc.ncbi.nlm.nih.gov/articles/PMC3557065/
doi: 10.1073/pnas.1109672110
arxiv: null
cite: Galla, T., & Farmer, J. D. (2013). Complex dynamics in learning complicated games. Proceedings of the National Academy of Sciences, 110(4), 1232–1236.
topics: [marl-emergence]
added_by: dmarz/marl-emergence-audit
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: "118 (Crossref is-referenced-by-count, 2026-10-03)"
code: []
---

## Summary

Two players repeatedly play a randomly generated game with many moves and learn by experience-weighted attraction
(EWA), a reinforcement-learning rule with memory loss alpha and intensity of choice beta. Varying the payoff
correlation Gamma between the players (from zero-sum to identical payoffs) and the memory, the authors map three
regimes of learning dynamics: convergence to a unique fixed point, a huge multiplicity of stable fixed points, and
high-dimensional chaos in which total payoffs fluctuate intermittently with heavy tails.

## Contribution

Founding statistical-physics paper on the dynamics of learning in "complicated" games, showing that equilibrium
is not the generic outcome when agents learn. It motivates the many-player extension [[sanders-2018-prevalence]]
and the multi-state extension [[barfuss-2019-deterministic]].

## Key results

- Simulations with N = 50 moves per player (a 98-dimensional strategy space) show the three regimes; a unique
  fixed point at large alpha and low Gamma, many fixed points (often more than 100) for Gamma > 0,
  and limit cycles or chaos for negative Gamma and small alpha (measured).
- Attractor dimension is highest for moderately anticorrelated payoffs (around Gamma = -0.6) (measured).
- In the chaotic regime payoffs show bursty, intermittent fluctuations reminiscent of turbulence and financial
  markets (measured, qualitative comparison).
- Path-integral methods from disordered systems give the stability boundary of the unique fixed point for
  N -> infinity in a continuous-time limit, where for fixed Gamma stability depends only on alpha/beta; the line
  agrees well with simulations (derived and measured).

## Methods and models

EWA learning: each move's attraction is a discounted running sum of its payoffs, with memory-loss parameter alpha
(the paper states alpha = 1 means no memory and alpha = 0 means all past steps weighted equally); strategies are
a softmax of attractions with intensity of choice beta (I did not transcribe the exact update equation); random payoff matrices with correlation Gamma between
players. Deterministic (expected-payoff) learning dynamics; Lyapunov exponents and attractor dimension estimated
numerically. Abstract read in full; main text skimmed on the PMC page.

## Limitations and open questions

Two players, random normal-form games, no state or space. Whether these regimes carry over to spatially embedded
learning swarms with local interactions is untested.

## Relevance to us

A warning and a measurement programme: learning agents can produce non-equilibrium, chaotic collective dynamics,
and the right description may be dynamical-systems language rather than equilibrium. Read with
[[sanders-2018-prevalence]] and [[barfuss-2019-deterministic]].

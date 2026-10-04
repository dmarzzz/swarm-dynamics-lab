---
id: littman-1994-markov
type: paper
title: Markov games as a framework for multi-agent reinforcement learning
authors:
- Michael L. Littman
year: 1994
venue: Machine Learning Proceedings 1994 (Proceedings of the Eleventh International Conference on Machine Learning)
url: https://courses.cs.duke.edu/spring07/cps296.3/littman94markov.pdf
doi: 10.1016/b978-1-55860-335-6.50027-1
arxiv: null
cite: Littman, M. L. (1994). Markov games as a framework for multi-agent reinforcement learning. In Machine Learning Proceedings 1994 (pp. 157–163). Morgan Kaufmann.
topics:
- marl-emergence
added_by: dmarz/marl-emergence
accessed: '2026-10-03'
read_depth: abstract
relevance: 2
citations: 3396 (Semantic Scholar, 2026-10-03); 1461 (Crossref, 2026-10-03)
code: []
---

## Summary

The MDP view of RL treats other agents as a fixed part of the environment. Littman adopts Markov (stochastic) games to include multiple adaptive agents and studies the two-player zero-sum case, giving minimax-Q, a Q-learning-like algorithm that finds optimal (possibly stochastic) policies, and demonstrates it on a simple two-player soccer-like game whose optimal policy is probabilistic.

## Contribution

Founding formalism of MARL: the Markov game is the object every later MARL paper, including [[yang-2018-mean]], defines first.

## Key results

- Minimax-Q learns a probabilistic optimal policy in a small zero-sum game (per abstract and introduction).

## Methods and models

Markov games, minimax-Q with linear programming at each state. Read abstract and introduction of the PDF.

## Limitations and open questions

Two-player zero-sum only.

## Relevance to us

Formal background; cite when defining the game. Related: [[tan-1993-multi]], [[busoniu-2008-comprehensive]].

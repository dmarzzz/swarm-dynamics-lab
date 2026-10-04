---
id: tan-1993-multi
type: paper
title: 'Multi-Agent Reinforcement Learning: Independent vs. Cooperative Agents'
authors:
- Ming Tan
year: 1993
venue: Machine Learning Proceedings 1993 (Proceedings of the Tenth International Conference on Machine Learning)
url: https://web.media.mit.edu/~cynthiab/Readings/tan-MAS-reinfLearn.pdf
doi: 10.1016/b978-1-55860-307-3.50049-6
arxiv: null
cite: 'Tan, M. (1993). Multi-agent reinforcement learning: Independent vs. cooperative agents. In Machine Learning Proceedings 1993 (pp. 330–337). Morgan Kaufmann.'
topics:
- marl-emergence
added_by: dmarz/marl-emergence
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 1067 (Crossref, 2026-10-03); 1859 (OpenAlex, 2026-10-03)
code: []
---

## Summary

Asks whether, for a fixed number of RL agents in a predator-prey style grid task, cooperative agents beat independent ones, and at what cost. Cooperation is implemented as sharing sensations, sharing episodes, or sharing learned policies. Extra sensation helps if used efficiently; sharing policies or episodes speeds learning at a communication cost; and in joint tasks partners significantly outperform independent agents after a slower start.

## Contribution

The origin of independent Q-learning as a MARL baseline and of policy and experience sharing, the trick behind parameter sharing in swarm RL ([[huttenrauch-2019-deep]], [[brambati-2025-learning]] centralised training).

## Key results

- Policy or episode sharing accelerates learning; joint-task partnerships outperform independent learners (per abstract).

## Methods and models

Tabular Q-learning hunters and prey on a grid. Read abstract and introduction.

## Limitations and open questions

Tiny tasks; tabular.

## Relevance to us

Historical root of the shared-versus-independent training choice that [[brambati-2025-learning]] shows matters at scale (decentralised training degrades at N = 1600).

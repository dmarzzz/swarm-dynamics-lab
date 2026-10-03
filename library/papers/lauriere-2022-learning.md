---
id: lauriere-2022-learning
type: paper
title: 'Learning in Mean Field Games: A Survey'
authors:
- Mathieu Laurière
- Sarah Perrin
- Julien Pérolat
- Sertan Girgin
- Paul Muller
- Romuald Élie
- Matthieu Geist
- Olivier Pietquin
year: 2022
venue: arXiv preprint
url: https://arxiv.org/abs/2205.12944
doi: null
arxiv: '2205.12944'
cite: 'Laurière, M., Perrin, S., Pérolat, J., Girgin, S., Muller, P., Élie, R., Geist, M., & Pietquin, O. (2022). Learning in mean field games: A survey. arXiv preprint arXiv:2205.12944.'
topics:
- marl-emergence
added_by: dmarz/marl-emergence
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 96 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Mean field games let the number of players go to infinity through a mean-field approximation, but classical solvers need full model knowledge and PDEs. This survey reviews RL methods to learn equilibria and social optima in MFGs, distinguishes static, stationary and evolutive settings, presents a general framework of iterative methods (best response, policy evaluation, fictitious play) with exact updates, explains how RL makes them model-free, and gives numerical illustrations on a benchmark.

## Contribution

The reference survey connecting [[lasry-2007-mean]] to model-free RL; the theory context in which [[yang-2018-mean]] (mean-field MARL) and [[borra-2021-optimal]] (MFG for collision avoidance) sit.

## Key results

- Review with benchmark illustrations (per abstract).

## Methods and models

Literature survey and unified algorithmic framework. Abstract-level read.

## Limitations and open questions

Mathematical focus; few collective-motion examples.

## Relevance to us

If a hackathon project wants an infinite-swarm limit of a learned policy, this is the toolkit. Related: [[yang-2018-mean]], [[borra-2021-optimal]].

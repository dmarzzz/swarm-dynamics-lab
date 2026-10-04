---
id: busoniu-2008-comprehensive
type: paper
title: A Comprehensive Survey of Multiagent Reinforcement Learning
authors:
- Lucian Buşoniu
- Robert Babuška
- Bart De Schutter
year: 2008
venue: IEEE Transactions on Systems, Man, and Cybernetics, Part C (Applications and Reviews)
url: https://www.dcsc.tudelft.nl/~bdeschutter/pub/rep/07_019.pdf
doi: 10.1109/TSMCC.2007.913919
arxiv: null
cite: Buşoniu, L., Babuška, R., & De Schutter, B. (2008). A comprehensive survey of multiagent reinforcement learning. IEEE Transactions on Systems, Man, and Cybernetics, Part C (Applications and Reviews), 38(2), 156–172.
topics:
- marl-emergence
added_by: dmarz/marl-emergence
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 2322 (Semantic Scholar, 2026-10-03); 1753 (Crossref, 2026-10-03)
code: []
---

## Summary

The standard pre-deep-learning survey of MARL. It organises the field around the formal statement of the multi-agent learning goal, identifying two focal points, stability of the agents' learning dynamics and adaptation to the changing behaviour of other agents, and classifies algorithms by whether they target fully cooperative, fully competitive or general-sum settings. It discusses representative algorithms in each class, the benefits and challenges of MARL, and application domains such as robotics, distributed control and economics.

## Contribution

Canonical taxonomy (cooperative, competitive, mixed; stability versus adaptation) that later deep-MARL surveys ([[hernandez-leal-2019-survey]], [[gronauer-2022-multi]]) build on, and that physics-side papers ([[durve-2020-learning]], [[yang-2018-mean]]) cite as their MARL reference.

## Key results

- Review; no new results. Frames non-stationarity and the equilibrium-selection problem as the central difficulties.

## Methods and models

Literature survey. Read the abstract and introduction from the authors' TU Delft technical-report version of the published paper.

## Limitations and open questions

Predates deep MARL entirely (2008).

## Relevance to us

Background reference for game-theoretic vocabulary (Markov games, Nash-Q, joint-action learners) needed to read [[yang-2018-mean]] and [[littman-1994-markov]].

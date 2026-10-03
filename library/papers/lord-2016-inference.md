---
id: lord-2016-inference
type: paper
title: 'Inference of Causal Information Flow in Collective Animal Behavior'
authors: ['Warren M. Lord', 'Jie Sun', 'Nicholas T. Ouellette', 'Erik M. Bollt']
year: 2016
venue: 'IEEE Transactions on Molecular, Biological and Multi-Scale Communications'
url: https://arxiv.org/abs/1606.01932
doi: 10.1109/tmbmc.2016.2632099
arxiv: '1606.01932'
cite: 'Lord, W. M., Sun, J., Ouellette, N. T., & Bollt, E. M. (2016). Inference of Causal Information Flow in Collective Animal Behavior. IEEE Transactions on Molecular, Biological and Multi-Scale Communications, 2(1), 107–116.'
topics: [criticality-measurement, collective-motion, swarm-detection]
added_by: dmarz/criticality-measurement
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: '52 (OpenAlex, 2026-10-03)'
code: []
---

## Summary

Applies optimal causation entropy (oCSE), a conditional-mutual-information network inference method,
to 3D trajectories of laboratory midge swarms (Chironomus riparius) to identify direct information channels
among insects. The inferred networks contain long-range channels more often than expected if causal influence
were spatially local.

## Contribution

Network-level causal-flow inference in a real 3D swarm, going beyond pairwise transfer entropy by
conditioning on other agents.

## Key results

- oCSE identifies direct information channels in midge swarms (measured).
- Long spatial-range channels are more common than expected under spatial locality (measured).

## Methods and models

Optical 3D tracking of midges; oCSE greedy forward selection and backward elimination with
permutation tests over sliding time windows. arXiv 1606.01932.

## Limitations and open questions

Causation entropy is still observational; windowed averages hide local dynamics (noted by
[[crosato-2018-informative]]). Abstract-level read.

## Relevance to us

Template for inferring interaction networks in swarms with many agents; compare
[[sinhuber-2017-phase]] (same lab) and [[attanasi-2014-collective]].

## Notes from dmarz/sd-coordination

Read the arXiv abstract this session. Optimal causation entropy (oCSE) infers direct causal information channels among tracked midges from 3-D trajectories, and finds long-range channels more common than expected. This is the information-theoretic route to detecting hidden coupling between agents from trajectories; complements the kernel-regression route of [[lu-2019-nonparametric]] and the point-process route for online accounts of [[sharma-2021-identifying]].

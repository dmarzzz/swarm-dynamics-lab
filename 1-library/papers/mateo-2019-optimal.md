---
id: mateo-2019-optimal
type: paper
title: 'Optimal network topology for responsive collective behavior'
authors: ['David Mateo', 'Nikolaj Horsevad', 'Vahid Hassani', 'Mohammadreza Chamanbaz', 'Roland Bouffanais']
year: 2019
venue: 'Science Advances'
url: https://arxiv.org/abs/1807.04631
doi: 10.1126/sciadv.aau0999
arxiv: null
cite: 'Mateo, D., Horsevad, N., Hassani, V., Chamanbaz, M., & Bouffanais, R. (2019). Optimal network topology for responsive collective behavior. Science Advances, 5(4), eaau0999.'
topics: [criticality-measurement, swarm-robotics, sync-consensus]
added_by: dmarz/criticality-measurement
accessed: 2026-10-03
read_depth: abstract
relevance: 5
citations: '63 (OpenAlex, 2026-10-03)'
code: []
---

## Summary

Studies leader-follower linear consensus in which a leader follows a dynamic driving signal, varying
interaction topology and size. Collective response is optimal when each agent interacts with a certain number
of others, which decreases with signal frequency and becomes independent of system size for large systems.
Experiments with a swarm of land robots confirm the dependence for slow and fast leaders.

## Contribution

Experimental (robot) and theoretical evidence that optimal interaction-network degree depends on
the timescale of the environmental signal, implying dynamic rewiring is needed for responsive swarms.

## Key results

- Optimal number of neighbours decreases monotonically with driving frequency (analysis).
- Optimal degree is size-independent for large systems.
- Confirmed with land-robot swarm experiments for slow and fast leaders.

## Methods and models

Leader-follower linear consensus on k-nearest-neighbour networks; frequency response analysis;
land-robot swarm experiments. arXiv preprint 1807.04631 under the title "Optimal Network Topology for Effective
Collective Response".

## Limitations and open questions

Linear consensus model; abstract-level read.

## Relevance to us

Actionable design rule for robot swarms and a frequency-response measure of responsiveness. See
[[mateo-2017-effect]], [[lei-2023-exploring]].

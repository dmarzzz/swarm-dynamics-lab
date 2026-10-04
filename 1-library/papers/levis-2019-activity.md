---
id: levis-2019-activity
type: paper
title: "Activity induced synchronization: Mutual flocking and chiral self-sorting"
authors: [D. Levis, I. Pagonabarraga, B. Liebchen]
year: 2019
venue: Physical Review Research
url: https://journals.aps.org/prresearch/abstract/10.1103/PhysRevResearch.1.023026
doi: 10.1103/physrevresearch.1.023026
arxiv: null
cite: "Levis, D., Pagonabarraga, I., & Liebchen, B. (2019). Activity induced synchronization: Mutual flocking and chiral self-sorting. Physical Review Research, 1(2), 023026."
topics: [sync-consensus, active-matter, collective-motion]
added_by: dmarz/sync-consensus
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "115 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Treats chiral self-propelled particles (circle swimmers with distributed intrinsic rotation frequencies) as
mobile oscillators whose phase is their heading. Self-propulsion lets them synchronise over very large distances
even with local coupling in 2D, unlike passive oscillators. Two new phases appear: "mutual flocking", where
particles of opposite chirality form overlapping flocks moving at different angles, and "chiral self-sorting",
where particles segregate by handedness into large counter-rotating clusters.

## Contribution

Shows that motion itself changes the synchronisation transition (activity-induced sync), complementing the
swarmalator approach of [[okeeffe-2017-oscillators]] where phase is an internal variable rather than the heading.
Extends Liebchen and Levis's 2017 chiral active-matter work.

## Key results

- Abstract-level (APS page): long-range sync with local coupling in 2D; mutual flocking phase; chiral
  self-sorting into counter-rotating clusters; mechanism is the two-way coupling between phase and propulsion.

## Methods and models

Vicsek/Kuramoto-type model of chiral active Brownian particles with frequency disorder; simulations and
continuum theory (not read in detail).

## Limitations and open questions

Full text not read; parameter ranges and finite-size checks unknown to us.

## Relevance to us

Relevant whenever robots or drones have a preferred turning direction (chirality, as in
[[ceron-2023-diverse]]): mixing chiralities may sort or flock in non-obvious ways.

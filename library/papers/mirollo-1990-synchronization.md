---
id: mirollo-1990-synchronization
type: paper
title: Synchronization of Pulse-Coupled Biological Oscillators
authors: [Renato E. Mirollo, Steven H. Strogatz]
year: 1990
venue: SIAM Journal on Applied Mathematics
url: https://api.openalex.org/works/doi:10.1137/0150098
doi: 10.1137/0150098
arxiv: null
cite: "Mirollo, R. E., & Strogatz, S. H. (1990). Synchronization of pulse-coupled biological oscillators. SIAM Journal on Applied Mathematics, 50(6), 1645-1662."
topics: [sync-consensus, swarm-robotics]
added_by: dmarz/sync-consensus
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "2118 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Analyses a population of identical integrate-and-fire oscillators, based on Peskin's cardiac pacemaker model, with
pulsatile all-to-all coupling: when one oscillator fires it kicks every other up by a fixed amount or to
threshold, whichever is less. The main theorem: for almost all initial conditions the population evolves to a
state where all oscillators fire in unison. The paper discusses fireflies, chirping crickets, pacemaker cells and
menstrual synchrony as motivating examples.

## Contribution

The founding result for pulse-coupled ("firefly") synchronisation, the model class behind most engineered
clock-sync protocols in sensor networks and swarm robotics, where agents can only broadcast events, not
continuous phases.

## Key results

- Abstract-level: for almost all initial conditions, identical all-to-all pulse-coupled integrate-and-fire
  oscillators end up firing synchronously. Conditions on the charging curve were not re-read here.

## Methods and models

Return-map (firing map) analysis of absorptions, where oscillators that fire together stay together. Abstract
read from the OpenAlex record (SIAM page blocked).

## Limitations and open questions

Identical oscillators, all-to-all coupling, no transmission delays; robustness to delays, sparse graphs and
heterogeneity is outside this paper and is the main question for hardware use.

## Relevance to us

The algorithm a drone swarm actually runs when it syncs LED flashes by observing neighbours' flashes;
[[quinn-2025-decentralised]] starts from this model. Pair with [[trianni-2009-self]].

---
id: anwar-2024-collective
type: paper
title: Collective dynamics of swarmalators with higher-order interactions
authors: [Md Sayeed Anwar, Gourab Kumar Sar, Matjaž Perc, Dibakar Ghosh]
year: 2024
venue: Communications Physics
url: https://arxiv.org/abs/2309.03343
doi: 10.1038/s42005-024-01556-2
arxiv: '2309.03343'
cite: "Anwar, M. S., Sar, G. K., Perc, M., & Ghosh, D. (2024). Collective dynamics of swarmalators with higher-order interactions. Communications Physics, 7(1), 59."
topics: [sync-consensus, active-matter]
added_by: dmarz/sync-consensus
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "85 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Adds three-body (simplicial, higher-order) interactions to an analytically tractable 1D swarmalator model and
tracks the four states (async, phase wave, mixed, sync) of [[yoon-2022-sync]]. Even a small fraction of
higher-order coupling makes the async-to-phase-wave and async-to-sync transitions abrupt (first order, with
hysteresis implied), lets the system jump from phase wave directly to sync without the mixed state, and keeps
phase wave and sync alive even when pairwise interactions are repulsive.

## Contribution

Brings the "higher-order interactions cause explosive synchronisation" result from static oscillator networks
(simplicial Kuramoto, see [[ghosh-2022-synchronized]]) to mobile oscillators; the most cited swarmalator paper of
2024.

## Key results

- Abstract-level: minute fractions of higher-order coupling produce abrupt transitions; phase wave to sync can
  bypass the mixed state; higher-order coupling sustains order under repulsive pairwise coupling.

## Methods and models

1D ring swarmalator model with pairwise plus triadic terms; Ott-Antonsen-style reduction and simulation
(from the abstract; full text not read).

## Limitations and open questions

1D ring, all-to-all; whether real swarms have meaningful three-body sync interactions is not established.

## Relevance to us

If a hackathon experiment sees abrupt, hysteretic transitions in a sync-plus-motion swarm, this is the
mechanism to compare against. Related: [[okeeffe-2022-collective]], [[sar-2026-interplay]].

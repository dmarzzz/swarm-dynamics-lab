---
id: fujiwara-2011-synchronization
type: paper
title: Synchronization in networks of mobile oscillators
authors: [Naoya Fujiwara, Jürgen Kurths, Albert Díaz-Guilera]
year: 2011
venue: Physical Review E
url: https://journals.aps.org/pre/abstract/10.1103/PhysRevE.83.025101
doi: 10.1103/physreve.83.025101
arxiv: null
cite: "Fujiwara, N., Kurths, J., & Díaz-Guilera, A. (2011). Synchronization in networks of mobile oscillators. Physical Review E, 83(2), 025101(R)."
topics: [sync-consensus, collective-motion]
added_by: dmarz/sync-consensus
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "181 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Models synchronisation among autonomous agents that move in space, so the interaction network changes as they
move. Two timescales compete: the rate of topological change from motion and the rate of local synchronisation.
When motion is much faster, an approximation that averages out motion (an effectively static, averaged network)
works; in the opposite regime the time to synchronise is longer than that approximation predicts, especially near
the continuum percolation transition of the agents' proximity graph. Simulations are confirmed by spectral
analysis of the time-dependent Laplacian.

## Contribution

A key one-way-coupled predecessor of swarmalators (motion changes the network, phases do not change motion),
cited by [[okeeffe-2017-oscillators]]; it states the timescale-separation principle (motion versus local
synchronisation) clearly for mobile networks.

## Key results

- Abstract: fast-motion limit is well approximated by averaging; slow motion gives longer-than-predicted sync
  times, worst near the percolation threshold; design trade-off between mobility and coupling timescales.

## Methods and models

Mobile agents whose links depend on their positions (continuum percolation of the proximity graph), local
synchronisation dynamics, spectral analysis of the time-dependent Laplacian. From the APS abstract page; the
motion model and oscillator type were not read.

## Limitations and open questions

Motion is independent of phase (no feedback); specific motion model and oscillator type not checked.

## Relevance to us

Directly predicts how a drone swarm's speed relative to its sync coupling affects time to synchronise when radio
range is limited, a cheap hackathon experiment. Compare with consensus under switching graphs
([[jadbabaie-2003-coordination]]) and with two-way coupled swarmalators ([[yoon-2022-sync]]).

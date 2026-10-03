---
id: dorfler-2013-synchronization
type: paper
title: Synchronization in complex oscillator networks and smart grids
authors: [Florian Dörfler, Michael Chertkov, Francesco Bullo]
year: 2013
venue: Proceedings of the National Academy of Sciences
url: https://arxiv.org/abs/1208.0045
doi: 10.1073/pnas.1212134110
arxiv: '1208.0045'
cite: "Dörfler, F., Chertkov, M., & Bullo, F. (2013). Synchronization in complex oscillator networks and smart grids. Proceedings of the National Academy of Sciences, 110(6), 2005-2010."
topics: [sync-consensus]
added_by: dmarz/sync-consensus
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "899 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Gives a concise, closed-form condition for synchronisation of a network of heterogeneous phase oscillators with
an arbitrary interaction graph and sinusoidal diffusive coupling. The condition can be stated in terms of the
network topology and parameters, or equivalently through a linear, static auxiliary (DC power-flow-like) system.
It is provably exact for several network classes, statistically correct for almost all random networks tested,
and is demonstrated on power grid models.

## Contribution

Replaced loose sufficient conditions for network synchronisation with a near-exact, interpretable one; widely
used in power-systems stability and summarised in [[dorfler-2014-synchronization]].

## Key results

- Abstract-level: closed-form sync condition, exact for some topologies and "statistically correct for almost
  all networks" in their tests; the exact form of the condition was not read in this session.

## Methods and models

Kuramoto-type oscillators on weighted graphs with an auxiliary linear static system; validation on complex
network scenarios and smart-grid applications (per the abstract). Abstract read on arXiv.

## Limitations and open questions

Static networks; first-order phase model.

## Relevance to us

A quick check of whether a given communication graph and spread of natural frequencies can synchronise at all,
useful for sizing coupling gains in a robot or drone sync demo.

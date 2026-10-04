---
id: ha-2022-collective
type: paper
title: 'Collective intelligence for deep learning: A survey of recent developments'
authors: [David Ha, Yujin Tang]
year: 2022
venue: Collective Intelligence
url: https://arxiv.org/abs/2111.14377
doi: 10.1177/26339137221114874
arxiv: '2111.14377'
cite: 'Ha, D., & Tang, Y. (2022). Collective intelligence for deep learning: A survey of recent developments. Collective Intelligence, 1(1), 26339137221114874.'
topics: [marl-emergence, swarm-intelligence]
added_by: dmarz/marl-emergence-audit
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: "55 (Crossref is-referenced-by-count, 2026-10-03)"
code: []
---

## Summary

A perspective-style review arguing that ideas from complex systems (self-organisation, emergence, cellular
automata, swarm models) address deep learning's brittleness. After a history linking cellular neural networks,
Brownian agents and swarm optimisation to modern neural nets, it surveys four areas: image processing with neural
cellular automata, deep RL with modular and morphology-agnostic agents, multi-agent learning at scale, and
meta-learning with networks of identical units.

## Contribution

The most-cited bridge review written from the deep-learning side toward collective intelligence. It frames
large-population MARL (for example [[zheng-2018-magent]]) as studying macro-level emergent properties with 1000+
agents, rather than micro-level coordination of two to four agents.

## Key results

- Review; no new measurements. Its main claim is qualitative: systems built from many identical, locally
  communicating units (neural CA, self-organising agents, permutation-invariant policies) are more robust and
  adaptable than monolithic networks.
- Points to large-population environments such as MAgent and Neural MMO as the place where emergent collective
  phenomena in MARL can be studied.

## Methods and models

Narrative review with figures from the reviewed work. Covers neural cellular automata (Mordvintsev et al.),
self-organising and modular soft-robot and locomotion agents, permutation-invariant "sensory neuron" policies,
large-scale MARL platforms, and meta-learning with shared local rules.

## Limitations and open questions

Selective, written by authors whose own work is featured; little quantitative comparison and no systematic search.
Physics-side collective-behaviour work (order parameters, criticality) is barely touched.

## Relevance to us

Good orientation for the deep-learning reading of "swarm": local rules, shared weights and permutation invariance.
Pair with the physics-side review [[cichos-2020-machine]] and the mean-embedding swarm policy of
[[huttenrauch-2019-deep]].

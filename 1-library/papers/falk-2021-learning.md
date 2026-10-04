---
id: falk-2021-learning
type: paper
title: Learning to control active matter
authors:
- Martin J. Falk
- Vahid Alizadehyazdi
- Heinrich Jaeger
- Arvind Murugan
year: 2021
venue: Physical Review Research
url: https://arxiv.org/abs/2105.04641
doi: 10.1103/PhysRevResearch.3.033291
arxiv: '2105.04641'
cite: Falk, M. J., Alizadehyazdi, V., Jaeger, H., & Murugan, A. (2021). Learning to control active matter. Physical Review Research, 3(3), 033291.
topics:
- marl-emergence
- active-matter
added_by: dmarz/marl-emergence
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 50 (Crossref, 2026-10-03)
code: []
---

## Summary

Instead of learning individual agent policies, a single RL controller learns where to shine a "spotlight" that locally increases activity in a simulated system of Vicsek-like self-propelled disks, with the goal of net transport in a chosen direction. The learned time-varying activity patterns exploit different physics in the strong- and weak-coupling regimes and are physically interpretable.

## Contribution

A clean example of the complementary "external controller of a collective" framing (as opposed to decentralised MARL), relevant to programmable active matter and swarm steering. Sits alongside the review [[cai-2025-reinforcement]] and [[cichos-2020-machine]].

## Key results

- Learned protocols induce directed transport; strategies differ between strong and weak alignment coupling (claimed in abstract; numbers not read).

## Methods and models

Simulated self-propelled disks with Vicsek-like alignment; RL agent chooses a spatio-temporal activity field (spotlight). Abstract-level read.

## Limitations and open questions

Centralised controller with global observation; single task (transport). Not a model of how individuals learn.

## Relevance to us

Shows how to pose "control the swarm" as RL over a field rather than over agents, useful if a hackathon team wants to steer a simulated Vicsek system. Related: [[vicsek-1995-novel]], [[cai-2025-reinforcement]].

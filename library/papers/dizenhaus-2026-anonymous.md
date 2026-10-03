---
id: dizenhaus-2026-anonymous
type: paper
title: "Anonymous leadership and stochastic resonance in collectives of self-propelled robots"
authors: ["M. Dizenhaus", "F. De Simone", "G. A. Patterson"]
year: 2026
venue: "Physical Review E"
url: https://arxiv.org/abs/2510.12580
doi: "10.1103/rntx-zg23"
arxiv: "2510.12580"
cite: "Dizenhaus, M., De Simone, F., & Patterson, G. A. (2026). Anonymous leadership and stochastic resonance in collectives of self-propelled robots. Physical Review E, 113(3), 035417."
topics: [swarm-robotics, collective-decision, active-matter, criticality-measurement]
added_by: dmarz/swarm-robotics-recent
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "0 (Crossref, 2026-10-03). OpenAlex daily budget exhausted on this IP during the session."
code: []
---

## Summary

In Kilobot experiments and simulations, a single anonymous leader alternates deterministically between clockwise and counter-clockwise motion while the other robots follow a stochastic majority rule. The leader does not change global order, but the correlation between leader and collective response peaks at an intermediate perturbation (noise) level, a stochastic-resonance signature. Simulations show the resonance occurs when the leader's reversal period matches the mean residence time of the unperturbed collective.

## Contribution

It connects minimal leadership in robot swarms with stochastic resonance and collective decision-making in active matter, and suggests a timing principle for steering swarms with one agent.

## Key results

- The leader-collective correlation peaks at intermediate perturbation levels (measured in Kilobots and simulations, per the abstract).
- The resonance condition is that the leader's period matches the mean residence time of the unperturbed system (from simulations).

## Methods and models

Kilobot collective with a stochastic majority-rule rotation-direction update, one deterministic leader, and matching numerical simulations.

## Limitations and open questions

Abstract-depth entry. A small Kilobot collective with a binary (CW/CCW) state, so its generality to continuous flocking is untested.

## Relevance to us

A cheap, testable hackathon experiment: periodic forcing of a swarm at its intrinsic switching timescale. Links to [[choi-2026-communication]] (implicit leaders) and [[verdoucq-2025-flocking]] (responsiveness near transitions).

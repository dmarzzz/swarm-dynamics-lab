---
id: strogatz-2024-how
type: talk
title: "How Is Flocking Like Computing?"
authors: [Steven Strogatz, Iain Couzin]
year: 2024
url: https://www.quantamagazine.org/how-is-flocking-like-computing-20240328/
venue: "The Joy of Why podcast, Quanta Magazine, 28 March 2024 (full transcript on the page)"
topics: [collective-motion, collective-decision, criticality-measurement]
added_by: shadow/sol-w3
accessed: 2026-10-03
read_depth: full
relevance: 3
---

## Summary

Podcast episode in which Steven Strogatz interviews Iain Couzin (MPI Animal Behavior, Konstanz); the full transcript was read on the page, so there are no audio timestamps. Main points in order. (1) Placozoa behave as a flock of cells, aligning through physical forces, analysed with the same models as bird flocks (Couzin's 2023 PNAS study). (2) Couzin's central framing: what unites cell, insect and bird collectives is computation; groups compute about the environment in ways individuals cannot. (3) Waves of turning in fish schools and starling flocks attacked by predators propagate about 10 times faster than the predator's maximum speed, so individuals respond to threats they never see. (4) Groups appear tuned near a critical point: strongly aligned schools are hard to turn, disordered ones do not propagate signals, and the intermediate regime balances robustness and sensitivity. (5) In fish exposed to the alarm substance schreckstoff, individuals did not change their response rules; they repositioned so that the interaction network changed, pushing the group toward the critical regime. Visual fields are reconstructed with raycasting to infer who actually influences whom. (6) Desert-locust marching bands are driven by cannibalism (follow those moving away, avoid those approaching), not information transfer, a warning that similar-looking patterns can have different causes; his lab tracked 10,000 locusts in a 15 x 15 x 8 m arena. (7) Current work: virtual-reality experiments suggesting brains represent space non-Euclideanly, reducing multi-option spatial decisions to a series of bifurcations.

## Relevance to us

Two points carry over directly to agent swarms. First, the claim that collectives adjust network structure rather than individual rules to change sensitivity suggests measuring an LLM swarm's interaction graph, not just per-agent behaviour, when probing how it responds to shocks. Second, the locust example is a ready-made caution for swarm detection: coordinated-looking output can arise from very different mechanisms. Primary sources: [[couzin-2002-collective]], [[couzin-2005-effective]], [[couzin-2009-collective]], [[couzin-2025-collective]]; criticality context [[munoz-2018-colloquium]], [[cavagna-2010-scale]]; locust disorder-order transition [[buhl-2006-disorder]]. Statements here are the guest's account of his own work, not independently checked.

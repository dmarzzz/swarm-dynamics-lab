---
id: okeeffe-2022-collective
type: paper
title: Collective behavior of swarmalators on a ring
authors: [Kevin O'Keeffe, Steven Ceron, Kirstin Petersen]
year: 2022
venue: Physical Review E
url: https://journals.aps.org/pre/abstract/10.1103/PhysRevE.105.014211
doi: 10.1103/physreve.105.014211
arxiv: null
cite: "O'Keeffe, K., Ceron, S., & Petersen, K. (2022). Collective behavior of swarmalators on a ring. Physical Review E, 105(1), 014211."
topics: [sync-consensus, active-matter]
added_by: dmarz/sync-consensus
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "78 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Introduces the 1D ring swarmalator model: identical agents with a position x on a circle and a phase theta, with
spatial dynamics J sin(x_j - x_i) cos(theta_j - theta_i) and phase dynamics K sin(theta_j - theta_i) cos(x_j - x_i). The
authors argue this captures the essence of 2D and 3D swarmalator motion while being solvable: most collective
states (async, phase wave, sync and others) and their bifurcations can be specified exactly. They note real
swarmalators that move on quasi-1D rings, such as bordertaxic vinegar eels and sperm.

## Contribution

The solvable toy model behind most analytic swarmalator results since 2022; [[yoon-2022-sync]] extends it to
non-identical agents and [[okeeffe-2025-global]] proves global stability of its sync state. As described in
[[okeeffe-2025-global]], it can be viewed as the rotational part of the 2D model of
[[okeeffe-2017-oscillators]].

## Key results

- Abstract-level: exact characterisation of most states and bifurcations for identical swarmalators on a ring.
  [[yoon-2022-sync]] reports that its identical-unit limit (phase-wave onset at J + K = 0, sync for J, K > 0)
  agrees with this paper; not checked against this paper's text.

## Methods and models

Linear stability of fixed points in sum/difference coordinates; simulations. Full text not read (APS page
abstract only).

## Limitations and open questions

Identical units and all-to-all coupling; ring geometry.

## Relevance to us

The cheapest analytically understood sync-plus-motion model; a good unit test for simulation code and for
learning-based controllers that should rediscover known states.

---
id: sepulchre-2007-stabilization
type: paper
title: "Stabilization of Planar Collective Motion: All-to-All Communication"
authors: [Rodolphe Sepulchre, Derek A. Paley, Naomi Ehrich Leonard]
year: 2007
venue: IEEE Transactions on Automatic Control
url: https://api.openalex.org/works/doi:10.1109/tac.2007.898077
doi: 10.1109/tac.2007.898077
arxiv: null
cite: "Sepulchre, R., Paley, D. A., & Leonard, N. E. (2007). Stabilization of planar collective motion: All-to-all communication. IEEE Transactions on Automatic Control, 52(5), 811-824."
topics: [sync-consensus, collective-motion, swarm-robotics]
added_by: dmarz/sync-consensus
accessed: 2026-10-03
read_depth: abstract
relevance: 5
citations: "521 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Designs feedback laws for identical unit-speed particles in the plane, coupled all-to-all, that stabilise
isolated relative equilibria: either parallel motion with fixed relative spacing or circular motion about a
common centre with fixed relative phases. Headings are treated as phase oscillators, so the steering laws are
Kuramoto-type couplings derived from Lyapunov functions that prove exponential stability and suggest almost
global convergence. The result is a low-order parametric family of stabilisable collective motions that serve
as primitives for higher-level group tasks.

## Contribution

Made the identification "heading = oscillator phase" a design method: synchronised phases give parallel
(flocking) motion, balanced phases give circular (milling) motion. A companion paper (Sepulchre, Paley and
Leonard 2008, "Stabilization of planar collective motion with limited communication", IEEE TAC, found in the
Crossref search) treats limited communication.

## Key results

- Abstract-level: stabilising feedbacks for parallel and circular relative equilibria with exponential
  stability proofs and almost-global convergence suggestions. The planar particle model and the K > 0 (sync,
  parallel) versus K < 0 (balanced, circular) behaviour are illustrated in [[dorfler-2014-synchronization]],
  Section 2.1.

## Methods and models

Unit-speed planar particle model (kinematics attributed to Justh and Krishnaprasad 2004 in
[[dorfler-2014-synchronization]]), phase-potential Lyapunov functions, spacing
potentials. Abstract from the OpenAlex record (IEEE page blocked).

## Limitations and open questions

All-to-all communication, identical unit-speed particles, no obstacles.

## Relevance to us

Directly usable controllers for drone or robot "flock in a line" and "orbit a point" behaviours, with proofs.
Connects Kuramoto ([[acebron-2005-kuramoto]]) with flocking control ([[olfati-saber-2006-flocking]]) and is the
heading-only cousin of the swarmalator model ([[okeeffe-2017-oscillators]]).

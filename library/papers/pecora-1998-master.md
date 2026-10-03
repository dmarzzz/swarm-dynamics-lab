---
id: pecora-1998-master
type: paper
title: Master Stability Functions for Synchronized Coupled Systems
authors: [Louis M. Pecora, Thomas L. Carroll]
year: 1998
venue: Physical Review Letters
url: https://doi.org/10.1103/physrevlett.80.2109
doi: 10.1103/physrevlett.80.2109
arxiv: null
cite: "Pecora, L. M., & Carroll, T. L. (1998). Master stability functions for synchronized coupled systems. Physical Review Letters, 80(10), 2109-2112."
topics: [sync-consensus]
added_by: dmarz/sync-consensus-audit
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "2662 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Shows that for identical oscillators coupled linearly through a network, the stability of the fully
synchronised state can be decided by a single "master stability function" of one complex parameter, evaluated
at the eigenvalues of the coupling matrix. This separates the oscillator dynamics from the network structure:
compute the function once for a given oscillator and coupling, then any network's sync stability follows from
its spectrum.

## Contribution

The founding paper of the master stability function (MSF) approach, the standard tool for complete
synchronisation of identical (possibly chaotic) units on arbitrary graphs. It complements the
phase-oscillator Kuramoto line ([[strogatz-2000-kuramoto]], [[acebron-2005-kuramoto]]) and the consensus
Laplacian line ([[olfati-saber-2004-consensus]]); reviews [[arenas-2008-synchronization]] and
[[boccaletti-2023-structure]] (higher-order extensions) build on it.

## Key results

- Abstract-level: many coupled-oscillator array configurations can be cast in one form, so synchronous stability
  reduces to a master stability function tailored to the chosen stability criterion; the authors claim this
  solves synchronous stability for any linear coupling of a given oscillator. Specific examples and numbers not
  read.

## Methods and models

Variational equations about the synchronisation manifold, block-diagonalised by the eigenvectors of the coupling
matrix; maximal Lyapunov exponent as a function of the (complex) scaled eigenvalue. Only the abstract was read
(OpenAlex record; APS full text not accessible).

## Limitations and open questions

- Identical units and linear, diffusive-type coupling; local (linear) stability only.
- Static networks; time-varying and mobile-agent networks need extensions ([[ghosh-2022-synchronized]]).

## Relevance to us

Background tool: if a hackathon swarm synchronises identical nonlinear units (oscillating LEDs, motor gaits)
over a fixed communication graph, the MSF tells which graphs can sync at all. Less useful for heterogeneous or
moving agents, where Kuramoto and swarmalator models ([[okeeffe-2017-oscillators]]) fit better.

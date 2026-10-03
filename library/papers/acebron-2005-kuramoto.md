---
id: acebron-2005-kuramoto
type: paper
title: "The Kuramoto model: A simple paradigm for synchronization phenomena"
authors: [Juan A. Acebrón, L. L. Bonilla, Conrad J. Pérez Vicente, Félix Ritort, Renato Spigler]
year: 2005
venue: Reviews of Modern Physics
url: https://journals.aps.org/rmp/abstract/10.1103/RevModPhys.77.137
doi: 10.1103/revmodphys.77.137
arxiv: null
cite: "Acebrón, J. A., Bonilla, L. L., Pérez Vicente, C. J., Ritort, F., & Spigler, R. (2005). The Kuramoto model: A simple paradigm for synchronization phenomena. Reviews of Modern Physics, 77(1), 137-185."
topics: [sync-consensus, criticality-measurement]
added_by: dmarz/sync-consensus
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "3592 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

The standard physics review of the Kuramoto model, dtheta_i/dt = omega_i + (K/N) sum_j sin(theta_j - theta_i): a
population of phase oscillators with distributed natural frequencies that spontaneously synchronise above a
critical coupling. It gives a rigorous mathematical treatment (mean-field theory, stability of incoherence,
finite-size effects), specific numerical methods, and many variants and extensions (noise, frequency-weighted
coupling, time delays, networks) with applications across physics, biology and engineering.

## Contribution

The go-to reference for the Kuramoto transition and its order parameter r exp(i psi) = (1/N) sum_j exp(i theta_j);
complements the historical and bifurcation-focused [[strogatz-2000-kuramoto]] and the network-focused
[[arenas-2008-synchronization]] and [[rodrigues-2016-kuramoto]].

## Key results

- Abstract-level only. The textbook results usually cited from it (critical coupling K_c = 2/(pi g(0)) for a
  symmetric unimodal frequency density g, square-root growth of r above K_c) were not verified against this
  review's text in this session.

## Methods and models

Review: kinetic (continuum) description, linear stability, Fokker-Planck treatment of noise, numerical methods.
Read the APS abstract page only.

## Limitations and open questions

Pre-dates the Ott-Antonsen reduction ([[ott-2008-low]]) and much of the network and mobile-oscillator work.

## Relevance to us

The order parameter r and the K_c formula are the default measurement and baseline for any synchronisation
experiment in the hackathon (drones flashing LEDs in sync, robots sharing a clock).

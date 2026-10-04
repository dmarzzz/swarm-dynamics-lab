---
id: dorfler-2014-synchronization
type: paper
title: "Synchronization in complex networks of phase oscillators: A survey"
authors: [Florian Dörfler, Francesco Bullo]
year: 2014
venue: Automatica
url: https://motion.me.ucsb.edu/pdf/2013b-db.pdf
doi: 10.1016/j.automatica.2014.04.012
arxiv: null
cite: "Dörfler, F., & Bullo, F. (2014). Synchronization in complex networks of phase oscillators: A survey. Automatica, 50(6), 1539-1564."
topics: [sync-consensus, collective-motion]
added_by: dmarz/sync-consensus
accessed: 2026-10-03
read_depth: skim
relevance: 5
citations: "1176 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

A control-theoretic survey of networks of coupled phase oscillators, dtheta_i/dt = omega_i - sum_j a_ij sin(theta_i - theta_j),
the Kuramoto model generalised to weighted sparse graphs. It explains why this is a locally canonical model of
weakly coupled limit-cycle oscillators, reviews applications that matter to control engineers (flocking and
vehicle coordination, electric power networks, clock synchronisation), defines synchronisation notions (phase,
frequency, phase balancing, patterns, partial sync) and collects the sharpest known necessary and sufficient
conditions on the critical coupling for identical and heterogeneous oscillators on complete and sparse graphs.

## Contribution

The bridge between the physics Kuramoto literature ([[strogatz-2000-kuramoto]], [[acebron-2005-kuramoto]],
[[arenas-2008-synchronization]]) and the multi-agent consensus literature
([[olfati-saber-2007-consensus]], [[ren-2007-information]]): consensus is the linearised, identical-oscillator
special case, and the Kuramoto steering law is the heading-consensus controller of [[sepulchre-2007-stabilization]].

## Key results

- Section 2.1 (read): unit-speed planar particles with steering control dtheta_i/dt = omega_0(t) - K sum_j a_ij(t) sin(theta_i - theta_j)
  give synchronised headings (parallel motion, K > 0) or balanced headings (K < 0); with omega_0 = 1 the motion is
  circular (Fig. 2, n = 6). This is the Kuramoto model on a time-varying graph.
- Section 4.3 (read): for identical oscillators the model is a gradient flow of a potential U(theta); by LaSalle all
  trajectories converge to critical points, phase sync is exponentially stable, and for "S1-synchronising" graphs
  all other equilibria are unstable (results attributed to Jadbabaie et al. 2004, Sepulchre et al. 2007 and others).
- Sections 6-7 (skimmed): explicit and implicit bounds on K_critical for the classic all-to-all Kuramoto model;
  two sufficient conditions for sparse heterogeneous networks, one with a region-of-attraction estimate and one
  sharper without; plus a sharp condition for some network classes (see [[dorfler-2013-synchronization]]).

## Methods and models

Survey; Lyapunov and potential-function methods, contraction, incremental boundedness, graph theory (Laplacian
pseudo-inverse, effective resistance). Read from the authors' preprint (23 March 2014) hosted at UCSB: abstract,
introduction, Section 2.1 and Section 4.3 read, the rest skimmed.

## Limitations and open questions

Focuses on synchronisation rather than richer dynamics (chimeras, chaos); time-varying and mobile-agent graphs
get limited treatment, which later reviews ([[ghosh-2022-synchronized]]) cover.

## Relevance to us

The best single reference for turning Kuramoto results into swarm heading controllers with guarantees, and for
graph-dependent sync conditions when communication is sparse. Use with [[sepulchre-2007-stabilization]] for
vehicles and with [[okeeffe-2025-global]] for the mobile-oscillator analogue of the gradient argument.

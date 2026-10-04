---
id: sepulchre-2008-stabilization
type: paper
title: Stabilization of Planar Collective Motion With Limited Communication
authors: [Rodolphe Sepulchre, Derek A. Paley, Naomi Ehrich Leonard]
year: 2008
venue: IEEE Transactions on Automatic Control
url: https://naomi.princeton.edu/wp-content/uploads/sites/744/2021/03/seppalleo08.pdf
doi: 10.1109/tac.2008.919857
arxiv: null
cite: "Sepulchre, R., Paley, D. A., & Leonard, N. E. (2008). Stabilization of planar collective motion with limited communication. IEEE Transactions on Automatic Control, 53(3), 706-719."
topics: [sync-consensus, collective-motion, swarm-robotics]
added_by: dmarz/sync-consensus-audit
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "462 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Companion to [[sepulchre-2007-stabilization]] (all-to-all case). Constant-speed, steered particles in the plane
(r_k' = exp(i theta_k), theta_k' = u_k) are driven to parallel motion, common-circle motion, or symmetric
"splay" patterns on a circle, but now each particle only uses information from neighbours in a communication
graph that may be directed and time-varying. Two routes are given: Laplacian-based potentials for fixed,
connected, undirected (or balanced) graphs, and consensus-style dynamic estimators (each agent keeps a local
estimate of a group average) for uniformly connected time-varying digraphs.

## Contribution

Joins the oscillator-based collective-motion controllers (heading = phase, Kuramoto order parameter = mean
velocity) with the consensus results of [[jadbabaie-2003-coordination]], [[moreau-2005-stability]] and
[[olfati-saber-2004-consensus]]. It is the reference result for steering-control formation design under
realistic communication, motivated by underwater glider fleets ([[leonard-2007-collective]]).

## Key results

- Theorem 1 (from the all-to-all paper): the potential U_m = (N/2)|p_m theta|^2, with p_m theta = (1/(mN)) sum_k
  exp(i m theta_k), is maximised by synchronisation modulo 2 pi/m and minimised by balancing; other critical points
  are saddles. For m = 1, |p_theta| is the Kuramoto order parameter and equals the speed of the centre of mass.
- Theorems 2 and 5: Laplacian-weighted versions of the potentials yield gradient controls that stabilise
  synchronised/balanced phases and parallel or circular formations for connected, balanced graphs; for
  d0-circulant graphs the global extrema match the all-to-all case.
- Theorems 3, 4, 6, 8: with a dynamic consensus estimator, synchronisation, balancing, and parallel or circular
  formations are recovered for uniformly connected, possibly directed, time-varying graphs (balancing needs a
  balanced graph and proper estimator initialisation, a stated limitation).
- Theorem 7: symmetric (M, N) circular patterns (including the splay state) stabilised with circulant graphs;
  convergence is local, simulations suggest large basins.
- Simulation (Section VIII, measured in simulation): N = 50 particles in a 50 x 50 periodic domain, zonal sensing
  radius 7, K = -0.1, omega_0 = 0.1: the group converges to one circular formation of radius 1/omega_0; in a larger
  domain it splits into several disconnected circles.

## Methods and models

Lyapunov and gradient design on the shape space of N copies of SE(2), graph Laplacians, circulant-graph
spectra, consensus-estimator dynamics for time-varying digraphs (Scardovi-Sepulchre style). Read: model,
Sections II-III theorem statements, Sections VII-VIII; proofs skipped.

## Limitations and open questions

- Constant speed, identical particles, no noise; collision avoidance is not addressed.
- Results for proximity-based (state-dependent) sensing graphs are simulation only: uniform connectivity is not
  guaranteed and the group can fragment.
- Several stability results are local.

## Relevance to us

Ready-made steering laws for fixed-wing drones or boats that cannot stop, with explicit graph conditions, and the
cleanest statement that "heading is a Kuramoto phase". Directly reusable as a baseline controller for circling
or parallel-flight demos with limited radios, and a bridge between [[okeeffe-2017-oscillators]]-style
sync-plus-motion and [[olfati-saber-2006-flocking]]-style control.

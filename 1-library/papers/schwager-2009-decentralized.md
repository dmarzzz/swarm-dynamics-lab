---
id: schwager-2009-decentralized
type: paper
title: "Decentralized, Adaptive Coverage Control for Networked Robots"
authors: [Mac Schwager, Daniela Rus, Jean-Jacques Slotine]
year: 2009
venue: The International Journal of Robotics Research, vol. 28, no. 3, pp. 357-375
url: https://web.mit.edu/nsl/www/preprints/Adaptive_Coverage08.pdf
doi: 10.1177/0278364908100177
arxiv: null
cite: "Schwager, M., Rus, D., & Slotine, J.-J. (2009). Decentralized, Adaptive Coverage Control for Networked Robots. The International Journal of Robotics Research, 28(3), 357-375. https://doi.org/10.1177/0278364908100177"
topics: [swarm-robotics, sync-consensus, sybil-resistance]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: "391 (Crossref, 2026-10-03)"
code: []
---

## Summary

Presents a decentralized controller that drives n mobile robots to an optimal sensing configuration over a region Q while each robot simultaneously learns, online, where the sensory information is concentrated. The position dynamics follow the locational-optimization (Voronoi centroid) framework of Cortes et al. 2004, but the unknown sensory density phi(q) is replaced by a parametric estimate K(q)^T a_hat_i built from Gaussian basis functions, and each robot adapts its parameter vector a_hat_i from its own sensor readings with an adaptive-control style law. A second version adds a consensus term on the parameters over the Delaunay/Voronoi neighbour graph (weighted by shared Voronoi edge length) so measurements made by any one robot propagate to all. Lyapunov-type proofs show robots converge to the estimated centroids of their Voronoi cells and the estimation error vanishes along sufficiently rich trajectories; with consensus all robots' parameters converge to a common value, and under a persistence-of-excitation condition to the true parameters. Matlab simulations with n = 20 robots over a bimodal Gaussian field (two peaks, amin = 0.1 elsewhere, gains K = 3I, Gamma = I9, gamma = 300) show the consensus variant reaches the true optimal configuration with zero true position error and converges fast enough that the authors plot it on a log time axis, whereas the basic variant only reaches a near-optimal configuration with non-converged parameters. Read: abstract, introduction, related work, problem set-up, Section 7 simulations and conclusion; proofs in Sections 3-6 skimmed.

## Contribution

Combines adaptive parameter estimation with Voronoi coverage control and shows that a consensus term on the learned parameters turns local sensing into network-wide learning with provable convergence, one of the standard references for "learning while covering".

## Key results

- Theorem 1: robots converge to estimated Voronoi centroids; estimation error integral over each robot's visited path goes to zero (proof via a Lyapunov-like function, Barbalat's lemma since the system is time-varying).
- Consensus law makes parameters agree across the network; Corollary 2: with rich trajectories the parameter error converges to zero.
- Simulation (20 robots): consensus controller achieves optimal coverage with true position error to zero and a lower Lyapunov value, basic controller does not (Figures 5-7).

## Methods and models

Integrator robots p_dot_i = u_i, cost H = sum_i integral over V_i of 1/2 ||q - p_i||^2 phi(q) dq, control u_i = K (C_hat_V_i - p_i); basis-function approximator phi_hat_i = K(q)^T a_hat_i with a projection to keep parameters above amin; data-weighted recursive adaptation; consensus via a graph Laplacian with weights proportional to shared Voronoi face length. Numerical simulations only in this paper (hardware follows in later work).

## Limitations and open questions

Simulation only here; simple integrator dynamics; basis functions must span the true density; the consensus analysis assumes the Voronoi neighbour graph stays connected. No adversarial model at all: every robot's measurements and parameters are trusted, which is the gap later Sybil/spoofing work exploits.

## Relevance to us

Catalogued from the backward-citation trail of [[gil-2015-guaranteeing]], which plugs spoof-confidence weights into exactly this class of weighted-Voronoi coverage controller. The parameter-consensus mechanism is also the attack surface: one spoofed sender presenting as many neighbours can bias every robot's shared estimate, so this paper is the honest baseline against which Sybil-resilient coverage is measured. Background for swarm-robotics and sync-consensus; see [[olfati-saber-2007-consensus]] and [[jadbabaie-2003-coordination]] for the consensus theory it leans on.

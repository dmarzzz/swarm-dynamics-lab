---
id: olfati-saber-2007-consensus
type: paper
title: Consensus and Cooperation in Networked Multi-Agent Systems
authors: [Reza Olfati-Saber, J. Alex Fax, Richard M. Murray]
year: 2007
venue: Proceedings of the IEEE
url: https://api.openalex.org/works/doi:10.1109/jproc.2006.887293
doi: 10.1109/jproc.2006.887293
arxiv: null
cite: "Olfati-Saber, R., Fax, J. A., & Murray, R. M. (2007). Consensus and cooperation in networked multi-agent systems. Proceedings of the IEEE, 95(1), 215-233."
topics: [sync-consensus, swarm-robotics, collective-motion]
added_by: dmarz/sync-consensus
accessed: 2026-10-03
read_depth: abstract
relevance: 5
citations: "10541 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

The canonical tutorial-review of consensus algorithms: agents on a (possibly directed, switching, delayed)
communication graph run dx_i/dt = sum_j a_ij (x_j - x_i), i.e. dx/dt = -L x, and agree on a common value. The paper
gives the analysis framework (matrix theory, algebraic graph theory, control theory), convergence and performance
results with emphasis on directed information flow, robustness to link and node failures, and time delays, and
connects consensus to oscillator synchronisation, flocking, formation control, small-world networks, Markov
chains and gossip, load balancing, rendezvous, distributed sensor fusion and belief propagation. Simulations show
small-world shortcuts speed up consensus.

## Contribution

The most cited consensus reference (over 10,000 OpenAlex citations); it unified [[olfati-saber-2004-consensus]],
[[fax-2004-information]], [[jadbabaie-2003-coordination]] and related work into one framework, and it is the
standard citation linking consensus speed to the graph spectrum (algebraic connectivity, lambda_2).

## Key results

- Abstract-level: direct links between spectral and structural network properties and the speed of
  information diffusion under consensus; nonlocal (small-world) information flow is much faster than lattice-like
  nearest-neighbour interaction (simulation results).
- Not re-read: the standard results it reviews (average consensus on balanced digraphs, convergence rate set by
  lambda_2 of the Laplacian, delay margin) are summarised in [[olfati-saber-2004-consensus]]'s abstract.

## Methods and models

Tutorial and review with simulations. Full text could not be retrieved (author preprint link on the Caltech wiki
returns 404, IEEE blocks automated access); abstract from the OpenAlex record. Forward citations (8697 citing works
in OpenCitations, 2026-10-03) were chased for this scan.

## Limitations and open questions

Linear, first-order integrator agents; nonlinear dynamics, adversaries ([[leblanc-2013-resilient]]) and
antagonistic links ([[altafini-2013-consensus]]) came later.

## Relevance to us

Must-cite foundation for any hackathon work on swarm agreement, distributed estimation or alignment. The
lambda_2 speed result gives a concrete, testable prediction for how swarm communication topology changes
convergence time. Bridges to synchronisation ([[dorfler-2014-synchronization]]) and to the unified
consensus/synchronisation view of [[li-2010-consensus]].

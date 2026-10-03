---
id: krishna-2018-network
type: talk
title: "Network dynamics (Lecture 03): the Erdos-Renyi giant-component transition via aggregation kinetics"
authors: [Sandeep Krishna]
year: 2018
url: https://www.youtube.com/watch?v=z2u7DjBX-w8
venue: "Bangalore School on Statistical Physics IX, ICTS Bangalore (27 June to 13 July 2018); uploaded 2 November 2018, 89 min"
topics: [criticality-measurement, sync-consensus]
added_by: shadow/sol-w6
accessed: 2026-10-03
read_depth: skim
relevance: 2
---

## Summary

Blackboard lecture (last of a three-lecture network-dynamics course at a statistical-physics summer school) deriving the connectivity phase transition of the Erdos-Renyi random graph by treating edge addition as an aggregation (Smoluchowski) process. Read from the auto-generated transcript, which is a chalk talk with student questions, so this is a skim; the title on YouTube is just "Network dynamics (Lecture 03)", the subtitle above is mine. Timestamps approximate.

- 00:15 to 15:00: recap of random-graph ensembles (small path lengths, clustering), then the claim to be derived: for average degree K below 1 the graph is many small tree-like components with exponentially distributed sizes; above 1 a giant component appears; at K = 1 the component-size distribution is a power law, and the second moment of the size distribution diverges there like a susceptibility (14:57). He draws the analogy to magnetisation in the Ising model.
- 17:58 to 41:49: setting up the kinetics. Add links at rate N/2 per unit time between random node pairs so that average degree equals time t. Writing c_k for the (normalised) density of components of size k, the rate at which an i-cluster and a j-cluster merge is proportional to i j c_i c_j, which gives the Smoluchowski coagulation equation with multiplicative kernel; terms where both chosen nodes fall in the same cluster are second order and vanish as N goes to infinity.
- 41:49 to 72:37: solving it. Monodisperse initial condition c_1 = 1; a generating function G(z,t) = sum k c_k e^{kz} turns the equation into a first-order PDE solved by characteristics; Lagrange inversion gives c_k(t) = k^{k-2} t^{k-1} e^{-kt} / k! (the Cayley tree count appears, 69:33). Stirling's approximation then gives, at t = 1, c_k proportional to k^{-5/2} / sqrt(2 pi) (78:27): the mean-field percolation exponent.
- 81:21 to 89:05: moments. The first moment (fraction of nodes in finite clusters) is conserved only until t = 1 and then drops, the deficit being the giant component; the second moment diverges at t = 1. He acknowledges the normalisation "trick" and points to finite-size scaling for a rigorous treatment.

Standard material (Krapivsky-Redner-Ben-Naim style), presented as a worked derivation; no original results.

## Relevance to us

Background. This lecture is the connectivity side of the result Strogatz reports in [[strogatz-2022-global]]: Erdos-Renyi graphs become connected at p = log n / n and (per Strogatz's 2022 preprint) globally synchronising at the same threshold, so the giant-component and connectivity transitions set the floor for when a randomly wired agent population can reach consensus at all. The aggregation-kinetics view (clusters merging at a rate proportional to the product of sizes, with a critical point where the size distribution is k^{-5/2}) is also a reasonable null model for how coordinated agent clusters would grow in a swarm-detection setting, i.e. what cluster-size statistics look like with no coordination beyond random pairwise contact. Related: [[munoz-2018-colloquium]] for the broader criticality framing.

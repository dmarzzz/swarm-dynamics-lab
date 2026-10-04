---
id: strogatz-2022-global
type: talk
title: "Global Synchronization: New Theorems, New Puzzles"
authors: [Steven Strogatz]
year: 2022
url: https://www.youtube.com/watch?v=0l-UwTLiIX4
venue: "Plenary (via Zoom), PCS Institute for Basic Science conference, Daejeon; uploaded 5 December 2022, 53 min including Q&A"
topics: [sync-consensus, criticality-measurement]
added_by: shadow/sol-w6
accessed: 2026-10-03
read_depth: full
relevance: 4
---

## Summary

Strogatz on the question "which network topologies force a Kuramoto network of identical oscillators to synchronise from every initial condition?" Read from the full auto-generated transcript; timestamps approximate. The YouTube description gives the abstract: each oscillator connected to at least mu(N-1) others, coupling equal and bidirectional, what is the critical connectivity mu_c above which global in-phase sync is the only attractor.

- 05:48 to 10:13: setup. Winfree's phase reduction, then Kuramoto's 1975 universal phase model theta_i' = omega_i + sum_j K_ij f(theta_j - theta_i). He restricts to identical omegas, f = sin, K_ij = 0/1 adjacency of an undirected graph. In the rotating frame this is a gradient system (the XY model at zero temperature), so the only attractors are equilibria: no limit cycles, no chimeras (19:35 to 20:19). He connects the question to machine learning's "no spurious local minima" landscape question (11:38).
- 13:06 to 14:35: ring with nearest-neighbour coupling supports a stable rotating (twisted) wave as a competing attractor; firefly waves in Japan shown as a natural example.
- 14:35 to 18:51: the 2006 Wiley, Strogatz, Girvan experiment. Ring of N = 40, 60, 80 oscillators coupled to k nearest neighbours each side; 100,000 random initial conditions per point; fraction reaching perfect sync collapses on one curve in k/N and hits 1 at k/N around 0.34, i.e. when each oscillator sees at least about 68 percent of the others.
- 21:04 to 27:36: state of the dense-graph problem. Taylor 2012: mu > about 0.94 suffices. Ling, Xu, Bandeira 2019 (optimisation community, spectral graph theory): 0.79. Lu and Steinerberger 2020: 0.7889. Kassabov, Strogatz, Townsend (Chaos, 2021): 0.75, conjectured exact. Lower bound from counterexamples with other stable patterns: 0.6809 (2006) to 0.6818, 0.6828, and 0.6838 (best known). Proof strategy (25:25): equilibrium plus stability give trigonometric inequalities; the degree condition bounds the first two Daido order parameters; together they confine all phases to a half circle, and a Lyapunov argument then gives in-phase sync.
- 28:20 to 31:14: linear stability "has gone as far as it can"; the gap between 0.6838 and 0.75 needs nonlinear analysis. They enumerate small graphs with algebraic geometry: trees always synchronise, dense ones are excluded by a centre-manifold argument of Lee DeVille, and the surviving sparse graphs (rotating wave, wave with a twig, wave with a triangle) do not raise the lower bound. Plot for graphs up to size 500 shows lower bounds approaching 0.68 and upper 0.75.
- 31:57 to 37:03: Erdos-Renyi random graphs. Ling, Xu, Bandeira 2019 conjectured (open problem 3.4) that the sync threshold coincides with the connectivity threshold p = log n / n, proving only p >> (log n / n)^(1/3). Strogatz's group got within a log n factor (Chaos, 2022), and a preprint with Bandeira's group proves the conjecture: for p > (1+epsilon) log n / n the graph is globally synchronising with probability tending to 1. Open: scale-free graphs, simplicial complexes, hypergraphs, directed and non-normal networks (no gradient structure).
- Q&A (37:48 onward): on universality he says the sine coupling is probably special (adding a second harmonic changes the mean-field critical exponent from 1/2 to 1, ~45:46); different degree scalings such as sqrt(N) are unexplored; directed graphs not studied.

All numbers are as stated in the talk; I have not checked them against the papers (none of the 2012 to 2022 papers are in the library yet).

## Relevance to us

This is the sharpest known statement of "how connected does a population need to be before consensus is the only outcome". For agent swarms it gives two reusable results: (1) dense enough interaction graphs (each node talking to more than about 75 percent of the others) make in-phase agreement inevitable regardless of initial state, while below about 68 percent stable non-consensus patterns exist; (2) on random interaction graphs, as soon as the graph is connected it is almost surely globally synchronising, so sparse random communication is enough for consensus in the identical-agent limit. The gradient-system framing (consensus = global minimum, waves = spurious local minima) is the same lens used for loss landscapes, which may help when reasoning about LLM collectives that settle into persistent disagreement clusters. Related: [[strogatz-2011-coupled]] (mean-field prerequisite), [[okeeffe-2025-global]] (global sync theorem for swarmalators, the same programme extended to position-coupled oscillators), [[arenas-2008-synchronization]] and [[rodrigues-2016-kuramoto]] (surveys of Kuramoto on networks), [[dorfler-2014-synchronization]], [[kuramoto-1984-chemical]].

---
id: strogatz-2020-networks
type: talk
title: "Networks of Oscillators That Synchronise Themselves"
authors: [Steven Strogatz]
year: 2020
url: https://www.youtube.com/watch?v=e5xxdNeNkmE
venue: "The Archimedeans (Cambridge University mathematical society), online talk; uploaded 3 November 2020, 82 min including a long Q&A"
topics: [sync-consensus]
added_by: shadow/sol-w6
accessed: 2026-10-03
read_depth: full
relevance: 3
---

## Summary

Strogatz on the same dense-graph global-synchronisation problem as [[strogatz-2022-global]], two years earlier and in a more technical, interactive register for a maths-society audience (Alex Townsend is present and comments). Read from the full auto-generated transcript, which is cleaner than most; timestamps approximate. Content that duplicates the 2022 talk is only sketched; new material is itemised.

- 03:36 to 17:54: setup for identical Kuramoto oscillators on a 0/1 adjacency graph, sine coupling; two questions, "sparsest graph that globally synchronises" (dismissed as not interesting as posed) and "densest graph that does not", which is the talk.
- 21:27 to 25:05: gradient structure gives flow downhill on a potential, so attractors are equilibria; linear stability of in-phase sync via an eigenvalue (Ritz-type) bound.
- 28:42 to 39:24: circulant graphs. A ring of 32 with each node coupled to 10 neighbours per side (degree 20) does not globally synchronise; it supports "Mexican wave" twisted states, indexed by the winding number p; all twisted states are equilibria on circulant graphs. The 2006 result: twisted states remain stable up to about 68 percent connectivity.
- 32:13 to 35:49: Townsend summarises the Ling, Xu, Bandeira (NYU) result on random graphs; the then-best upper bound quoted as 79 percent (Ling et al.), so the open gap is 68 to 79 at the time of this talk (it was 68.38 to 75 by 2022).
- 43:02 to 46:40: the twinning trick (credited to Canale and Monzon): replace each node of a non-synchronising graph by a clique wired identically to the rest; stability of the twisted states is unchanged while density rises, lifting the lower bound to 68.16 percent, and a contrived twinning-plus-extra-edges construction to 68.28.
- 46:40 to 48:50: a failed 75 percent counterexample. A family of graphs whose twisted-state Jacobian has all eigenvalues negative except four zeros looked stable in simulation, but a 1e-6 perturbation leaks along a weakly unstable nonlinear direction on a time scale of about 1e6 and the system ends in full synchrony. Lesson stated explicitly: long simulations can mislead when there are zero eigenvalues.
- 50:15 to 53:50: equilibria as roots of a quadratic polynomial system in sines and cosines, solved exhaustively for small graphs with Mike Stillman's computer-algebra package; DeVille's candidates turn out to be globally synchronising.
- 59:35 to 61:47 (Q&A): a new claim not in the 2022 talk: on graphs of size 2^m one can add only a logarithmic number of edges to a ring (example: 32 nodes, degree 9) and destabilise every twisted state, so density asymptotically zero may suffice for global sync; they believe but cannot prove these graphs are globally synchronising because other exotic equilibria are not ruled out.
- Later Q&A: weighted adjacency unexplored (62:31); figure-eight constructions of two large cycles joined by one edge produce patterns easily, "it's hard to make them with dense graphs" (68:16); non-sine coupling (sawtooth, step) is tractable but little studied (71:53); Hamiltonian versions more subtle (79:05).

All statements are his own account of published or in-progress work; the specific percentages differ slightly from the 2022 talk because the bounds moved.

## Relevance to us

Supplements [[strogatz-2022-global]] with three points relevant to agent collectives. (1) Twinning: replacing an agent by a clique of copies with identical third-party wiring does not change which collective states are stable. This is a precise statement that duplicated agents (Sybils, forks, replicas) are invisible to the dynamics unless they are wired differently, which cuts both ways for sybil-resistance and fork-merge analysis. (2) The leaky 75 percent example is a methodological warning for anyone simulating agent swarms: a state that persists for 1e5 steps can still be transient. (3) The log-many-edges result suggests that a few long-range links added to a locally coupled population may be enough to kill all non-consensus patterns, a cheap intervention to test in agent networks. Related: [[strogatz-2011-coupled]], [[okeeffe-2025-global]], [[arenas-2008-synchronization]], [[rodrigues-2016-kuramoto]], [[pecora-1998-master]].

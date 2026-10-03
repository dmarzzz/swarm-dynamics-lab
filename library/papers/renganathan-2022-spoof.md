---
id: renganathan-2022-spoof
type: paper
title: "Spoof Resilient Coordination in Distributed and Robust Robotic Networks"
authors: [Venkatraman Renganathan, Kaveh Fathian, Sleiman Safaoui, Tyler Summers]
year: 2022
venue: IEEE Transactions on Control Systems Technology, vol. 30, no. 2, pp. 803-810
url: https://ieeexplore.ieee.org/document/9388749
doi: 10.1109/tcst.2021.3063924
arxiv: null
cite: "Renganathan, V., Fathian, K., Safaoui, S., & Summers, T. (2022). Spoof Resilient Coordination in Distributed and Robust Robotic Networks. IEEE Transactions on Control Systems Technology, 30(2), 803-810. https://doi.org/10.1109/TCST.2021.3063924"
topics: [sybil-resistance, sync-consensus, swarm-robotics]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "11 (Crossref, 2026-10-03)"
code: []
---

## Summary

Journal version of the group's MRS 2017 work ([[renganathan-2017-spoof]]). Resilient consensus algorithms of the W-MSR family (each agent discards the F most extreme neighbour values before averaging) guarantee convergence of honest agents when the graph is sufficiently robust and at most F neighbours are malicious, but a spoofer that spawns many identities breaks the F-bound and the robustness assumption at once. The paper generalises W-MSR with a physical-layer authentication step: agents compare the physical fingerprints of received wireless signals (channel or angle-of-arrival profiles) to detect that several claimed neighbours are one transmitter, then isolate those identities before running the MSR filter. The technical contribution is handling stochastic fingerprints: worst-case misclassification probabilities are bounded with distributionally robust Chebyshev inequalities computed by semidefinite programming, using only the first two moments of the fingerprint distribution rather than assuming a Gaussian or known model. Numerical simulations and hardware experiments (multirobot coordination over wireless) are reported as showing effectiveness. Abstract only for the journal version (IEEE paywalled; the arXiv id in the batch metadata, 2202.09223, is a different paper by the first author on history-driven trust in consensus). The 2017 conference entry in the library has more detail on the base algorithm.

## Contribution

Composes physical-layer Sybil detection with MSR resilient consensus and gives distribution-free (Chebyshev/SDP) bounds on misclassifying honest agents as spoofers when fingerprints are noisy.

## Key results

- Spoof-resilient W-MSR: fingerprint-based isolation restores W-MSR guarantees under identity multiplication (abstract).
- Worst-case misclassification bounded via distributionally robust Chebyshev bounds solved as SDPs (abstract).
- Validated in simulation and robot experiments (numbers not visible).

## Methods and models

W-MSR consensus, wireless physical-fingerprint authentication, moment-based distributionally robust optimisation; details not read.

## Limitations and open questions

Abstract-level read for this version. Assumes fingerprints of distinct physical transmitters are separable in expectation; an adversary with beamforming (see [[wang-2013-analysis]]) or co-located radios narrows that gap; bounds use only two moments so may be loose.

## Relevance to us

The most complete "detect Sybils physically, then run a Byzantine-tolerant aggregator" design in the robotics literature, and the distribution-free misclassification bound is exactly the kind of guarantee an agent-platform detector would want when fingerprints (timing, style, provenance signals) are noisy. Sits with [[gil-2015-guaranteeing]], [[gil-2018-resilient]], [[jiang-2019-resilient]] on the physical-layer side and [[leblanc-2013-resilient]] style MSR consensus on the algorithmic side; threat taxonomy in [[higgins-2009-threats]]. Root: [[douceur-2002-sybil]].

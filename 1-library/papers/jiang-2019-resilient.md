---
id: jiang-2019-resilient
type: paper
title: "Resilient Consensus of Second-Order Multi-Agent Systems Based on WiFi Signals"
authors: [Ying Jiang, Dequan Li, Xiongjun Wu, Yue Xu]
year: 2019
venue: 2019 Chinese Control Conference (CCC), pp. 5865-5870
url: https://ieeexplore.ieee.org/document/8865835
doi: 10.23919/chicc.2019.8865835
arxiv: null
cite: "Jiang, Y., Li, D., Wu, X., & Xu, Y. (2019). Resilient Consensus of Second-Order Multi-Agent Systems Based on WiFi Signals. In 2019 Chinese Control Conference (CCC), pp. 5865-5870. IEEE. https://doi.org/10.23919/ChiCC.2019.8865835"
topics: [sybil-resistance, sync-consensus, swarm-robotics]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: abstract
relevance: 2
citations: "1 (Crossref, 2026-10-03)"
code: []
---

## Summary

Extends the Wi-Fi-fingerprint resilient consensus idea of Gil et al. from first-order to second-order (position plus velocity) discrete-time multi-agent systems on an undirected network containing spoofed attack agents (one adversary presenting several identities). The agents use only information carried over wireless Wi-Fi links; the channel is measured, each neighbour's weight in the consensus update is set from the experimental measurement (a confidence that it is a distinct physical transmitter) and allowed to vary in time, and the paper derives, in limit form, sufficient conditions for consensus together with the required relationship between the velocity and position coupling coefficients. Simulation comparisons across several cases are reported as validating the algorithm. Abstract only (IEEE Xplore; paywalled, no OA copy); the specific conditions, number of agents, and spoofer fraction are not visible.

## Contribution

Carries spatial-fingerprint-weighted consensus to double-integrator agents, which is the model needed for actual vehicles and drones rather than kinematic points.

## Key results

- Sufficient conditions for second-order consensus under time-varying confidence weights derived from Wi-Fi channel measurements, with a coefficient relation between velocity and position gains (abstract; not stated numerically).
- Simulation verification only.

## Methods and models

Second-order discrete-time consensus x_{k+1}, v_{k+1} with weights from Wi-Fi measurements; undirected graph; spoofed agents as in Gil et al.'s model. Details not read.

## Limitations and open questions

Abstract-only; simulation, no hardware; a 6-page CCC paper with one citation. It inherits the assumption that the directional Wi-Fi profile is reliable enough to separate spoofers, which was validated by the MIT group experimentally but not here.

## Relevance to us

Minor extension in the physical-layer Sybil-resilient consensus line: [[gil-2015-guaranteeing]] (coverage), [[gil-2018-resilient]] (first-order consensus), [[gil-2015-adaptive]] (the signal-profile primitive). Worth citing in the sybil-resistance survey as evidence the approach generalises to second-order dynamics, nothing more. Theory background: [[olfati-saber-2007-consensus]].

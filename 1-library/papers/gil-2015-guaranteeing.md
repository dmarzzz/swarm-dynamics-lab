---
id: gil-2015-guaranteeing
type: paper
title: "Guaranteeing Spoof-Resilient Multi-Robot Networks"
authors: ["Stephanie Gil", "Swarun Kumar", "Mark Mazumder", "Dina Katabi", "Daniela Rus"]
year: 2015
venue: "Robotics: Science and Systems XI (RSS 2015)"
url: https://www.roboticsproceedings.org/rss11/p20.pdf
doi: "10.15607/rss.2015.xi.020"
arxiv: null
cite: "Gil, S., Kumar, S., Mazumder, M., Katabi, D., & Rus, D. (2015). Guaranteeing Spoof-Resilient Multi-Robot Networks. In Robotics: Science and Systems XI (RSS 2015)."
topics: [sybil-resistance, swarm-robotics, sync-consensus]
added_by: dmarz/sybil-foundations
accessed: 2026-10-03
read_depth: skim
relevance: 5
citations: "8 (Crossref, RSS version, 2026-10-03); the extended Autonomous Robots 2017 version (doi 10.1007/s10514-017-9621-5) has 110 on Semantic Scholar and 98 on OpenAlex"
code: []
---

## Summary

The paper defends multi-robot networks against Sybil attacks, where one malicious robot spoofs many fake clients, without cryptographic key distribution. Server robots use commercial Wi-Fi radios to build a "spatial fingerprint" of each client from the directional profile of its received signal (synthetic aperture from the robot's own motion). Identities that share one physical transmitter produce near-identical fingerprints. From fingerprint similarity each client gets a confidence weight α in (0, 1), and the weights are plugged into the coverage controller.

## Contribution

A physical-layer "virtual sensor" for spoofing with analytical guarantees on how much spoofed clients can distort a multi-robot controller, demonstrated on hardware. This is the main bridge between classical Sybil defence and swarm robotics control.

## Key results

- Proven: expected confidence weight is close to 1 for legitimate clients and close to 0 for spoofed ones; the influence of spoofers on a class of coverage problems is analytically bounded, with each service robot staying within a radius of its attack-free position.
- Measured on hardware (two AscTec Hummingbird quadrotor servers, ten iRobot Create ground clients, indoor settings): spoofer detection rate of 96%.
- Measured: converged service-robot positions were on average 3 cm from optimal even when more than 75% of all clients were spoofed.

## Methods and models

Wi-Fi channel measurements, synthetic aperture radar style angle-of-arrival profiles from robot motion, fingerprint similarity to confidence weights, weighted Voronoi coverage control with proofs of bounded deviation.

## Limitations and open questions

Assumes the attacker has one (or few) physical transmitters; an adversary with many cheap radios at different positions is not Sybil in this sense. Needs robot motion to form the aperture and line-of-sight-like signal structure. The physical-identity idea does not transfer to purely software agents.

## Relevance to us

Directly in scope for swarm robotics: it shows how to turn "one body, one identity" into a continuous weight that a swarm controller can consume, giving a bounded-influence guarantee rather than binary exclusion. The same pattern (weight each agent by an unforgeable physical or provenance signal, then prove bounded deviation of the collective behaviour) is a candidate template for LLM agent swarms where the unforgeable signal would be provenance or attestation instead of radio physics. Follow-ups: [[huang-2019-lightweight]] (single-antenna version), [[mallmann-trenn-2021-crowd]] (neighbour opinions, flocking). Classical precursor: [[newsome-2004-sybil]]. Related blockchain approach to Byzantine robots: [[strobel-2023-robot]].

## Notes from dmarz/sybil-robotics

Read in full (RSS PDF) on 2026-10-03. Details worth keeping for the survey:

- Confidence weight alpha_i = beta_i times the product over j of (1 - gamma_ij): beta is an honesty term (does the fingerprint peak point where the client claims to be), gamma a similarity term (is the fingerprint indistinguishable from client j's). Using the ratio of two antennas' channels makes fingerprints invariant to per-packet transmit power scaling.
- Measured in a multipath room with 2 AscTec Hummingbird servers and 10 iRobot Create clients: TPR 96.3% (static and mobile attacker), 100% (power-scaling attacker), FPR 3.0 to 6.1%; RSSI baseline 74.1 to 85.2% TPR with up to 27.3% FPR.
- Coverage: across 12 runs the no-defence servers ended on average 3.77 m from the oracle positions; with alpha weights 0.02 m, with spoofed clients up to 300% of the network.
- Clients 3 degrees apart are separable in an anechoic chamber, 0 degrees in multipath rooms.
- Defends against many identities from one radio, not against several real colluding robots; adversarial servers are out of scope.

Follow-on robotics work in this lane: [[gil-2018-resilient]], [[renganathan-2017-spoof]], [[mallmann-trenn-2021-crowd]], [[yemini-2021-characterizing]], [[cavorsi-2024-exploiting]], [[huang-2019-lightweight]], [[gil-2023-physicality]]. Contrast with economic Sybil resistance in [[strobel-2020-blockchain]].

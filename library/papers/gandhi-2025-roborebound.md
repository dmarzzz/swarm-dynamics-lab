---
id: gandhi-2025-roborebound
type: paper
title: "RoboRebound: Multi-Robot System Defense with Bounded-Time Interaction"
authors: [Neeraj Gandhi, Yifan Cai, Andreas Haeberlen, Linh Thi Xuan Phan]
year: 2025
venue: EuroSys '25, Proceedings of the Twentieth European Conference on Computer Systems, Rotterdam, pp. 176-192
url: https://www.cis.upenn.edu/~linhphan/papers/roborebound-eurosys2025.pdf
doi: 10.1145/3689031.3696079
arxiv: null
cite: "Gandhi, N., Cai, Y., Haeberlen, A., & Phan, L. T. X. (2025). RoboRebound: Multi-Robot System Defense with Bounded-Time Interaction. In Proceedings of the Twentieth European Conference on Computer Systems (EuroSys '25), pp. 176-192. ACM. https://doi.org/10.1145/3689031.3696079"
topics: [sybil-resistance, swarm-robotics, fork-merge-security]
added_by: shadow/sol-p2
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "2 (Crossref, 2026-10-03)"
code: []
---

## Summary

Extends Byzantine fault tolerance thinking to multi-robot systems (MRS), where a compromised robot can do physical damage, not just send bad messages. The authors argue classic masking (hide the effect of f faults entirely) is impractical for robots, and propose a weaker property, bounded-time interaction (BTI): a compromised robot gets only a short, bounded window in which it can act or feed others incorrect information before it is shut down. RoboRebound achieves BTI by adding two tiny trusted MCUs per robot (an s-node interposing on sensors, an a-node interposing on actuators, each a few lines of fixed code on roughly 3 euro PIC chips), tamper-evident hash-chained logs, deterministic-replay auditing by other robots, and a token scheme: a robot's a-node only keeps actuating if it holds fresh audit tokens from f_max+1 distinct robots, otherwise it forces Safe Mode. Threat model: adversary compromises up to f_max robots' main controllers (reprograms them) but cannot tamper with the fixed-function MCUs. Evaluated with an ns-3 simulator and a SecBot hardware prototype using Olfati-Saber flocking as the case study. Motivating example (Figure 2): with 10 of 125 robots compromised and spoofing other robots' positions, the whole flock stalls away from the goal because correct robots avoid phantom neighbours. In the 25-robot, 100 m x 100 m flocking experiment, one robot compromised at t=15 s keeps the flock from the destination for the whole 150 s run without RoboRebound; with it the compromised node can act only during a short shaded window (Figure 9) and the flock recovers. Overhead measured on the PIC: hashing a ten-message log batch in about 144 us, worst-case a-node and s-node CPU load well under 1 percent, per-robot radio goodput on the order of 0.15 Kbps. Methods and evaluation skimmed; cryptographic details in Section 3 not read closely.

## Contribution

First general-purpose MRS defence for a fully Byzantine threat model (lying about sensor inputs, actuator outputs, or protocol state), as opposed to prior robot-security work that targets specific attacks (Sybil via Wi-Fi fingerprinting, physical masquerade). Introduces the BTI property and shows that a minimal trusted hardware root plus accountability-style auditing (in the PeerReview/TrInc lineage) suffices.

## Key results

- 10/125 compromised robots spoofing positions stall a flocking MRS entirely (simulation, Figure 2).
- With RoboRebound, a single compromised robot's influence is confined to a bounded window and the 25-robot flock still reaches the goal (Figures 8 and 9).
- Trusted nodes cost about 3.16 euro each; ten-message log batch hashed in ~144 us on the PIC; worst-case CPU load for the a-node is a fraction of a percent (Tables 1 and 2).
- Scales in ns-3 with varying density and robot count (Figure 7); exact numbers not extracted here.

## Methods and models

Two trusted MCUs per robot (sensor relay and actuator relay), hash-chained logs with MAC authenticators, periodic audit requests with deterministic replay by f_max+1 auditors, audit tokens with expiry enforced by the a-node, leaky-bucket rate limit on token requests. ns-3 simulation of s/c/a-nodes and 915 MHz radio; SecBot wheeled robots with PIC32MX130F064B as the trusted node. Olfati-Saber flocking (Algorithm 1) as the running application.

## Limitations and open questions

Authors (Section 3.9): a compromised robot can still misbehave within the audit window, and a robot that lies consistently about sensor readings that auditors cannot cross-check is a fundamental limit of accountability. Assumes the adversary cannot physically tamper with the fixed-function MCUs. The spoofing attack in the evaluation is simple, so the measured damage is a lower bound. Audits need f_max+1 reachable correct robots in radio range, which is a connectivity assumption on the swarm. Not an identity mechanism: RoboRebound assumes each physical robot has a provisioned key, so it bounds damage from compromised legitimate members rather than from fresh Sybil identities.

## Relevance to us

Directly relevant to the "corrupted member of a collective" question. Compare the Sybil-specific robot defences it cites and positions against: [[gil-2015-guaranteeing]], [[gil-2018-resilient]], [[mallmann-trenn-2021-crowd]], [[wardega-2019-resilience]], [[wardega-2023-byzantine]]. Builds on [[olfati-saber-2006-flocking]] as the workload and on the PBFT lineage ([[castro-1999-practical]]). The BTI idea (accept a bounded harm window, detect and eject fast) is a useful framing for agent swarms where masking every bad output is impossible, and the trusted-minimal-root plus audit pattern maps onto attestation of agent tool calls.

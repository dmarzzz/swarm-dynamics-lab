---
id: wardega-2023-byzantine
type: paper
title: "Byzantine Resilience at Swarm Scale: A Decentralized Blocklist Protocol from Inter-robot Accusations"
authors: ["Kacper Wardega", "Max von Hippel", "Roberto Tron", "Cristina Nita-Rotaru", "Wenchao Li"]
year: 2023
venue: "arXiv preprint (cs.RO)"
url: https://arxiv.org/pdf/2301.06977
doi: null
arxiv: "2301.06977"
cite: "Wardega, K., von Hippel, M., Tron, R., Nita-Rotaru, C., & Li, W. (2023). Byzantine Resilience at Swarm Scale: A Decentralized Blocklist Protocol from Inter-robot Accusations. arXiv:2301.06977."
topics: [sybil-resistance, swarm-robotics, sync-consensus]
added_by: dmarz/sybil-robotics
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: "11 (Semantic Scholar, 2026-10-03)"
code: [gh-gitsper-decentralized-blocklist-protocol]
---

## Summary

Proposes the Decentralized Blocklist Protocol (DBP) as a swarm-scale alternative to W-MSR [[leblanc-2013-resilient]]. Cooperative robots issue signed accusations Acc_i(j) when local observations contradict a peer's messages (application-specific rules, such as an observation that would have had to travel faster than the network allows). Accusations are flooded; each robot builds the accusation graph and computes a deterministic maximum matching (Edmonds), blocking every matched vertex. Because a sound accusation means "i or j is Byzantine", the graph is semi-bipartite and a maximum matching blocks every Byzantine robot exactly when Hall's marriage condition holds, at the cost of also blocking at most one cooperative accuser per Byzantine robot.

## Contribution

Replaces outlier trimming with accusation matching, which removes the need to know the Byzantine count F in advance, lowers the worst-case connectivity requirement from (2F+1)-connected to (F+1)-floodable, and lowers the observers needed to propagate new information from F+1 to 1. Works for non-consensus tasks such as cooperative localization.

## Key results

- Theorem 1 (Eventual Blocklist Consensus): on a (F, n)-floodable time-varying network with at most F Byzantine robots, all cooperative robots eventually hold the same accusation graph and therefore the same blocklist.
- ARGoS simulation, target tracking: 200 cooperative and 100 Byzantine robots; all Byzantines blocked by about timestep 200 to 400 after which tracking error is near zero. W-MSR with F = 100 stalls (information cannot propagate); with F = 15 parts of the swarm are captured.
- Time synchronization: 100 cooperative (50 anchors) and 45 Byzantine robots with a +1000-step clock offset attack; DBP blocks all Byzantines by about timestep 400; W-MSR with F = 45 cannot converge, with F = 10 is perturbed.
- Cooperative localization: 120 cooperative (80 anchors), 50 Byzantine robots with up to 20 m false offsets; errors return to nominal once blocked. W-MSR is not applicable.

## Methods and models

Threat model: a strong adversary coordinating Byzantine robots centrally with arbitrary messages and motion, but Sybil attacks are explicitly assumed impossible because a trusted central authority issues identities at deploy time (closed swarm). Turtlebots in ARGoS, 4 m radio, 0.9 m camera range, 30 Hz controller.

## Limitations and open questions

Requires sound accusations (cooperative robots never accuse each other), which the authors list as future work to relax. Influence is temporary rather than bounded at all times. Relies on a central identity issuer, so it is Byzantine-resilient but delegates Sybil resistance; with free identities an attacker could exhaust the matching by burning fresh identities, each of which takes one cooperative accuser with it.

## Relevance to us

A clean and portable mechanism for agent swarms: accusations as signed evidence, global consistency via flooding, and a combinatorial rule (maximum matching) that is robust to false accusations from Byzantines because each false accusation costs the accuser its own standing. The cost structure (one blocked honest agent per blocked adversary) is exactly what makes cheap identities dangerous, so DBP must be paired with an admission-cost or physical-identity mechanism such as [[gil-2015-guaranteeing]] or [[strobel-2020-blockchain]]. Compare neighbour-majority vetting in [[mallmann-trenn-2021-crowd]].

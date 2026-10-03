---
id: vyzovitis-2020-gossipsub
type: paper
title: "GossipSub: Attack-Resilient Message Propagation in the Filecoin and ETH2.0 Networks"
authors: ["Dimitris Vyzovitis", "Yusef Napora", "Dirk McCormick", "David Dias", "Yiannis Psaras"]
year: 2020
venue: "Protocol Labs Technical Report PL-TechRep-2020-002; arXiv preprint"
url: https://arxiv.org/pdf/2007.02754
doi: null
arxiv: "2007.02754"
cite: "Vyzovitis, D., Napora, Y., McCormick, D., Dias, D., & Psaras, Y. (2020). GossipSub: Attack-Resilient Message Propagation in the Filecoin and ETH2.0 Networks. Protocol Labs Technical Report PL-TechRep-2020-002. arXiv:2007.02754."
topics: [sybil-resistance, sync-consensus, collective-decision]
added_by: dmarz/sybil-foundations
accessed: 2026-10-03
read_depth: skim
relevance: 5
citations: "87 (Semantic Scholar, 2026-10-03)"
code: [gh-libp2p-specs]
---

## Summary

GossipSub is the libp2p publish-subscribe protocol used for block and transaction propagation in Filecoin and Ethereum's consensus layer. It combines an eager-push mesh of degree D (default 8, bounds 6 to 12) with lazy-pull gossip of message IDs to peers outside the mesh, and adds a local, unshared peer score that drives who stays in the mesh. Mitigations built on the score include score-based pruning that keeps the best D_score peers, an outbound connection quota D_out, opportunistic grafting when the median mesh score falls, flood publishing of a node's own messages, and adaptive gossip. In a testbed of 1,000 honest nodes and 4,000 Sybils on AWS (Sybil:honest connection ratio 20:1), the authors report no successful attack among those tested.

## Contribution

Treats Sybil resistance in a permissionless gossip layer as an influence problem rather than an identity problem: Sybils are allowed to connect, but each peer's own observations of delivery, validity and IP colocation decide whether a peer may stay in its mesh. It is the main deployed instance of peer scoring as decentralised reputation.

## Key results

- Score(p) = TopicCap(sum over topics of weighted P1..P4) + w5*P5 + w6*P6: P1 time in mesh, P2 first message deliveries, P3a mesh delivery-rate deficit (squared), P3b sticky delivery failures, P4 invalid messages, P5 application score (for example staked participation), P6 IP colocation surplus (squared). Counters decay periodically.
- Attacks considered: Sybil, eclipse, censorship (hard to detect because Sybils relay everything except the target's messages), cold boot (Sybils join at the same time as honest nodes, so no score history protects the mesh) and covert flash (Sybils behave for 2 minutes to build score, then stop relaying).
- Under the covert flash attack, plain GossipSub lost messages with delays above 15 s; Bitcoin-style flooding and ETH1.0 sqrt(N) pubsub missed the 6 s deadline, flooding producing 3.2M duplicate messages. With the full mitigation set GossipSub kept delivery within bounds.
- In the cold boot attack (Sybils connect first and form meshes; honest nodes join 2 minutes later), plain GossipSub delivered with delays up to 17 s (p99 10 s) and failed to propagate about 4% of messages; GossipSub with the mitigations reached 100% propagation. A nearby paragraph reports p99 of 205 ms with default settings versus 269 ms with opportunistic grafting disabled; in my text extraction it is ambiguous which attack figure that paragraph belongs to.
- The authors estimate an attacker operational cost of up to about $40,000 per month for a coordinated attack that still did not succeed (Appendix 10.1).
- Tests with collocated Sybils (P6) and spam were run but not reported.

## Methods and models

Testbed of 5,000 containers on AWS (1.2 vCPU, 2 GB RAM each), production go-libp2p-pubsub code (about 16k LOC), 100 publishers and 900 full nodes, Sybils with 100 connections each against honest nodes with 20. Metrics derived from Filecoin and ETH2.0 block-topic requirements. I read the abstract, introduction, attack taxonomy, score function, mitigation strategies, setup, the covert flash results and the summary; not every figure.

## Limitations and open questions

Self-evaluation by the protocol's designers, as a technical report rather than peer-reviewed. Score weights are left to the application and the v1.1 spec's tuning section is still marked TBD ([[gh-libp2p-specs]]). The censorship attack is acknowledged as hard to detect by scoring. Score is per-peer and local, so a Sybil can rebuild reputation with new peers.

## Relevance to us

This is the closest deployed analogue to reputation-based Sybil resistance in an agent swarm: every agent keeps a private score of each neighbour from first-hand evidence (who delivered useful messages first, who withheld, who sent invalid content, how many identities share an address) and only well-scored neighbours stay in its active set. It bounds influence, not identities. The cold boot and covert flash attacks are exactly the failure modes to expect when many agents are spawned at once or when Sybil agents behave well before defecting, which links to [[bara-2026-epistemic]] and [[karten-2026-agent]]. Outbound quotas (the victim chooses some peers itself) are the general fix for eclipse that also appears in [[heilman-2015-eclipse]] and [[marcus-2018-low-resource]]. The P5 hook is where stake or credentials ([[kadianakis-2023-proof]], [[alpturer-2026-aetherweave]]) enter. Related: [[singh-2006-eclipse]], [[gh-libp2p-specs]], [[gh-vacp2p-zerokit]].

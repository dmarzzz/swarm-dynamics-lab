---
id: castro-2002-secure
type: paper
title: "Secure routing for structured peer-to-peer overlay networks"
authors: ["Miguel Castro", "Peter Druschel", "Ayalvadi Ganesh", "Antony Rowstron", "Dan S. Wallach"]
year: 2002
venue: "5th USENIX Symposium on Operating Systems Design and Implementation (OSDI 2002); also ACM SIGOPS Operating Systems Review 36(SI)"
url: https://people.mpi-sws.org/~druschel/publications/security.pdf
doi: "10.1145/844128.844156"
arxiv: null
cite: "Castro, M., Druschel, P., Ganesh, A., Rowstron, A., & Wallach, D. S. (2002). Secure routing for structured peer-to-peer overlay networks. In Proceedings of the 5th USENIX Symposium on Operating Systems Design and Implementation (OSDI '02), Boston, MA. ACM SIGOPS Operating Systems Review, 36(SI), 299-314."
topics: [sybil-resistance, sync-consensus]
added_by: dmarz/sybil-foundations
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "931 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

The paper splits secure routing in structured overlays (Pastry, Chord, CAN, Tapestry) into three problems: secure assignment of node identifiers, secure routing table maintenance, and secure message forwarding. It answers the first with offline certification authorities that sign random nodeIds bound to a public key and an IP address, the second with a constrained routing table whose entries must be the node closest to a fixed point in id space, and the third with a routing failure test based on nodeId density plus redundant routing to replica roots. Measured on Pastry simulations, the techniques keep routing correct with up to 25% malicious nodes.

## Contribution

This is the paper that names the eclipse problem for overlays (routing tables that fill up with attacker entries) and states that it cannot be solved without first controlling identity issuance. It is the overlay-network companion to [[douceur-2002-sybil]], published the same year, and the reference point that [[singh-2006-eclipse]] and [[baumgart-2007-skademlia]] react to.

## Key results

- Secure routing maintained with up to 25% malicious nodes, with overhead proportional to the fraction of malicious nodes (abstract and conclusion).
- Section 3.2.1 prices Sybil identities directly: if nodeId certificates cost $20, controlling 10% of a 1,000-node overlay costs $2,000 and of a 1,000,000-node overlay $2,000,000; obtaining the nodeId closest to a chosen point costs an expected $20,000 in a 1,000-node overlay.
- Section 3.3 rejects fully distributed nodeId generation by crypto puzzles: the puzzle must be cheap enough for the slowest honest node yet costly for an attacker with many fast machines, which caps its effectiveness. A puzzle variant binding nodeId to IP and periodic invalidation of ids are described but not adopted.
- No known identity scheme works for very small overlays; the authors require all members to be trusted until the network reaches critical mass.
- The routing failure test avoids redundant routing in the common case: without faults, redundant routing is invoked 0.5% (l=16) and 0.4% (l=32) of the time in the two scenarios plotted.

## Methods and models

Abstract model of a structured overlay with uniform random nodeIds, keys, root nodes and replica sets; analysis of attack probability under a fraction f of colluding faulty nodes; simulations of Pastry with up to 100,000 nodes. I read the introduction, Sections 2, 3 and parts of 5, and the conclusions; I did not check the routing-failure-test derivations.

## Limitations and open questions

Relies on a trusted, offline CA and on payment or real-world identity to limit certificates; the paper itself says decentralised assignment has "fundamental security limitations" and cites Douceur. The constrained routing table removes the freedom to pick low-latency neighbours, which is the cost [[singh-2006-eclipse]] later tries to avoid. Evaluation is only on Pastry.

## Relevance to us

For agent swarms this is the clearest statement that influence over who you route to (your neighbour set) is the asset a Sybil attacker wants, and that it splits into two controls: bound identities (certified ids, priced at $X each) and bound influence (constrained neighbour slots so that each identity can occupy only its fair share of any victim's table). Agent registries such as ERC-8004 or A2A agent cards are the CA analogue; per-agent neighbour constraints in a gossip mesh are the constrained-routing-table analogue. The pricing arithmetic carries over directly to agent identity fees. Bounds identities (CA) and influence (constrained tables). Related: [[douceur-2002-sybil]], [[levine-2006-survey]], [[castro-1999-practical]], [[hu-2025-inter-agent]].

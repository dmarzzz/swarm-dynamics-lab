---
id: blockchain-at-berkeley-2020-distributed
type: talk
title: "Lecture 6: Distributed Systems & Consensus (Blockchain Fundamentals, Fall 2020)"
authors: [Blockchain at Berkeley]
year: 2020
url: https://www.youtube.com/watch?v=FzayrHDx-Gw
venue: "Blockchain at Berkeley public Blockchain Fundamentals webinar series, Fall 2020; uploaded 25 October 2020, 70 min"
topics: [sync-consensus, sybil-resistance]
added_by: shadow/sol-w6
accessed: 2026-10-03
read_depth: skim
relevance: 1
---

## Summary

Introductory student-run webinar (two undergraduate presenters give first names only; I attribute to the organisation) that walks from distributed-systems basics to blockchain consensus families. Read from the auto-generated transcript; skim. Timestamps approximate.

- 02:52 to 14:20: why consensus matters, with avionics (redundant flight computers voting) and SpaceX Dragon's triple-redundant computers as examples of agreement under hostile conditions; link back to the previous lecture on mining and pool attacks.
- 14:20 to 28:35: properties. Safety versus liveness framed as a trade-off; the three correctness conditions of agreement, validity (the decision must be one of the proposed inputs) and termination; CAP theorem (consistency, availability, partition tolerance) illustrated with a toy replicated-database example where a network cut forces a choice between answering stale and not answering.
- 28:35 to 37:07: the Byzantine Generals problem with the three-general example showing why one traitor among three cannot be tolerated (the Lamport, Shostak, Pease impossibility, though they do not cite it by name), and the mapping of generals to nodes, messengers to unreliable links, traitors to faulty or malicious nodes.
- 37:07 to 45:46: voting-based consensus: Paxos told through Lamport's Part-Time Parliament fiction (proposers, acceptors, learners; decrees with unique ids), used at Google-scale systems where nodes are trusted and only third-party attackers are a concern; Raft as a leader-with-heartbeat simplification. They draw the contrast that blockchains must assume some nodes are adversarial.
- 45:46 to 60:06: blockchain-style (lottery) consensus, organised by the resource consumed to earn the right to propose: computation (proof of work), native currency (proof of stake), burned coins (proof of burn), wall-clock time in a trusted execution environment (proof of elapsed time), and proof of authority (dismissed as suitable only for testnets).
- 60:06 to 68:43: federated Byzantine agreement (Stellar-style quorum slices): each node chooses whom it trusts, overlapping slices yield network-wide quorum, faster at the cost of explicit trust choices. Closing remark that no single mechanism is best for all goals.

Educational overview, no original content, no measurements; several points are simplified (e.g. the safety/liveness "trade-off" framing).

## Relevance to us

Background at most. Its one framing worth keeping is the taxonomy "what resource does an agent consume to earn a vote", which is precisely the Sybil-resistance question for open agent populations: votes weighted by head count are free to forge, so swarm-level agreement needs a scarce resource or an explicit trust graph (the quorum-slice idea is a trust-graph answer). The technical primary sources already catalogued cover this properly: [[lamport-1982-byzantine]], [[castro-1999-practical]], [[castro-2002-secure]]; linear averaging consensus for comparison in [[ganesh-2020-introduction]] and [[degroot-1974-reaching]].

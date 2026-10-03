---
id: moses-2019-melanie
type: talk
title: Melanie Moses on Metabolic Scaling in Biology & Computation
authors:
- Melanie Moses
- Michael Garfield
year: 2019
url: https://dts.podtrac.com/redirect.mp3/cdn.simplecast.com/audio/812a29/812a2932-f271-4e9b-a23f-8d2d443a1682/cb3e0ca6-b7d2-4a5f-8f46-65cb9908fea6/complexity-10-melanie-moses-on-metabolic-scaling-in-biology-and-computation_tc.mp3?aid=rss_feed&feed=OzDH_At2
venue: COMPLEXITY, 2019-12-04
topics:
- swarm-robotics
- swarm-intelligence
- criticality-measurement
- fork-merge-security
added_by: shadow/sol-aud
accessed: '2026-10-03'
read_depth: full
relevance: 5
---

## Summary

Melanie Moses discusses scaling constraints and search algorithms with host Michael Garfield. Read the complete approximately 67-minute Deepgram transcript. She distinguishes observed scaling patterns, mechanistic models, and broader evolutionary analogies.

- [11:03] Moses introduces approximate three-quarter-power metabolic scaling in animals, then explains why the same exponent need not apply to bacteria or unicellular eukaryotes. [24:57] Ant-colony data also approach three-quarter scaling despite a prior expectation of a different exponent; [30:52] the mechanism remains uncertain, with a growing share of inactive workers discussed as one hypothesis.
- [48:44] Combining energy dissipation and transport time in a model, with equal importance assumed rather than independently established, produces curvature closer to observed mammalian data. [50:40] Fitting straight lines at different positions on a curved relation can yield different apparent exponents.
- [53:03] Decentralization alone does not guarantee scalability. [54:04] A proposed resource-search architecture separates local robot search from a branching transport network with successively larger carriers; otherwise return trips eventually dominate work. This is a theoretical design explanation, not a report of thousands of robots operating on Mars.
- [59:02] Moses reports four years of NASA Swarmathon activity involving about 100 robots, 45 teams, and 1,500 students, with changing resource distributions testing flexibility. [61:13] The theoretically best search policy was not necessarily empirically best on inexpensive robots. [63:17] Communicating abstract waypoints failed when lost robots broadcast incorrect locations; embodied pheromone trails physically constrain where signals can be deposited, motivating error-tolerant alternatives.

## Relevance to us

Useful for scaling analysis that includes communication, transport, and time rather than only agent count. The waypoint failure supplies a concrete analogy for erroneous shared-memory updates propagating through a swarm, but no malicious poisoning or secure merge protocol is measured. Compare [[moses-2024-physics]] for exploration and coordination overhead, and [[gordon-2021-deborah]] for ecology-dependent feedback rules.

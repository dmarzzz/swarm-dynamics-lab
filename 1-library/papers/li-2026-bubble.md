---
id: li-2026-bubble
type: paper
title: "Bubble-raft inspired shape-assembly in flying robot swarm for uniform formation and obstacle traversal"
authors: ["Hanxun Li", "Jinshu Su", "Zhiqiang Li", "Yining Zhao", "Tingyu Chen", "Biao Han"]
year: 2026
venue: "Communications Engineering"
url: https://www.nature.com/articles/s44172-026-00715-3
doi: "10.1038/s44172-026-00715-3"
arxiv: null
cite: "Li, H., Su, J., Li, Z., Zhao, Y., Chen, T., & Han, B. (2026). Bubble-raft inspired shape-assembly in flying robot swarm for uniform formation and obstacle traversal. Communications Engineering (published online 2 July 2026; volume and article number not yet assigned in Crossref). https://doi.org/10.1038/s44172-026-00715-3"
topics: [swarm-robotics, collective-motion]
added_by: dmarz/swarm-robotics-recent-audit
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "0 (Crossref is-referenced-by-count, 2026-10-03; OpenAlex search budget exhausted during this audit)"
code: []
---

## Summary

A distributed 3D shape-assembly controller for flying robot swarms. Borrowing the picture of a bubble raft, each robot owns a non-overlapping region inside the target shape and sets its velocity from three terms: exploring its region, balancing region sizes with neighbours, and fine-tuning inter-robot distance. A lightweight velocity-obstacle step then bends this nominal velocity into a collision-free command with little disruption to the formation. Simulations and real flights show complex 3D shapes formed with uniform coverage, safe spacing, fast shape changes, tolerance of robots joining or failing, and obstacle traversal.

## Contribution

Extends assignment-free shape assembly (mean-shift shape assembly of Sun et al., 2023, Nature Communications; not in the library) from ground robots to 3D aerial swarms, adding uniformity of coverage and obstacle traversal. It belongs to the formation and pattern-formation strand rather than emergent flocking.

## Key results

- (per the abstract) Arbitrary 3D target shapes formed with uniform coverage and maintained safety distances, in simulation and in real-world swarm flights.
- (per the abstract) Fast shape transformation, and resilience when robots join or fail.
- (per the abstract) Reliable obstacle traversal with minimal formation disruption via the velocity-obstacle filter.
- Swarm sizes, timings and error metrics were not available to me (full text not accessible in this session).

## Methods and models

Region-based (Voronoi-like) shape assembly with three velocity terms (region exploration, region balancing, distance fine-tuning) plus a velocity-obstacle collision filter. Distributed: each robot uses neighbour information only. Validation in simulation and with real quadrotors (platform not stated in the abstract).

## Limitations and open questions

Abstract-level read. The target shape is global information given to every robot, so this is programmed formation, not self-organisation from purely local rules. Whether region balancing behaves like a pressure (the bubble-raft analogy suggests a foam-like elasticity) is an interesting physics question the abstract does not address.

## Relevance to us

A shape-assembly baseline for any hackathon experiment on morphogenesis or pattern formation with drones. Compare with GO-Flock [[tan-2025-go]], Primitive-Swarm [[hou-2025-primitive]] and the self-assembly classic [[rubenstein-2014-programmable]].

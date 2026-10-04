---
id: sagwal-2026-detecting
type: paper
title: "Detecting Sybil Identities in Distributed Multi-Robot Exploration via Geometric Ranking"
authors: ["Rubal Sagwal", "Vishal Gupta", "Avinash Gautam"]
year: 2026
venue: "Journal of Intelligent & Robotic Systems"
url: https://api.openalex.org/works/doi:10.1007/s10846-026-02452-3
doi: "10.1007/s10846-026-02452-3"
arxiv: null
cite: "Sagwal, R., Gupta, V., & Gautam, A. (2026). Detecting Sybil Identities in Distributed Multi-Robot Exploration via Geometric Ranking. Journal of Intelligent & Robotic Systems."
topics: [sybil-resistance, swarm-robotics]
added_by: dmarz/sybil-robotics
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "0 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Studies strategically placed Sybil identities that manipulate shared coverage information in cooperative multi-robot exploration, and proposes IsoRank, which flags identities whose broadcast positions are geometrically inconsistent with a physically realisable team. It combines density-based clustering, global centroid-isolation analysis and local neighbour-consistency checks, needs only broadcast positions, and uses no central infrastructure or special hardware.

## Contribution

A 2026 software-only Sybil detector for robots, relying on spatial consistency rather than radio physics.

## Key results

- The combined multi-stage design improves detection over individual stages across robot densities and environments (abstract; no numbers given there).

## Methods and models

Geometric anomaly detection on broadcast positions; ablation and sensitivity analysis. Abstract read only; details beyond the abstract not checked.

## Limitations and open questions

A careful attacker can place Sybils at plausible positions; consistency checks bound but do not prevent this. Same authors report attack placement strategies in earlier conference work (WCNC 2026, NOMS 2026, seen in a citation listing, not opened).

## Relevance to us

Spatial consistency is a semantic consistency check; the agent-swarm analogue is checking whether an identity's claims are consistent with what other agents observe, as in [[wardega-2023-byzantine]].

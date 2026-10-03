---
id: krongauz-2024-vision
type: paper
title: "Vision-based collective motion: A locust-inspired reductionist model"
authors: ["David L. Krongauz", "Amir Ayali", "Gal A. Kaminka"]
year: 2024
venue: "PLOS Computational Biology"
url: https://doi.org/10.1371/journal.pcbi.1011796
doi: "10.1371/journal.pcbi.1011796"
arxiv: null
cite: "Krongauz, D. L., Ayali, A., & Kaminka, G. A. (2024). Vision-based collective motion: A locust-inspired reductionist model. PLOS Computational Biology, 20(1), e1011796."
topics: [collective-motion, swarm-robotics]
added_by: dmarz/collective-motion-recent
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "20 (OpenAlex W4391307170, 2026-10-03)"
code: []
---
## Summary

A model of collective motion for locust-like agents with elongated bodies, an omnidirectional horizontal visual sensor and no stereoscopic depth. Agents must estimate neighbour distance and velocity from monocular cues and cope with occlusion; three strategies for handling partly occluded neighbours are compared at different computational cost. Simulations in toroidal, corridor and ring arenas show ordered or near-ordered states for all strategies, differing in how fast order is reached and sensitive to body elongation.

## Contribution

Drops the idealised perception assumption of SPP models and asks what minimal visual processing still gives order; relevant both to locust biology and to camera-only robots.

## Key results

- Simulation (abstract): order emerges under monocular, occluded vision; convergence rate depends on the occlusion strategy and on body elongation.

## Methods and models

Agent-based simulations with geometric visual projection, occlusion handling and three interpretation strategies.

## Limitations and open questions

Abstract only; no quantitative comparison to locust data.

## Relevance to us

A vision-only baseline for robot swarms alongside [[mezey-2025-purely]]; biologically complementary to [[sayin-2025-behavioral]].

## Notes from dmarz/collective-motion-recent-audit

Metadata (title, authors, year, venue, DOI/arXiv) cross-checked against OpenAlex and passes verify. citations replaced with the OpenAlex cited_by_count (2026-10-03) in place of the Crossref count.

---
id: xiao-2024-perception
type: paper
title: "Perception of motion salience shapes the emergence of collective motions"
authors: ["Yandong Xiao", "Xiaokang Lei", "Zhicheng Zheng", "Yalun Xiang", "Yang-Yu Liu", "Xingguang Peng"]
year: 2024
venue: "Nature Communications"
url: https://doi.org/10.1038/s41467-024-49151-x
doi: "10.1038/s41467-024-49151-x"
arxiv: null
cite: "Xiao, Y., Lei, X., Zheng, Z., Xiang, Y., Liu, Y.-Y., & Peng, X. (2024). Perception of motion salience shapes the emergence of collective motions. Nature Communications, 15(1), 4779."
topics: [collective-motion, swarm-robotics]
added_by: dmarz/collective-motion-recent
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "24 (OpenAlex W4399362230, 2026-10-03)"
code: []
---
## Summary

The authors define a first-person measure of a neighbour's motion salience (relative motion change seen by the focal bird) and test it on three large bird-flock datasets. Individuals converge their velocity faster with neighbours of higher past motion salience, a positive correlation prevalent in real flocks and linked to leader-follower structure. They turn this into an adaptive motion-salience (AMS) interaction rule and implement it on about 100 miniature robots, where it improves self-organised evacuation from confined spaces.

## Contribution

Empirical evidence from bird flocks that interaction weights are selective and depend on perceived motion change, plus a robot implementation; precursor to [[zheng-2024-body]].

## Key results

- Measured (abstract): positive correlation between past perceived motion salience and future rate of velocity consensus in real flocks.
- Robot experiments (abstract): AMS swarms evacuate confined environments more smoothly than baselines.

## Methods and models

Three bird-flocking datasets (likely pigeon GPS; not checked), correlation analysis, SPP model with adaptive weights, swarm of about 10^2 robots.

## Limitations and open questions

Abstract only. Correlational evidence; causality of salience in birds not established experimentally.

## Relevance to us

Selective-attention rules are a recurrent 2024-2026 theme: [[zheng-2024-body]], [[puy-2024-selective]], [[ito-2024-selective]].

## Notes from dmarz/collective-motion-recent-audit

Spot-checked against the abstract: three bird datasets and about 10^2 robots match. citations replaced with the OpenAlex cited_by_count (2026-10-03) in place of the Crossref count.

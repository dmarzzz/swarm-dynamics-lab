---
id: kim-2025-commanding
type: paper
title: "Commanding emergent behavior with neural networks"
authors: ["Dongjo Kim", "Jeongsu Lee", "Ho-Young Kim"]
year: 2025
venue: "Cell Reports Physical Science"
url: https://arxiv.org/abs/2407.11330
doi: "10.1016/j.xcrp.2025.102857"
arxiv: null
cite: "Kim, D., Lee, J., & Kim, H.-Y. (2025). Commanding emergent behavior with neural networks. Cell Reports Physical Science, 6(10), 102857."
topics: [collective-motion, swarm-robotics]
added_by: dmarz/collective-motion-recent
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "1 (OpenAlex W7083295157, 2026-10-03)"
code: []
---
## Summary

Trains physics-obeying deep neural networks to find inter-agent interaction rules that produce a desired collective pattern at a desired time. Rules are decomposed into distancing and aligning forces expressed as polynomial series, which makes training tractable. Examples: tuning mean radius and cluster size in vortical swarms, timing the random-to-ordered transition, continuously switching between collective modes, and superposing modes into hybrid patterns such as protective formations. Per the published summary seen in search results, the framework also reproduces pigeon flocking from GPS data. The abstract read is from the arXiv preprint 2407.11330 ("Navigating the swarm: Deep neural networks command emergent behaviours").

## Contribution

Inverse design of interaction rules for target emergent behaviour, a control-oriented counterpart to rule inference.

## Key results

- Claimed (abstract): control of cluster radius, size, transition timing and mode; hybrid modes.

## Methods and models

Differentiable simulation with NN-parameterised polynomial distancing and aligning forces (details not read).

## Limitations and open questions

Abstract only; whether the pigeon-inferred rules are unique is not addressed in the abstract.

## Relevance to us

Inverse design is a natural hackathon project; compare the evolutionary approach in [[reynolds-2026-evoflock]] and inference in [[gao-2024-learning]].

## Notes from dmarz/collective-motion-recent-audit

The url is arXiv 2407.11330, whose arXiv title is 'Navigating the swarm: Deep neural networks command emergent behaviours' (DataCite). Left arxiv: null because verify flags the title mismatch against the journal title; the preprint is the same work under its earlier title. citations replaced with the OpenAlex cited_by_count (2026-10-03) in place of the Crossref count.

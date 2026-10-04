---
id: zakir-2025-bio
type: paper
title: "Bio-inspired decision making in robot swarms under biases"
authors: ["Raina Zakir", "Timoteo Carletti", "Marco Dorigo", "Andreagiovanni Reina"]
year: 2025
venue: "arXiv preprint"
url: "https://arxiv.org/abs/2509.07561"
doi: null
arxiv: "2509.07561"
cite: "Zakir, R., Carletti, T., Dorigo, M., & Reina, A. (2025). Bio-inspired decision making in robot swarms under biases. arXiv preprint arXiv:2509.07561. https://arxiv.org/abs/2509.07561"
topics: ["collective-decision", "swarm-robotics"]
added_by: dmarz/collective-decision
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: null  # not found in OpenAlex by arXiv DOI on 2026-10-03
code: []
---

## Summary

Compares direct-switch (copy a neighbour's opinion) with cross-inhibition (conflicting opinion makes the receiver uncommitted) for best-of-n decisions in minimal robot swarms whose members make frequent sensing errors, extending mean-field models with asocial biases. Direct-switch picks the best option without biases but degrades into deadlock with them; cross-inhibition gives faster, more cohesive, accurate, robust and scalable decisions across biased conditions.

## Contribution

Generalises [[reina-2023-cross]] to n options and to several bias sources (stubborn robots, corrupted communication, independent discovery, per the v1 title).

## Key results

- Cross-inhibition outperforms direct-switch under asocial biases on speed, cohesion, accuracy and scalability (mean-field models; simulations).
- Abstract-level reading only; numbers beyond the abstract were not checked.

## Methods and models

Mean-field opinion dynamics with asocial bias terms; robot swarm simulations (details not checked). Preprint, two versions (v1 9 Sep 2025).

## Limitations and open questions

Preprint, not yet peer reviewed as far as the arXiv page shows (no journal reference).

## Relevance to us

Most recent statement of the case for cross-inhibition in minimal swarms. Related: [[valentini-2017-best]], [[talamali-2021-when]].

## Notes from dmarz/collective-decision-audit

Audited 2026-10-03: title, authors and year match the arXiv record (DataCite). read_depth abstract is accurate.

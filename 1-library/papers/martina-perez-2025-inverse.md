---
id: martina-perez-2025-inverse
type: paper
title: "Inverse statistics of active matter trajectories to distinguish interaction kernel anisotropy from emergent correlations"
authors: ["Simon F. Martina-Perez"]
year: 2025
venue: "arXiv preprint"
url: https://arxiv.org/abs/2510.04193
doi: null
arxiv: "2510.04193"
cite: "Martina-Perez, S. F. (2025). Inverse statistics of active matter trajectories to distinguish interaction kernel anisotropy from emergent correlations. arXiv preprint arXiv:2510.04193."
topics: [collective-motion, active-matter, criticality-measurement]
added_by: dmarz/collective-motion-recent-audit
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: null  # arXiv-only preprint; not indexed in OpenAlex by arXiv DOI on 2026-10-03
code: []
---

## Summary

When front-back or lateral biases appear in the neighbour statistics of tracked cells, animals or synthetic particles, it is unclear whether the interaction kernel itself is anisotropic or whether isotropic interactions produce the anisotropy collectively. The paper derives a linear partial differential equation linking measurable two-point velocity correlations to an unknown distance- and angle-dependent interaction kernel. It shows Turing-like instabilities can produce dipolar or quadrupolar correlation patterns from an angle-independent attraction-repulsion law, that weak velocity alignment suppresses the dipolar patterns, and validates the predictions with agent-based simulations.

## Contribution

A theoretical caution for data-driven inference of interaction rules: anisotropic force maps (as reported for fish and birds) can be emergent rather than intrinsic, and the paper offers a way to tell them apart.

## Key results

- Theory (abstract): linear PDE connecting pair velocity correlations to the interaction kernel.
- Theory: isotropic attraction-repulsion can generate dipolar/quadrupolar correlation patterns via Turing-like instability.
- Theory: weak alignment suppresses dipolar patterns.
- Simulation: agent-based tests agree with predictions; design guidance offered for experiments.

## Methods and models

Pair-density formulation of velocity-velocity correlation fields, linear stability analysis of pair correlations, agent-based simulations. Single-author preprint (arXiv, October 2025). No code link checked.

## Limitations and open questions

Read at abstract level. Not yet peer reviewed as far as seen; applies a linearised theory, so strongly nonlinear regimes may differ. Not tested on real tracking data in the abstract.

## Relevance to us

Directly relevant to every force-map style inference in the library: [[puy-2024-selective]], [[de-lamo-2025-data]], [[han-2024-collective]], [[gao-2024-learning]], [[hem-2025-learning]], [[escobedo-2026-closed]]. A check we should run before claiming an anisotropic rule from simulated or real trajectories.

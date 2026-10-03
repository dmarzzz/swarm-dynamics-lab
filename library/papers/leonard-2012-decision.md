---
id: leonard-2012-decision
type: paper
title: "Decision versus compromise for animal groups in motion"
authors: ["Naomi E. Leonard", "Tian Shen", "Benjamin Nabet", "Luca Scardovi", "Iain D. Couzin", "Simon A. Levin"]
year: 2012
venue: "Proceedings of the National Academy of Sciences"
url: https://doi.org/10.1073/pnas.1118318108
doi: "10.1073/pnas.1118318108"
arxiv: null
cite: "Leonard, N. E., Shen, T., Nabet, B., Scardovi, L., Couzin, I. D., & Levin, S. A. (2012). Decision versus compromise for animal groups in motion. Proceedings of the National Academy of Sciences, 109(1), 227–232. https://doi.org/10.1073/pnas.1118318108"
topics: ["collective-decision", "collective-motion", "sync-consensus"]
added_by: dmarz/collective-decision
accessed: 2026-10-03
read_depth: abstract
relevance: 5
citations: "108 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Continuous-time analytical model of a moving group with two informed subgroups preferring different directions and an uninformed subgroup with no preference. The authors prove a necessary and sufficient condition for stable convergence to a collective decision: above a threshold difference in preferred directions the group decides for one direction, below it the decision is unstable and the group compromises. Adding uninformed individuals makes collective decisions more likely.

## Contribution

Analytical counterpart of the agent-based results in [[couzin-2005-effective]] and [[couzin-2011-uninformed]]; one of the first rigorous bifurcation treatments of decision versus compromise in animal groups, leading to [[leonard-2024-fast]].

## Key results

- Stability of a decision depends on the magnitude of the difference in preferred directions, with a sharp threshold (proved).
- The likelihood of a collective decision increases with the number of uninformed individuals (analytical).
- Abstract-level reading only; numbers beyond the abstract were not checked.

## Methods and models

Coupled-oscillator style model of heading dynamics for three subgroups with all-to-all or graph coupling; stability analysis.

## Limitations and open questions

Mean-field subgroup model; no spatial structure; full text not accessible to us at this session (PMC page behind a bot check).

## Relevance to us

Gives the threshold behaviour to test in a simulated swarm; same bifurcation appears in [[biro-2006-from]], [[strandburg-peshkin-2015-shared]] and [[sridhar-2021-geometry]].

---
id: aina-2022-toward
type: paper
title: "Toward Task Capable Active Matter: Learning to Avoid Clogging in Confined Collectives via Collisions"
authors: ["Kehinde O. Aina", "Ram Avinery", "Hui-Shun Kuan", "Meredith D. Betterton", "Michael A. D. Goodisman", "Daniel I. Goldman"]
year: 2022
venue: "Frontiers in Physics"
url: https://doi.org/10.3389/fphy.2022.735667
doi: "10.3389/fphy.2022.735667"
arxiv: "2505.15033"
cite: "Aina, K. O., Avinery, R., Kuan, H.-S., Betterton, M. D., Goodisman, M. A. D., & Goldman, D. I. (2022). Toward Task Capable Active Matter: Learning to Avoid Clogging in Confined Collectives via Collisions. Frontiers in Physics, 10, 735667."
topics: ["active-matter", "swarm-robotics", "collective-decision"]
added_by: dmarz/active-matter
accessed: 2026-10-03
read_depth: abstract
relevance: 5
citations: "8 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Aina, Goldman and colleagues task small groups of robots with carrying pellets through a narrow tunnel, a dense,
confined regime where clogging dominates. Without adaptation, clogs and clusters are common. Letting a robot reverse and
exit when blocked improves flow; letting robots adapt reversal probabilities from collisions and a noisy self-measured
tunnel length produces unequal workload distributions like those of fire ants and better excavation performance. Simple
collision-based learning rules mitigate clogging in task-capable dense active matter. Read from the abstract in the Semantic Scholar API record in `url`; details beyond the abstract are not checked.

## Contribution

Robophysics study linking dense active matter (glassy, jammed regimes) to task performance and learning in robot
swarms, extending earlier fire-ant and robot work by the same group.

## Key results

- Measured (robots): reversal rule and adaptive reversal probabilities reduce clogging and raise excavation
  performance; unequal workloads emerge (abstract; numbers not recorded).

## Methods and models

Physical robot experiments in a confined tunnel (Frontiers in Physics 2022; arXiv:2505.15033).

## Limitations and open questions

Small groups; specific task.

## Relevance to us

Directly relevant to dense robot swarms doing work: the antidote to MIPS-like clogging ([[cates-2015-motility]]) is
simple reversal and workload inequality. Related: [[ziepke-2025-acoustic]], [[janzen-2026-active]].

## Notes from dmarz/active-matter-audit

Audit 2026-10-03: metadata confirmed against OpenAlex and DataCite (the arXiv id 2505.15033 is a 2025 posting of the 2022 paper, same title and authors). The url is the Semantic Scholar API record the scan agent read, i.e. abstract only, consistent with read_depth abstract. Citation count replaced with OpenAlex.

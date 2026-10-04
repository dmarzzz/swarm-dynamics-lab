---
id: etcheverry-2026-reasoning
type: paper
title: Reasoning with Neural Cellular Automata
authors: [Mayalen Etcheverry, Pietro Miotti, Aidan Sirbu, Konstantin Schürholt, Mariia Drozdova, Arna Ghosh, Blaise Agüera y Arcas, James Manyika, Blake Richards, Eyvind Niklasson]
year: 2026
venue: arXiv
url: https://arxiv.org/html/2609.36126v1
doi: null
arxiv: '2609.36126'
cite: 'Etcheverry, M., Miotti, P., Sirbu, A., Schürholt, K., Drozdova, M., Ghosh, A., Agüera y Arcas, B., Manyika, J., Richards, B., & Niklasson, E. (2026). Reasoning with Neural Cellular Automata. arXiv:2609.36126.'
topics: [marl-emergence, swarm-intelligence]
added_by: dmarz/question-atlas
accessed: 2026-10-03
read_depth: skim
relevance: 5
citations: null
code: []
---

## Summary

Studies learned local recurrent cells on mazes, Sudoku and ARC. The authors report reasoning, generalization and damage-recovery results, with sample replay, perturbation training and stochastic updates contributing to performance. These are reported results, not independently reproduced here.

## Contribution

Connects NCA computation to scored reasoning tasks beyond target-image regeneration.

## Key results

- Figure 8 reports adaptive maze repair using 0.52 times the cell operations of uniform updates.
- That operation count is not a measured wall-clock or energy saving.

## Methods and models

Shared local rule, mutable state and task inputs, Bernoulli update masks, replay training. Read introduction, selected method sections, Figures 7–8 descriptions, Discussion and Appendix B.5 limitations.

## Limitations and open questions

Not a full appendix read. Implementation computes dense updates before masking; asynchronous deployment semantics require checking. Training and ensemble selection use global machinery. Code/checkpoint availability was not established, and nothing was run.

## Relevance to us

Closest reasoning-and-repair anchor for the NCA observatory; [[mordvintsev-2020-growing]] supplies the earlier morphogenesis model.

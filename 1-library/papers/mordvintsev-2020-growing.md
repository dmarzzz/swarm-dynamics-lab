---
id: mordvintsev-2020-growing
type: paper
title: Growing Neural Cellular Automata
authors: [Alexander Mordvintsev, Ettore Randazzo, Eyvind Niklasson, Michael Levin]
year: 2020
venue: Distill
url: https://distill.pub/2020/growing-ca/
doi: 10.23915/distill.00023
arxiv: null
cite: 'Mordvintsev, A., Randazzo, E., Niklasson, E., & Levin, M. (2020). Growing Neural Cellular Automata. Distill, 5(2), e23. https://doi.org/10.23915/distill.00023'
topics: [marl-emergence, swarm-intelligence]
added_by: dmarz/question-atlas
accessed: 2026-10-03
read_depth: skim
relevance: 5
citations: null
code: []
---

## Summary

A shared learned local update rule grows an image from a seed. The article distinguishes growth, persistence and regeneration training, demonstrating that sample-pool training and deliberate damage exposure can improve stability and repair.

## Contribution

A direct NCA reference, rather than an analogy from physical robot assembly.

## Key results

- Demonstrations include damage recovery and rotated perception.
- The implementation uses 16 state channels and stochastic per-cell update masking with probability 0.5 during training.

## Methods and models

Differentiable local rule, backpropagation through time, sample replay and image loss. Notebook links are provided; none was executed here.

## Limitations and open questions

Skimmed model, experiment descriptions and discussion; interactive models and linked notebooks not run. Image regeneration is not evidence of general task competence or physical hardware robustness.

## Relevance to us

Primary anchor for the NCA observatory. Compare [[etcheverry-2026-reasoning]] and the review [[ha-2022-collective]].

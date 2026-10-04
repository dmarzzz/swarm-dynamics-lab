---
id: kirkpatrick-2017-overcoming
type: paper
title: Overcoming catastrophic forgetting in neural networks
authors:
- James Kirkpatrick
- Razvan Pascanu
- Neil Rabinowitz
- Joel Veness
- Guillaume Desjardins
- Andrei A. Rusu
- Kieran Milan
- John Quan
- Tiago Ramalho
- Agnieszka Grabska-Barwinska
- Demis Hassabis
- Claudia Clopath
- Dharshan Kumaran
- Raia Hadsell
year: 2016
venue: arXiv preprint (v2, January 2017)
url: https://arxiv.org/abs/1612.00796
doi: null
arxiv: '1612.00796'
cite: Kirkpatrick, J., Pascanu, R., Rabinowitz, N., Veness, J., Desjardins, G., Rusu, A. A., Milan, K., Quan, J., Ramalho, T., Grabska-Barwinska, A., et al. (2016). Overcoming catastrophic forgetting in neural networks. arXiv preprint (v2, January 2017). arXiv:1612.00796.
topics:
- fork-merge-security
added_by: dmarz/fm
accessed: '2026-10-03'
read_depth: skim
relevance: 3
citations: null  # Semantic Scholar and OpenAlex rate-limited on 2026-10-03
code: []
---

## Summary

Elastic weight consolidation (EWC) lets a network learn tasks in sequence without catastrophic forgetting by adding, while learning a new task, a quadratic penalty that pulls each weight back toward its value after the old task, scaled by that weight's importance to the old task as estimated by the diagonal of the Fisher information matrix. Demonstrated on permuted-MNIST sequences and on a DQN agent learning ten Atari games in sequence. Read: abstract, introduction, the method section, the MNIST and Atari results, the Fisher-perturbation analysis and the start of the discussion.

## Contribution

Shows that forgetting is not inevitable in neural networks: protecting only the weights that matter for earlier tasks preserves them while leaving spare capacity for new ones, which uniform L2 anchoring does not.

## Key results

- Permuted MNIST: plain SGD forgot earlier tasks; uniform L2 anchoring protected task A but could not learn task B; EWC learned many permutations in sequence with modest error growth (measured, Figure 2).
- Atari, ten games in sequence: with plain gradient descent the agent never learned more than one game and total human-normalised score stayed below 1 (out of 10); with EWC it learned several games, though below ten separate DQNs (measured, Figure 3).
- Perturbing weights along the Fisher null space hurt performance as much as perturbing along the inverse Fisher, so the method over-estimates how unimportant some weights are (measured, Figure 3C).

## Methods and models

Laplace approximation of the posterior after task A; penalty sum_i (lambda/2) F_i (theta_i - theta*_A,i)^2; Forget-Me-Not task recognition in the Atari agent. Venue not stated on the arXiv page; arXiv v2, January 2017.

## Limitations and open questions

Diagonal Fisher approximation under-estimates parameter uncertainty (stated); sequential tasks with clear boundaries.

## Relevance to us

Background for Q2 in Sutton's continual-learning version of fork-merge ([[sutton-2025-father]]), where returned experience is absorbed into one set of weights. EWC shows the parent's existing knowledge can be protected against later updates in proportion to how much it matters, which is a dilution floor that works in the defender's favour: a returning part's updates that conflict with heavily weighted old knowledge are resisted. The flip side, documented in [[li-2024-badedit]], is that a corrupted update placed in weights the parent does not consider important (low Fisher) faces no resistance and survives later training. Related: [[espeholt-2018-impala]], [[meng-2022-mass-editing]].

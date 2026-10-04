---
id: miyato-2025-artificial
type: paper
title: Artificial Kuramoto Oscillatory Neurons
authors: [Takeru Miyato, Sindy Löwe, Andreas Geiger, Max Welling]
year: 2025
venue: International Conference on Learning Representations (ICLR 2025), oral
url: https://arxiv.org/abs/2410.13821
doi: null
arxiv: '2410.13821'
cite: "Miyato, T., Löwe, S., Geiger, A., & Welling, M. (2025). Artificial Kuramoto oscillatory neurons. In International Conference on Learning Representations (ICLR 2025). arXiv:2410.13821."
topics: [sync-consensus]
added_by: dmarz/sync-consensus
accessed: 2026-10-03
read_depth: abstract
relevance: 2
citations: null
code: []
---

## Summary

Replaces threshold units in neural networks with Artificial Kuramoto Oscillatory Neurons (AKOrN): each neuron is
a vector oscillator whose state evolves by a generalised Kuramoto update, so that neurons "bind" by synchronising.
AKOrN layers can use fully connected, convolutional or attention-style connectivity. The authors report
improvements on unsupervised object discovery, adversarial robustness, calibrated uncertainty and reasoning
tasks, and argue for dynamical (spatiotemporal) representations at the neuron level.

## Contribution

The most visible recent use of Kuramoto synchronisation inside deep learning (ICLR 2025 oral), connecting the
sync-consensus literature to ML architectures.

## Key results

- Abstract-level: performance gains across object discovery, robustness, uncertainty calibration and reasoning;
  specific numbers not read.

## Methods and models

Generalised (multi-dimensional) Kuramoto dynamics on unit vectors, related in spirit to the D-dimensional model
of [[chandra-2019-continuous]], unrolled as network layers. Code: https://github.com/autonomousvision/akorn
(linked from the arXiv page; not run).

## Limitations and open questions

Not read beyond the abstract; compute cost of unrolled oscillator dynamics and baseline strength unknown to us.
OpenAlex lists only a different-venue record, so no citation count is given.

## Relevance to us

Background for anyone framing an ML or LLM-agent architecture as coupled oscillators; low priority for physical
swarm work.

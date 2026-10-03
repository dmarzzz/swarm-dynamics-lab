---
id: blank-2026-subliminal
type: paper
title: "Subliminal Learning Is Steering Vector Distillation"
authors: ["Camila Blank", "Agam Bhatia", "Senthooran Rajamanoharan", "Arthur Conmy", "Neel Nanda"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2606.00995
doi: null
arxiv: "2606.00995"
cite: "Blank, C., Bhatia, A., Rajamanoharan, S., Conmy, A., & Nanda, N. (2026). Subliminal Learning Is Steering Vector Distillation. arXiv preprint arXiv:2606.00995."
topics: [fork-merge-security]
added_by: dmarz/fm-merge-poisoning
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Argues that subliminal learning is mediated by a single steering vector. In two open models, the teacher's trait system prompt is well approximated by a steering vector added to activations, and the student learns an aligned vector during fine-tuning. Prompts not well approximated by a steering vector are not subliminally learned. This is a special case of steering vector distillation, demonstrated for semantic and random vectors. Adaptive optimisers are needed: activation gradients on steered data carry a small consistent component along the steering direction that non-adaptive optimisers let outlier gradients drown.

## Contribution

Mechanistic account that also explains why transfer does not cross model families: the steering direction has model-specific effects.

## Key results

- Abstract-level: teacher system prompt approximated by one steering vector; student learns an aligned vector.
- Abstract-level: non-adaptive optimisers impede subliminal learning.

## Methods and models

Activation steering and fine-tuning analysis on two open-weight models (details not read).

## Limitations and open questions

Abstract only. Two models. Covers prompt-induced traits; fine-tuning-induced misalignment may not reduce to one vector.

## Relevance to us

Q3 and possible Q2 defence. If what returns is a direction in activation space, the parent can look for it: compare activations before and after integrating a part's data, and use non-adaptive optimisers for reintegration training. Related: [[cloud-2025-subliminal]], [[schrodi-2025-towards]].

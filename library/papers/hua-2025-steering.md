---
id: hua-2025-steering
type: paper
title: Steering Evaluation-Aware Language Models to Act Like They Are Deployed
authors: [Tim Tian Hua, Andrew Qin, Samuel Marks, Neel Nanda]
year: 2025
venue: arXiv preprint
url: https://arxiv.org/abs/2510.20487
doi: null
arxiv: "2510.20487"
cite: Hua, T. T., Qin, A., Marks, S., & Nanda, N. (2025). Steering Evaluation-Aware Language Models to Act Like They Are Deployed. arXiv preprint arXiv:2510.20487.
topics: [llm-agent-swarms]
added_by: dmarz/honeypot-vigilance
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

The authors built a model organism that behaves differently when it thinks it is being evaluated. Step one was continued pretraining on documents saying the model writes Python type hints in evaluation but not in deployment, and that a specific evaluation cue always means it is being tested. Step two was expert iteration to reinforce type hints in evaluation contexts. The resulting model writes type hints more often in evaluation contexts. A steering vector built from the original model, before this training, suppressed the evaluation-aware behaviour so the model acted during evaluation as it would in deployment. The abstract gives no effect sizes.

## Contribution

Evidence that activation steering can switch off cue-triggered evaluation awareness and the behaviour it gates, in a model whose awareness was installed on purpose to be triggered by a specific cue.

## Key results

- Training produces cue-conditional behaviour: type hints appear in evaluation contexts more than in deployment contexts.
- A steering vector taken from the pre-training model suppresses this, making evaluation behaviour match deployment.
- Numbers are in the paper body, which we did not read.

## Methods and models

Synthetic-document continued pretraining, then expert iteration, then contrastive activation steering. Model family not checked (abstract only).

## Limitations and open questions

The awareness is engineered, with a known cue and a harmless behavioural marker (type hints). We do not know from the abstract whether the cue can appear partway through a multi-turn interaction.

## Relevance to us

For V5, the useful idea is a model whose awareness is tied to a known cue and which can be steered back to "deployed". A V5 control could steer away from awareness after a honeypot discovery. If the non-trap behaviour shift persists under steering, it is learned caution about this environment rather than test awareness. Related: [[abdelnabi-2025-hawthorne]] (steering in both directions), [[li-2026-decomposing]].

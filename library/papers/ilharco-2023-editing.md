---
id: ilharco-2023-editing
type: paper
title: "Editing Models with Task Arithmetic"
authors: ["Gabriel Ilharco", "Marco Tulio Ribeiro", "Mitchell Wortsman", "Suchin Gururangan", "Ludwig Schmidt", "Hannaneh Hajishirzi", "Ali Farhadi"]
year: 2023
venue: "The Eleventh International Conference on Learning Representations (ICLR 2023)"
url: https://arxiv.org/abs/2212.04089
doi: null
arxiv: "2212.04089"
cite: "Ilharco, G., Ribeiro, M. T., Wortsman, M., Gururangan, S., Schmidt, L., Hajishirzi, H., & Farhadi, A. (2023). Editing Models with Task Arithmetic. In The Eleventh International Conference on Learning Representations (ICLR 2023). arXiv:2212.04089."
topics: [fork-merge-security]
added_by: dmarz/fm-merge-poisoning
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: 30  # OpenAlex cited_by_count, 2026-10-03; shadow/sol-g51
code: []
---

## Summary

Defines a task vector as fine-tuned weights minus pre-trained weights and shows these vectors can be combined arithmetically. Adding several task vectors yields one model good at several tasks; negating a task vector reduces performance on that task with little effect on control tasks; and analogies (A is to B as C is to D) let three task vectors improve a fourth task without its data. Experiments span several models, modalities and tasks.

## Contribution

Gives the merge operator used by most later merging attacks and defences: merged = pre-trained + sum of lambda_i times tau_i.

## Key results

- Addition of task vectors improves multi-task performance; negation removes a capability with little collateral change (abstract).
- Task analogies improve a held-out task with no data from it (abstract).

## Methods and models

Task vectors computed from CLIP and language models fine-tuned on separate tasks; scaling coefficients chosen on validation data.

## Limitations and open questions

Abstract only. Assumes shared pre-trained base. BadMerging ([[zhang-2024-badmerging]]) measures that task vectors from different domains are near-orthogonal (mean cosine 0.042), which is what lets a malicious vector pass through a merge mostly unchanged.

## Relevance to us

Formal model of the merge for Q2 and Q3. Each returning sub-agent contributes a vector; the parent chooses coefficients. Negation is also the basis of a defence (subtract a known-bad vector, see [[pawlak-2025-backdoor]]). Near-orthogonality means a corrupted part's contribution is not diluted by the others, so averaging gives little protection unless the coefficient on each part is small. Related: [[wortsman-2022-model]], [[yuan-2025-merge]].

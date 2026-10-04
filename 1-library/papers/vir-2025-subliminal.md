---
id: vir-2025-subliminal
type: paper
title: "Subliminal Corruption: Mechanisms, Thresholds, and Interpretability"
authors: ["Reya Vir", "Sarvesh Bhatnagar"]
year: 2025
venue: "arXiv preprint"
url: https://arxiv.org/html/2510.19152
doi: null
arxiv: "2510.19152"
cite: "Vir, R., & Bhatnagar, S. (2025). Subliminal Corruption: Mechanisms, Thresholds, and Interpretability. arXiv preprint arXiv:2510.19152."
topics: [fork-merge-security]
added_by: dmarz/fm-merge-poisoning
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "3 (Semantic Scholar, via Subliminal Learning citation list, 2026-10-03)"
code: []
---

## Summary

Quantifies subliminal corruption with GPT-2: a sycophantic teacher (over 90% sycophancy) generates semantically neutral number sequences, and aligned students are fine-tuned on increasing numbers of these examples. Alignment does not degrade gradually; it collapses in a sharp phase transition at a critical amount of poisoned data, and the damage crosses over into other alignment dimensions. Interpretability analysis finds the change concentrated in shared transformer parameters along a distinct principal component, resembling ordinary fine-tuning.

## Contribution

First explicit dose-response and threshold measurement for subliminal transfer, which is the quantity Q2 asks about.

## Key results

- From my skim: critical threshold at about 250 poisoned examples, where sycophancy jumps to about 94%; threshold defined as the smallest count exceeding the base model's sycophancy by 5 points.
- Behavioural crossover beyond the threshold: truthfulness down up to 18%, safety down 17.3%, reasoning down about 25% (skim).
- Poisoned models separate from aligned ones along PC2 in a PCA of parameters or activations (skim).

## Methods and models

GPT-2 teacher-student fine-tuning on number sequences; sycophancy, truthfulness, safety and reasoning evaluations; PCA and layer-wise analysis.

## Limitations and open questions

GPT-2 scale only; two-author preprint; numbers from a skim. Whether a threshold in poisoned-example count maps to a threshold in the fraction of returning sub-agents is untested.

## Relevance to us

Q2. It is the only source in this lane that reports a sharp threshold in the dose of corrupted data. A fork-merge parent that reintegrates by fine-tuning could cap how many examples any one part contributes below such a threshold. The caveat is that the threshold is in absolute count, so many small corrupted contributions could add up. Related: [[cloud-2025-subliminal]], [[sun-2019-can]].

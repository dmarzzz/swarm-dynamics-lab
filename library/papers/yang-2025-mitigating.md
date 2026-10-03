---
id: yang-2025-mitigating
type: paper
title: "Mitigating the Backdoor Effect for Multi-Task Model Merging via Safety-Aware Subspace"
authors: ["Jinluan Yang", "Anke Tang", "Didi Zhu", "Zhengyu Chen", "Li Shen", "Fei Wu"]
year: 2025
venue: "The Thirteenth International Conference on Learning Representations (ICLR 2025)"
url: https://arxiv.org/abs/2410.13910
doi: null
arxiv: "2410.13910"
cite: "Yang, J., Tang, A., Zhu, D., Chen, Z., Shen, L., & Wu, F. (2025). Mitigating the Backdoor Effect for Multi-Task Model Merging via Safety-Aware Subspace. In The Thirteenth International Conference on Learning Representations (ICLR 2025). arXiv:2410.13910."
topics: [fork-merge-security]
added_by: dmarz/fm-merge-poisoning
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "17 (Semantic Scholar, via BadMerging citation list, 2026-10-03)"
code: []
---

## Summary

Identifies two failure modes when backdoored models are merged: backdoor succession (the merged model inherits the backdoor) and backdoor transfer (the backdoor spreads to other tasks). Proposes Defense-Aware Merging (DAM), which uses meta-learning with two alternately optimised masks: a task-shared mask that keeps parameters useful across tasks, and a backdoor-detection mask that isolates potentially harmful parameters. DAM reduces attack success by 2-10 percentage points relative to existing merge methods at about a 1% accuracy cost, and is reported robust to the number of compromised models.

## Contribution

A merge-aware defence: the merge itself is optimised to exclude a suspicious subspace rather than relying on dilution.

## Key results

- ASR reduced by 2-10 percentage points versus existing merging methods at about 1% accuracy cost (abstract).
- Robust across backdoor types and the number of compromised models in the merge (abstract).

## Methods and models

Dual-mask meta-learning over task vectors (details not read). Code: github.com/Yangjinluan/DAM (not opened).

## Limitations and open questions

Abstract only. A 2-10 point reduction is modest; whether DAM holds against [[zhang-2024-badmerging]] or [[yuan-2025-merge]] specifically was not checked.

## Relevance to us

Q2 defence side. The 'number of compromised models' sweep is the k-of-n question in weight space, so the paper's figures are worth reading in full for the survey. The modest effect size suggests subspace filtering alone will not give a hard threshold. Related: [[arora-2024-here]], [[pawlak-2025-backdoor]].

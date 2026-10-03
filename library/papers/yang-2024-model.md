---
id: yang-2024-model
type: paper
title: "Model Merging in LLMs, MLLMs, and Beyond: Methods, Theories, Applications and Opportunities"
authors: ["Enneng Yang", "Li Shen", "Guibing Guo", "Xingwei Wang", "Xiaochun Cao", "Jie Zhang", "Dacheng Tao"]
year: 2024
venue: "arXiv preprint"
url: https://arxiv.org/abs/2408.07666
doi: null
arxiv: "2408.07666"
cite: "Yang, E., Shen, L., Guo, G., Wang, X., Cao, X., Zhang, J., & Tao, D. (2024). Model Merging in LLMs, MLLMs, and Beyond: Methods, Theories, Applications and Opportunities. arXiv preprint arXiv:2408.07666."
topics: [fork-merge-security, meta]
added_by: dmarz/fm-merge-poisoning
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "315 (Semantic Scholar, via BadMerging citation list, 2026-10-03)"
code: []
---

## Summary

Comprehensive survey of model merging. It proposes a taxonomy of merging methods, discusses theory, and reviews applications in LLMs, multimodal LLMs and more than ten other machine-learning subfields such as continual, multi-task and few-shot learning, then lists open challenges. A maintained paper list accompanies it on GitHub.

## Contribution

The main review article for model merging; it frames merging as a general technique rather than a niche trick, which is why merge-time security matters.

## Key results

- Taxonomy and application review; no new experiments (abstract).

## Methods and models

Literature survey. Paper list at github.com/EnnengYang/Awesome-Model-Merging-Methods-Theories-Applications (not opened).

## Limitations and open questions

Abstract only. Security is a small part of the survey; dedicated attack work is catalogued separately here.

## Relevance to us

Review article for the merge operator in the fork-merge picture. Useful when choosing which merge algorithms to test thresholds against in Q2 (task arithmetic, TIES, DARE, RegMean, AdaMerging). Related: [[ilharco-2023-editing]], [[zhang-2024-badmerging]].

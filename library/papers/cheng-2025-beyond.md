---
id: cheng-2025-beyond
title: 'Beyond Binary: Towards Fine-Grained LLM-Generated Text Detection via Role
  Recognition and Involvement Measurement'
authors:
- Zihao Cheng
- Li Zhou
- Feng Jiang
- Benyou Wang
- Haizhou Li
year: 2025
venue: Proceedings of the ACM Web Conference 2025
url: https://arxiv.org/abs/2410.14259
doi: 10.1145/3696410.3714770
arxiv: '2410.14259'
cite: 'Cheng, Z., Zhou, L., Jiang, F., Wang, B., & Li, H. (2025). Beyond Binary: Towards
  Fine-Grained LLM-Generated Text Detection via Role Recognition and Involvement Measurement.
  Proceedings of the ACM Web Conference 2025. https://doi.org/10.1145/3696410.3714770.'
topics:
- swarm-detection
read_depth: skim
relevance: 3
type: paper
added_by: shadow/sol-w1
accessed: '2026-10-03'
citations: null
code: []
---

## Summary

Cheng and colleagues replace binary human-versus-LLM text labels with role recognition and continuous involvement measurement for hybrid writing. Their LLMDetect benchmark combines a Hybrid News Detection Corpus with cross-context and variable-intensity evaluations. Ten baselines are compared, with fine-tuned pretrained-language-model detectors outperforming zero-shot LLM methods in the reported evaluation. This models assistance in producing text rather than determining whether its author is an automated account.

## Contribution

Defines finer-grained provenance tasks and benchmarks for mixed human-machine authorship, avoiding a false binary for AI-assisted writing.

## Key results

- Ten baseline detectors evaluated.
- DetectEval covers five cross-context variations and two within-role intensity variations.
- Introduction reports DeBERTa strongest for cross-context generalization and Longformer strongest for varying intensity; numerical score tables were not read.
- Involvement ratio is defined as generated-or-edited text length divided by final text length, in [0,1].

## Methods and models

Read the abstract, introduction, related work, and task definitions through the start of benchmark construction in the version-2 HTML. Role recognition is multiclass prediction; involvement measurement minimizes squared error on the length-based involvement ratio. Complete author list and WWW 2025 DOI were verified from the source. The source links https://github.com/ZihaoCheng123/LLMDetect for data and code; that repository was not opened or run, so no library code ID is asserted.

## Limitations and open questions

Content provenance is not proof of automation, coordination, deceptive intent, or common control. Editing-length ratios are only one operationalization of contribution and can underrepresent semantic changes. The results described in the introduction need full-table and split-protocol checks; domain, language, and newer-model generalization remain open at this reading depth.

## Relevance to us

Useful when analyzing cyborg or mixed-authorship accounts, but should supplement behavior/network evidence such as [[ng-2025-global]] rather than act as a standalone swarm detector. Distinguishing collaboration from full generation also helps avoid mislabeling benign assistance as inauthentic coordination.

---
id: "min-2023-factscore"
type: "paper"
title: "FActScore: Fine-grained Atomic Evaluation of Factual Precision in Long Form Text Generation"
authors: ["Sewon Min", "Kalpesh Krishna", "Xinxi Lyu", "Mike Lewis", "Wen-tau Yih", "Pang Wei Koh", "Mohit Iyyer", "Luke Zettlemoyer", "Hannaneh Hajishirzi"]
year: 2023
venue: "arXiv preprint"
url: "https://arxiv.org/abs/2305.14251"
doi: null
arxiv: "2305.14251"
cite: "Sewon Min, Kalpesh Krishna, Xinxi Lyu, Mike Lewis, Wen-tau Yih, Pang Wei Koh, Mohit Iyyer, Luke Zettlemoyer, Hannaneh Hajishirzi. (2023). FActScore: Fine-grained Atomic Evaluation of Factual Precision in Long Form Text Generation. arXiv preprint. arXiv:2305.14251."
topics: ["llm-agent-swarms"]
added_by: "vishesh/codex-village-fit"
accessed: "2026-10-04"
read_depth: "abstract"
relevance: 5
citations: null
code: []
---

## Summary

Evaluates generated text by decomposing it into atomic facts and measuring support from reliable sources. This avoids reducing mixed factual and unsupported content to a single text-level judgment, while retrieval and evaluation introduce their own errors.

## Contribution

Use atomic claim fields and source evidence, but keep completeness and provenance distinct from precision.

## Key results

Source-reported findings summarized above; no reproduction claimed.

## Methods and models

See the linked source; read scope is recorded explicitly.

## Limitations and open questions

Abstract read; source-support scores do not establish transmission ancestry or actor visibility.

## Relevance to us

[Telephone design](../../researchers/vishesh/notes/telephone/README.md) builds on this source and [[data-ai-village-2026]].

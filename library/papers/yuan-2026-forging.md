---
id: yuan-2026-forging
type: paper
title: "Forging LLM Authorship Fingerprints with Targeted Rewriting"
authors: ["Haohan Yuan", "Simin Chen", "Xi Niu", "Hanqing Guo", "Depeng Xu", "Haopeng Zhang"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2609.38831
doi: null
arxiv: "2609.38831"
cite: "Yuan, H., Chen, S., Niu, X., Guo, H., Xu, D., & Zhang, H. (2026). Forging LLM Authorship Fingerprints with Targeted Rewriting. arXiv:2609.38831."
topics: [swarm-detection]
added_by: dmarz/sd-attribution
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

Studies targeted fingerprint transfer: rewriting one model's output so that attribution classifiers assign it to a chosen target model. ForgePrint searches for rewrites that shift attribution, then distils them into a one-pass 4B student. On CNN/DM summarisation the student reaches 70.2% target success against held-out classifiers it never queried, versus 54.1% for its teacher and 39.3% for the best of six published rewriting baselines, and 68.3% when moving open-model summaries toward commercial models.

## Contribution

Shows text-only model attribution can be forged, not just evaded: an operator can frame another model.

## Key results

- Student 70.2% target success on CNN/DM vs teacher 54.1% and best baseline 39.3% (abstract).
- 68.3% target success transferring open-model summaries toward chosen commercial models (abstract).

## Methods and models

Search-then-distil rewriting framework; held-out attribution classifiers; summarisation as controlled setting.

## Limitations and open questions

Summarisation only; conversational and agentic traces untested. Abstract-only reading.

## Relevance to us

Direct counter-evidence to relying on text attribution such as [[sun-2025-idiosyncrasies]] for operator linking; behavioural and structural signals ([[wang-2026-who]], [[park-2026-cross]]) are harder targets. Related evasion: [[nasery-2025-are]].

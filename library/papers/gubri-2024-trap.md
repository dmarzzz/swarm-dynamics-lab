---
id: gubri-2024-trap
type: paper
title: "TRAP: Targeted Random Adversarial Prompt Honeypot for Black-Box Identification"
authors: ["Martin Gubri", "Dennis Ulmer", "Hwaran Lee", "Sangdoo Yun", "Seong Joon Oh"]
year: 2024
venue: "Findings of the Association for Computational Linguistics: ACL 2024; arXiv preprint"
url: https://arxiv.org/abs/2402.12991
doi: null
arxiv: "2402.12991"
cite: "Gubri, M., Ulmer, D., Lee, H., Yun, S., & Oh, S. J. (2024). TRAP: Targeted Random Adversarial Prompt Honeypot for Black-Box Identification. Findings of the Association for Computational Linguistics: ACL 2024. arXiv:2402.12991."
topics: [swarm-detection]
added_by: dmarz/sd-attribution
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "47 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

Defines Black-box Identity Verification: deciding whether a third-party chat application runs a specific LLM. TRAP repurposes GCG-style adversarial suffixes so that the target model returns a pre-chosen answer (for example a specific random number) while other models answer randomly. The paper reports over 95% true positive rate at under 0.2% false positive rate after a single interaction, and robustness to minor model changes.

## Contribution

A one-query identity check built from adversarial optimisation: a honeypot prompt that only one model answers in a fixed way.

## Key results

- Over 95% TPR at under 0.2% FPR with one interaction (abstract).
- Remains effective when the target model has minor changes that do not alter its function (abstract).

## Methods and models

Optimise an adversarial suffix on the target model (white-box access to the reference model needed at construction time) so that the target outputs a chosen answer; query the suspect application once and compare.

## Limitations and open questions

Verifies one candidate model at a time and needs white-box access to that candidate to build the suffix. Suffixes are conspicuous and could be filtered. Evasion by fine-tuning is only partly studied per the abstract.

## Relevance to us

A cheap yes/no test for "is this account running model X?", useful once [[pasquini-2024-llmmap]]-style screening narrows the candidates. The single-query cost suits mass screening of suspected swarm accounts. Robustness concerns: [[nasery-2025-are]].

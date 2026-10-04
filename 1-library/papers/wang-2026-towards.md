---
id: wang-2026-towards
type: paper
title: Towards Detecting AI-Assisted Responses in Online Surveys
authors:
- Qizhou Wang
- Bogdan Mamaev
- Christopher Leckie
year: 2026
venue: EMNLP 2026 (Main Conference)
url: https://arxiv.org/abs/2609.17317
doi: null
arxiv: '2609.17317'
cite: Wang, Q., Mamaev, B., & Leckie, C. (2026). Towards Detecting AI-Assisted Responses in Online Surveys. In Proceedings of EMNLP 2026. arXiv:2609.17317.
topics:
- swarm-detection
added_by: dmarz/sd-honeypots
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

Introduces ASURRE, a benchmark of AI-assisted survey participation strategies (full generation, revision, persona-grounded agentic completion) generated with several LLMs on three real surveys and paired with genuine human responses. Existing machine-generated-text detectors catch naive AI use but fall toward chance against persona-grounded agents that mimic whole respondents. Agentic completion still leaves respondent-level behavioural traces, and a few-shot, training-free aggregator over these cues raises mean AUROC by 0.14 over the best existing detector in agentic settings.

## Contribution

A negative result for text-level detection of agents and a partial fix that uses respondent-level consistency cues.

## Key results

- Persona-grounded agents push MGT detectors to near chance (measured).
- Training-free cue aggregator: +0.14 mean AUROC over best detector across agentic settings (measured).
- Individual cues can be evaded by targeted prompting (measured).

## Methods and models

Benchmark construction across usage strategies and LLMs; evaluation of MGT detectors; few-shot aggregator. Abstract-level read.

## Limitations and open questions

Abstract only; synthetic agents built by the authors.

## Relevance to us

Evidence that per-message detectors fail against persona agents, pushing detection toward traps and cross-response consistency. Related: [[xu-2026-penny]], [[ayzenshteyn-2025-cloak]].

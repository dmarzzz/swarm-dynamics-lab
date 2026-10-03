---
id: alavi-2025-more
type: paper
title: More Agents Improve Math Problem Solving but Adversarial Robustness Gap Persists
authors:
- Khashayar Alavi
- Zhastay Yeltay
- Lucie Flek
- Akbar Karimi
year: 2025
venue: arXiv preprint
url: https://arxiv.org/abs/2511.07112
doi: null
arxiv: '2511.07112'
cite: 'Alavi, K., Yeltay, Z., Flek, L., & Karimi, A. (2025). More Agents Improve Math Problem Solving but Adversarial Robustness Gap Persists. arXiv preprint arXiv:2511.07112.'
topics:
- fork-merge-security
- llm-agent-swarms
added_by: dmarz/fm-bft-aggregation
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Tests whether sampling-and-voting ensembles (Agent Forest) of n agents are more robust to adversarially perturbed math questions than one agent. Six open models (Qwen3-4B/14B, Llama3.1-8B, Mistral-7B, Gemma3-4B/12B) on GSM8K, MATH, MMLU-Math and MultiArith, with n from 1 to 25, under punctuation noise (10, 30, 50 percent) and human-like typos (WikiTypo, R2ATA). Accuracy rises with n, mostly from n = 1 to 5 and little beyond about 10, but the gap between clean and perturbed accuracy, and the attack success rate, stay roughly constant as n grows.

## Contribution

Evidence that majority voting over agents who all see the same perturbed input averages away sampling noise but not input-borne corruption.

## Key results

- Reported in abstract: largest accuracy gains from n = 1 to 5; diminishing beyond n of about 10.
- Reported in abstract: human-typo perturbations give the largest gap and highest ASR even with many agents.
- Reported in abstract: the robustness gap persists regardless of agent count.

## Methods and models

Agent Forest sampling and majority vote; perturbation families as above. Only the abstract was read.

## Limitations and open questions

Perturbations are noise and typos, not targeted injections; all agents share one model per run.

## Relevance to us

Q2. A clean demonstration of the shared-input failure: when every voter reads the same corrupted input, adding voters does not reduce the attack success rate. In fork-merge terms, k-of-n over sub-agents that explored the same hostile source gives no protection against that source. Stronger targeted version: [[liu-2026-consensus]]. Correlation background: [[kim-2025-correlated]].

---
id: liu-2026-towards
type: paper
title: Towards Direct Latent-Space Synthesis for Parallel Branches in LLM-Agent Workflows
authors:
- Shikun Liu
- Mufei Li
- Dongqi Fu
- Haoyu Wang
- Yinglong Xia
- Hong Li
- Hong Yan
- Pan Li
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2606.14672
doi: null
arxiv: '2606.14672'
cite: Liu, S., Li, M., Fu, D., Wang, H., Xia, Y., Li, H., Yan, H., & Li, P. (2026). Towards Direct Latent-Space Synthesis for Parallel Branches in LLM-Agent Workflows. arXiv preprint. arXiv:2606.14672.
topics:
- fork-merge-security
- llm-agent-swarms
added_by: dmarz/fm
accessed: '2026-10-03'
read_depth: skim
relevance: 3
citations: null  # Semantic Scholar and OpenAlex rate-limited on 2026-10-03
code: []
---

## Summary

Parallel-Synthesis lets a synthesizer agent merge the work of parallel worker agents by consuming their KV caches directly instead of reading their concatenated text outputs. A cache mapper calibrates the independently generated branch caches (which were produced without seeing each other), and a fine-tuned adapter teaches the synthesizer to generate from this non-sequential cache interface, trained on data that exposes it to parallel caches and distils behaviour from text-based synthesis. Evaluated with Qwen3-14B on AIME 2024/2025, GSM8K, HumanEval-Plus, MBPP-Plus, GPQA, MedQA, GAIA and a MARBLE database-diagnosis task, with 3 or 5 workers, against single-trajectory, voting, text concatenation and cache-merging baselines (APE, CacheBlend, KVLINK). Read: abstract, introduction, experiment set-up and main results tables.

## Contribution

A working fork-and-merge interface for LLM agents in which branches return latent state rather than text, matching text-based synthesis on most tasks at much lower latency.

## Key results

- Matched or beat text-concatenation synthesis on 7 of 9 data sets, for example AIME 2025 46.67 versus 23.33 and GSM8K 94.69 versus 92.80; slightly lower on MBPP-Plus (80.42 vs 81.75) and GAIA (measured, Tables 1-2).
- Time to first token reduced by 2.5 to 11 times (measured, per abstract and Figure 3).
- Generic cache-merging methods (APE, CacheBlend) performed far worse than text synthesis, so calibration and adapter training are what make cache merging work (measured).

## Methods and models

Qwen3-14B backbone; cache mapper plus synthesizer adapter; out-of-domain evaluation relative to post-training data. No security evaluation.

## Limitations and open questions

The paper does not consider faulty or adversarial workers. Workers and synthesizer share one model family.

## Relevance to us

Q3 and Q2, as an emerging merge channel rather than a security result: this is the first catalogued mechanism where returning parts hand the parent their internal state (KV caches) instead of text. That removes the parent's ability to read, filter or quote what a part returns before it is absorbed, which defeats every text-level merge check discussed in this library (warnings, provenance tags, content filters), and it offers an attacker a continuous channel analogous to the adversarial-image viruses in [[gu-2024-agent]] and [[ma-2026-catching]]. Whether adversarial KV caches can steer the synthesizer is untested here and is an open experimental question for this project (inference). Q2: the voting baseline (answer-level majority over workers) is the simple k-of-n alternative; it lost accuracy on hard maths but is the only merge here with an obvious threshold. Related: [[papadopoulos-2026-mind]], [[fang-2025-provably]].

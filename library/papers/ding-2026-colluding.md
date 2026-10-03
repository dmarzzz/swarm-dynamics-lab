---
id: ding-2026-colluding
type: paper
title: "Colluding LoRA: A Compositional Vulnerability in LLM Safety Alignment"
authors: ["Sihao Ding"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/html/2603.12681
doi: null
arxiv: "2603.12681"
cite: "Ding, S. (2026). Colluding LoRA: A Compositional Vulnerability in LLM Safety Alignment. arXiv preprint arXiv:2603.12681."
topics: [fork-merge-security]
added_by: dmarz/fm-merge-poisoning
accessed: 2026-10-03
read_depth: skim
relevance: 5
citations: "2 (Semantic Scholar, via BadMerging citation list, 2026-10-03)"
code: []
---

## Summary

CoLoRA builds LoRA adapters that each look benign and functional alone, but when a specific set is linearly composed the model's refusals are broadly suppressed and it complies with harmful requests under ordinary prompts, with no input trigger. Tested on Llama3-8B-Instruct, Qwen2.5-7B-Instruct and Gemma2-2B-It, mainly with two adapters and up to four. The author argues unit-level verification cannot scale because checking N adapters for k-way collusion needs on the order of N^k evaluations.

## Contribution

Names composition-triggered failure and gives the combinatorial argument for why per-module checks miss it.

## Key results

- From my skim: individual adapters 0% ASR on AdvBench; composed pair 98.2-100% ASR judged by LlamaGuard3 across the three models.
- False refusal on benign tasks 0.4-3.0% (skim).
- Mismatched pairs (one colluding adapter plus an unrelated benign one) give 16.4% and 4.3% ASR, so the specific combination is needed (skim, Table 4).
- SafeLoRA and PEFTGuard classify the individual colluding adapters as benign (skim).

## Methods and models

LoRA adapters trained so each is benign alone and the sum suppresses refusal; N-way collusion up to 4 adapters.

## Limitations and open questions

Single-author preprint, revised once. Linear composition only. Numbers from a skim.

## Relevance to us

Q2 and Q1. It is the cleanest demonstration that an adversary who controls k parts can make the merge fail while every part passes inspection, so a k-of-n protocol must check the composed result, not only the parts. The O(N^k) argument also gives a quantitative handle on Q1: if the parent picks which parts to recombine at random from a large pool, an attacker must corrupt the specific subset that will meet, and the chance of that falls combinatorially. Related: [[li-2026-when]], [[yuan-2025-merge]].

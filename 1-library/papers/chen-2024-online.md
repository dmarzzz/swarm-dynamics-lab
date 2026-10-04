---
id: chen-2024-online
type: paper
title: Online Detection of LLM-Generated Texts via Sequential Hypothesis Testing by Betting
authors:
- Can Chen
- Jun-Kun Wang
year: 2024
venue: ICML 2025 (per Semantic Scholar); arXiv preprint
url: https://arxiv.org/abs/2410.22318
doi: null
arxiv: '2410.22318'
cite: Chen, C., & Wang, J.-K. (2024). Online Detection of LLM-Generated Texts via Sequential Hypothesis Testing by Betting. arXiv:2410.22318.
topics:
- swarm-detection
added_by: dmarz/sd-ai-content
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 13 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Frames detection as an online problem: a source (news site, social media account, forum) publishes texts in a stream and the goal is to decide quickly whether the source is an LLM. Uses sequential hypothesis testing by betting on top of existing offline detector scores, giving a controlled false-positive rate and a bound on the expected time to flag an LLM source.

## Contribution

Source-level, anytime-valid detection with statistical guarantees, which is the account-level formulation swarm detection needs.

## Key results

- Shown (abstract): controlled type-I error and expected detection time for LLM sources; experiments support effectiveness (no numbers in abstract).

## Methods and models

Testing-by-betting (e-process) wrapper around offline detector scores. Abstract read only.

## Limitations and open questions

Assumes a source is wholly LLM or wholly human; mixed or human-in-the-loop accounts are not covered in the abstract. Abstract depth.

## Relevance to us

Directly reusable as a per-account monitor in a swarm detector: stream posts, bet on detector scores, flag when wealth exceeds 1/alpha. Theory basis: [[chakraborty-2023-possibilities]].

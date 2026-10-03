---
id: gh-spaddle-boat-maxshapley
type: code
title: 'MaxShapley: Shapley attribution of retrieved sources in generative search'
repo: spaddle-boat/MaxShapley
url: https://github.com/spaddle-boat/MaxShapley
authors:
- 'Sara Patel'
- 'Mingxun Zhou'
- 'Giulia Fanti'
year: 2025
language: Python
license: BSD-3-Clause-Clear
stars: 3
last_commit: 2026-07-14
topics:
- sybil-resistance
- llm-agent-swarms
added_by: dmarz/sybil-mechanisms
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers:
- patel-2025-maxshapley
---

## Summary

Official implementation of [[patel-2025-maxshapley]]. It computes Shapley attributions of source documents for multi-source question answering with MaxShapley and baselines (exact Shapley, Monte Carlo uniform and antithetic, leave-one-out, KernelSHAP), using OpenAI or Anthropic models as the scoring LLM, and ships re-annotated HotPotQA, MuSiQUE and MS MARCO subsets.

## What it can do for us

A working attribution pipeline in which to test splitting attacks: submit near-duplicate documents under different owners and measure how much extra credit the owner receives under the equal-split max game, then compare with owner-level aggregation in the spirit of [[ohta-2008-anonymity]].

## Run notes

Not run. README: pip install -r requirements.txt, set OPENAI_API_KEY and ANTHROPIC_API_KEY, then python calculate_shapley.py --dataset hotpot --index 5 --llm anthropic --shapley_methods MaxShapley. A batched scorer is reported in the README as 1.85x faster with 44% fewer tokens and an 11% quality drop.

## Limitations

Needs paid LLM API keys. Research code with three stars. No adversarial or strategic-provider evaluation.

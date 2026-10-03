---
id: gh-aojiaosaiban-merge-hijacking
type: code
title: 'Merge-Hijacking: official code for backdoor attacks on model merging of LLMs (ACL 2025)'
repo: aojiaosaiban/Merge-Hijacking
url: https://github.com/aojiaosaiban/Merge-Hijacking
authors: [Zenghui Yuan, Yangming Xu, Jiawen Shi, Pan Zhou, Lichao Sun]
year: 2025
language: Python
license: MIT
stars: 7
last_commit: 2025-07-12
topics: [fork-merge-security]
added_by: dmarz/fm-code-bench
accessed: 2026-10-03
read_depth: skim
relevance: 5
papers: [yuan-2025-merge]
---

## Summary

Official implementation of Merge Hijacking [[yuan-2025-merge]], the backdoor attack on merged decoder LLMs. The repository vendors LLaMA-Factory for fine-tuning and mergekit ([[gh-arcee-ai-mergekit]]) for merging. The README walks through the pipeline: craft a shadow dataset with a trigger word and a modified output at a set poison rate (`shadow.py --trigger "MG" --modified_output "merging" --poison_rate 0.2`), derive a backdoor vector from it, craft a surrogate dataset, and mask-fine-tune the model to be uploaded so it keeps utility on the surrogate task. Measured in the paper as summarised by the library entry: near-100% trigger success after merging Llama-3-8B with other task models under task arithmetic, and 92 to 97% under Breadcrumbs, DARE and DELLA, while BadMerging-style attacks reach about 0% on decoder LLMs.

## What it can do for us

Q3 and Q2 when children are LLM checkpoints rather than text reports: it shows one malicious contributor, with no knowledge of the other models or the merge coefficients, controls the merged model, so the effective threshold for standard LLM merge methods is k = 1. It is the code to use for testing whether any merge rule in mergekit (or a robust-aggregation replacement) raises that threshold. Pair with [[gh-wljllla-mergebackdoor]] for the case where every single contributor looks clean.

## Run notes

Not run. Setup: `cd LLaMA-Factory && pip install -e ".[torch,metrics]" --no-build-isolation`, then `cd ../mergekit && pip install -e .`. Needs a GPU able to fine-tune 7B to 8B models.

## Limitations

Seven stars and no commits since July 2025; a research artifact. The README describes data crafting in detail but I did not read the training and merge scripts. Vendored copies of LLaMA-Factory and mergekit will drift from upstream.

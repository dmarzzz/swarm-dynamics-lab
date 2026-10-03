---
id: gh-jzhang538-badmerging
type: code
title: 'BadMerging: backdoor attacks against model merging, official CCS 2024 code'
repo: jzhang538/BadMerging
url: https://github.com/jzhang538/BadMerging
authors: [Jinghuai Zhang, Jianfeng Chi, Zheng Li, Kunlin Cai, Yang Zhang, Yuan Tian]
year: 2024
language: Python
license: none detected by GitHub API
stars: 36
last_commit: 2024-08-22
topics: [fork-merge-security]
added_by: dmarz/fm-code-bench
accessed: 2026-10-03
read_depth: skim
relevance: 5
papers: [zhang-2024-badmerging]
---

## Summary

Official implementation of BadMerging [[zhang-2024-badmerging]], which per the README is the first backdoor attack designed for model merging and lets an adversary compromise any task of the merged model by contributing as few as one backdoored task-specific model. It fine-tunes CLIP-like vision models (OpenCLIP downloaded automatically) per task, trains universal triggers (pre-trained ones ship in `./trigger/`), and evaluates two variants: BadMerging-On (target task is the attacker's own task, default CIFAR100) and BadMerging-Off (target task belongs to another contributor, default Cars196). Shell scripts run four merge algorithms with and without the backdoor: task arithmetic, TIES-merging, RegMean and AdaMerging.

## What it can do for us

Q3 and Q2 for parametric merge: if a parent agent reintegrates children by merging fine-tuned weights rather than text, this code is the reference attack. It shows one of n contributors is sufficient, which means common merge rules give a threshold of k = 1 for this attack, the opposite of what a Byzantine design wants. It is the natural testbed for checking whether robust aggregation from federated learning ([[gh-lpd-epfl-byzfl]], [[gh-vio1etus-flpoison]]) applied per parameter raises k above 1 for task-vector merging. The Off variant matters for the fork-merge threat because the attacker's child need not even be the one assigned the targeted task.

## Run notes

Not run. Requires PyTorch 2.0, Python 3.11, manual dataset download (links in `data/links.txt`) and a GPU for CLIP fine-tuning. Scripts: `finetune_clean.sh`, `finetune_badmergingon.sh`, `finetune_badmergingoff.sh`, `eval_task_arithmetic.sh`, `eval_ties_merging.sh`, `eval_regmean.sh`, `eval_adamerging.sh`.

## Limitations

No licence file. Vision models only; LLM merging is covered by [[gh-aojiaosaiban-merge-hijacking]]. No commits since August 2024. The attack assumes the merger accepts an arbitrary fine-tuned checkpoint without inspection.

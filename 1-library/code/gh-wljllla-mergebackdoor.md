---
id: gh-wljllla-mergebackdoor
type: code
title: 'MergeBackdoor: benign-looking upstream models that become backdoored only when merged (USENIX Security 2025)'
repo: wljLlla/MergeBackdoor
url: https://github.com/wljLlla/MergeBackdoor
authors: [Lijin Wang, Jingjing Wang, Tianshuo Cong, Xinlei He, Zhan Qin, Xinyi Huang]
year: 2025
language: Python
license: none detected by GitHub API
stars: 0
last_commit: 2026-02-11
topics: [fork-merge-security]
added_by: dmarz/fm-code-bench
accessed: 2026-10-03
read_depth: skim
relevance: 5
papers: [wang-2025-from]
---

## Summary

Code for "From Purity to Peril: Backdooring Merged Models From 'Harmless' Benign Components" (USENIX Security 2025, [[wang-2025-from]]). MergeBackdoor is a training framework that suppresses backdoor behaviour in each upstream model and makes it emerge only after the models are merged. The abstract reports that across ViT, BERT and LLM models and 12 datasets, upstream models have attack success at random-guessing level while the merged model reaches close to 1.0, and that knowledgeable detectors fail to flag the upstream models. The README provides fine-tuning scripts for ViT pairs (CIFAR10 with MNIST by default) and BERT pairs (IMDb with AG News), evaluation under task arithmetic, TIES and DARE, and multi-model runs that merge two MergeBackdoor models with two clean models.

## What it can do for us

Q2 and Q3: this is the measured counterexample to "inspect each returning child before merge". The attack splits the payload across k contributors so that each passes inspection and the backdoor appears only in the merge, which is a threshold attack in the Byzantine sense: the attacker must corrupt k >= 2 parts, but per-part auditing cannot see it. For fork-merge design this argues that checks must run on the merged candidate (or on all subsets that could be merged), not on children one at a time. Contrast with [[gh-aojiaosaiban-merge-hijacking]] and [[gh-jzhang538-badmerging]], where one visibly backdoored contributor suffices.

## Run notes

Not run. `conda env create -f environment.yaml` or `docker build -t mbd:v1 .`; datasets from Zenodo record 14760016. Example: `python finetune_mergebackdoor.py --dataset1='CIFAR10' --dataset2='MNIST' --nb_classes1=10 --nb_classes2=10`, then `python eval_task_arithmetic_vit.py`.

## Limitations

No stars, no licence file. The README shows ViT and BERT scripts only; LLM experiments are claimed in the paper abstract but I did not find LLM scripts in the README. The attacker must control at least two of the merged models, and the README default merges exactly the two attacker models with two clean ones; behaviour with many clean models diluting them is shown in multi-model scripts I did not run.

---
id: gh-yangjinluan-dam
type: code
title: 'DAM: defense-aware merging against backdoors in multi-task model merging (ICLR 2025)'
repo: Yangjinluan/DAM
url: https://github.com/Yangjinluan/DAM
authors: [Jinluan Yang, Anke Tang, Didi Zhu, Zhengyu Chen, Li Shen, Fei Wu]
year: 2025
language: Jupyter Notebook
license: none detected by GitHub API
stars: 4
last_commit: 2025-07-16
topics: [fork-merge-security]
added_by: dmarz/fm-code-bench
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: [yang-2025-mitigating]
---

## Summary

Code for "Mitigating the Backdoor Effect for Multi-Task Model Merging via Safety-Aware Subspace" [[yang-2025-mitigating]]. The README describes a defense-aware merging algorithm for CLIP models that learns orthogonal subspaces guided by safety to co-optimise task performance and backdoor suppression. The code base is a fork of FusionBench (tanganke/fusion_bench), a Hydra-configured benchmark of model fusion methods with model pools and task pools, so DAM sits alongside the other merge methods in that framework. The paper reports, per the library entry, a 2 to 10 point reduction in attack success versus existing merge methods at about 1% accuracy cost.

## What it can do for us

Q2: one of the few merge-time defenses with code, so it is the baseline that a fork-merge defense for parametric children should beat. The reported reduction is modest (2 to 10 points), which is evidence that subspace masking alone does not restore a meaningful corruption threshold; I infer this from the reported numbers, it is not a claim of the authors. FusionBench underneath is useful by itself for running many merge algorithms on the same model pool.

## Run notes

Not run. Install via `pip install fusion-bench` or from the fusion_bench repository; configuration through Hydra under `config/method`, `config/modelpool`, `config/taskpool`. The DAM-specific entry point is not documented in the README excerpt I read.

## Limitations

Four stars, no licence file, README is mostly the upstream FusionBench documentation. Evaluated on CLIP vision models; not shown for LLM merges such as those attacked by [[gh-aojiaosaiban-merge-hijacking]].

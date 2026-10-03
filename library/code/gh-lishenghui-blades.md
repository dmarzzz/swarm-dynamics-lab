---
id: gh-lishenghui-blades
type: code
title: 'Blades: unified benchmark suite for Byzantine attacks and defenses in federated learning'
repo: lishenghui/blades
url: https://github.com/lishenghui/blades
authors: [Shenghui Li, Edith Ngai, Fanghua Ye, Li Ju, Tianru Zhang, Thiemo Voigt]
year: 2022
language: Python
license: Apache-2.0
stars: 157
last_commit: 2025-02-16
topics: [fork-merge-security]
added_by: dmarz/fm-code-bench
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: [blanchard-2017-byzantine, yin-2018-byzantine, baruch-2019-little, xie-2019-fall, fang-2020-local]
---

## Summary

Blades (IoTDI 2024, arXiv 2206.05359) is a Ray Tune based benchmark for Byzantine-resilient federated learning from Uppsala and Hong Kong University authors. Built-in attacks: noise, label flipping [[fang-2020-local]], sign flipping, ALIE [[baruch-2019-little]], IPM [[xie-2019-fall]] and an adaptive distance-maximisation attack from Shejwalkar and Houmansadr. Built-in robust aggregators: Multi-Krum [[blanchard-2017-byzantine]], geometric median, median and trimmed mean [[yin-2018-byzantine]], centered clipping, clustering, clipped clustering, DnC and SignGuard, plus Dirichlet and sharding data partitioners. The paper abstract reports a re-evaluation of about 1,500 trials that found previously overlooked limitations of defenses when baselines and attack settings are varied.

## What it can do for us

Q2: an alternative to [[gh-vio1etus-flpoison]] and [[gh-lpd-epfl-byzfl]] that scales across a Ray cluster, useful if a sweep over (n children, f corrupted, aggregation rule, heterogeneity) gets large. Heterogeneity matters for fork-merge because children sent to different domains (the "explore another country's web" case) return legitimately different updates, which is exactly the non-IID regime where robust aggregators lose power and attacks like ALIE hide best.

## Run notes

Not run. README: `git clone`, `pip install -v -e .`, then `cd blades/blades && python train.py file ./tuned_examples/fedsgd_cnn_fashion_mnist.yaml`; results land in `~/ray_results`.

## Limitations

Last push February 2025. Fewer backdoor attacks than FLPoison. Depends on Ray, which is heavier to install than ByzFL. Numeric updates only.

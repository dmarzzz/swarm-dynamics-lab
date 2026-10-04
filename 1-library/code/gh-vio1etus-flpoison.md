---
id: gh-vio1etus-flpoison
type: code
title: 'FLPoison: benchmark of 15 poisoning attacks and 17 defenses in federated learning'
repo: vio1etus/FLPoison
url: https://github.com/vio1etus/FLPoison
authors: [Heyi Zhang, Yule Liu, Xinlei He, Jun Wu, Tianshuo Cong, Xinyi Huang]
year: 2025
language: Python
license: GPL-2.0
stars: 67
last_commit: 2026-04-15
topics: [fork-merge-security, sybil-resistance]
added_by: dmarz/fm-code-bench
accessed: 2026-10-03
read_depth: skim
relevance: 4
papers: [blanchard-2017-byzantine, el-mhamdi-2018-hidden, yin-2018-byzantine, baruch-2019-little, xie-2019-fall, fang-2020-local, bagdasaryan-2020-how]
---

## Summary

FLPoison is the PyTorch benchmark accompanying the SoK "Benchmarking Poisoning Attacks and Defenses in Federated Learning" (arXiv 2502.03801), which per its abstract evaluates 15 attacks and 17 defenses across FedSGD, FedOpt and FedAvg and several data heterogeneity settings. The README separates data poisoning attacks that implant backdoors (Neurotoxin, edge-case, model replacement [[bagdasaryan-2020-how]], alternating minimisation, DBA, BadNets, label flipping) from model poisoning attacks that block convergence (HIDRA, Mimic, Min-Max and Min-Sum, Fang [[fang-2020-local]], IPM [[xie-2019-fall]], ALIE [[baruch-2019-little]], sign flipping, Gaussian). Defenses include Krum and Multi-Krum [[blanchard-2017-byzantine]], Bulyan [[el-mhamdi-2018-hidden]], coordinate median and trimmed mean [[yin-2018-byzantine]], geometric median (RFA), centered clipping, bucketing, DnC, FLTrust, FLDetector, SignGuard, LASA, FLAME, DeepSight, CRFL, norm clipping, FoolsGold and Auror, each mapped to a source file.

## What it can do for us

Q2: the largest single catalogue of implemented robust aggregators next to the adaptive attacks that were designed to beat them, in one framework. For the fork-merge question it answers "which k-of-n aggregation rule survives which corruption strategy" for numeric updates, and is where the classic thresholds (Krum is proved for 2f + 2 < n [[blanchard-2017-byzantine]]; a coordinate median breaks once corrupted inputs are a majority) can be checked against attacks like ALIE that stay inside the honest spread. Q3: its split between backdoor attacks (stealthy, targeted) and convergence attacks (loud) maps onto the two goals an attacker controlling a child could have at merge time. FoolsGold is a Sybil defense, hence the sybil-resistance tag.

## Run notes

Not run. Getting started is in the repository wiki. Datasets: MNIST, FashionMNIST, EMNIST, CIFAR10, CINIC10, CIFAR100, CHMNIST, TinyImageNet.

## Limitations

GPL-2.0 licence constrains reuse in permissive code. Scope is gradient or weight updates on image classifiers; nothing here handles text reports or LLM memories. Several defenses are adapted from one FL algorithm to others by the authors (marked in brackets in the README), so results for adapted pairs are the benchmark's own, not the original papers'.

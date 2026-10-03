---
id: gh-lpd-epfl-byzfl
type: code
title: 'ByzFL: Byzantine-resilient aggregators, attacks and FL simulation library from EPFL and INRIA'
repo: LPD-EPFL/byzfl
url: https://github.com/LPD-EPFL/byzfl
authors: [EPFL Distributed Computing Laboratory, INRIA Rennes WIDE team]
year: 2024
language: Python
license: MIT
stars: 36
last_commit: 2026-10-02
topics: [fork-merge-security, sync-consensus]
added_by: dmarz/fm-code-bench
accessed: 2026-10-03
read_depth: ran
relevance: 5
papers: [blanchard-2017-byzantine, el-mhamdi-2018-hidden, yin-2018-byzantine, baruch-2019-little, xie-2019-fall]
---

## Summary

ByzFL is a pip-installable library from the EPFL group that introduced Krum and Bulyan [[blanchard-2017-byzantine]] [[el-mhamdi-2018-hidden]], co-developed with INRIA Rennes. It works on both NumPy arrays and PyTorch tensors and provides robust aggregators, pre-aggregators, Byzantine attack simulators, an honest/Byzantine client and server simulation, and a benchmarking harness. In version 0.0.11 the aggregators module exports Average, CAF, CenteredClipping, GeometricMedian, Krum, MDA, Meamed, Median, MoNNA, MultiKrum, SMEA and TrMean, and the attacks module exports ALittleIsEnough [[baruch-2019-little]] and an optimised variant, InnerProductManipulation [[xie-2019-fall]] and an optimised variant, SignFlipping, LabelFlipping, Gaussian, Inf and Mimic. Each aggregator takes the assumed number of Byzantine inputs f as a constructor argument.

## What it can do for us

Q2: the lightest way to test threshold claims on vectors that stand in for children's returned updates (embeddings of reports, parameter deltas, belief vectors). Because aggregators and attacks are plain callables on arrays, they can be dropped into a fork-merge simulation without adopting an FL framework. My toy run (below) shows the expected picture: with n = 11 children and an attacker who sends a far-off target, the plain average is pulled linearly with f, while median, trimmed mean and Krum stay bounded up to f = 5 and all snap to the attacker's target at f = 6 (a majority). Against ALIE, which stays inside honest variance, Krum's error roughly doubled at f = 4 to 5 compared with f = 3. This is a toy illustration of the known breakdown points, not a new result.

## Run notes

Ran on macOS (Apple silicon, CPU only), Python 3.9 venv:
`python3 -m venv byzvenv && ./byzvenv/bin/pip install byzfl` installed byzfl 0.0.11.
Script: n = 11 vectors in d = 50, honest vectors drawn N(0, 1); f corrupted vectors either all equal to a target of 10 in every coordinate ("shift") or set by `ALittleIsEnough(tau=1.5)(honest)`; aggregators `Average()`, `Median()`, `TrMean(f)`, `Krum(f)` with f capped at 4, `GeometricMedian()`; metric is L2 distance of the aggregate from the honest mean.
Output (shift attack, distance for Average / Median / TrMean / Krum / GeoMed): f=0: 0.00 / 1.17 / 0.00 / 6.14 / 0.20; f=3: 19.39 / 4.15 / 4.23 / 5.59 / 2.83; f=5: 32.44 / 9.28 / 9.28 / 5.91 / 7.41; f=6: 38.66 / 70.88 / 70.88 / 70.88 / 14.36 (70.7 is the distance to the attacker target). ALIE, Krum: f=3 5.59, f=4 10.80, f=5 10.06. Krum's nonzero error at f = 0 is because it returns one selected input rather than a mean. Single seed; no error bars.

## Limitations

Version 0.0.x and the API may change. Aggregators operate on fixed-length real vectors, so applying them to LLM agents requires choosing an embedding of what a child returns, and robustness in embedding space does not imply robustness of the text that is finally merged. Documentation is on byzfl.epfl.ch; I read the README and introspected the installed package, not the source of every aggregator.

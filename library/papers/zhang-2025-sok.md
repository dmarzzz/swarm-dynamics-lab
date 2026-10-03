---
id: zhang-2025-sok
type: paper
title: "SoK: Benchmarking Poisoning Attacks and Defenses in Federated Learning"
authors: ["Heyi Zhang", "Yule Liu", "Xinlei He", "Jun Wu", "Tianshuo Cong", "Xinyi Huang"]
year: 2025
venue: "arXiv preprint"
url: https://arxiv.org/abs/2502.03801
doi: null
arxiv: "2502.03801"
cite: "Zhang, H., Liu, Y., He, X., Wu, J., Cong, T., & Huang, X. (2025). SoK: Benchmarking Poisoning Attacks and Defenses in Federated Learning. arXiv preprint arXiv:2502.03801."
topics: [fork-merge-security, meta]
added_by: dmarz/fm-merge-poisoning
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Systematisation of knowledge plus benchmark for poisoning in federated learning. It separates client-side data poisoning attacks from model poisoning attacks, gives a taxonomy of both and of defences, and evaluates 15 attacks against 17 defences across FL algorithms and degrees of data heterogeneity in a unified framework called FLPoison. The motivation is that defences are usually evaluated in isolation against a few attacks, which overstates their effectiveness.

## Contribution

The most comprehensive head-to-head benchmark of FL poisoning attacks and defences found in this scan, with released code.

## Key results

- 15 representative poisoning attacks and 17 defences evaluated in one framework (abstract).
- Abstract-level claim that defences tested in isolation look stronger than they are under a unified evaluation; specific rankings not read.

## Methods and models

Unified benchmark FLPoison (github.com/vio1etus/FLPoison, not opened) across FL algorithms and heterogeneity levels.

## Limitations and open questions

Abstract only. Federated settings with many clients; transfer to a handful of sub-agents with LLM-sized state is not tested.

## Relevance to us

Review article for this lane. A ready benchmark if the team wants to measure k-of-n thresholds (Q2) for weight-space merges before moving to LLM agents. Data heterogeneity is the knob that corresponds to sub-agents exploring different domains. Related: [[sagar-2023-poisoning]], [[fang-2020-local]].

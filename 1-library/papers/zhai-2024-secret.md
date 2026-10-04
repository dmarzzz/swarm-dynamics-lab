---
id: zhai-2024-secret
type: paper
title: "Secret Multiple Leaders & Committee Election With Application to Sharding Blockchain"
authors: ["Mingzhe Zhai", "Qianhong Wu", "Yizhong Liu", "Bo Qin", "Xiaopeng Dai", "Qiyuan Gao", "Willy Susilo"]
year: 2024
venue: "IEEE Transactions on Information Forensics and Security, 19"
url: https://ieeexplore.ieee.org/document/10502325
doi: "10.1109/TIFS.2024.3390584"
arxiv: null
cite: "Zhai, M., Wu, Q., Liu, Y., Qin, B., Dai, X., Gao, Q., & Susilo, W. (2024). Secret Multiple Leaders & Committee Election With Application to Sharding Blockchain. IEEE Transactions on Information Forensics and Security, 19, 4482-4497. https://doi.org/10.1109/TIFS.2024.3390584"
topics: [fork-merge-security]
added_by: shadow/sol-fm
accessed: 2026-10-04
read_depth: abstract
relevance: 4
citations: 12  # OpenAlex cited_by_count, 2026-10-04; shadow/sol-fm
code: []
---

## Summary

Extends single secret leader election (SSLE) to Secret Multiple Leaders Election (SMLE): a group elects several consecutive secret leaders in one run, each leader's identity hidden until self-reveal, while reducing the average per-leader communication cost to constant complexity. SMLE is built on linkable membership proof and is proven to satisfy a "consistent unpredictability" property per leader. Two constructions: a non-interactive one (no pre-configured nodes) and an interactive one for a committee setting. The authors further extend SMLE to Secret Committee Election (SCE) and use it for anonymous node allocation in sharding blockchains, reporting that it raises an adversary's attack difficulty by roughly the shard number with minimal communication and computational overhead.

## Contribution

The missing bridge between "hide which single part returns" (SSLE) and "hide which k parts return" (a committee). It gives a construction for secretly electing a *set* of returners, with a proven per-member unpredictability property and constant amortized cost.

## Key results

- One-time election of multiple consecutive secret leaders at constant average per-leader communication cost, versus the high complexity of iterating SSLE.
- New "consistent unpredictability" security property proven for each elected leader.
- Non-interactive and interactive (committee) constructions.
- Applied to sharding: adversary attack difficulty increases by approximately the shard number, with minimal overhead (experimental).

## Methods and models

Linkable membership proof as the cryptographic core; two SMLE constructions; extension to SCE for anonymous shard allocation. Evaluation measures communication and computation overhead against SSLE baselines.

## Limitations and open questions

Abstract depth: the exact security definitions, the overhead figures and the shard-count claim need the body. The setting is blockchain consensus, not agent forks; applying SCE to "which k of n forks will be merged/audited" is an untested inference.

## Relevance to us

Fills the Q1-to-Q2 bridge the fork-merge survey flagged as "found but not catalogued" and issue #75 asked for: it extends secret selection from one returner to a committee of k, which is what you need to hide *which set* of forks will be reintegrated or audited. Pairs with [[boneh-2020-single]] (the single-leader base) and the hiding-defence line. Related: [[boneh-2020-single]], [[ethresear-2022-whisk]], [[burianova-2025-secret]].

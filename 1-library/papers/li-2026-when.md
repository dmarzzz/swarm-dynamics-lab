---
id: li-2026-when
type: paper
title: "When Safe Models Merge into Danger: Exploiting Latent Vulnerabilities in LLM Fusion"
authors: ["Jiaqing Li", "Zhibo Zhang", "Shide Zhou", "Yuxi Li", "Tianlong Yu", "Kailong Wang"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/html/2604.00627
doi: null
arxiv: "2604.00627"
cite: "Li, J., Zhang, Z., Zhou, S., Li, Y., Yu, T., & Wang, K. (2026). When Safe Models Merge into Danger: Exploiting Latent Vulnerabilities in LLM Fusion. arXiv preprint arXiv:2604.00627."
topics: [fork-merge-security]
added_by: dmarz/fm-merge-poisoning
accessed: 2026-10-03
read_depth: skim
relevance: 5
citations: "1 (Semantic Scholar, via BadMerging citation list, 2026-10-03)"
code: []
---

## Summary

TrojanMerge splits an attack across two source models. Each carries a latent perturbation that keeps that model individually safe and capable, but the two perturbations sum during merging into a pre-computed attack vector that breaks safety alignment. The construction is a constrained optimisation with directional-consistency constraints (each source stays safe) and Frobenius directional alignment (capabilities preserved), applied to MLP layers. Across 9 LLMs from 3 families, merged models reach high harmful-response rates while each source model scores like an unmodified one.

## Contribution

A distributed, threshold-style attack in weight space: corruption only appears when both parts are merged, so per-part inspection passes.

## Key results

- From my skim of the HTML: individual source models harmful score 3.1-29.0%; merged poisoned models 71.9-85.4%; clean merged models 1.9-24.0%.
- Holds across task arithmetic, DARE, TIES and KnOTS merging (skim).
- MMLU drops 7.6-15.9 points in merged models, perplexity rises 0.3-3.8 (skim).
- Safety-aware merging (SAM) defence converges to degenerate solutions on TrojanMerge models (skim).

## Methods and models

Two-model fusion; perturbations on MLP layers solved as constrained optimisation; nine LLMs from three families.

## Limitations and open questions

Two-model fusion only; the authors leave larger merges and other layers open. Requires the attacker to control both source models. The MMLU cost is noticeable and could serve as a merge-time signal. Numbers are from a skim and not cross-checked against tables.

## Relevance to us

Key for Q2, in the reverse direction from what dmarz asked: it shows an attacker can deliberately build a k-of-n attack (here 2-of-2) that defeats per-part checks. A k-of-n threshold therefore needs the parts to be independent; if the adversary controls k parts it can split the payload so none looks bad alone. For Q1, hiding which parts will be merged together breaks this attack, because the payload only assembles if the right parts meet. Related: [[ding-2026-colluding]], [[hammoud-2024-model]], [[zhang-2024-badmerging]].

## Notes from dmarz/fm-bft-aggregation

Opened the arXiv abstract page this session (2026-10-03). Bearing on Q2 (merge thresholds): TrojanMerge is the parameter-space proof that a per-part check before merging is not enough. Each source model passes safety evaluation on its own, yet the merge composes their perturbations into a pre-computed attack vector. In fork-merge terms an attacker who corrupts several returning sub-agents slightly, each below any per-part anomaly threshold, can still get a harmful parent; a k-of-n rule that inspects parts one at a time is defeated by design, which matches the in-distribution attacks on robust aggregation in [[baruch-2019-little]] and [[el-mhamdi-2018-hidden]]. Defences that check agreement at use time rather than merging weights, such as consensus decoding in [[narang-2026-inference]], are the contrasting design (that paper measures that weight averaging keeps single-source poison).

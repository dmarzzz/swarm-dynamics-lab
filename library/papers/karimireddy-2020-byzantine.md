---
id: karimireddy-2020-byzantine
type: paper
title: Byzantine-Robust Learning on Heterogeneous Datasets via Bucketing
authors:
- Sai Praneeth Karimireddy
- Lie He
- Martin Jaggi
year: 2020
venue: ICLR 2022 (arXiv preprint)
url: https://arxiv.org/abs/2006.09365
doi: null
arxiv: '2006.09365'
cite: 'Karimireddy, S. P., He, L., & Jaggi, M. (2020). Byzantine-Robust Learning on Heterogeneous Datasets via Bucketing. arXiv preprint arXiv:2006.09365.'
topics:
- fork-merge-security
- sync-consensus
added_by: dmarz/fm-bft-aggregation
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

Most Byzantine-robust aggregation defenses assume honest workers hold identically distributed data. With heterogeneous (non-i.i.d.) data the authors design new attacks that circumvent current defenses and cause large performance loss, then propose bucketing: randomly group worker updates into buckets, average within each bucket, and apply an existing robust aggregator to the bucket means. They claim the first guaranteed convergence for the non-i.i.d. Byzantine-robust problem under realistic assumptions.

## Contribution

Shows heterogeneity among honest participants is itself an attack surface for robust aggregation, and gives a cheap randomised fix.

## Key results

- Shown (per abstract): new attacks defeat existing defenses under non-i.i.d. data.
- Proved (per abstract): bucketing plus existing robust aggregators converges in the non-i.i.d. case.

## Methods and models

Random bucketing of updates before robust aggregation. Only the abstract was read.

## Limitations and open questions

Abstract-level reading; tolerated fraction and heterogeneity bounds not checked.

## Relevance to us

Q1 and Q2. Sub-agents sent to explore different domains (Sutton's example of one going to another country's web) are heterogeneous by design, so a corrupted explorer can hide inside legitimate diversity: its odd return looks like a domain effect. That is the setting where these defenses fail. Bucketing is also a form of randomised grouping at merge time, which overlaps with Q1: if the parent randomly decides which returners are combined and checked together, an attacker cannot plan which honest parts its contribution will be averaged with. Related: [[karimireddy-2020-learning]], [[blanchard-2017-byzantine]].

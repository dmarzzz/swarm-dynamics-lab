---
id: baruch-2019-little
type: paper
title: 'A Little Is Enough: Circumventing Defenses For Distributed Learning'
authors:
- Moran Baruch
- Gilad Baruch
- Yoav Goldberg
year: 2019
venue: Advances in Neural Information Processing Systems 32 (NeurIPS 2019)
url: https://arxiv.org/abs/1902.06156
doi: null
arxiv: '1902.06156'
cite: 'Baruch, M., Baruch, G., & Goldberg, Y. (2019). A Little Is Enough: Circumventing Defenses For Distributed Learning. Advances in Neural Information Processing Systems 32. arXiv:1902.06156.'
topics:
- fork-merge-security
- sync-consensus
added_by: dmarz/fm-bft-aggregation
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 98  # OpenAlex cited_by_count, 2026-10-03; shadow/sol-g51
code: []
---

## Summary

Shows that Byzantine-robust aggregation rules can be beaten without omniscience and without large perturbations. Corrupt workers send small, well-crafted changes that stay within the natural variation of honest updates, so no existing defense detects them. The attack can both prevent convergence and implant backdoors. With 20 percent of workers corrupt, the authors report a 50 percent drop in CIFAR-10 accuracy and backdoors in MNIST and CIFAR-10 models that do not hurt clean accuracy.

## Contribution

Breaks the assumption behind distance and median defenses that Byzantine inputs must be outliers; small coordinated shifts inside the honest spread are enough.

## Key results

- Measured (per abstract): 20 percent corrupt workers degrade CIFAR-10 accuracy by 50 percent.
- Measured (per abstract): backdoors implanted in MNIST and CIFAR-10 models without hurting their accuracy.
- Claimed: undetected by all defenses tested at the time.

## Methods and models

Non-omniscient attack using small, well-crafted parameter changes, evaluated on MNIST and CIFAR-10 against the defenses of the time. Only the abstract was read; the exact construction and the list of defenses tested were not checked.

## Limitations and open questions

Abstract-level reading; later defenses such as [[karimireddy-2020-learning]] address time-coupled versions.

## Relevance to us

Q3. The ML version of the stealthiest merge attack: corrupted sub-agents that return contributions indistinguishable from honest ones, coordinated so their small shifts add up, and carrying a backdoor rather than an obvious error. It argues that a parent's anomaly check on each returning sub-agent will not catch a careful attacker, and that a backdoor (behaviour triggered later) is the natural payload. Related: [[el-mhamdi-2018-hidden]], [[xie-2019-fall]].

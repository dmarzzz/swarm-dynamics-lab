---
id: zhang-2026-roguemerge
type: paper
title: "RogueMerge: Robust and Unified Attacks against LLM Model Merging"
authors: ["Jinghuai Zhang", "Yetian He", "Kunlin Cai", "Han Zhao", "Fnu Suya", "Yuan Tian"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2606.03344
doi: null
arxiv: "2606.03344"
cite: "Zhang, J., He, Y., Cai, K., Zhao, H., Suya, F., & Tian, Y. (2026). RogueMerge: Robust and Unified Attacks against LLM Model Merging. arXiv preprint arXiv:2606.03344."
topics: [fork-merge-security]
added_by: dmarz/fm-merge-poisoning
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "1 (Semantic Scholar, via BadMerging citation list, 2026-10-03)"
code: []
---

## Summary

Follow-up from the BadMerging group, aimed at generative LLMs. It argues static task-vector heuristics fail because merge-induced drift compounds over autoregressive decoding, the attacker does not know the victim's merge settings, and attacks must generalise to unseen prompts. RogueMerge jointly optimises for attack success after merging, treats unknown merge settings as a stochastic min-max problem solved by meta-learning-style simulation, and uses distributionally robust optimisation with a first-order Taylor approximation with a stated error bound. Evaluated over four threat types, six merge algorithms and more than 170 merged LLMs.

## Contribution

Generalises merge attacks from fixed backdoors to arbitrary threats encoded in a task vector, robust to unknown merge configuration.

## Key results

- Abstract-level: outperforms existing merge attacks across four threats, six merge algorithms and over 170 merged LLMs.
- Abstract-level: stable across merge settings and resists standard defences.

## Methods and models

Simulated-merge min-max optimisation, distributionally robust objective, Taylor approximation at LLM scale (details not read).

## Limitations and open questions

Abstract only; recent preprint, not yet peer reviewed as far as the page shows.

## Relevance to us

Q3: the strongest current weight-space attacker model. Its framing that 'merging grants third-party vectors direct write access to model weights' is the fork-merge threat in one sentence. The min-max over unknown merge settings means randomising the merge (one form of Q1 hiding) is something the attacker can already optimise against. Related: [[zhang-2024-badmerging]], [[yuan-2025-merge]].

---
id: hammoud-2024-model
type: paper
title: "Model Merging and Safety Alignment: One Bad Model Spoils the Bunch"
authors: ["Hasan Abed Al Kader Hammoud", "Umberto Michieli", "Fabio Pizzati", "Philip Torr", "Adel Bibi", "Bernard Ghanem", "Mete Ozay"]
year: 2024
venue: "arXiv preprint"
url: https://arxiv.org/abs/2406.14563
doi: null
arxiv: "2406.14563"
cite: "Hammoud, H. A. A. K., Michieli, U., Pizzati, F., Torr, P., Bibi, A., Ghanem, B., & Ozay, M. (2024). Model Merging and Safety Alignment: One Bad Model Spoils the Bunch. arXiv preprint arXiv:2406.14563."
topics: [fork-merge-security]
added_by: dmarz/fm-merge-poisoning
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

Evaluates popular LLM merging methods for their effect on safety alignment and finds they transfer not only domain expertise but also misalignment: merging in one misaligned expert yields a merged model that is substantially misaligned. The proposed fix generates synthetic safety data and domain data and feeds both into existing data-aware merging methods, treating alignment as one more skill to preserve during the merge.

## Contribution

Non-adversarial version of the fork-merge problem: no trigger or attacker optimisation is needed for one unaligned part to degrade the merged model's alignment.

## Key results

- Abstract-level: existing merge methods propagate misalignment from a single misaligned expert.
- Abstract-level: adding synthetic safety and domain data to data-aware merging yields models strong in both expertise and alignment.

## Methods and models

Several LLM merging techniques evaluated on alignment benchmarks; data-aware merging with generated safety data (details not read).

## Limitations and open questions

Abstract only. The defence assumes the parent can generate representative safety data for the merge objective, which an adaptive attacker can target.

## Relevance to us

Q2 and Q3. The title result ('one bad model spoils the bunch') says plain merging has no threshold even for unintended misalignment. The defence, making alignment an explicit merge objective evaluated on the parent's own data, is the template for a merge-time check in a fork-merge agent. Related: [[zhang-2024-badmerging]], [[li-2026-when]], [[cloud-2025-subliminal]].

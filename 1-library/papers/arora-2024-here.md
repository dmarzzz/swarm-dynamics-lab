---
id: arora-2024-here
type: paper
title: "Here's a Free Lunch: Sanitizing Backdoored Models with Model Merge"
authors: ["Ansh Arora", "Xuanli He", "Maximilian Mozes", "Srinibas Swain", "Mark Dras", "Qiongkai Xu"]
year: 2024
venue: "Findings of the Association for Computational Linguistics: ACL 2024"
url: https://arxiv.org/abs/2402.19334
doi: null
arxiv: "2402.19334"
cite: "Arora, A., He, X., Mozes, M., Swain, S., Dras, M., & Xu, Q. (2024). Here's a Free Lunch: Sanitizing Backdoored Models with Model Merge. In Findings of the Association for Computational Linguistics: ACL 2024. arXiv:2402.19334."
topics: [fork-merge-security]
added_by: dmarz/fm-merge-poisoning
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: 1  # OpenAlex cited_by_count, 2026-10-03; shadow/sol-g51
code: []
---

## Summary

Proposes merging as a defence: merging a backdoored language model with other homogeneous models, even ones that are not fully trusted, substantially removes the backdoor. Tested on BERT-Base, RoBERTa-Large, Llama2-7B and Mistral-7B over SST-2, OLID, AG News and QNLI, the method outperforms several dedicated backdoor defences, with an average reduction of about 75% in attack success rate and no extra training resources.

## Contribution

The dilution argument made explicit: averaging with independent models washes out a backdoor that one model carries, provided the attacker did not design for the merge.

## Key results

- About 75% average reduction in attack success rate across models and datasets (abstract).
- Outperforms several advanced inference-stage backdoor defences (abstract).

## Methods and models

Merge a suspect model with other models fine-tuned for the same or related tasks using standard merge operators (details not read).

## Limitations and open questions

Abstract only. Tested against backdoors not designed for merging. [[zhang-2024-badmerging]] and [[yuan-2025-merge]] are built precisely to survive this dilution, so the defence is a baseline rather than a guarantee.

## Relevance to us

Q2: this is the optimistic case for 'merge many parts so one bad part is diluted'. Read together with merge-aware attacks it shows that dilution provides a threshold only against non-adaptive corruption. A fork-merge agent should treat dilution as a floor and add bounded per-part influence. Related: [[zhang-2024-badmerging]], [[yuan-2025-merge]], [[yang-2025-mitigating]].

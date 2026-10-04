---
id: zou-2024-poisonedrag
type: paper
title: 'PoisonedRAG: Knowledge Corruption Attacks to Retrieval-Augmented Generation of Large Language Models'
authors: [Wei Zou, Runpeng Geng, Binghui Wang, Jinyuan Jia]
year: 2024
venue: USENIX Security Symposium 2025; arXiv preprint 2024
url: https://arxiv.org/abs/2402.07867
doi: null
arxiv: '2402.07867'
cite: 'Zou, W., Geng, R., Wang, B., & Jia, J. (2024). PoisonedRAG: Knowledge Corruption Attacks to Retrieval-Augmented Generation of Large Language Models. arXiv:2402.07867. To appear in the 34th USENIX Security Symposium (2025).'
topics: [fork-merge-security]
added_by: dmarz/fm-memory-injection
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: 13  # OpenAlex cited_by_count, 2026-10-03; shadow/sol-g51
code: [gh-sleeeepeer-poisonedrag]
---

## Summary

PoisonedRAG is the reference knowledge-corruption attack on RAG. For an attacker-chosen target question and target answer, the attacker crafts a handful of texts that will be retrieved for that question and will lead the LLM to output the target answer. The crafting is framed as an optimisation problem with a black-box solution (an LLM writes the texts) and a white-box one (gradient-based HotFlip, according to the repo README). Measured (abstract): about 90% attack success when five malicious texts per target question are injected into a knowledge database of millions of texts. The defences tested were insufficient.

## Contribution

It shows that a tiny absolute number of poisoned items suffices regardless of corpus size, because retrieval selects on similarity to the question rather than on prevalence.

## Key results

- 90% ASR with 5 injected texts per target question in a database of millions of texts (abstract).
- The evaluated defences are insufficient (abstract; which defences was not checked).

## Methods and models

Datasets NQ, HotpotQA and MS-MARCO through BEIR with a Contriever retriever. LLMs include PaLM 2, GPT-3.5, GPT-4, LLaMA-2 and Vicuna (from the repo configuration in [[gh-sleeeepeer-poisonedrag]]).

## Limitations and open questions

It is a static-corpus attack in which the attacker writes into the knowledge base. Robust aggregation defences ([[xiang-2024-certifiably]]) cut its ASR to about 10% in their evaluation.

## Relevance to us

For Q3, this shows the merge does not need to replace the parent's memory to corrupt it. A few highly targeted records per topic are enough, because the parent retrieves by similarity. Volume-based thresholds (Q2) that count how much of the merged memory came from one sub-agent therefore do not help on their own. What matters is how many of the records retrieved for a given query come from compromised sources. That is the quantity bounded in [[xiang-2024-certifiably]] and [[sharma-2026-smsr]].

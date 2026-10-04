---
id: meng-2022-mass-editing
type: paper
title: Mass-Editing Memory in a Transformer
authors:
- Kevin Meng
- Arnab Sen Sharma
- Alex Andonian
- Yonatan Belinkov
- David Bau
year: 2022
venue: International Conference on Learning Representations (ICLR 2023)
url: https://arxiv.org/abs/2210.07229
doi: null
arxiv: '2210.07229'
cite: Meng, K., Sharma, A. S., Andonian, A., Belinkov, Y., & Bau, D. (2022). Mass-Editing Memory in a Transformer. International Conference on Learning Representations (ICLR 2023). arXiv:2210.07229.
topics:
- fork-merge-security
added_by: dmarz/fm
accessed: '2026-10-03'
read_depth: skim
relevance: 3
citations: null  # Semantic Scholar and OpenAlex rate-limited on 2026-10-03
code: []
---

## Summary

MEMIT extends ROME from one edit to thousands applied at once: it computes target hidden states for each new fact and spreads the required weight change across a range of mid-layer MLP modules in a single batched least-squares update, rather than a rank-one change to one layer. Tested on GPT-J (6B) and GPT-NeoX (20B) with zsRE (adding true facts) and CounterFact (adding counterfactuals), against fine-tuning, MEND and ROME, with edit counts from 1 to 10,000. Read: abstract, introduction, method overview, experiment set-up and results text; tables partly lost in extraction.

## Contribution

Shows direct weight editing scales to about 10,000 facts in one operation, orders of magnitude beyond earlier editors, while keeping most of the generalisation and specificity of single edits.

## Key results

- At 10,000 zsRE edits on GPT-J, MEMIT had the best combined editing score; plain constrained fine-tuning beat MEND and ROME at that scale (measured, Table 1).
- On CounterFact, ROME worked up to about 10 edits and degraded from 32; MEND degraded rapidly after 1; MEMIT performed best at large edit counts (measured, Figure 5).
- At small edit counts ROME generalised to paraphrases slightly better, at a small cost in specificity (measured).

## Methods and models

Edits spread over a set of critical layers identified by causal tracing; the update minimises error on new keys while preserving outputs on a covariance estimate of existing keys. ICLR 2023 (per the PDF header). Code and data at memit.baulab.info.

## Limitations and open questions

Factual (subject, relation, object) associations only; evaluation via probability-based and generation-based metrics on two model families.

## Relevance to us

Q3: if a split agent's parts return what they learned as batches of knowledge edits, MEMIT shows a single returned batch can rewrite thousands of associations in one merge while preserving general behaviour, so the parent's routine competence checks would not flag it. Q2: the update is a deterministic function of the requested edits, so a parent could in principle require each requested fact to be independently attested by k of n parts before including it in a batch. That is a per-fact threshold the paper does not discuss (inference). Related: [[meng-2022-locating]], [[li-2024-badedit]], [[chen-2024-can]].

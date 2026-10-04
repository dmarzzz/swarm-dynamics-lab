---
id: kohli-2026-nine
type: paper
title: 'Nine Judges, Two Effective Votes: Correlated Errors Undermine LLM Evaluation Panels'
authors: [Guneet Kohli]
year: 2026
venue: arXiv
url: https://arxiv.org/html/2605.29800
doi: null
arxiv: '2605.29800'
cite: 'Kohli, G. (2026). Nine Judges, Two Effective Votes: Correlated Errors Undermine LLM Evaluation Panels. arXiv:2605.29800.'
topics: [llm-agent-swarms]
added_by: shadow/sol-1
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: null
code: []
---

## Summary

A panel of 9 frontier LLM judges from 7 families labels three ChaosNLI natural-language-inference datasets (100 human annotations per item). Using the Kish effective sample size and a Condorcet null model, the panel carries roughly 2 independent votes of information: about three quarters of its nominal independence is lost because models err on the same items. Panel accuracy falls 8 to 22 points short of the independent-voting prediction, the best single judge matches or beats the panel in every condition, adding judges beyond 5 gives negligible gain, and established aggregation methods close at most 11% of the gap even with access to labels.

## Contribution

An independent (single-author, different group from [[bertalanic-2026-ringelmann]]) measurement of a Kish-style effective-N ceiling for multi-model aggregation, with a Condorcet gap as the null. Same structure as the N_eff ceiling, measured on judge panels rather than debate.

## Key results

- n_eff of about 2 for 9 judges across three NLI datasets, three prompt variants, two temperatures, chain-of-thought, and RewardBench (pairwise preference), with panel accuracy from 69% to 93%.
- Condorcet gap 8 to 22 percentage points (permutation test).
- Smarter aggregation closes at most 11% of the gap.

## Methods and models

Kish effective sample size on judge error correlations; Condorcet jury model as independent-voting null; ChaosNLI (SNLI, MNLI, alpha-NLI subsets) and RewardBench. Read: abstract, introduction and contribution list in the arXiv HTML; methods details skimmed.

## Limitations and open questions

Judges vote once with no interaction, so this is error correlation without social influence. Classification tasks only.

## Relevance to us

Independent support for "homogeneous agents add agreement, not evidence" beside [[kim-2025-correlated]], [[bara-2026-epistemic]] and [[begin-2026-preference]]. The Kish n_eff and Condorcet gap are the same instruments an N_eff-on-a-board experiment would use.

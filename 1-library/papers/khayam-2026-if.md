---
id: khayam-2026-if
type: paper
title: 'If It Walks Like an Arbitrage: Protocol-Agnostic Detection with Decidable Structural Equivalence'
authors:
- Adam Khayam
- Hamid Kolli
- Mohamed Iguernlala
- Çagdas Bozman
year: 2026
venue: arXiv preprint (cs)
url: https://arxiv.org/abs/2608.20377
doi: null
arxiv: '2608.20377'
cite: 'Khayam, A., Kolli, H., Iguernlala, M., & Bozman, Ç. (2026). If It Walks Like an Arbitrage: Protocol-Agnostic Detection with Decidable Structural Equivalence. arXiv preprint arXiv:2608.20377.'
topics:
- swarm-detection
added_by: dmarz/sd-onchain
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Protocol-agnostic arbitrage detection from EVM execution traces. Each trace becomes an abstract syntax tree of token transfers grouped by call-frame nesting and is reduced by a 16-rule term rewriting system whose termination, preservation, soundness, uniqueness of normal form and decidability of structural equivalence are machine-checked in Rocq. Arbitrage cycles are read off the normal form with no protocol-specific rules. Over 220,000 Ethereum blocks it finds 469,801 confirmed arbitrages (83.5% overlap with EigenPhi, 81% with the ArbiNet GNN on 1,000 shared blocks), 245,497 attempted arbitrages and 60,199 confirmed arbitrages EigenPhi misses; manual validation of 500 found no false positives among confirmed detections.

## Contribution

A sound, label-free detector for one class of bot behaviour, with structural equivalence of fund flows as a second query that can group transactions by identical strategy, which is a candidate signal for linking bots run by one operator (inferred use, not tested in the paper).

## Key results

- 469,801 confirmed arbitrages in 220K blocks; 60,199 not reported by EigenPhi; 0 false positives in 500 manual checks.

## Methods and models

Trace normalisation by term rewriting; mechanised proofs in Rocq; evaluation against EigenPhi and ArbiNet; runs unmodified on Arbitrum and BSC.

## Limitations and open questions

Abstract-level read; detects arbitrage transactions, not who operates them.

## Relevance to us

MEV-bot activity labels underlie many bot datasets ([[niedermayer-2024-detecting]] relies on mev-inspect); a sound detector improves those labels. Found by forward citation of [[niedermayer-2024-detecting]].

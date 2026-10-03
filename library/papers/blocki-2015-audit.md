---
id: blocki-2015-audit
type: paper
title: Audit Games with Multiple Defender Resources
authors:
- Jeremiah Blocki
- Nicolas Christin
- Anupam Datta
- Ariel Procaccia
- Arunesh Sinha
year: 2015
venue: Proceedings of the AAAI Conference on Artificial Intelligence, 29(1)
url: https://ojs.aaai.org/index.php/AAAI/article/view/9317
doi: 10.1609/aaai.v29i1.9317
arxiv: null
cite: Blocki, J., Christin, N., Datta, A., Procaccia, A., & Sinha, A. (2015). Audit Games with Multiple Defender Resources. Proceedings of the AAAI Conference on Artificial Intelligence, 29(1).
topics:
- fork-merge-security
- collective-decision
added_by: dmarz/fm
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 11 (Crossref, 2026-10-03)
code: []
---

## Summary

Generalises [[blocki-2013-audit]] to several audit resources, each able to audit only a subset of possible violations. The resulting optimisation is non-convex; the paper gives an FPTAS built on an optimisation transformation and reports that the transformation speeds up computation for a class of audit and security games. Abstract only.

## Contribution

Audit games with restricted, heterogeneous auditors.

## Key results

- FPTAS for multi-resource audit games (abstract).
- Experimental speedups (magnitude not checked).

## Methods and models

Stackelberg audit games with resource-target restrictions.

## Limitations and open questions

Abstract-level read.

## Relevance to us

- Q1: matches a parent with domain-specific checkers (one validator per foreign domain) that can each audit only the children returning from their domain.
Related: [[sinha-2018-stackelberg]].

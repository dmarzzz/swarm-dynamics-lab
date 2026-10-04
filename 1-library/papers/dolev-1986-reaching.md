---
id: dolev-1986-reaching
type: paper
title: Reaching Approximate Agreement in the Presence of Faults
authors:
- Danny Dolev
- Nancy A. Lynch
- Shlomit S. Pinter
- Eugene W. Stark
- William E. Weihl
year: 1986
venue: Journal of the ACM
url: https://groups.csail.mit.edu/tds/papers/Lynch/jacm86.pdf
doi: 10.1145/5925.5931
arxiv: null
cite: 'Dolev, D., Lynch, N. A., Pinter, S. S., Stark, E. W., & Weihl, W. E. (1986). Reaching approximate agreement in the presence of faults. Journal of the ACM, 33(3), 499-516.'
topics:
- fork-merge-security
- sync-consensus
added_by: dmarz/fm-bft-aggregation
accessed: '2026-10-03'
read_depth: skim
relevance: 4
citations: 378 (Crossref, 2026-10-03)
code: []
---

## Summary

A variant of Byzantine agreement where processes start with arbitrary real values and need only approximate agreement: all non-faulty processes must halt with outputs within epsilon of each other (agreement) and inside the range of non-faulty initial values (validity). Each round, every process broadcasts its value and replaces it with an averaging function of the received multiset designed to handle t faulty processes. The synchronous algorithm converges when n >= 3t + 1; the asynchronous one when n >= 5t + 1. Convergence rate depends on the ratio of faulty to total processes, and the authors prove lower bounds showing their averaging functions are optimal for algorithms of this form. This contrasts with the impossibility of exact asynchronous agreement with one crash fault.

## Contribution

Founds approximate agreement: iterated fault-tolerant averaging gives Byzantine-tolerant convergence on real values with explicit thresholds, the ancestor of MSR and W-MSR algorithms.

## Key results

- Proved: synchronous approximate agreement for n >= 3t + 1 (Theorem 1).
- Proved: asynchronous approximate agreement for n >= 5t + 1 (Theorem 2).
- Proved: lower bounds on convergence rate; the paper's averaging functions are optimal among algorithms of the stated form.
- Validity: outputs stay within the range of non-faulty inputs.

## Methods and models

Round-based message exchange with an averaging function applied to the received multiset; the exact reduction step was not read. Skimmed: abstract, introduction, theorem statements; proofs not read.

## Limitations and open questions

Scalar real values; complete communication graph; faults bounded by t and independent.

## Relevance to us

Q2. The closest classical model for merging continuous state (belief scores, parameter values, numeric estimates) from sub-agents without a trusted merger: iterated fault-tolerant averaging tolerates t corrupted parts if n >= 3t + 1 (synchronous) or n >= 5t + 1 (asynchronous, which matches sub-agents returning at unpredictable times). Validity is the property a parent wants: the merged value cannot leave the range spanned by honest returners. Descendants: [[leblanc-2013-resilient]] (W-MSR on graphs), [[lee-2026-robust]] (LLM version), [[cambus-2025-approximate]] (vector case for learning). Cited as the related problem in [[blanchard-2017-byzantine]].

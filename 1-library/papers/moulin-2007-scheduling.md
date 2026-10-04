---
id: moulin-2007-scheduling
type: paper
title: "On Scheduling Fees to Prevent Merging, Splitting, and Transferring of Jobs"
authors: [Hervé Moulin]
year: 2007
venue: Mathematics of Operations Research, vol. 32, no. 2, pp. 266-283
url: http://www.ruf.rice.edu/~econ/papers/2004papers/schedfees4.pdf
doi: 10.1287/moor.1060.0239
arxiv: null
cite: "Moulin, H. (2007). On Scheduling Fees to Prevent Merging, Splitting, and Transferring of Jobs. Mathematics of Operations Research, 32(2), 266-283. https://doi.org/10.1287/moor.1060.0239"
topics: [sybil-resistance, collective-decision]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: "48 (Crossref, 2026-10-03)"
code: []
---

## Summary

A single deterministic server serves jobs of arbitrary length for users with identical linear waiting costs; efficiency requires shortest-job-first. The server sees job lengths but not who owns a job, so users can manipulate cooperatively: merge several jobs under one identity, split one job across several identities (explicitly linked to Douceur's Sybil attack as the case where "assuming a false identity should be easy"), or partially transfer work to each other. The question is whether cash transfers (scheduling fees) can neutralise these. Theorem 1: for four or more users, no scheduling mechanism is both merge-proof and split-proof together with either continuity or equal treatment of equals; likewise no mechanism prevents all job transfers among three or more agents. On the positive side, robustness to pairwise transfers is feasible and Theorem 2 characterises the mechanisms that achieve it as a one-dimensional family, a convex-like combination of two extreme methods, the merge-proof S+ and the split-proof S-, plus a budget-balanced shift term. Proposition 1 shows an efficient continuous method cannot be both merge- and split-proof; Propositions 2-3 characterise merge-proof separable methods and show split-proofness, unlike merge-proofness, conflicts with simple equity tests, so the two properties are "far from equally demanding". Read: abstract, introduction (motivation and the two illustrative mechanisms), statements of Theorem 1, Theorem 2, Propositions 1-3 and the discussion around them; proofs in the appendix skimmed.

## Contribution

Carries false-name analysis from auctions into queueing/scheduling with transfers and shows an impossibility: in a shared server you can price out merging or price out splitting (Sybil-style identity multiplication), but not both, and transfer-proofness beyond pairs is unattainable.

## Key results

- Theorem 1: merge-proof + split-proof + (continuity or equal treatment) is impossible for |N| >= 4.
- No mechanism prevents job transfers among 3+ agents; pairwise transfer-proofness is achievable.
- Theorem 2: the pairwise-transfer-proof methods form a line spanned by S+ (merge-proof) and S- (split-proof).
- Split-proofness is incompatible with several equity axioms that merge-proofness satisfies.

## Methods and models

Axiomatic mechanism design on a queueing problem with quasi-linear utilities and cash transfers; characterisation proofs.

## Limitations and open questions

Identical waiting costs, one server, deterministic jobs; identity is costless by assumption; results are about existence/characterisation, with no quantification of the gain from splitting.

## Relevance to us

Shows that the Sybil tension is not specific to auctions or voting: any shared-resource allocation that cannot see identities faces a merge-vs-split trade-off, and a designer must choose which manipulation to tolerate. That matters for agent platforms allocating compute or queue positions among agents that may be one operator split many ways or many operators pooling as one. Related mechanism-design roots: [[sakurai-1999-limitation]], [[yokoo-2003-characterization]], [[bachrach-2008-divide]] (where merging/splitting bounds are quantified for voting), [[aziz-2011-false]]. Root: [[douceur-2002-sybil]].

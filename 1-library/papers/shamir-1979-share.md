---
id: shamir-1979-share
type: paper
title: How to Share a Secret
authors:
- Adi Shamir
year: 1979
venue: Communications of the ACM
url: https://web.mit.edu/6.857/OldStuff/Fall03/ref/Shamir-HowToShareASecret.pdf
doi: 10.1145/359168.359176
arxiv: null
cite: 'Shamir, A. (1979). How to share a secret. Communications of the ACM, 22(11), 612-613.'
topics:
- fork-merge-security
added_by: dmarz/fm-bft-aggregation
accessed: '2026-10-03'
read_depth: full
relevance: 3
citations: 10721 (Crossref, 2026-10-03)
code: []
---

## Summary

Defines a (k, n) threshold scheme: split data D into n pieces so that any k pieces reconstruct D and any k - 1 reveal nothing (all values equally likely). The construction picks a random polynomial of degree k - 1 with constant term D over a prime field, and hands out its values at n points; Lagrange interpolation from any k points recovers D. With n = 2k - 1 the key survives destruction of floor(n/2) pieces while an opponent holding k - 1 pieces learns nothing. Pieces can be added, removed, or refreshed (new polynomial, same D) without changing D, and weighting by giving some holders several points yields hierarchical schemes. The paper frames threshold schemes as a way to let a large enough majority act while a large enough minority can block.

## Contribution

The standard information-theoretic k-of-n primitive, two pages long.

## Key results

- Proved: perfect secrecy with k - 1 shares; reconstruction with any k.
- Design properties: share size equals secret size; refreshable shares so leaked pieces from different editions cannot be combined; hierarchical weighting.
- Example: a (3, n) scheme means a dishonest executive needs at least two accomplices to forge a signature.

## Methods and models

Polynomial interpolation over integers modulo a prime.

## Limitations and open questions

Assumes honest dealer and honest shares at reconstruction; a corrupted share yields a wrong secret without detection (verifiable secret sharing came later and is not catalogued here).

## Relevance to us

Q1 and Q2. For Q2 it is the cryptographic way to make an action, not a belief, require k of n parts: split the parent's write key for its long-term memory or its identity key among sub-agents so that a merge commits only when k distinct returners co-sign. It does nothing about k returners sharing the same corruption (see [[kim-2025-correlated]]). For Q1, share refresh is relevant: if shares are re-randomised at each fork, an attacker who corrupts a sub-agent in one epoch cannot combine its share with shares from another, which limits the value of corrupting any particular part in advance. Related: [[lamport-1982-byzantine]] (signatures relax the 3m + 1 bound).

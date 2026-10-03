---
id: xiao-2004-fast
type: paper
title: Fast linear iterations for distributed averaging
authors: [Lin Xiao, Stephen Boyd]
year: 2004
venue: Systems & Control Letters
url: https://web.stanford.edu/~boyd/papers/pdf/fastavg.pdf
doi: 10.1016/j.sysconle.2004.02.022
arxiv: null
cite: "Xiao, L., & Boyd, S. (2004). Fast linear iterations for distributed averaging. Systems & Control Letters, 53(1), 65-78."
topics: [sync-consensus]
added_by: dmarz/sync-consensus
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "2770 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Asks which linear iteration x(t+1) = W x(t), using only neighbour communication, makes all nodes converge fastest to
the average of their initial values. For symmetric W, minimising the asymptotic convergence factor (the spectral
radius of W - 11^T/n) is a semidefinite program that can be solved globally and efficiently. The optimal weights
are often substantially faster than several common heuristics based on the graph Laplacian.
Structure-exploiting interior-point methods handle networks with up to about a thousand edges, and a subgradient
method handles up to 100,000 edges.

## Contribution

Turned consensus weight design into convex optimisation; the starting point for optimised gossip
([[boyd-2006-randomized]]) and for "fastest mixing" designs.

## Key results

- Abstract: optimal symmetric weights via SDP; often substantially faster than Laplacian heuristics; scalable
  algorithms for 10^3 (interior-point) and 10^5 (subgradient) edges.

## Methods and models

Linear algebra, semidefinite programming, subgradient methods. Read the abstract and introduction in the
authors' PDF.

## Limitations and open questions

Fixed, known graph; the optimisation itself is centralised (the subgradient method is a step toward distributed
design).

## Relevance to us

If a swarm can precompute its communication weights (a fixed formation), this gives the fastest possible
linear agreement; also a benchmark for learned communication policies.

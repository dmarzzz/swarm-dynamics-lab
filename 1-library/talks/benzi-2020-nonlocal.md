---
id: benzi-2020-nonlocal
type: talk
title: "Nonlocal dynamics on networks via fractional graph Laplacians: theory and numerical methods"
authors: [Michele Benzi]
year: 2020
url: https://www.youtube.com/watch?v=xWEKzC30gxk
venue: "E-NLA online seminar series on numerical linear algebra, streamed live 6 May 2020, 65 min including Q&A"
topics: [sync-consensus, meta]
added_by: shadow/sol-w6
accessed: 2026-10-03
read_depth: skim
relevance: 2
---

## Summary

Benzi (Scuola Normale Superiore, Pisa) on diffusion, random walks and consensus driven by fractional powers L^alpha (0 < alpha < 1) of the graph Laplacian, which make a sparse graph's dynamics nonlocal: an agent can jump to any node with power-law-decaying probability instead of only to neighbours. Joint work with Daniele Bertaccini, Fabio Durastante and Igor Simunec; he says the paper was accepted the day before in the Journal of Complex Networks. Read from the auto-generated transcript (speaker names and some terms garbled) plus the description abstract; skim, numbers below are as spoken. Timestamps approximate.

- 02:12 to 13:08: setup. Adjacency and (out-degree) Laplacian for directed graphs; for strongly connected digraphs the zero eigenvalue is simple (Perron-Frobenius), which is what makes L^alpha definable via the Jordan form. Classical diffusion x' = -L x and the discrete random walk with P = I - D^{-1} L are local processes.
- 13:08 to 22:07: motivation from Riascos and Mateos (Phys. Rev. E) who introduced fractional Laplacians for undirected graphs; Benzi's group extends this to nonsymmetric Laplacians, proving L^alpha is a singular M-matrix (so I minus the normalised version is still row-stochastic) using either the Jordan form or a binomial series. L^alpha of a sparse irreducible graph is dense: the Laplacian of a weighted complete graph.
- 26:45 to 40:07: decay results. For Holder-continuous functions of L the entries decay only like a power law in graph distance with exponent set by alpha (for alpha = 1/2, like the square root of distance), versus the Gaussian-fast decay of exp(-tL); this is the precise sense in which classical diffusion is localised and fractional diffusion is not. The fractional dynamics are superdiffusive (mean square displacement grows superlinearly), also proved on the infinite directed path.
- 40:07 to 44:39: network exploration. On three directed test graphs (he names Roget, a Wikipedia vote graph and Gnutella) fractional random walks with alpha = 0.25 converge to the stationary distribution much faster (log scale) than the classical walk when the graph's spectral gap is small; when the gap is already large the gain shrinks.
- 47:39 to 56:35: computation. Rational Krylov (shift-and-invert) methods for f(L) v, with the complication that for nonsymmetric L the field of values contains part of the negative real axis where x^alpha is not analytic; removing the singularity by a rank-one update helps in the symmetric case. Experiments on a power-grid graph and the directed Roget and Wiki graphs (about 1,000 nodes) show polynomial Krylov converging very slowly and rational methods converging fast.
- 56:35 to 61:15: he states that the paper also treats consensus dynamics in multi-agent systems with the fractional Laplacian but there was no time to present it. In Q&A he notes that on a directed path the out-degree Laplacian behaves as a transport (advection) operator rather than a diffusion operator, and that general digraph Laplacians mix the two.

Consensus content is therefore only asserted, not shown, in this recording.

## Relevance to us

Low direct relevance; useful as a pointer. The idea that replacing the local consensus operator L by L^alpha gives every agent a small probability of interacting with distant agents, and that this accelerates mixing on poorly connected graphs, is a concrete mechanism for speeding up agreement in sparse agent swarms without redesigning the topology. The advection-versus-diffusion remark for directed graphs is a reminder that one-way information flow between agents (e.g. orchestrator to workers) is not averaging at all. Baseline consensus background: [[olfati-saber-2007-consensus]], [[degroot-1974-reaching]] (see also [[ganesh-2020-introduction]] for the linear-averaging derivation this generalises). The Riascos-Mateos paper and the Benzi et al. JCN paper are not yet in the library.

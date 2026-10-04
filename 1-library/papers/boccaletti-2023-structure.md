---
id: boccaletti-2023-structure
type: paper
title: The structure and dynamics of networks with higher order interactions
authors: [S. Boccaletti, P. De Lellis, C. I. del Genio, K. Alfaro-Bittner, R. Criado, S. Jalan, M. Romance]
year: 2023
venue: Physics Reports
url: "https://www.iris.unina.it/retrieve/fe5dfcae-155c-4bce-ad7d-d637f0472b02/1-s2.0-S0370157323001643-main%20(1).pdf"
doi: 10.1016/j.physrep.2023.04.002
arxiv: null
cite: "Boccaletti, S., De Lellis, P., del Genio, C. I., Alfaro-Bittner, K., Criado, R., Jalan, S., & Romance, M. (2023). The structure and dynamics of networks with higher order interactions. Physics Reports, 1018, 1-64."
topics: [sync-consensus]
added_by: dmarz/sync-consensus-audit
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: "364 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

A 64-page review of networks whose interactions involve groups rather than pairs, represented as hypergraphs or
simplicial complexes. It covers the mathematical formalism (incidence tensors, generalised Laplacians, paths and
centralities on hypergraphs, generative models), spreading, social contagion and games on higher-order
structures, and, in Chapter 4, collective dynamics: synchronisation of identical and non-identical units,
consensus, pinning control and controllability of hypergraphs.

## Contribution

The broadest recent review of higher-order network dynamics from the network-science side; it extends the
pairwise-network synchronisation picture reviewed in [[arenas-2008-synchronization]] to group interactions. For our topic
the key sections are 4.1-4.3: master-stability approaches extended to hypergraphs, higher-order Kuramoto models,
and nonlinear multi-body consensus. It is the natural review to read alongside [[anwar-2024-collective]]
(swarmalators with higher-order interactions).

## Key results

- Synchronisation of identical systems (4.1): extensions of the master stability function
  ([[pecora-1998-master]]) to hypergraphs, with conditions for existence and stability of the sync state.
- Non-identical oscillators (4.2): adding or replacing pairwise Kuramoto coupling with three-body interactions can
  produce abrupt (explosive) synchronisation and desynchronisation transitions with hysteresis; Millan et al.'s
  model places oscillators on simplices (links, triangles) instead of nodes. Multilayer and adaptive higher-order
  wirings are surveyed.
- Consensus (4.3): with linear interaction functions, three-body consensus reduces to pairwise consensus on an
  equivalent graph; the nonlinear three-way consensus model (3CM) of Neuhauser et al., with
  f = (1/2) s(|x_j - x_k|)((x_j - x_i) + (x_k - x_i)), models peer pressure (pairs that agree push harder); its
  effective adjacency matrix is asymmetric, so the average state is not conserved and the consensus value shifts
  depending on s, the initial states and the hypergraph; consensus on time-varying hypergraphs and simplicial
  complexes is also covered.
- Open problems (Section 5): whether higher-order structure should be summarised by scalar or vector measures,
  how to define directed or "structured" hyperedges, and dynamics on evolving higher-order structures.

## Methods and models

Review. Representative models: Kuramoto models in which triadic terms with coupling K_2/N^2 summed over pairs
(j, k) replace or add to pairwise coupling (exact functional forms vary by reference; equation not legible in the
text extraction); hypergraph Laplacians; 3CM consensus (eqs. 61-62);
pinning control via equivalence with signed graphs. Read: abstract, table of contents, Sections 4.2-4.3 and the
conclusions; Chapters 2-3 not read.

## Limitations and open questions

- Mostly theory and simulation on synthetic hypergraphs; evidence that higher-order interactions are needed to
  explain a measured collective behaviour (rather than being an equivalent pairwise effect) is limited.
- Spatial, mobile-agent settings (where group interactions arise from proximity) are hardly covered.

## Relevance to us

If a hackathon project tests whether group-level (three-or-more agent) rules change swarm sync or consensus,
this is the map of what is known: explosive transitions and peer-pressure consensus are the two headline
effects. Background for [[anwar-2024-collective]] and for any "majority among neighbours" rule in
[[castellano-2009-statistical]]-style opinion models.

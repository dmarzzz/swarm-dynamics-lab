---
id: mendes-2004-fully
type: paper
title: 'The fully informed particle swarm: simpler, maybe better'
authors:
- Rui Mendes
- James Kennedy
- José Neves
year: 2004
venue: IEEE Transactions on Evolutionary Computation
url: https://api.openalex.org/works/W2139339670
doi: 10.1109/TEVC.2004.826074
arxiv: null
cite: 'Mendes, R., Kennedy, J., & Neves, J. (2004). The fully informed particle swarm: Simpler, maybe better. IEEE Transactions on Evolutionary Computation, 8(3), 204–210. https://doi.org/10.1109/TEVC.2004.826074'
topics:
- swarm-intelligence
- sync-consensus
added_by: dmarz/swarm-intelligence
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 1753 (OpenAlex, 2026-10-03)
code: []
---

## Summary

Replaces the "follow the best neighbour" rule of canonical PSO with a fully informed rule in which each particle is
influenced by all of its neighbours. The authors report that fully informed individuals find better solutions on all
the benchmark functions tested.

## Contribution

Changes the social term from a max (best neighbour) to a weighted average over neighbours, which is structurally the
same move CBO makes ([[pinnau-2017-consensus]]) to obtain a smooth, analysable interaction.

## Key results

- Claimed in abstract: FIPS outperforms canonical PSO on all benchmark functions tested (numbers not read).

## Methods and models

PSO variant with neighbourhood-averaged attraction across several topologies; benchmark tests (abstract only).

## Limitations and open questions

Abstract-level reading. Performance is expected to depend on the neighbourhood topology (not checked here); see [[kennedy-1999-small]].

## Relevance to us

Shows the averaging-vs-leader trade-off in swarm information use, the same axis studied in collective decision and
leadership literature.

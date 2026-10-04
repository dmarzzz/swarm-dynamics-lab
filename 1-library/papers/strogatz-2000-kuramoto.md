---
id: strogatz-2000-kuramoto
type: paper
title: "From Kuramoto to Crawford: exploring the onset of synchronization in populations of coupled oscillators"
authors: [Steven H. Strogatz]
year: 2000
venue: "Physica D: Nonlinear Phenomena"
url: https://doi.org/10.1016/s0167-2789(00)00094-4
doi: 10.1016/s0167-2789(00)00094-4
arxiv: null
cite: "Strogatz, S. H. (2000). From Kuramoto to Crawford: exploring the onset of synchronization in populations of coupled oscillators. Physica D: Nonlinear Phenomena, 143(1-4), 1-20."
topics: [sync-consensus]
added_by: dmarz/sync-consensus
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "3121 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

A historical and technical review of 25 years of work on the Kuramoto model: a large population of coupled
limit-cycle oscillators with natural frequencies drawn from a distribution, which above a coupling threshold
undergoes a phase transition in which some oscillators lock while others drift. Strogatz follows the analysis of
this bifurcation from Kuramoto's self-consistency argument through the false turns (the puzzling neutral
stability of incoherence) to Crawford's centre-manifold and amplitude-equation results, with excursions into
mathematical biology, kinetic theory and plasma physics (Landau damping).

## Contribution

The most readable entry point to the Kuramoto transition and why its stability analysis was hard; it frames the
open problems that [[ott-2008-low]] later resolved for Lorentzian frequency distributions.

## Key results

- Abstract-level: partial synchronisation above a threshold; incoherent state's linear stability is subtle
  (continuous spectrum), resolved via Landau-damping-type arguments and Crawford's amplitude expansions.

## Methods and models

Review. Kuramoto model and continuum limit. Publisher page blocked automated access; abstract read from the
OpenAlex record.

## Limitations and open questions

Review of the all-to-all model; networks and mobile oscillators came later ([[arenas-2008-synchronization]],
[[okeeffe-2017-oscillators]]).

## Relevance to us

Background reading for anyone using Kuramoto as a swarm sync primitive; seeds the citation trail of the
swarmalator literature. See also [[acebron-2005-kuramoto]].

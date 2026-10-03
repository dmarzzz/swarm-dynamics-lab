---
id: czaran-2014-selection
type: paper
title: "Selection against somatic parasitism can maintain allorecognition in fungi"
authors: ["T. Czárán", "R. F. Hoekstra", "D. K. Aanen"]
year: 2014
venue: "Fungal Genetics and Biology"
url: https://europepmc.org/article/MED/25305337
doi: 10.1016/j.fgb.2014.09.010
arxiv: null
cite: "Czárán, T., Hoekstra, R. F., & Aanen, D. K. (2014). Selection against somatic parasitism can maintain allorecognition in fungi. Fungal Genetics and Biology, 73, 128-137."
topics: [fork-merge-security, collective-decision]
added_by: dmarz/fm-biology
accessed: 2026-10-03
read_depth: abstract
relevance: 5
citations: 20  # Europe PMC citedByCount, 2026-10-03
code: []
---
## Summary

Simulation model of the joint evolution of allorecognition and somatic parasitism in an asexual fungus-like organism. On a 1000 by 1000 grid, neighbouring individuals fuse only if they share an allotype. Fusing with a parasitic individual lowers the total reproductive output of the fused pair, but the parasite takes a disproportionate share of the offspring. Results (simulated): allorecognition prevents invasion of somatic parasites, and the presence of parasite mutations selects for high allorecognition diversity. If diversity does not build up fast enough, parasites go to fixation, and once they have, diversity never builds up. The mere threat of parasitism can select for high allorecognition diversity that blocks invasion. Moderate population viscosity with weak global dispersal was optimal for this joint outcome. Earlier models without spatial structure had failed to explain the observed high allele diversity. Abstract only.

## Contribution

Shows in an explicit spatial model that defence against fusion parasites can by itself maintain many recognition alleles, provided the population is spatially structured, and that there is a race: diversity must arise before parasites fix.

## Key results

- Allorecognition blocks parasite invasion; parasites select for allorecognition diversity (simulated).
- Race condition: slow diversification leads to parasite fixation, after which diversity does not recover (simulated).
- Threat of parasitism alone sufficient to drive diversity (simulated).
- Optimum at moderate viscosity plus weak global dispersal (simulated).

## Methods and models

Spatially explicit individual-based simulation on a 1000 x 1000 lattice with fusion restricted to same-allotype neighbours, parasite mutation, and reproductive share parameters (abstract only; parameter values not checked).

## Limitations and open questions

Abstract only. Model results; parameters and sensitivity analysis not checked. Asexual-ascomycete assumptions.

## Relevance to us

Q1 and Q2, strong. Model-based support for a design principle: many distinct lineage credentials (high allotype diversity) protect a population of merging units better than one shared credential, and the protection depends on spatial structure, i.e. who can merge with whom. For a fork-merge agent, giving each fork its own credential and limiting which parts can merge directly (locality) is the analogue; a single credential for all parts is the "fixed parasite" end state. The race result is a warning: credential diversity has to be in place before compromise spreads, because after a corrupted lineage dominates the merge pool the defence does not rebuild itself. Q1: high allotype diversity also means returning parts are mutually distinguishable to each other but not interchangeable to an attacker. Related: [[bastiaans-2015-experimental]] (cost side, Crozier's paradox), [[giraud-2002-evolution]] (what happens when diversity collapses), [[cortesi-2001-genetic]].

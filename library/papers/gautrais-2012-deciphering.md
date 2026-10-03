---
id: gautrais-2012-deciphering
type: paper
title: Deciphering Interactions in Moving Animal Groups
authors: [Jacques Gautrais, Francesco Ginelli, Richard Fournier, Stéphane Blanco, Marc Soria, Hugues Chaté, Guy Theraulaz]
year: 2012
venue: PLoS Computational Biology
url: https://europepmc.org/article/MED/23028277
doi: 10.1371/journal.pcbi.1002678
arxiv: null
cite: 'Gautrais, J., Ginelli, F., Fournier, R., Blanco, S., Soria, M., Chaté, H., & Theraulaz, G. (2012). Deciphering interactions in moving animal groups. PLoS Computational Biology, 8(9), e1002678.'
topics: [collective-motion]
added_by: dmarz/collective-motion
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "370 (OpenAlex, 2026-10-03); 340 (Crossref is-referenced-by-count, 2026-10-03)"
code: []
---

## Summary

Bottom-up construction of a fish schooling model from tank video tracks (barred flagtails, Kuhlia mugil):
incremental local analysis determines the stimulus/response function for turning. Positional (attraction)
and orientational (alignment) effects both act on turning speed and depend on swimming speed, giving a
schooling model whose parameters are all estimated from data. A density-dependent behavioural change appears
in the largest groups, suggesting reaction patterns change with group size in confinement. Read at abstract
level via Europe PMC.

## Contribution

The data-driven model whose phase diagram is mapped in [[calovi-2014-swarming]]; a methodological template
for building models incrementally from individual-scale data.

## Key results

- Measured/inferred: both attraction and alignment act on turning rate, modulated by speed; group-size
  dependent behaviour.

## Methods and models

Persistent turning walker model with social terms fitted to video tracks of fish shoals in a tank (group
sizes not checked in this session).

## Limitations and open questions

Abstract-level read; tank confinement may shape the inferred rules (as the authors note for the largest groups).

## Relevance to us

A concrete pipeline for going from trajectories to an agent model, the reverse of what we do when we
simulate.

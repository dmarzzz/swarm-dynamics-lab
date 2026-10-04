---
id: heras-2019-deep
type: paper
title: Deep attention networks reveal the rules of collective motion in zebrafish
authors: [Francisco J. H. Heras, Francisco Romero-Ferrero, Robert C. Hinz, Gonzalo G. de Polavieja]
year: 2019
venue: PLOS Computational Biology
url: https://europepmc.org/article/MED/31518357
doi: 10.1371/journal.pcbi.1007354
arxiv: null
cite: 'Heras, F. J. H., Romero-Ferrero, F., Hinz, R. C., & de Polavieja, G. G. (2019). Deep attention networks reveal the rules of collective motion in zebrafish. PLOS Computational Biology, 15(9), e1007354.'
topics: [collective-motion, marl-emergence]
added_by: dmarz/collective-motion
accessed: 2026-10-03
read_depth: abstract
relevance: 5
citations: "109 (OpenAlex, 2026-10-03); 102 (Crossref is-referenced-by-count, 2026-10-03); 68 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

Trains a modular deep attention network to predict individual zebrafish movement from neighbours. On
simulated data it recovers the ground-truth rule and number of interacting neighbours. On groups of 60-100
zebrafish, pair interactions look repulsive, attractive or aligning only at low speed; at high speed they
are alignment or alignment plus close-range repulsion. Each fish aggregates neighbours by a weighted average
with weights higher for close, collision-course, faster, frontal and lateral neighbours. The number of
interacting neighbours is dynamic, typically 8-22, with 1-10 more important. Read at abstract level via
Europe PMC.

## Contribution

A bridge from data-driven inference to machine learning: interpretable attention models as rule discovery,
built on idtracker.ai trajectories.

## Key results

- Measured (model inferred): speed-dependent interaction types; attention-weighted aggregation; dynamic
  neighbour count 8-22.

## Methods and models

Pairwise-interaction subnetwork plus attention (aggregation) subnetwork; trained on idtracker.ai trajectories
of 60-100 zebrafish (Danio rerio).

## Limitations and open questions

Abstract-level read; code availability not checked.

## Relevance to us

Directly reusable approach for learning interpretable interaction rules from our agent trajectories; also
relevant to marl-emergence.

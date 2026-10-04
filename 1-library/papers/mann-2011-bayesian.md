---
id: mann-2011-bayesian
type: paper
title: Bayesian Inference for Identifying Interaction Rules in Moving Animal Groups
authors: [Richard P. Mann]
year: 2011
venue: PLoS ONE
url: https://europepmc.org/article/MED/21829657
doi: 10.1371/journal.pone.0022827
arxiv: null
cite: 'Mann, R. P. (2011). Bayesian inference for identifying interaction rules in moving animal groups. PLoS ONE, 6(8), e22827.'
topics: [collective-motion]
added_by: dmarz/collective-motion
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "56 (OpenAlex, 2026-10-03); 43 (Crossref is-referenced-by-count, 2026-10-03)"
code: []
---

## Summary

Because many different self-propelled particle models produce the same macroscopic patterns (universality),
macroscopic data cannot identify the interaction rules. Proposes a Bayesian framework for learning
interaction rules from fine-scale trajectories and tests it on simulated data: parameters can often be
inferred from few observations with quantified confidence; attraction and alignment are identifiable when
animals mill in a torus but interaction radius is not; sampling rate matters; topological and metric
neighbourhood models can be compared. Read at abstract level via Europe PMC.

## Contribution

Makes explicit the identifiability problem behind rule inference and offers model comparison as the fix;
used later on fish data (Mann et al. 2013, PLoS Comput Biol, not catalogued).

## Key results

- Simulated tests: parameter identifiability depends on the collective state (e.g., radius unidentifiable in
  milling); data rate affects inference.

## Methods and models

Bayesian likelihood of individual heading updates under candidate SPP models; posterior estimation and model
selection.

## Limitations and open questions

Abstract-level read; synthetic data only in this paper.

## Relevance to us

Use for honest rule inference on our agent swarms: report posteriors and identifiability, not point fits.

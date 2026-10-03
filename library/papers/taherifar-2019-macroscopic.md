---
id: taherifar-2019-macroscopic
type: paper
title: "A macroscopic approach for calibration and validation of a modified social force model for bidirectional pedestrian streams"
authors: [Neda Taherifar, Homayoun Hamedmoghadam, Sushmitha Sree, Meead Saberi]
year: 2019
venue: "Transportmetrica A: Transport Science"
url: https://doi.org/10.1080/23249935.2019.1636156
doi: 10.1080/23249935.2019.1636156
arxiv: null
cite: "Taherifar, N., Hamedmoghadam, H., Sree, S., & Saberi, M. (2019). A macroscopic approach for calibration and validation of a modified social force model for bidirectional pedestrian streams. Transportmetrica A: Transport Science, 15(2), 1637-1661. https://doi.org/10.1080/23249935.2019.1636156"
topics: [crowds-and-traffic]
added_by: shadow/sol-w5
accessed: 2026-10-03
read_depth: abstract
relevance: 2
citations: "45 (Semantic Scholar and OpenAlex, 2026-10-03)"
code: []
---

## Summary

The paper calibrates and validates a modified social force pedestrian model for bidirectional streams at the macroscopic level rather than per trajectory. The calibration target is the pedestrian macroscopic fundamental diagram (p-MFD), the area-wide relation between pedestrian density and flow. Per the abstract, the calibrated model reproduces the empirically observed p-MFD, including its hysteresis (different loading and unloading branches), while still generating the microscopic emergent phenomena of self-organisation and lane formation. Only the abstract and Crossref metadata were read; the paper is not open access.

## Contribution

A calibration procedure for social force models aimed at high-density counterflow where lane formation matters, using an aggregate observable (p-MFD) as the fit target. The authors note that parameter estimation and validation of social force variants in such dense, self-organising settings had received little attention.

## Key results

- Calibrated model reproduces the empirical p-MFD, including hysteresis (abstract; no numbers available without full text).
- Calibrated model consistently produces lane formation and self-organisation in bidirectional flow (abstract).

## Methods and models

Modified social force model (base: [[helbing-1995-social]]), calibrated against an area-wide pedestrian fundamental diagram built from empirical data. Details of the modification, data source and fitting algorithm not read.

## Limitations and open questions

Not assessed beyond the abstract. Open question for us: how sensitive the emergent lane formation is to the calibrated parameters, i.e. whether matching the aggregate diagram pins down the micro-dynamics or many parameter sets fit equally well.

## Relevance to us

Background for the crowds topic. The recipe (fit to a macroscopic diagram with hysteresis, then check the micro-level emergent order) transfers to validating agent-swarm simulations. Presented as a seminar in [[saberi-2018-calibrating]]. Related empirical crowd work: [[moussaid-2009-experimental]], [[moussaid-2011-simple]], [[helbing-2007-dynamics]].

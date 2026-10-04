---
id: liang-2024-unraveling
type: paper
title: Unraveling the causes of the Seoul Halloween crowd-crush disaster
authors:
- Haoyang Liang
- Seunghyeon Lee
- Jian Sun
- S. C. Wong
year: 2024
venue: PLOS ONE
url: https://pmc.ncbi.nlm.nih.gov/articles/PMC11244771/
doi: 10.1371/journal.pone.0306764
arxiv: null
cite: Liang, H., Lee, S., Sun, J., & Wong, S. C. (2024). Unraveling the causes of the Seoul Halloween crowd-crush disaster. PLOS ONE, 19(7), e0306764. https://doi.org/10.1371/journal.pone.0306764
topics:
- crowds-and-traffic
added_by: dmarz/crowds-and-traffic-audit
accessed: '2026-10-03'
read_depth: skim
relevance: 3
citations: 21 (Crossref is-referenced-by-count, 2026-10-03; OpenAlex budget exhausted)
code: []
---

## Summary

Post-hoc reconstruction of the 29 October 2022 Itaewon (Seoul) crowd crush. LTE mobile-device data show more than 38,000 visitors trapped in the neighbourhood, over three times the October average, hours before the incident. A two-population continuum (hydrodynamic) crowd model with a slope-induced leaning force is then used to simulate two streams meeting head-on in a sloping alley less than 4 m wide. The simulation gives an average crush-zone density of 7.57 ped/m^2 (maximum 9.95), crowd pressure peaking at 1,063 N/m on average (maximum 1,961 N/m) and velocity entropy up to 10.99. Simulated management interventions (inflow control and similar) reduce these indicators.

## Contribution

One of the first quantitative analyses of the Itaewon disaster, combining population data with a continuum model, and an example of the macroscopic (Hughes-type, mixed continuum) modelling tradition applied to a real crush. It complements the video-based analyses of the Love Parade ([[helbing-2012-crowd]]) and Mecca ([[helbing-2007-dynamics]]) and the accident statistics in [[feliciani-2023-trends]].

## Key results

- Measured (mobile data, as reported): over 38,000 visitors in Itaewon on the night, more than three times the average October population.
- Simulated (not measured): average density 7.57 ped/m^2 and maximum 9.95 ped/m^2 in the crush region; average crowd pressure peaking at 1,063 N/m, maximum 1,961 N/m; maximum velocity entropy 10.99 by about 22:15.
- Claimed causes: very large population, bidirectional collision of streams in a narrow alley, and "escalating panic", aggravated by the slope and darkness.
- Simulated: management strategies (for example restricting inflow or directionality) lower density, pressure and entropy relative to the baseline scenario.

## Methods and models

Multi-class continuum model: conservation equations for the density of each pedestrian stream k, momentum relaxation toward a desired velocity given by an eikonal (reactive-dynamic, Hughes-style) route choice ||∇φ^(k)|| = 1/f(Q) + g(ρ), with a pressure-gradient term and a leaning force from the terrain slope. Inflow boundary conditions informed by the population data. Indicators: density, crowd "pressure" (force per length) and velocity entropy as a disorder measure.

## Limitations and open questions

- The key numbers (density, pressure) are model outputs with simplified boundary conditions and assumed inflow rates, not measurements; the authors acknowledge limited quantitative predictive accuracy at critical moments.
- The "panic" explanation conflicts with the evidence summarised in [[haghani-2024-revisiting]] that crowds rarely panic; the model does not test it.
- I read the abstract, introduction, model description and conclusion; the management-scenario section was skimmed.

## Relevance to us

A case study for continuum (fluid) models of dense human swarms and for the role of counterflow and slope in a crush, useful as a contrast with the active-matter view of dense crowds ([[gu-2025-emergence]], [[bain-2019-dynamic]]). Shows how aggregate phone data can supply population inputs to swarm models. Review context: [[corbetta-2023-physics]].

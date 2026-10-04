---
id: bonnemain-2023-pedestrians
type: paper
title: Pedestrians in static crowds are not grains, but game players
authors:
- Thibault Bonnemain
- Matteo Butano
- Théophile Bonnet
- Iñaki Echeverría-Huarte
- Antoine Seguin
- Alexandre Nicolas
- Cécile Appert-Rolland
- Denis Ullmo
year: 2023
venue: Physical Review E
url: https://arxiv.org/abs/2201.08592
doi: 10.1103/physreve.107.024612
arxiv: '2201.08592'
cite: Bonnemain, T., Butano, M., Bonnet, T., Echeverría-Huarte, I., Seguin, A., Nicolas, A., Appert-Rolland, C., & Ullmo, D. (2023). Pedestrians in static crowds are not grains, but game players. Physical Review E, 107(2), 024612. https://doi.org/10.1103/physreve.107.024612
topics:
- crowds-and-traffic
- marl-emergence
added_by: dmarz/crowds-and-traffic
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 23 (Crossref, 2026-10-03)
code: []
---

## Summary

Shows experimentally that when an intruder crosses a dense static crowd, pedestrians plan beyond the next interaction and may briefly move towards denser regions, which reactive models (the "pedestrians as grains" view) fail to reproduce. A minimal mean-field game model, where each pedestrian optimises a cost over a future horizon given the anticipated crowd density, reproduces the observations and other everyday dense situations such as partial metro boarding.

## Contribution

Introduces mean-field game theory as an operational model of anticipation in dense crowds, contrasting with myopic force and heuristic models.

## Key results

- Measured (abstract): key features of crowd response to an intruder that reactive models miss.
- Modelled: mean-field game reproduces those features and metro boarding.

## Methods and models

Controlled experiments with a static crowd and an intruder; minimal mean-field game model (equations not read). PRE 107, 024612.

## Limitations and open questions

Minimal model; calibration across crowd types not shown. Abstract only.

## Relevance to us

Links crowd dynamics to mean-field games and mean-field RL ([[yang-2018-mean]]), the same mathematics used for large learned swarms. See also [[raulin-foissac-2026-physics]] and [[murakami-2021-mutual]].

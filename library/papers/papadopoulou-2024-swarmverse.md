---
id: papadopoulou-2024-swarmverse
type: paper
title: "swaRmverse: An R package for the comparative analysis of collective motion"
authors: ["Marina Papadopoulou", "Simon Garnier", "Andrew J. King"]
year: 2024
venue: "Methods in Ecology and Evolution"
url: https://api.crossref.org/works/10.1111/2041-210x.14460
doi: "10.1111/2041-210x.14460"
arxiv: null
cite: "Papadopoulou, M., Garnier, S., & King, A. J. (2024). swaRmverse: An R package for the comparative analysis of collective motion. Methods in Ecology and Evolution, 16(1), 29-39."
topics: [collective-motion, criticality-measurement, meta]
added_by: dmarz/collective-motion-recent
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "8 (OpenAlex W4404697844, 2026-10-03)"
code: []
---
## Summary

An R package that, from x-y-t-id trajectory data, detects collective-motion "events" from the joint distribution of polarisation and group speed, computes a suite of validated metrics per event, and places events in a low-dimensional "swarm space" for comparison across species and contexts. Built on trackdf and swaRm, it implements the comparative framework of Papadopoulou et al. 2023 and is demonstrated on several species' datasets and on agent-based simulations.

## Contribution

A standardised pipeline for comparing collective motion across species and between real and simulated groups.

## Key results

- Software (abstract): automated event detection and metric calculation; swarm-space embedding by dimensionality reduction.

## Methods and models

R package; polarisation and speed thresholds; metrics such as shape, nearest-neighbour geometry (details not read).

## Limitations and open questions

Abstract only; 2D positional data assumed.

## Relevance to us

A ready-made way to compare our simulated swarms to real data; flag for the code-scan task (CRAN package). Same first author: [[papadopoulou-2026-mechanistic]].

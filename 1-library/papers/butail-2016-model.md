---
id: butail-2016-model
type: paper
title: 'Model-free information-theoretic approach to infer leadership in pairs of zebrafish'
authors: ['Sachit Butail', 'Violet Mwaffo', 'Maurizio Porfiri']
year: 2016
venue: 'Physical Review E'
url: https://europepmc.org/article/MED/27176333
doi: 10.1103/physreve.93.042411
arxiv: null
cite: 'Butail, S., Mwaffo, V., & Porfiri, M. (2016). Model-free information-theoretic approach to infer leadership in pairs of zebrafish. Physical Review E, 93(4), 042411.'
topics: [criticality-measurement, collective-decision]
added_by: dmarz/criticality-measurement
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: '108 (OpenAlex, 2026-10-03)'
code: []
---

## Summary

Demonstrates that transfer entropy can infer leader-follower relationships in pairs of zebrafish. A
data-driven stochastic model of zebrafish swimming generates coupled pairs with controlled coupling strength and
direction, on which transfer entropy accurately and reliably recovers the leader.

## Contribution

Validation of transfer entropy for leadership detection with ground-truth synthetic data from a
calibrated animal model.

## Key results

- Transfer entropy recovers direction and extent of coupling across a wide parameter range in synthetic zebrafish pairs (simulation).

## Methods and models

Stochastic jump-persistent-turning model of zebrafish calibrated on data; transfer entropy on
heading time series.

## Limitations and open questions

Pairs only; abstract-level read.

## Relevance to us

Ground-truth validation design worth copying when we test information measures on simulated
swarms. Related: [[sattari-2022-modes]] (pitfalls even for two agents).

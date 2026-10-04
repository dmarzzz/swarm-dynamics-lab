---
id: mugica-2022-scale
type: paper
title: 'Scale-free behavioral cascades and effective leadership in schooling fish'
authors: ['Julia Múgica', 'Jordi Torrents', 'Javier Cristín', 'Andreu Puy', 'M. Carmen Miguel', 'Romualdo Pastor-Satorras']
year: 2022
venue: 'Scientific Reports'
url: https://arxiv.org/abs/2203.05473
doi: 10.1038/s41598-022-14337-0
arxiv: '2203.05473'
cite: 'Múgica, J., Torrents, J., Cristín, J., Puy, A., Miguel, M. C., & Pastor-Satorras, R. (2022). Scale-free behavioral cascades and effective leadership in schooling fish. Scientific Reports, 12(1), 10783.'
topics: [criticality-measurement, collective-motion, collective-decision]
added_by: dmarz/criticality-measurement
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: '29 (OpenAlex, 2026-10-03)'
code: []
---

## Summary

Defines behavioural cascades in tracked fish schools as avalanches of consecutive large heading
changes (above a minimum turning angle). Avalanche size and duration distributions show scale-free signatures
reminiscent of self-organised criticality, and avalanches are usually triggered by a few fish acting as effective
leaders. A Vicsek-based model with one leader subject to random reorientations qualitatively reproduces the
empirical avalanche statistics.

## Contribution

Brings avalanche statistics (the neural-criticality toolkit of [[beggs-2003-neuronal]]) to schooling
fish turning behaviour and links them to effective leadership.

## Key results

- Scale-free distributions of avalanche size and duration in schooling fish (measured).
- Avalanches typically triggered by a small number of effective leaders (measured).
- Vicsek model with a randomly reorienting leader reproduces avalanche behaviour qualitatively (simulation).

## Methods and models

Tracked fish schools; avalanche definition by thresholded turning angle; Vicsek-type model with a
leader. arXiv 2203.05473.

## Limitations and open questions

Avalanche statistics depend on the threshold; power laws alone do not prove criticality
([[touboul-2017-power]]). Abstract-level read.

## Relevance to us

Turning-avalanche analysis is cheap to run on any trajectory data, ours included; continued in
[[puy-2024-signatures]]. Compare minority-triggered cascades in [[syga-2026-minority]].

---
id: lizier-2014-jidt
type: paper
title: 'JIDT: An Information-Theoretic Toolkit for Studying the Dynamics of Complex Systems'
authors: ['Joseph T. Lizier']
year: 2014
venue: 'Frontiers in Robotics and AI'
url: https://arxiv.org/abs/1408.3270
doi: 10.3389/frobt.2014.00011
arxiv: '1408.3270'
cite: 'Lizier, J. T. (2014). JIDT: An Information-Theoretic Toolkit for Studying the Dynamics of Complex Systems. Frontiers in Robotics and AI, 1, 11.'
topics: [criticality-measurement, meta]
added_by: dmarz/criticality-measurement
accessed: 2026-10-03
read_depth: abstract
relevance: 5
citations: '420 (OpenAlex, 2026-10-03)'
code: []
---

## Summary

Describes JIDT, an open-source Java toolkit (usable from MATLAB, Octave and Python) for estimating
information-theoretic measures from time series: entropy, mutual and conditional mutual information, transfer
entropy, active information storage, their multivariate and local variants, with discrete, Gaussian, kernel and
Kraskov-Stoegbauer-Grassberger estimators.

## Contribution

The de facto software for information dynamics in complex-systems and collective-behaviour
research; used by [[crosato-2018-informative]] and [[rosas-2020-reconciling]].

## Key results

- Implements local and average transfer entropy and active information storage with interchangeable estimators (software paper).

## Methods and models

Software design paper with examples; GNU GPL v3. Code originally hosted at
http://code.google.com/p/information-dynamics-toolkit/ (URL as given in the paper; the code-scan task should
locate the current repository).

## Limitations and open questions

Abstract-level read; KSG estimators need care with sample size and embedding choices.

## Relevance to us

The tool to compute transfer entropy and active information storage on our swarm trajectories.

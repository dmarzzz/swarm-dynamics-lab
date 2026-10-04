---
id: wilting-2018-inferring
type: paper
title: 'Inferring collective dynamical states from widely unobserved systems'
authors: ['Jens Wilting', 'Viola Priesemann']
year: 2018
venue: 'Nature Communications'
url: https://arxiv.org/abs/1608.07035
doi: 10.1038/s41467-018-04725-4
arxiv: '1608.07035'
cite: 'Wilting, J., & Priesemann, V. (2018). Inferring collective dynamical states from widely unobserved systems. Nature Communications, 9(1), 2325.'
topics: [criticality-measurement]
added_by: dmarz/criticality-measurement-audit
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: '126 (OpenAlex, 2026-10-03)'
code: []
---

## Summary

When only a few units of a spreading process are observed, the naive estimate of the branching ratio m
(the regression of activity at t+1 on activity at t) is badly biased toward zero. The authors show that
subsampling scales every lag-k regression slope r_k by the same constant but leaves its exponential decay
r_k = b m^k intact, and build a multistep regression (MR) estimator that fits this decay. They validate it on
branching networks and the Bak-Tang-Wiesenfeld model, apply it to disease case reports (measles, norovirus,
MRSA) and to spiking recorded in rat, cat and monkey cortex, where it finds a reverberating, slightly
subcritical state rather than either asynchronous-irregular activity or exact criticality.

## Contribution

A subsampling-invariant estimator of distance to criticality for any process that can be approximated by
a branching (autoregressive) process. It reframes the brain-criticality debate as a measurement-bias problem,
the same problem we face when we track only part of a swarm.

## Key results

- Branching network with m = 0.99 and N = 10^4: naive estimate gives m-hat = 0.37, 0.1, 0.02 when sampling 100, 10, 1 units; MR returns the true value (simulation, Fig. 1).
- With m = 0.9, sampling 10% or 1% of units gives naive m-hat = 0.312 or 0.047 (simulation).
- In vivo spiking (monkey prefrontal, cat visual, rat hippocampus): MR m-hat between 0.963 and 0.998, median 0.984, autocorrelation times 100 to 2000 ms; the naive estimator on the same cat data gives 0.271 (measured).
- Disease data: norovirus m-hat = 0.98, measles 0.88 (Germany), MRSA about 0; across 124 countries measles m-hat correlates negatively with vaccination rate (Spearman r = -0.342) (measured).

## Methods and models

Process model A_{t+1} = m A_t + h + noise (branching or autoregressive). Subsampled activity a_t = alpha A_t
+ beta. Linear regression slopes r_k between a_t and a_{t+k} for k = 1..kmax; fit r_k = b m^k, so tau =
-Delta t / log m. Software was later released as the Python toolbox "mrestimator" (not checked in this session).

## Limitations and open questions

Assumes approximately stationary, linear (autoregressive) dynamics and a constant sampling fraction; m is a
time-scale-dependent quantity, so a reverberating state with m = 0.98 at one bin size is a statement about
tau. For swarms the "events" (startles, turns) are not obviously a branching process, though
[[poel-2022-subcritical]] uses exactly a branching ratio.

## Relevance to us

Directly usable: estimate the branching ratio of startle or turn cascades in a partly tracked swarm without
bias. Companion review: [[levina-2022-tackling]]. Related skeptic line on sampling artefacts:
[[nonnenmacher-2017-signatures]], [[priesemann-2014-spike]].

---
id: bizyaeva-2023-nonlinear
type: paper
title: Nonlinear Opinion Dynamics With Tunable Sensitivity
authors: [Anastasia Bizyaeva, Alessio Franci, Naomi Ehrich Leonard]
year: 2023
venue: IEEE Transactions on Automatic Control
url: https://arxiv.org/abs/2009.04332
doi: 10.1109/tac.2022.3159527
arxiv: '2009.04332'
cite: "Bizyaeva, A., Franci, A., & Leonard, N. E. (2023). Nonlinear opinion dynamics with tunable sensitivity. IEEE Transactions on Automatic Control, 68(3), 1415-1430."
topics: [sync-consensus, collective-decision]
added_by: dmarz/sync-consensus
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "112 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Generalises linear weighted-average (DeGroot-type) opinion dynamics to a continuous-time, multi-option nonlinear
model in which opinion exchanges are saturated. Saturation alone yields a much wider range of behaviours than
linear or earlier nonlinear models: multistable agreement and disagreement, tunable sensitivity to inputs,
robustness to disturbances, flexible switching between opinion patterns, and opinion cascades. The authors derive
network-dependent tuning rules and state-feedback dynamics for the model parameters so that
behaviour adapts to changing conditions, with applications to collective decision making and task allocation.

## Contribution

Breaks the "linear consensus always averages" limitation: with saturation, a decision-making group can be tuned
to form agreement or disagreement, respond sensitively to inputs and switch patterns when conditions change,
behaviours that linear weighted averaging ([[olfati-saber-2007-consensus]], [[degroot-1974-reaching]]) does not
produce.

## Key results

- Abstract: multistable agreement/disagreement, tunable sensitivity, robustness, cascades; network-dependent
  tuning rules and adaptive parameter feedback.

## Methods and models

Saturated nonlinear opinion exchange on networks; analysis and tuning rules. Abstract read on arXiv.

## Limitations and open questions

Abstract-level reading only; the analysis tools and any robot or human-data validation were not checked.

## Relevance to us

The modern model for fast, flexible collective decisions in robot or agent swarms (choose site A or B, split
tasks), bridging sync-consensus and collective-decision. A strong baseline against which to compare honeybee-type
decision models in the collective-decision topic.

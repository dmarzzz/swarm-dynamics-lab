---
id: gans-2026-calibrated
type: paper
title: 'Calibrated Bait: Defensive Information Design under Adversarial Fingerprinting'
authors:
- Joshua S. Gans
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2609.26797
doi: null
arxiv: '2609.26797'
cite: 'Gans, J. S. (2026). Calibrated Bait: Defensive Information Design under Adversarial Fingerprinting. arXiv preprint arXiv:2609.26797.'
topics:
- swarm-detection
added_by: dmarz/sd-honeypots
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

Models honeytoken deployment as Bayesian persuasion followed by the adversary's costly information acquisition: the defender chooses trap prevalence and appearance; the adversary can pay to fingerprint before acting. Without fingerprinting, the optimal design places the attacked pool exactly at the adversary's participation boundary ("calibrated bait"). With a perfect covert test, expensive testing preserves calibrated bait, intermediate-cost testing gives under-calibrated bait, and cheap testing yields pooling, protected segmentation or abstention. Along a path of falling fingerprinting cost, lower cost reduces trap activations without reducing genuine compromise, so evaluations against fresh attackers can overstate how long reusable bait keeps working.

## Contribution

An economic theory of when traps keep yielding detections as adversaries (such as LLM agents with cheap probing) get better at fingerprinting.

## Key results

- Closed-form, prior-dependent characterisation of optimal trap appearance under covert testing (theorem, abstract).
- Falling fingerprinting cost lowers trap activation without lowering real compromise in the under-calibrated regime: trap hit counts become a misleading health metric (theorem, abstract).

## Methods and models

Information design with receiver information acquisition. Abstract-level read.

## Limitations and open questions

Abstract only; no empirical calibration.

## Relevance to us

A warning for interpreting honeypot counts as base rates: as agents get cheaper at spotting traps, a falling hit count does not mean fewer swarms. Companion to [[gans-2026-when]]; empirical analogue [[cordeiro-2026-rouxii]]; low base-rate observation in [[reworr-2024-llm]].

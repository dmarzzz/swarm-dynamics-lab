---
id: magistrali-2026-aligned
type: paper
title: 'Aligned Alone, Misaligned Together: Forecasting Adversarial Capture in LLM Agent Populations'
authors: [Isotta Magistrali, Chen Shani]
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2608.22444
doi: null
arxiv: '2608.22444'
cite: 'Magistrali, I., & Shani, C. (2026). Aligned Alone, Misaligned Together: Forecasting Adversarial Capture in LLM Agent Populations. arXiv preprint arXiv:2608.22444.'
topics: [llm-agent-swarms, collective-decision]
added_by: shadow/sol-1
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

Populations of LLM monitors decide whether to escalate or dismiss security alerts while reading each other's decisions; the authors inject a committed minority that always pushes one way. Reported findings: two alerts a single agent judges almost identically alone can drive the population to very different collective outcomes, so a single-agent audit does not predict population behaviour; a response function calibrated from the population's benign, adversary-free operation forecasts, before any attack, how far a committed minority will move it; letting agents see each other's reasoning neutralises a weak attack but only delays a strong one (the question becomes when, not whether); and once committed agents are removed the population drifts back, so capture is a temporary state, not an absorbing trap. Abstract only.

## Contribution

Turns the committed-minority tipping result of [[ashery-2024-emergent]] and [[flint-2026-indirect]] into a forecasting tool (a response function measured in benign operation) and adds the recovery result. Same family as [[wu-2026-how]] (defection scales with deceiver proportion) and the Flag Game zealot model in [[pavlova-2026-flag]].

## Key results

- Reported: a benign-operation response function predicts the shift under a committed minority before the attack is run (magnitudes not read).
- Reported: reasoning visibility neutralises weak attacks and delays strong ones.
- Reported: capture reverses after the committed agents leave.

## Methods and models

Security-triage task, populations of LLM monitors, committed-minority injection, response-function calibration. Models, N and minority fractions not read.

## Limitations and open questions

- Abstract-level read. Whether the response function is the same object as the coupling gain of [[yang-2026-when]] or the majority force of [[de-marzo-2024-ai]] is not stated.
- Reversibility contradicts the absorbing-state picture in the naming game ([[flint-2026-group]]); the difference is probably memory (monitors see current decisions, naming-game agents accumulate payoff memory), which is testable.

## Relevance to us

A ready hackathon design: measure a population's susceptibility curve in benign runs, then test whether it predicts the tipping fraction. The reversibility claim is also directly testable in the sealed-swarm setting ([[gh-killy-netsphere-sealed-swarm-transcripts]]).

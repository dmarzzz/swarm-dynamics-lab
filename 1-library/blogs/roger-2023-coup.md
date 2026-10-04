---
id: roger-2023-coup
type: blog
title: 'Coup probes: Catching catastrophes with probes trained off-policy'
authors:
- Fabien Roger
year: 2023
url: https://www.alignmentforum.org/posts/WCj7WgFSLmyKaMwPR/coup-probes-catching-catastrophes-with-probes-trained-off
site: AI Alignment Forum
topics:
- swarm-detection
added_by: shadow/sol-w7
accessed: '2026-10-03'
read_depth: skim
relevance: 3
---

## Summary

Roger proposes cheap activation probes trained on synthetic takeover-like actions to triage suspicious model outputs. The actual experiments instead detect theft advice in Llama2-7B-Chat, testing changes in format and adversarial prefixes. Probes generalized well on this toy task, but translating that result to genuine catastrophic actions is an explicitly uncertain extrapolation.

## Key claims

- The positive training set contained 43 theft-advice sequences; 1,000 Alpaca examples supplied negatives.
- A logistic probe used residual-stream activations after layer 16; all 46 unchanged positive validation examples were detected at 1% false-positive rate.
- The suggested roughly 50% chance of catching a first real coup is a subjective forecast, not an experimental result.

## Evidence quality

Small exploratory toy experiments with methods and comparison to BERT. The author warns results were not deeply checked. Generalization to format changes and jailbroken text does not establish detection of scheming or distributed coordination.

## Relevance to us

Candidate low-cost signal for per-agent triage, not proof of swarm detection. Adversarial calibration problems in [[taylor-2025-auditing]] are a relevant counterweight.

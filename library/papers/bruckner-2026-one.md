---
id: bruckner-2026-one
type: paper
title: "One Token Is Enough: Fingerprinting and Verifying Large Language Models from Single-Token Output Distributions"
authors: ["Tomas Bruckner"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2607.10252
doi: null
arxiv: "2607.10252"
cite: "Bruckner, T. (2026). One Token Is Enough: Fingerprinting and Verifying Large Language Models from Single-Token Output Distributions. arXiv:2607.10252."
topics: [swarm-detection]
added_by: dmarz/sd-attribution
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

Defines an LLM's behavioural fingerprint as the empirical distribution of its one-token answers to trivial prompts such as "name a random number between 1 and 100", in four languages. Measuring 165 models on OpenRouter, the distributions are low-entropy (median 1.0 bit per cell) and model-specific; Jensen-Shannon divergence assigns models to their documented family at 59.5% leave-one-out accuracy (chance 18.4%), and a verification protocol reaches 7.3% equal error rate with 40 cells or under 11% with 8 cells (about 100 one-token queries).

## Contribution

Very cheap, innocuous attribution evidence, with an ecosystem audit that found a proprietary-branded endpoint indistinguishable from an open Qwen model.

## Key results

- Split halves of the same model are an order of magnitude closer than different models (abstract).
- Family assignment 59.5% vs 18.4% chance (abstract).
- EER 7.3% with 40 cells; under 11% with 8 cells (abstract).
- A proprietary-branded flagship endpoint was distributionally indistinguishable from an open-weight Qwen model (abstract).

## Methods and models

One-output-token queries across a 40-cell battery in four languages; JS divergence; biometric-style verification. Data and code released per abstract (not catalogued).

## Limitations and open questions

Needs many samples per account; a persona instruction may shift these distributions. Abstract-only reading.

## Relevance to us

A plausible covert probe for social swarms: ask accounts for a "random number". Low entropy means colluding accounts on the same model would answer alike. Weakness inside harnesses: [[wang-2026-who]].

---
id: gh-google-deepmind-synthid-text
type: code
title: "SynthID Text: reference implementation of Google DeepMind's generation-time text watermark and detectors"
repo: google-deepmind/synthid-text
url: https://github.com/google-deepmind/synthid-text
authors: ["Google DeepMind"]
year: 2024
language: Python
license: "Apache-2.0"
stars: 1130
last_commit: 2026-09-30
topics: [swarm-detection, sybil-resistance]
added_by: dmarz/sd-code-data
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: []
---

## Summary

Reference code for the SynthID Text watermark published in Nature: a Transformers mix-in for Gemma and GPT-2 that biases sampling with a keyed scheme, plus two detectors, a training-free weighted-mean detector and a trained Bayesian detector. The README recommends calibrating thresholds per token length at the desired false-positive rate. Not intended for production; the core library is on PyPI.

## What it can do for us

Watermarking is the only text-provenance method that can attribute output to a specific provider with controlled false positives, if the provider cooperates. For swarm detection it is a provider-side tool: it helps when the platform and the model vendor share keys, not when agents run open-weight models.

## Run notes

Not run.

## Limitations

Only detects text from watermarking-enabled models; open-weight models and paraphrasing remove it. Detection needs the key.

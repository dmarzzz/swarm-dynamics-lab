---
id: salman-2026-captchas
type: paper
title: "CAPTCHAs in the Agentic Era: Solvers That Learn from Every Encounter"
authors: ["Oguzhan Salman", "Kemal Bicakci"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2609.02393
doi: "10.48550/arXiv.2609.02393"
arxiv: "2609.02393"
cite: "Salman, O., & Bicakci, K. (2026). CAPTCHAs in the Agentic Era: Solvers That Learn from Every Encounter. arXiv preprint arXiv:2609.02393."
topics: ["swarm-detection", "sybil-resistance", "llm-agent-swarms"]
added_by: dmarz/sd-web-agents
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Salman and Bicakci pair a fine-tuned YOLOv8 detector with an open-weight VLM behind a confidence router, working only from screenshots and operating-system input events, with no browser automation or DOM access. It reaches 85.4% overall (84.2% macro) accuracy across 16 CAPTCHA classes. Every VLM answer becomes a training label, so the detector learns new categories after one or two encounters and recovers from adversarial perturbations aimed at it; in a simulated year-long arms race with monthly re-crafted perturbations the solver recovers each round, and a roughly 70%-accurate teacher hardens it about as well as a perfect oracle.

## Contribution

A self-improving solver that runs through OS input rather than CDP, which sidesteps the automation-artifact signals agent detectors rely on.

## Key results

- Measured (abstract): 85.4% overall, 84.2% macro accuracy over 16 classes.
- Measured (abstract): detector learns unseen categories after about one or two encounters.
- Simulated (abstract): recovers from monthly adversarial perturbation for a year.

## Methods and models

YOLOv8 plus open-weight VLM with confidence routing; screenshot input and OS-level events; self-training loop; simulated arms race. Abstract only.

## Limitations and open questions

Abstract only; arms race is simulated.

## Relevance to us

Directly tests the escape route [[choudhary-2026-what]] names: OS-level input avoids the CDP event-stream absence signature. For swarm detection, expect agents to move to this architecture.

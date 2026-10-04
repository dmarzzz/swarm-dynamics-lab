---
id: mittelsteadt-2026-detecting
type: paper
title: 'Detecting Offensive Cyber Agents: A Detection-in-Depth Approach'
authors:
- Matt Mittelsteadt
- Jam Kraprayoon
- Robin Staes-Polet
- Oskar Galeev
- Jan Wehner
- Christopher Covino
- Shaun Ee
year: 2026
venue: arXiv preprint (policy report)
url: https://arxiv.org/abs/2605.21956
doi: null
arxiv: '2605.21956'
cite: 'Mittelsteadt, M., Kraprayoon, J., Staes-Polet, R., Galeev, O., Wehner, J., Covino, C., & Ee, S. (2026). Detecting Offensive Cyber Agents: A Detection-in-Depth Approach. arXiv preprint arXiv:2605.21956.'
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

A 95-page policy report arguing that AI agents can now orchestrate cyberattacks and that defenders face a "detection gap" relative to traditional tooling. It proposes "detection-in-depth" and five mechanisms: (1) agent identifiers for critical infrastructure, (2) agent honeypots, (3) AI-automated alert triage, (4) an agentic security alert reporting standard for providers, and (5) an Agentic Cybersecurity Exchange (ACE) modelled on the Global Signal Exchange, in which model and cloud providers pool signals to catch offensive agents at their origin.

## Contribution

A policy synthesis that puts agent honeypots alongside provider-side detection. Its argument is that the most informative sensor sits at the model provider, not at the target.

## Key results

- No empirical results in the abstract; it is a framework and recommendations document.

## Methods and models

Policy analysis. Abstract-level read.

## Limitations and open questions

Abstract only; whether the honeypot section cites in-the-wild numbers (e.g. [[reworr-2024-llm]]) is not checked.

## Relevance to us

Useful framing for a write-up: honeypots are a target-side sensor with low base rates, while provider-side signal sharing sees the whole swarm. That supports pairing traps with attribution work. Related: [[bridges-2025-sok]], [[pasquini-2024-hacking]].

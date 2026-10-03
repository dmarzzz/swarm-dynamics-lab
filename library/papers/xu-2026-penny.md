---
id: xu-2026-penny
type: paper
title: 'A Penny for Your Prompts: Experiments Detecting and Mitigating LLM Usage by Survey Respondents'
authors:
- Zane Xu
- Nathan Malkin
year: 2026
venue: SOUPS 2026 (Symposium on Usable Privacy and Security)
url: https://arxiv.org/abs/2607.00403
doi: null
arxiv: '2607.00403'
cite: 'Xu, Z., & Malkin, N. (2026). A Penny for Your Prompts: Experiments Detecting and Mitigating LLM Usage by Survey Respondents. In Proceedings of the Symposium on Usable Privacy and Security (SOUPS 2026). arXiv:2607.00403.'
topics:
- swarm-detection
added_by: dmarz/sd-ai-content
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 0 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Runs survey experiments (N = 250) varying platform, survey length, explicit requests not to use AI and disabled copy-paste, and characterises LLM-assisted answers. The share of LLM-assisted responses ranged from under 10% on Prolific to over 80% on Mechanical Turk. Mitigations reduced LLM use without necessarily improving data quality. No participant used a browser-use agent at the time, but the authors ran their own agent-detection experiments and recommend keystroke recording and questions crafted to trip AI.

## Contribution

Updates the crowd-worker base rate (Prolific vs MTurk spread of an order of magnitude) and explicitly tests for browser-use agents posing as respondents.

## Key results

- Measured (abstract): LLM-assisted responses under 10% on Prolific and over 80% on MTurk.
- Measured (abstract): mitigations lowered LLM use but did not reliably raise data quality.
- Observed (abstract): no browser-use agents among participants at survey time.

## Methods and models

Controlled survey conditions across platforms; response characterisation; keystroke data; AI-targeted questions (honeypot-like instructions). Abstract read only.

## Limitations and open questions

N = 250 total across conditions. Abstract depth.

## Relevance to us

One of the few papers that looks for autonomous browser agents among "human" participants, and it found none yet, a useful negative base rate as of 2026. AI-targeted instructions are a canary technique relevant to the honeypot lane. Builds on [[veselovsky-2023-artificial]].

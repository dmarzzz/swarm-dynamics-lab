---
id: xu-2026-penny
type: paper
title: 'A Penny for Your Prompts: Experiments Detecting and Mitigating LLM Usage by Survey Respondents'
authors:
- Zane Xu
- Nathan Malkin
year: 2026
venue: Symposium on Usable Privacy and Security (SOUPS 2026)
url: https://arxiv.org/abs/2607.00403
doi: null
arxiv: '2607.00403'
cite: 'Xu, Z., & Malkin, N. (2026). A Penny for Your Prompts: Experiments Detecting and Mitigating LLM Usage by Survey Respondents. In Symposium on Usable Privacy and Security (SOUPS 2026). arXiv:2607.00403.'
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

A series of surveys (N = 250) measured how often crowd workers use LLMs to answer and tested mitigations: platform choice, survey length, asking participants not to use AI, and disabling copy-paste. LLM-assisted responses had distinct characteristics; prevalence ranged from under 10% on Prolific to over 80% on Mechanical Turk. Mitigations reduced LLM use but did not necessarily improve data quality. No participant used a browser-use agent at the time, so the authors ran their own agent-detection experiments. They recommend recording keystrokes and writing instructions and questions aimed at AI.

## Contribution

A measured base rate of AI-assisted responses by platform, plus the recommendation to plant AI-targeted questions (a survey canary) alongside keystroke telemetry.

## Key results

- LLM-assisted responses: under 10% on Prolific, over 80% on MTurk (measured, N = 250).
- No browser-use agents observed among participants at study time (measured).
- Mitigations cut LLM use without clearly improving quality (measured).

## Methods and models

Randomised survey conditions across platforms; response characterisation; keystroke analysis. Abstract-level read.

## Limitations and open questions

Abstract only; small N; agent experiments were the authors' own.

## Relevance to us

Survey platforms are a population where agent prevalence has been measured, and where canary questions are already practice. Related: [[wang-2026-towards]] (persona agents defeat text detectors), [[rao-2025-detecting]].

## Notes from dmarz/sd-ai-content

This lane catalogued the same source independently (added_by dmarz/sd-ai-content, accessed 2026-10-03). Its distinct content:

- Frontmatter `venue` in this lane's version: SOUPS 2026 (Symposium on Usable Privacy and Security)
- Frontmatter `cite` in this lane's version: 'Xu, Z., & Malkin, N. (2026). A Penny for Your Prompts: Experiments Detecting and Mitigating LLM Usage by Survey Respondents. In Proceedings of the Symposium on Usable Privacy and Security (SOUPS 2026). arXiv:2607.00403.'
- Frontmatter `citations` in this lane's version: 0 (Semantic Scholar, 2026-10-03)

### Summary

Runs survey experiments (N = 250) varying platform, survey length, explicit requests not to use AI and disabled copy-paste, and characterises LLM-assisted answers. The share of LLM-assisted responses ranged from under 10% on Prolific to over 80% on Mechanical Turk. Mitigations reduced LLM use without necessarily improving data quality. No participant used a browser-use agent at the time, but the authors ran their own agent-detection experiments and recommend keystroke recording and questions crafted to trip AI.

### Contribution

Updates the crowd-worker base rate (Prolific vs MTurk spread of an order of magnitude) and explicitly tests for browser-use agents posing as respondents.

### Key results

- Measured (abstract): LLM-assisted responses under 10% on Prolific and over 80% on MTurk.
- Measured (abstract): mitigations lowered LLM use but did not reliably raise data quality.
- Observed (abstract): no browser-use agents among participants at survey time.

### Methods and models

Controlled survey conditions across platforms; response characterisation; keystroke data; AI-targeted questions (honeypot-like instructions). Abstract read only.

### Limitations and open questions

N = 250 total across conditions. Abstract depth.

### Relevance to us

One of the few papers that looks for autonomous browser agents among "human" participants, and it found none yet, a useful negative base rate as of 2026. AI-targeted instructions are a canary technique relevant to the honeypot lane. Builds on [[veselovsky-2023-artificial]].

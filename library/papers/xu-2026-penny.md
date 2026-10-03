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

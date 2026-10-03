---
id: teoh-2025-captchas
type: paper
title: Are CAPTCHAs Still Bot-hard? Generalized Visual CAPTCHA Solving with Agentic
  Vision Language Model
authors:
- Xiwen Teoh
- Yun Lin
- Siqi Li
- Ruofan Liu
- Avi Sollomoni
- Yaniv Harel
- Jin Song Dong
year: 2025
venue: 34th USENIX Security Symposium (USENIX Security 25), pp. 3747-3766
url: https://www.usenix.org/conference/usenixsecurity25/presentation/teoh
doi: null
arxiv: null
cite: Xiwen Teoh; Yun Lin; Siqi Li; Ruofan Liu; Avi Sollomoni; Yaniv Harel; Jin Song
  Dong. (2025). Are CAPTCHAs Still Bot-hard? Generalized Visual CAPTCHA Solving with
  Agentic Vision Language Model. 34th USENIX Security Symposium (USENIX Security 25),
  pp. 3747-3766. https://www.usenix.org/conference/usenixsecurity25/presentation/teoh
topics:
- swarm-detection
added_by: shadow/sol-g51
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Halligan treats visual CAPTCHA instructions as optimization objectives and challenge content as a search space, using a vision-language model to solve unseen challenge types. The official abstract reports evaluation across 26 types plus a thirty-day in-the-wild comparison.

## Contribution

Frames visual CAPTCHA solving as search with a vision-language model and evaluates on 26 challenge types plus a 30-day live comparison.

## Key results

- 60.7% solving on 2,600 challenges across 26 types; 70.6% on unseen in-the-wild challenges over thirty days.

## Methods and models

Generalized vision-language-model solver framed as a search problem.

## Limitations and open questions

A visual challenge solving rate is not an end-to-end account-farming success rate; nonvisual defenses and deployment policies may differ.

## Relevance to us

Measures how far CAPTCHAs still gate automated agents (60.7% on 2,600 challenges, 70.6% on unseen live ones); background for any detection design that leans on challenges.

## Access provenance

Read the primary abstract directly or via Exa content extraction on 2026-10-03. A public full-text URL was found, but the entry is not marked full.

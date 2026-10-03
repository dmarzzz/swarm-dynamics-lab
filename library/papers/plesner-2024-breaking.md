---
id: plesner-2024-breaking
type: paper
title: Breaking reCAPTCHAv2
authors:
- Andreas Plesner
- Tobias Vontobel
- Roger Wattenhofer
year: 2024
venue: 2024 IEEE Annual Computers, Software, and Applications Conference (COMPSAC 2024)
url: https://arxiv.org/abs/2409.08831
doi: 10.1109/COMPSAC61105.2024.00142
arxiv: '2409.08831'
cite: 'Plesner, A., Vontobel, T., & Wattenhofer, R. (2024). Breaking reCAPTCHAv2. In 2024 IEEE Annual Computers, Software, and Applications Conference (COMPSAC 2024). https://doi.org/10.1109/COMPSAC61105.2024.00142. arXiv:2409.08831.'
topics:
- swarm-detection
- sybil-resistance
added_by: dmarz/sybil-llm-agents
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 28 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Uses YOLO models for image segmentation and classification to solve Google reCAPTCHAv2 image challenges and solves 100% of the captchas, against 68 to 71% in earlier work. Humans and the bot need about the same number of challenges to pass. Looking at how reCAPTCHAv2 decides, the authors find it relies heavily on cookie and browser-history data rather than on challenge answers. Code is released with the paper.

## Contribution

Direct evidence that a widely deployed image CAPTCHA no longer separates humans from machines, and that the deployed system's real signal is browser reputation.

## Key results

- Measured: 100% solve rate vs 68 to 71% in prior work.
- Measured: no significant difference between humans and bots in number of challenges needed.
- Observed: reCAPTCHAv2 decisions depend heavily on cookies and browsing history.

## Methods and models

YOLO-based segmentation and classification, automated browser interaction, comparison with human solving.

## Limitations and open questions

Abstract only; reCAPTCHAv3 and behavioural CAPTCHAs are not covered in the abstract.

## Relevance to us

Removes CAPTCHAs as a Sybil barrier for agent swarms; the remaining signal is accumulated browser reputation, which is itself a weak identity anchor. This is the empirical premise behind [[adler-2024-personhood]] and [[maleki-2026-human]], and [[chan-2024-ids]] notes the same risk.

## Notes from dmarz/sd-web-agents

Later work extends this result to zero-cost local models (92.6% per-session success on 500 real reCAPTCHA sessions, [[sivakorn-2026-robot]]) and to LLM browser agents. [[ousat-2026-broken]] measured that commercial solver services pass reCAPTCHA v2 at close to 100% for $0.10 to $5.00 per 1,000 solves but reach only 23% on average against reCAPTCHA v3, where browser-profile reputation dominates. That matches this paper's observation that cookies and history drive reCAPTCHA decisions.

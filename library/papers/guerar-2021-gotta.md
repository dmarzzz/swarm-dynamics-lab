---
id: guerar-2021-gotta
type: paper
title: "Gotta CAPTCHA 'Em All: A Survey of 20 Years of the Human-or-computer Dilemma"
authors: ["Meriem Guerar", "Luca Verderame", "Mauro Migliardi", "Francesco Palmieri", "Alessio Merlo"]
year: 2021
venue: "ACM Computing Surveys, 54(9)"
url: https://arxiv.org/abs/2103.01748
doi: "10.1145/3477142"
arxiv: "2103.01748"
cite: "Guerar, M., Verderame, L., Migliardi, M., Palmieri, F., & Merlo, A. (2021). Gotta CAPTCHA 'Em All: A Survey of 20 Years of the Human-or-computer Dilemma. ACM Computing Surveys, 54(9), 1-33. https://doi.org/10.1145/3477142. arXiv:2103.01748."
topics: ["swarm-detection", "sybil-resistance"]
added_by: dmarz/sd-web-agents
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: "47 (Crossref, 2026-10-03)"
code: []
---

## Summary

Guerar, Verderame, Migliardi, Palmieri and Merlo review twenty years of CAPTCHA schemes, propose a classification covering text, image, audio, video, puzzle, game and behavioural (frictionless) designs, summarise the most successful attack per category, and trace how each category evolved under attack. They discuss security, usability and compatibility limits and open problems for next-generation CAPTCHAs. The motivating figure is that malicious bots generated nearly a quarter of website traffic in 2019 (cited industry report).

## Contribution

The standard review of the CAPTCHA arms race up to 2021, before multimodal LLM solvers.

## Key results

- Review: taxonomy of CAPTCHA categories with best-known attacks per category (abstract).
- Cited context (abstract): malicious bots generated nearly a quarter of web traffic in 2019.

## Methods and models

Literature survey. Abstract only.

## Limitations and open questions

Pre-dates LLM and VLM solvers; see [[wang-2025-cognition]], [[luo-2025-open]] for the 2025-26 picture.

## Relevance to us

Review article for the CAPTCHA branch of agent detection. Its conclusion that each CAPTCHA family falls to the next ML generation is borne out by [[plesner-2024-breaking]] and [[sivakorn-2026-robot]].

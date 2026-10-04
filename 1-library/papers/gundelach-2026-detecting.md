---
id: gundelach-2026-detecting
type: paper
title: "Detecting Bot Detection: Prevalence, Techniques, and Implications for Web Measurement Research"
authors: ["Ralf Gundelach", "Michael Mühlhauser", "Dominik Herrmann"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2606.14525
doi: "10.48550/arXiv.2606.14525"
arxiv: "2606.14525"
cite: "Gundelach, R., Mühlhauser, M., & Herrmann, D. (2026). Detecting Bot Detection: Prevalence, Techniques, and Implications for Web Measurement Research. arXiv preprint arXiv:2606.14525."
topics: ["swarm-detection"]
added_by: dmarz/sd-web-agents
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Gundelach, Mühlhauser and Herrmann survey top security, privacy and measurement venues and find 83% of papers that use browser automation never discuss being blocked by bot detection. They visit 10,000 websites with four browser configurations (40,000 visits) with instrumentation that sees when pages probe for automation. Headless Chromium hits a 15% soft-block rate versus 7% for other configurations; 82% of blocks are attributable to bot detection, mostly by Cloudflare (37% block rate) and Akamai (26%). 75% of headless-only blocks are caused by header-level signals alone.

## Contribution

Measures how widespread automation probing is on the live web, from the automated client's side, with a taxonomy of detection techniques.

## Key results

- Measured (abstract): 83% of surveyed measurement papers omit bot-detection blocking.
- Measured (abstract): headless Chromium soft-block rate 15% vs 7% for other configurations.
- Measured (abstract): 82% of blocks due to bot detection (59% vendor-confirmed); Cloudflare 37% and Akamai 26% block rates.
- Measured (abstract): 75% of headless-only blocks explained by header signals alone.

## Methods and models

Literature survey; 10,000-site measurement across four browser configurations; custom instrumentation for detection probes; header-spoofing experiment. Abstract only.

## Limitations and open questions

Abstract only. Measures blocking of research crawlers, not LLM agents specifically.

## Relevance to us

Gives a prevalence baseline for the defences an agent swarm meets in the wild, and a taxonomy of probes we could reuse in a detector. Complements [[fayolle-2026-internet]].

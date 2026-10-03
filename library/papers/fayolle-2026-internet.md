---
id: fayolle-2026-internet
type: paper
title: 'On the Internet, Nobody Knows You''re an LLM Bot: Unmasking Web Agents with Multi-Layer Fingerprinting'
authors:
- Iliana Fayolle
- Sihem Bouhenniche
- Samuel Pélissier
- Pierre Laperdrix
- Clémentine Maurice
- Walter Rudametkin
year: 2026
venue: arXiv preprint
url: https://arxiv.org/html/2606.30119
doi: null
arxiv: '2606.30119'
cite: 'Fayolle, I., Bouhenniche, S., Pélissier, S., Laperdrix, P., Maurice, C., & Rudametkin, W. (2026). On the Internet, Nobody Knows You''re an LLM Bot: Unmasking Web Agents with Multi-Layer Fingerprinting. arXiv preprint arXiv:2606.30119.'
topics:
- swarm-detection
added_by: dmarz/sd-honeypots
accessed: '2026-10-03'
read_depth: full
relevance: 5
citations: null
code: []
---

## Summary

Nine honeysites, each behind zero, one or several anti-bot defences (robots.txt, User-Agent filtering, reCAPTCHA v3, Prosopo CAPTCHA, Anubis proof-of-work, Cloudflare Turnstile, Bot Fight Mode plus Block AI Bots, and two stacked combinations), were visited by 12 tools: HTTP scrapers, Selenium/Playwright/Puppeteer, and six LLM web agents (cloud and local), with stealth modes on and off. Each visit was logged at the IP, TLS (JA4) and browser-fingerprint layers and the authors trained classifiers to tell humans, automation frameworks and individual web agents apart.

## Contribution

First systematic test of current anti-bot stacks against LLM web agents plus a measured answer to "can a server tell an LLM agent from a human from a single visit". It also documents that stealth features backfire.

## Key results

- 1,449 active visits initiated, 1,383 usable with browser fingerprints and 1,358 TLS Client Hellos (Jan 28 to Feb 24, 2026) (measured).
- OpenClaw and Claude for Chrome (Sonnet 4.5) bypassed every tested defence, including the Prosopo CAPTCHA; ChatGPT Agent solved Prosopo but stalled on Turnstile (measured).
- Stacked defences blocked most tools; stealth modes of Crawl4AI and BrowserUse stayed detectable and introduced fingerprint inconsistencies (e.g. a non-standard "default" notification permission) (measured).
- Random-forest classification: IP features alone 0.596 accuracy (F1 0.540); IP+TLS 0.806 (F1 0.791); all layers near-perfect for every class (measured, 10 seeds, 80/20 split).
- Cloud agents carry stable unique tells (ChatGPT Agent: fixed screen resolution, 13 CPU cores, `signature-agent` headers; Skyvern: Edge, 32 cores); local agents share the human's browser and IP and are the hardest to separate (measured).
- Consumer assistants (ChatGPT, Gemini, Perplexity) fetch with simple HTTP requests and are trivial to detect (observation, excluded from the main study).

## Methods and models

nginx plus tshark capture at a reverse proxy; JA4 TLS fingerprints; a FingerprintJS/AmIUnique-style browser script; a dynamic page_id and a POST form to prove live interaction; attribute scoring by intra-tool probability and inter-tool exclusivity (V-score, A-score); RF, XGBoost and CatBoost classifiers with SMOTE.

## Limitations and open questions

Two Linux laptops as the local baseline; university IPs may have earned reputation that let some tools past; behavioural and canvas/GPU fingerprinting left out; the tool landscape moves monthly. Classification is on the authors' own instrumented visits, not wild traffic (a passive set is in an appendix).

## Relevance to us

Gives us the per-visit fingerprint features that let a honeysite separate agent families, which is the precondition for counting how many distinct operators sit behind a swarm. Local agents riding a human's browser are the blind spot. Complements [[seiden-2026-identifying]] (where content goes after the visit) and [[reworr-2024-llm]] (behavioural trap). Bot-traffic share background: [[hoetzlein-2025-protecting]].

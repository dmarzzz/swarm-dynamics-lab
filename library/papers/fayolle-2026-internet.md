---
id: fayolle-2026-internet
type: paper
title: "On the Internet, Nobody Knows You're an LLM Bot: Unmasking Web Agents with Multi-Layer Fingerprinting"
authors: ["Iliana Fayolle", "Sihem Bouhenniche", "Samuel Pélissier", "Pierre Laperdrix", "Clémentine Maurice", "Walter Rudametkin"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2606.30119
doi: "10.48550/arXiv.2606.30119"
arxiv: "2606.30119"
cite: "Fayolle, I., Bouhenniche, S., Pélissier, S., Laperdrix, P., Maurice, C., & Rudametkin, W. (2026). On the Internet, Nobody Knows You're an LLM Bot: Unmasking Web Agents with Multi-Layer Fingerprinting. arXiv preprint arXiv:2606.30119."
topics: ["swarm-detection", "llm-agent-swarms", "sybil-resistance"]
added_by: dmarz/sd-web-agents
accessed: '2026-10-03'
read_depth: full
relevance: 5
citations: null
code: []
---

## Summary

Fayolle, Bouhenniche, Pélissier, Laperdrix, Maurice and Rudametkin (Inria) deployed ten honeysites under a random domain, each behind zero, one or several anti-bot defences (robots.txt, User-Agent filtering, reCAPTCHA v3, Prosopo CAPTCHA, the Anubis proof-of-work, Cloudflare Turnstile, Cloudflare Bot Fight Mode plus Block AI Bots, and two combined stacks). Between 28 January and 24 February 2026 they drove 1,449 visits from humans, three HTTP scrapers, three automation frameworks and six LLM web agents (OpenClaw, Claude for Chrome, Crawl4AI, BrowserUse local and cloud, ChatGPT Agent, Skyvern), and recorded IP, JA4 TLS, HTTP header and JavaScript browser fingerprints for each. OpenClaw and Claude for Chrome on Sonnet 4.5 passed every defence, including the combined stacks. A Random Forest on all layers classifies humans, frameworks and each agent near perfectly; single layers do much worse (IP accuracy 0.596, JA4 alone 0.454, browser fingerprint 0.931, IP+TLS 0.806). Stealth modes made Crawl4AI and BrowserUse more detectable, not less.

## Contribution

First measurement that pits current deployed anti-bot products against LLM web agents and then asks which protocol layer separates agents from humans and from each other using single-request fingerprints. It sits beside [[wang-2026-fp-agent]] (behavioural) and [[kang-2026-whose]] (timing plus TLS/HTTP plus behaviour) as the third independent 2026 honeysite study.

## Key results

- Measured: OpenClaw and Claude for Chrome (Sonnet 4.5) bypassed all eight single defences and both combined stacks; ChatGPT Agent was stopped only by Turnstile (Table 3).
- Measured: Cloudflare Bot Fight Mode did not block cURL or wget from university IPs; it only acts on known datacenter ranges.
- Measured: Random Forest accuracy by layer: IP 0.596, JA4 0.454, browser fingerprint 0.931, IP+TLS 0.806, all layers near 1.0 (10 seeds, 1,370 fingerprints).
- Measured: cloud agents leak fixed environments (ChatGPT Agent: 13 CPU cores, one unique screen resolution, signature and signature-agent headers; Skyvern: 32 cores, Edge browser); local agents inherit the user's browser and are hardest to separate.
- Measured: BrowserUse-Stealth exited from low-reputation datacenter IPs (0.98 flagged) instead of its residential proxies; Crawl4AI stealth reported a non-standard 'default' notifications permission.
- Observed: Claude-based agents refused to solve the Prosopo CAPTCHA in 20 attempts, citing policy; Skyvern, when blocked, invented credentials and looped posting.
- Passive four-month capture (Jan to May 2026) on the same sites saw crawlers and scanners but no traffic matching the studied web agents.

## Methods and models

Nine nginx honeysites plus an unprotected main site, HTTP/1.1, HTTP/2 and HTTP/3. Capture with tshark (JA4), nginx logs and a FingerprintJS/AmIUnique-style script. Agents prompted to submit a three-field form that echoes a dynamic page_id, with a 'normal' prompt and a 'special' prompt allowing external solvers. Discriminative power per attribute scored with intra-tool probability, inter-tool exclusivity, V-score and A-score; classifiers Random Forest, XGBoost, CatBoost with SMOTE and an 80/20 split. Artifacts on anonymous.4open.science.

## Limitations and open questions

Two Linux laptops, university IPs and a single month of active testing; six agents; default CAPTCHA settings. Results are a snapshot: several tools changed behaviour during the four months. Classification is closed-world over known tools. Human baseline is the authors browsing. The paper does not test behavioural features, and it does not test Web Bot Auth adoption beyond noting ChatGPT Agent's signature headers.

## Relevance to us

This is the cleanest evidence that a honeysite with layered instrumentation can tell LLM agents apart from humans and attribute them to a product, while the deployed defences mostly let them through. For a swarm-detection experiment, it gives us a feature list (JA4, Sec-CH-UA vs userAgentData consistency, CPU cores, permissions, screen size) and a warning: local agents riding a real user's browser are the hard case. Compare [[wang-2026-fp-agent]], [[kang-2026-whose]], [[choudhary-2026-what]], [[ousat-2026-broken]] and the earlier evasive-bot work [[venugopalan-2024-fp-inconsistent]]. The cryptographic alternative it points to is Web Bot Auth, see [[gh-cloudflare-web-bot-auth]] and [[cloudflare-2025-forget]].

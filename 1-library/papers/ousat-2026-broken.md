---
id: ousat-2026-broken
type: paper
title: "Broken Gates: Re-evaluating Web Bot Defenses in the Age of LLM Agents"
authors: ["Behzad Ousat", "Nikita Turkmen", "Lalchandra Rampersaud", "Dillan Bailey", "Amin Kharraz"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2607.18659
doi: "10.48550/arXiv.2607.18659"
arxiv: "2607.18659"
cite: "Ousat, B., Turkmen, N., Rampersaud, L., Bailey, D., & Kharraz, A. (2026). Broken Gates: Re-evaluating Web Bot Defenses in the Age of LLM Agents. arXiv preprint arXiv:2607.18659."
topics: ["swarm-detection", "llm-agent-swarms", "sybil-resistance"]
added_by: dmarz/sd-web-agents
accessed: '2026-10-03'
read_depth: full
relevance: 4
citations: "1 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

Ousat, Turkmen, Rampersaud, Bailey and Kharraz (FIU) tested seven commercial CAPTCHA-solving services and six LLM browser agents (cloud and self-hosted Browser-Use, Skyvern, Manus, OpenManus, SeeAct, BrowserOS, Perplexity Comet, NanoBrowser extension) against hCaptcha easy/hard, reCAPTCHA v2 checkbox/invisible, reCAPTCHA v3 and Turnstile on seven test subdomains that had been live for about six months. Solver services pass challenge-based CAPTCHAs at close to 100% for $0.10 to $5.00 per 1,000 solves but average only 23% against reCAPTCHA v3 (best 63%). Agents mostly fail challenges unless they have a dedicated solver (cloud Skyvern). Against non-interactive checks they complete the form but get low scores, except NanoBrowser, which runs inside a real user profile.

## Contribution

Separates the two things deployed bot management measures: challenge solving, which is commoditised, and environment authenticity, which is the actual remaining barrier. The Browser-Use vs NanoBrowser comparison holds behaviour roughly fixed and varies the browser profile.

## Key results

- Measured: solver services at or near 100% on reCAPTCHA v2, hCaptcha easy and Turnstile; prices $0.10 to $5.00 per 1,000 solves.
- Measured: solver services average 23% success on reCAPTCHA v3 at the 0.5 threshold; best provider 63%; two providers produced no verifiable tokens.
- Measured: Browser-Use and NanoBrowser produce near-identical event traces (about 11 s sessions) yet only NanoBrowser passes reCAPTCHA v3; Browser-Use scores 0.1 to 0.3.
- Observed: Comet declined to submit login forms, a policy refusal rather than a capability failure.
- Cited (not measured here): 65% of attacks by 22 credential-stuffing groups used solver services plus residential proxies.

## Methods and models

Seven subdomains each with one defence and a fixed HTML form; 100 solver tasks per service per site, tokens verified with vendor siteverify APIs; agents screened with five attempts and expanded to ten more if any succeeded; success = at least one bypass per phase. Interaction traces recorded for the reCAPTCHA v3 comparison.

## Limitations and open questions

Small agent trial counts (5 to 15 per configuration) and a lenient 'at least once' success criterion. Default agent configurations only. The environment-authenticity claim rests mainly on one pair of agents. No code release by design.

## Relevance to us

For swarm detection, the defender's real signal is accumulated browser reputation, which is expensive to manufacture per identity. That is a per-Sybil cost, the quantity [[plesner-2024-breaking]] also pointed to. An agent swarm that runs inside many aged real profiles defeats it; one that spins up clean instrumented browsers does not. Compare [[fayolle-2026-internet]] (Claude for Chrome bypassed everything from a real profile).

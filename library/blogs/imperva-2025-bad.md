---
id: imperva-2025-bad
type: blog
title: "2025 Bad Bot Report: The Rapid Rise of Bots and the Unseen Risk for Business"
authors: [Imperva (Thales) Threat Research]
year: 2025
url: https://www.imperva.com/resources/wp-content/uploads/sites/6/reports/2025-Bad-Bot-Report.pdf
site: Imperva annual report (vendor, PDF)
topics: [swarm-detection]
added_by: dmarz/sd-informal
accessed: 2026-10-03
read_depth: skim
relevance: 3
---

## Summary

Twelfth annual vendor report on automated web traffic, based on Imperva's network in 2024 (13 trillion bad-bot requests blocked across thousands of domains). Headline: automated traffic was 51% of all web traffic in 2024, the first time in a decade it exceeded human traffic (49%); bad bots were 37% (up from 32% in 2023) and good bots 14%. Bad bots were 19% of bot traffic in 2015. Simple bot attacks rose to 45% of bot attacks (from 40%), which Imperva attributes to AI tools lowering the barrier; advanced plus moderate were 55%. 21% of ISP-routed bot attacks used residential proxies; 44% of advanced bot traffic targeted APIs; account-takeover attacks rose 40% year on year. Imperva blocked an average of 2 million "AI-powered" attacks a day. Of attacks it attributes to AI tools, 54% carried the ByteSpider user agent, 26% AppleBot, 13% ClaudeBot, 6% ChatGPT-User; Imperva itself attributes ByteSpider's lead to spoofing, because criminals disguise bots as whitelisted crawlers.

## Key claims

- Generative AI increases the volume of simple bots and helps attackers analyse failed attempts and refine evasion.
- Bots mimic browsers (a stated share of bot attacks use Chrome user agents) and use residential proxies to evade detection.

## Evidence quality

Vendor marketing report; methodology is one paragraph, classification of "AI-powered" attacks is not defined and appears to rest partly on user-agent strings, which the report itself says are spoofed. Treat the AI attribution figures as weak; the overall bot share is consistent in direction with other vendors but not independently checked. Skimmed: read the executive summary, key findings, AI-powered attacks section and methodology.

## Relevance to us

A widely quoted base rate (51% automated traffic) with a caution worth recording: "AI agent" counts based on declared user agents conflate real AI crawlers with impostors using their names. That is why cryptographic agent identity ([[cloudflare-2025-forget]]) and behaviour-based fingerprinting ([[cloudflare-2025-perplexity]]) matter for any population estimate.

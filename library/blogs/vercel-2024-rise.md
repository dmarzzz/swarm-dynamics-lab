---
id: vercel-2024-rise
type: blog
title: "The rise of the AI crawler"
authors: [Giacomo Zecchini, Alice Alexandra Moore, Malte Ubl, Ryan Siddle]
year: 2024
url: https://vercel.com/blog/the-rise-of-the-ai-crawler
site: Vercel Blog (vendor, with MERJ)
topics: [swarm-detection]
added_by: dmarz/sd-informal
accessed: 2026-10-03
read_depth: full
relevance: 3
---

## Summary

Vendor measurement post (17 December 2024) by Vercel and the agency MERJ on AI crawler behaviour across Vercel's network, nextjs.org and two job-board sites. In the month measured, GPTBot made 569 million requests and Anthropic's Claude crawler 370 million, together about 20% of Googlebot's 4.5 billion; GPTBot, Claude, AppleBot and PerplexityBot together made nearly 1.3 billion fetches (about 28% of Googlebot). None of the major AI crawlers rendered JavaScript, except Gemini (via Googlebot's infrastructure) and AppleBot; ChatGPT and Claude fetched JS files (11.50% and 23.84% of requests) without executing them. ChatGPT spent 34.82% of fetches on 404s and Claude 34.16%, versus 8.22% for Googlebot; ChatGPT spent 14.36% following redirects. All AI crawlers operated from US data centres. Microsoft Copilot was excluded because it has no unique user agent.

## Key claims

- AI crawlers are inefficient (high 404 and redirect rates, fetching stale /static/ assets) compared with Googlebot.
- Client-side rendered content is invisible to most AI crawlers.

## Evidence quality

Vendor telemetry, one month, declared user agents only. No uncertainty or method detail beyond data sources. Marketing angle (server-side rendering advice).

## Relevance to us

Behavioural fingerprints of 2024 AI crawlers (no JS execution, high 404 rate, single-region origin) are concrete features that separate them from browsers and from Googlebot. These features predate browser-using agents that do execute JS, so they will not transfer to agentic browsing. Complements [[cloudflare-2025-from]].

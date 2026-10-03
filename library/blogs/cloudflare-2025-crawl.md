---
id: cloudflare-2025-crawl
type: blog
title: "The crawl before the fall… of referrals: understanding AI's impact on content providers"
authors: [David Belson, Sam Rhea]
year: 2025
url: https://blog.cloudflare.com/ai-search-crawl-refer-ratio-on-radar/
site: Cloudflare Blog (vendor, Radar data)
topics: [swarm-detection]
added_by: dmarz/sd-informal
accessed: 2026-10-03
read_depth: full
relevance: 2
---

## Summary

Cloudflare Radar post (1 July 2025) introducing a crawl-to-referral ratio per AI or search platform: HTML requests from the platform's declared crawler user agents divided by HTML requests whose Referer header names the platform. For 19 to 26 June 2025 the ratio ranged from about 70,900:1 for Anthropic down to 0.1:1 for Mistral. Cloudflare notes that native apps (including Claude's) send no Referer header, so ratios for those providers are overstated by an unknown amount. Google prefetch traffic from its ASN is excluded. The post also launched a public directory of Cloudflare Verified Bots with per-bot pages and API access.

## Key claims

- AI platforms crawl far more than they refer traffic, unlike legacy search crawlers that sent roughly one visitor per couple of crawls (Cloudflare's characterisation).
- Ratios shift with crawl behaviour; GPTBot had periods of near-zero crawling in June 2025.

## Evidence quality

Vendor telemetry with a clearly stated metric and a stated bias (missing Referer from native apps). Declared crawlers only.

## Relevance to us

Peripheral to swarm detection; useful as an example of attributing automated traffic to an operator by joining two declared signals (user agent and referrer), and as the public Verified Bots directory, which is a reference list of declared agents against which undeclared ones (as in [[cloudflare-2025-perplexity]]) stand out.

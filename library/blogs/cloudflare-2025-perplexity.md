---
id: cloudflare-2025-perplexity
type: blog
title: "Perplexity is using stealth, undeclared crawlers to evade website no-crawl directives"
authors: [Gabriel Corral, Vaibhav Singhal, Brian Mitchell, Reid Tatoris]
year: 2025
url: https://blog.cloudflare.com/perplexity-is-using-stealth-undeclared-crawlers-to-evade-website-no-crawl-directives/
site: Cloudflare Blog (vendor)
topics: [swarm-detection, sybil-resistance]
added_by: dmarz/sd-informal
accessed: 2026-10-03
read_depth: full
relevance: 4
---

## Summary

Vendor investigation (4 August 2025). After customer complaints, Cloudflare registered fresh, never-indexed domains (named like testexample.com), set robots.txt to disallow all bots and added WAF rules blocking Perplexity's declared crawlers, then asked Perplexity about those domains. Perplexity still answered with details of the content. Cloudflare observed that when the declared agent (Perplexity-User, 20 to 25 million daily requests) was blocked, a second agent presenting a generic Chrome-on-macOS user agent (3 to 6 million daily requests) fetched the content, from IPs outside Perplexity's published ranges, rotating IPs and ASNs, across tens of thousands of domains. Cloudflare fingerprinted it "using a combination of machine learning and network signals", de-listed Perplexity as a verified bot and added signatures to its managed AI-crawler block rule. The same canary-domain test against ChatGPT-User showed it fetching robots.txt and stopping, with no follow-up from other agents.

## Key claims

- The undeclared crawler was scored as a bot by Cloudflare's bot management and could not pass managed challenges.
- When the stealth crawler was blocked, Perplexity's answers became vaguer, which Cloudflare reads as confirmation that the block worked.
- Over 2.5 million websites had chosen to disallow AI training via Cloudflare's managed robots.txt or block rule (as of the post).
- Cloudflare expects the behaviour to change after publication.

## Evidence quality

Vendor post with a clean canary experiment (unindexed domains plus asking the answer engine about them), but no released logs, no false-positive rate, and Perplexity disputed the findings publicly (dispute not catalogued here). Cloudflare sells the blocking product.

## Relevance to us

A reusable detection design: plant canary content that only a crawler ignoring directives could have read, then query the AI system to see if it knows it. That is a honeypot for agents that works at the level of the model's answers, not traffic, and it detected identity-switching (one operator, two agent identities) that user-agent rules missed. Related Cloudflare work on cryptographic agent identity: [[cloudflare-2025-forget]], [[cloudflare-2025-age]]; trap-based detection: [[cloudflare-2025-trapping]].

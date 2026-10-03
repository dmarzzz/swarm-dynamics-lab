---
id: cloudflare-2025-trapping
type: blog
title: Trapping misbehaving bots in an AI Labyrinth
authors:
- Reid Tatoris
year: 2025
url: https://blog.cloudflare.com/ai-labyrinth/
site: Cloudflare blog
topics:
- swarm-detection
added_by: dmarz/sd-honeypots
accessed: '2026-10-03'
read_depth: skim
relevance: 4
---

## Summary

Cloudflare's vendor post announcing AI Labyrinth (19 March 2025, page marked modified 15 July 2026). Instead of blocking suspected unauthorised crawlers, Cloudflare links them into a maze of pre-generated, sanitised AI-written pages (made with Workers AI and open models, stored in R2). The links are injected into customer pages so humans do not see them, and the pages carry no-index metadata. The post calls this "a next-generation honeypot": any client that walks several links deep is almost certainly a bot, and its traversal is fed to Cloudflare's ML models to find new bot signatures. It is available on all plans, including Free.

## Key claims

- AI crawlers generate more than 50 billion requests to Cloudflare per day, just under 1% of all web requests (vendor figure).
- Hidden-link traversal identifies bots that evade classic honeypot tricks; the traversal data trains detection models (vendor claim).
- Decoy content is real but irrelevant, to avoid spreading misinformation (vendor claim).

## Evidence quality

Vendor announcement; no detection-rate or false-positive numbers are published in the post. [[fayolle-2026-internet]] excluded it from their evaluation because it redirects rather than blocks, so it is independently untested as far as we found.

## Relevance to us

The largest deployed crawler tarpit, and an explicit statement that the tarpit is used as a detection sensor. Sibling designs: the agent tarpit in [[pasquini-2024-hacking]] and the adaptive decoy in [[wang-2026-agentsnare]]. Related Cloudflare agent-identity posts: [[cloudflare-2025-forget]], [[cloudflare-2025-age]].

## Notes from dmarz/sd-informal

This lane catalogued the same source independently (added_by dmarz/sd-informal, accessed 2026-10-03). Its distinct content:

- Frontmatter `authors` in this lane's version: [Reid Tatoris, Harsh Saxena, Luis Miglietti]
- Frontmatter `site` in this lane's version: Cloudflare Blog (vendor product announcement)
- Frontmatter `read_depth` in this lane's version: full

### Summary

Product announcement (19 March 2025) for AI Labyrinth, an opt-in Cloudflare feature (all plans, including Free) that, when it detects unauthorized crawling, injects hidden links to pre-generated AI-written pages instead of blocking. The pages are generated with an open-source model on Workers AI, sanitized, stored in R2, carry no-index meta tags, and are shown only to suspected scrapers. The stated goals are to waste crawler resources without tipping them off (blocking "can alert the attacker" and start an arms race) and to act as a "next-generation honeypot": a visitor that goes four links deep into irrelevant generated pages is almost certainly a bot, and those visits are fed back into Cloudflare's bot-detection models. Cloudflare reports AI crawlers send over 50 billion requests a day to its network, just under 1% of all web requests it sees.

### Key claims

- Hidden-link honeypots have become less effective because bots now look for them; future versions will build networks of realistic linked URLs that fit each site's structure.
- Content is factual (science topics) to avoid polluting the web with misinformation, but irrelevant to the protected site.
- Every trapped crawl improves detection for all customers (data feedback loop).

### Evidence quality

Product announcement; no measurements of how many bots were trapped, depth distributions or false positives. The 50 billion figure is Cloudflare's network telemetry. Cites the Cuckoo's Egg (1986) and Project Honeypot (2004) as precedents.

### Relevance to us

A deployed, internet-scale honeypot (tarpit) aimed at automated agents, with the explicit design choice to deceive rather than block so the adversary does not adapt. Open questions for us: how LLM-driven browsing agents (as opposed to bulk crawlers) behave in such mazes, and whether depth-of-traversal is a robust bot signal once agents are told to watch for generated decoys. Companion detection case: [[cloudflare-2025-perplexity]].


## Notes from shadow/sol-g49

Primary page reopened 2026-10-03 through Jina. Its 50B/day AI-crawler requests and just-under-1% all-request share use a different date/denominator from cloudflare-2025-radar HTML-only 4.2% plus Googlebot 4.5%. Mechanism is hidden links into generated noindex decoy pages, with traversal used for bot-signature learning. No public calibrated sensitivity/FPR or labelled traversal dump found; vendor deployment is not efficacy validation.

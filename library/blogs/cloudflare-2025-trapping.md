---
id: cloudflare-2025-trapping
type: blog
title: "Trapping misbehaving bots in an AI Labyrinth"
authors: [Reid Tatoris, Harsh Saxena, Luis Miglietti]
year: 2025
url: https://blog.cloudflare.com/ai-labyrinth/
site: Cloudflare Blog (vendor product announcement)
topics: [swarm-detection]
added_by: dmarz/sd-informal
accessed: 2026-10-03
read_depth: full
relevance: 4
---

## Summary

Product announcement (19 March 2025) for AI Labyrinth, an opt-in Cloudflare feature (all plans, including Free) that, when it detects unauthorized crawling, injects hidden links to pre-generated AI-written pages instead of blocking. The pages are generated with an open-source model on Workers AI, sanitized, stored in R2, carry no-index meta tags, and are shown only to suspected scrapers. The stated goals are to waste crawler resources without tipping them off (blocking "can alert the attacker" and start an arms race) and to act as a "next-generation honeypot": a visitor that goes four links deep into irrelevant generated pages is almost certainly a bot, and those visits are fed back into Cloudflare's bot-detection models. Cloudflare reports AI crawlers send over 50 billion requests a day to its network, just under 1% of all web requests it sees.

## Key claims

- Hidden-link honeypots have become less effective because bots now look for them; future versions will build networks of realistic linked URLs that fit each site's structure.
- Content is factual (science topics) to avoid polluting the web with misinformation, but irrelevant to the protected site.
- Every trapped crawl improves detection for all customers (data feedback loop).

## Evidence quality

Product announcement; no measurements of how many bots were trapped, depth distributions or false positives. The 50 billion figure is Cloudflare's network telemetry. Cites the Cuckoo's Egg (1986) and Project Honeypot (2004) as precedents.

## Relevance to us

A deployed, internet-scale honeypot (tarpit) aimed at automated agents, with the explicit design choice to deceive rather than block so the adversary does not adapt. Open questions for us: how LLM-driven browsing agents (as opposed to bulk crawlers) behave in such mazes, and whether depth-of-traversal is a robust bot signal once agents are told to watch for generated decoys. Companion detection case: [[cloudflare-2025-perplexity]].

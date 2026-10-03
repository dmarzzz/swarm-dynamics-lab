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

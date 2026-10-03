---
id: cloudflare-2025-from
type: blog
title: "From Googlebot to GPTBot: who's crawling your site in 2025"
authors: [João Tomé, Jorge Pacheco, Carlos Azevedo]
year: 2025
url: https://blog.cloudflare.com/from-googlebot-to-gptbot-whos-crawling-your-site-in-2025/
site: Cloudflare Blog (vendor, Radar data)
topics: [swarm-detection]
added_by: dmarz/sd-informal
accessed: 2026-10-03
read_depth: full
relevance: 3
---

## Summary

Cloudflare Radar analysis (1 July 2025) of declared AI and search crawler traffic, May 2024 to May 2025, identified by matching user-agent strings against an open-source AI-crawler list. About 30% of global web traffic comes from bots. Among AI-only crawlers, GPTBot's share rose from 5% to 30% and Meta-ExternalAgent entered at 19%, while Bytespider fell from 42% to 7%. On a fixed customer cohort, AI plus search crawler traffic grew 18% (48% including new customers), peaking in April 2025 at +32%. Among 30+ AI and search crawlers: Googlebot share 30% to 50% (+96% requests), GPTBot 2.2% to 7.7% (+305%), ChatGPT-User +2,825% to 1.3% share, PerplexityBot +157,490% from a tiny base (0.2% share), ClaudeBot 11.7% to 5.4% (-46%). Of 3,816 top-10k domains with a robots.txt, 546 (about 14%) had directives aimed at AI bots; GPTBot was the most disallowed (312 domains) and also the most explicitly allowed (61).

## Key claims

- Crawling increasingly comes from Google and OpenAI bots.
- Sites are moving from robots.txt to enforceable blocking (WAF) because compliance is voluntary.
- Some robots.txt tokens (Google-Extended) are not user-agent strings, so not every opt-out maps to observable traffic.

## Evidence quality

Vendor telemetry from one network with a stated method (fixed cohort to remove customer-growth bias). Only declared, self-identifying agents are counted; undeclared agents, which [[cloudflare-2025-perplexity]] shows exist, are invisible to this method.

## Relevance to us

Base rates for declared AI agent traffic on the web, and a clear example of what user-agent-based measurement can and cannot see. Any population estimate of AI agents on the web built from declared identities is a lower bound. Compare with the Vercel network figures in [[vercel-2024-rise]].

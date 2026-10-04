---
id: gh-blessedrebus-krawl
type: code
title: "Krawl: web honeypot and deception server for malicious crawlers, AI scrapers and scanners (spider traps, fake credentials, canary tokens, tarpit, federated banlists)"
repo: BlessedRebuS/Krawl
url: https://github.com/BlessedRebuS/Krawl
authors: [BlessedRebuS, Lore09, carnivuth, ptarrant]
year: 2025
language: Python
license: MIT
stars: 770
last_commit: 2026-10-03
topics: [swarm-detection]
added_by: shadow/sol-w1
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: []
---

## Summary

Krawl is an actively maintained (repo created 2025-12-10, release v2.4.0 on 2026-09-11, last push 2026-10-03, 770 stars, MIT) deception server that you put next to real services, usually behind a reverse proxy, to catch automated visitors. It serves fake vulnerable surfaces (WordPress, phpMyAdmin and admin login pages, honeypot paths advertised in robots.txt, realistic fake credentials and API keys wired to third-party canary tokens), infinite-link spider-trap pages to waste crawler budget, randomised server headers and injected errors, and optional LLM-generated deception pages produced on demand for whatever path the visitor requests. A dashboard records per-IP behaviour (geolocation, ASN, reputation, timeline, attack types such as SQLi and XSS), groups captured payloads into campaigns by TLSH fuzzy hash, holds suspects in a tarpit, and exports banlists. Instances can federate banlists over plain HTTP, and the maintainers publish a weekly banlist from their demo instance. Top contributors by commit count: Lore09 (683), BlessedRebuS (282), carnivuth (65), ptarrant (35).

The batch candidate pointed to https://github.com/authrain-cloud-abdullahformuli/krawl, a 1-star repository created 2026-09-30 with two commits ("initial release" and a CI fix) whose README is the upstream Krawl README with the owner name swapped. It is not marked as a GitHub fork and does not credit upstream. I catalogued the upstream project instead; see Limitations.

## What it can do for us

A ready-made, deployable trap for measuring automated traffic, including LLM-driven browsing and scraping agents, in the wild. For a swarm-detection experiment it gives: honeypot paths and robots.txt bait that legitimate crawlers should avoid; canary credentials whose later use reveals that an agent exfiltrated and acted on them; spider traps that separate budget-bounded crawlers from naive ones; and TLSH campaign grouping, which is a primitive form of "same operator" attribution across many IPs. The federated-banlist feature is a small working example of shared detection signals across sites. Nothing in the docs I read claims to distinguish LLM agents from classic scrapers specifically; that would be our addition.

## Run notes

Not run. Upstream quickstart is `docker run -d -p 5000:5000 -e KRAWL_DASHBOARD_SECRET_PATH=... -e KRAWL_DASHBOARD_PASSWORD=... -v krawl-data:/app/data ghcr.io/blessedrebus/krawl:latest`; standalone mode uses SQLite, scalable mode PostgreSQL plus Redis (Helm chart defaults to scalable). AI page generation is configured via OpenRouter, OpenAI or a local llama.cpp/Ollama endpoint, with `max_daily_requests` capping cost. Public demo at http://demo.krawlme.com (not visited).

## Limitations

Read depth is skim: I read the README and the AI-generation doc, not the source. Detection is behavioural and IP-centric (traps triggered, paths requested, payloads), so a careful agent swarm that respects robots.txt, rotates residential IPs and never touches bait is invisible to it. The README gives no detection-rate or false-positive figures. The AI deception pages explicitly let attacker requests shape generated content, which could itself be a prompt-injection surface for the generating model; not examined. The copy at authrain-cloud-abdullahformuli/krawl looks like an unattributed re-upload of this repo (identical README, created 2026-09-30, two commits); do not cite it as an independent project.

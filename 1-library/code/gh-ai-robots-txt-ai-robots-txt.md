---
id: gh-ai-robots-txt-ai-robots-txt
type: code
title: "ai.robots.txt: community list of AI crawlers, assistants and agents with user-agent tokens and ready block rules"
repo: ai-robots-txt/ai.robots.txt
url: https://github.com/ai-robots-txt/ai.robots.txt
authors: ["ai-robots-txt contributors"]
year: 2024
language: Python (generator) + data
license: "MIT"
stars: 4160
last_commit: 2026-10-03
topics: [swarm-detection]
added_by: dmarz/sd-code-data
accessed: 2026-10-03
read_depth: ran
relevance: 3
papers: []
---

## Summary

A maintained robots.json listing AI-related user agents, each with operator, whether it respects robots.txt, function and description, from which a GitHub action generates robots.txt, .htaccess, nginx, Caddy, HAProxy and lighttpd block rules. Many entries come from Known Agents (knownagents.com). The README links measurement datasets of how widely such blocking is deployed (Tranco top 5,000 census, a 600-domain .de panel).

## What it can do for us

A labelled taxonomy of self-declared AI agents on the web, including coding and browsing agents, that serves as the first, honest-agent layer of any agent-traffic classifier.

## Run notes

Ran 2026-10-03: downloaded `robots.json` from main and parsed it with Python. 181 entries. Functions: AI Assistants 29, AI Data Providers 20, AI Data Scrapers 20, AI Search Crawlers 11, AI Agents 9, Undocumented AI Agents 8, AI Coding Agents 8 (others smaller). Robots.txt respect: 106 entries 'Unclear', about 47 'Yes' in various phrasings, 8 'No'. Operator 'Unclear at this time.' for 53 entries. Agent-type entries include ChatGPT Agent, Claude-Code, Cursor, Devin, Google-Agent, GoogleAgent-Mariner, Kimi-Agent, Manus-User, NovaAct, Operator, opencode, Crawl4AI.

## Limitations

Detects only agents that announce themselves in the User-Agent header; an agent driving a stock browser is invisible to it. For most entries respect and operator are unknown. Contributions written by AI are not accepted, per the README.

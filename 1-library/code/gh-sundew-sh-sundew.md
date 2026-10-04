---
id: gh-sundew-sh-sundew
type: code
title: "Sundew: persona-randomised honeypot exposing MCP, OpenAPI and AI-plugin surfaces to fingerprint autonomous AI agents"
repo: sundew-sh/sundew
url: https://github.com/sundew-sh/sundew
authors: ["sundew-sh (karpie28)"]
year: 2026
language: Python
license: "Apache-2.0"
stars: 8
last_commit: 2026-03-01
topics: [swarm-detection]
added_by: dmarz/sd-code-data
accessed: 2026-10-03
read_depth: ran
relevance: 3
papers: []
---

## Summary

Python (FastAPI) honeypot that serves the surfaces agents look for: /.well-known/ai-plugin.json, /.well-known/mcp.json, robots.txt, an OpenAPI spec with fake endpoints and a protocol-compliant MCP server with fake tools. A persona engine (LLM-generated, or packaged personas when no LLM is set) gives each deployment different company names, paths, headers and latency so that agents cannot learn one fingerprint. The README describes five 0-1 signals (timing regularity, path enumeration, header anomalies, prompt leakage in request bodies, MCP connection) combined into a composite that maps to human (<0.3), automated (0.3-0.6), ai_assisted (0.6-0.8) and ai_agent (>0.8). The README demo output (confidence 0.91) is illustrative, not a measurement; the repo reports no field data.

## What it can do for us

A cheap, local trap for agents that discover services through AI-plugin and MCP manifests, with a persona engine that addresses the main weakness of fixed honeypots (one fingerprint per product). Useful as a test harness to see how our own agents' traffic looks to a defender.

## Run notes

Ran 2026-10-03 on macOS: `uv venv -p 3.12 && uv pip install sundewsh` (version 0.2.1), config with `llm.provider: none`, host 127.0.0.1 port 18080, `sundew -c sundew.yaml serve`. It loaded the persona 'LumenSolutions (ecommerce / carts)' from packs with 9 templates and served robots.txt, an ai-plugin manifest, an OpenAPI spec with 9 paths (/v1/products, /v1/orders, /v1/auth/token and so on) and an MCP initialize response. I then sent an agent-like session (python-httpx UA, systematic discovery of manifests and every endpoint, a POST body containing 'As an AI assistant', an MCP initialize call) and a browser-like session (Chrome UA, Google referer, 4 s gaps). Result: `sundew query` listed only 4 events, all 404 catch-all hits (/admin/, /internal/, /), each with every fingerprint score 0.0 and classification 'unknown'; the 200 responses on the trap routes were not stored as events, and both sessions merged into one session because they shared an IP. So in v0.2.1 without an LLM the classifier produced no discrimination in my test. I did not investigate whether this is a bug or a configuration issue.

## Limitations

Very early (8 stars, last commit 2026-03-01, v0.1/0.2 roadmap). No published detections or validation of the scoring weights. Session grouping by IP merges distinct clients behind one address. Header and timing heuristics are trivially spoofable by an agent that sets a browser UA and jitter.

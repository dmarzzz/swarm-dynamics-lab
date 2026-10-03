---
id: gh-kelkalot-moltbook-observatory
type: code
title: "Moltbook Observatory: passive poller, SQLite store and dashboard for the agent-only social network Moltbook"
repo: kelkalot/moltbook-observatory
url: https://github.com/kelkalot/moltbook-observatory
authors: ["Sushant Gautam", "et al."]
year: 2026
language: HTML/Python
license: "none found (paper says MIT; no LICENSE file via API)"
stars: 56
last_commit: 2026-05-15
topics: [llm-agent-swarms, swarm-detection]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 3
papers: [gautam-2026-moltbook]
---

## Summary

Collector: polls the Moltbook API (posts every 2 min, agent profiles every 15 min, trends every 10 min, submolts hourly, platform snapshots hourly) into SQLite with a web dashboard and REST API; snapshot on HF (SimulaMet/moltbook-observatory-archive); live instance linked from README.

## What it can do for us

Ground-truth data on a real agent society to validate sim outputs against; the poller is a template for instrumenting any live agent platform.

## Run notes

Not run. README read via the GitHub API on 2026-10-03.

## Limitations

Collection stopped being pushed in 2026-05; API-limited sampling (50 posts per poll). Related alternative collectors: takschdube/moltbook-dataset [[data-moltbook-dataset-2026]] and ExtraE113/moltbook_data (raw JSON dumps, 41 stars, not catalogued).

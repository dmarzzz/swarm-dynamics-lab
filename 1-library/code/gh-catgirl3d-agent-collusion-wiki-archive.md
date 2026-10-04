---
id: gh-catgirl3d-agent-collusion-wiki-archive
type: code
title: "agent-collusion-wiki-archive: mirror of the collusion.wiki dump (14,591 revisions, 4,579 pages, 3,102 agent labels) with viewer, read-only API and MCP tools"
repo: catgirl3d/agent-collusion-wiki-archive
url: https://github.com/catgirl3d/agent-collusion-wiki-archive
authors: ["catgirl3d"]
year: 2026
language: TypeScript
license: "none stated"
stars: 0
last_commit: 2026-09-26
topics: [llm-agent-swarms, criticality-measurement]
added_by: shadow/sol-1
accessed: 2026-10-03
read_depth: skim
relevance: 5
papers: []
---

## Summary

A 1:1 mirror of the canonical collusion.wiki export plus tooling. Data files (from collusion.wiki/explorer/download.html): full-wiki-logs.zip for all five wikis, pages.jsonl.gz (4,579 pages), revisions.jsonl.gz (14,591 revisions with full text, about 3.2 MB gzipped), events.jsonl.gz (saves, deletions, reverts, probes), labels.jsonl.gz (3,102 named labels plus one anonymous row), manifest and SHA256SUMS. A recovered 'other sites' layer adds 90 partial revisions across 8 pages. The React/Vite viewer has a timeline filterable by label, wiki and date, an agent-labels page sliceable by /16 IP prefix, literal text search run in a browser worker, and a research page with a coordination-topology assessment. A Cloudflare Worker exposes a read-only API and an MCP adapter exposes research tools to agents. Also holds an third-party anna.fyi agent-relay snapshot (88 pastes, captured 2026-09-12).

## What it can do for us

The fastest route to the full DseWiki corpus in JSONL with checksums, plus an MCP server so our own agents can query it. revisions.jsonl.gz is small enough to load in pandas in seconds.

## Run notes

Not run. Metadata (stars, licence, last commit) taken from the GitHub API on 2026-10-03; README read via the API.

## Limitations

No licence file on the repo (data licence follows collusion.wiki's terms, check there). 0 stars, single maintainer, last commit 2026-09-26. Not run here.

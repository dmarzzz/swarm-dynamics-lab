---
id: gh-microsoft-multi-agent-marketplace
type: code
title: "Magentic Marketplace: simulate two-sided markets of LLM buyer and seller agents (Microsoft Research)"
repo: microsoft/multi-agent-marketplace
url: https://github.com/microsoft/multi-agent-marketplace
authors: ["Microsoft Research"]
year: 2025
language: "Python"
license: "MIT"
stars: 191
last_commit: 2026-09-14
topics: [llm-agent-swarms, sybil-resistance]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: skim
relevance: 4
papers: [bansal-2025-magentic]
---

## Summary

Simulates: two-sided markets in which assistant agents (buyers) search, inquire, negotiate and pay service agents (sellers), in restaurant and contractor domains. Interaction model: HTTP/REST client-server with register, protocol-discovery and action endpoints; state in a Postgres database started with docker compose. Scale: the paper reports degradation as the number of options grows [[bansal-2025-magentic]]; no agent count in the README. LLM-driven: yes, with OpenAI, Anthropic, Gemini or local models. Adversarial hooks: manipulation resistance is a measured outcome in the paper; no Sybil seller tooling in the README. Weight: uv sync plus Docker plus API keys; `magentic-marketplace run data/mexican_3_9`.

## What it can do for us

A maintained LLM-agent market with a protocol layer we could extend with seller Sybils (one operator, many storefronts) and fake reviews, then measure buyer welfare. Pairs with [[gh-freedomintelligence-twinmarket]] for trading and [[gh-m1kuw1ll-mmasim]] for auctions.

## Run notes

Not run. Stars, licence and last commit from the GitHub API on 2026-10-03; README read via the API.

## Limitations

Needs Docker and paid API calls. Domains are consumer services, not on-chain order flow.

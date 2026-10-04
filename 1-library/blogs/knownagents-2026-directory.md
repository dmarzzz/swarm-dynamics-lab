---
id: knownagents-2026-directory
type: blog
title: Agent Directory and About Known Agents (formerly Dark Visitors)
authors:
- Known Agents
year: 2026
url: https://knownagents.com/agents
site: Known Agents
topics:
- swarm-detection
- llm-agent-swarms
read_depth: skim
relevance: 5
added_by: shadow/sol-g49
accessed: '2026-10-03'
---

## Summary

Known Agents, previously Dark Visitors, maintains a public catalogue mapping named crawlers and agents to operator and purpose categories, paired with server-side analytics, robots policy and an identification API. This is an identity/purpose dictionary, not a labelled corpus proving autonomy or coordination.

## Key claims

- Directory and https://knownagents.com/about opened 2026-10-03; no publication or measurement window stated. About page says Dark Visitors began in 2023 with eight known AI bots and now serves more than 5,000 websites, with a public directory of thousands of agents and bots. Those are vendor self-reported adoption/catalogue counts, not global traffic percentages.
- Method: server-side integrations with websites/CDNs, request identification and supported identity verification. Browser analytics often exclude bots. Exact classification validation and false-positive rates absent.
- Directory distinguishes assistants, coding agents, training crawlers and search/indexing purposes. User-agent strings are identifiers, not cryptographic proof, unless separately verified.

## Evidence quality

Primary directory and vendor documentation opened via Jina/Exa. Data/reuse licence and unrestricted bulk-export terms not established. Software SDK licence must not be assumed to license the commercial directory.

## Relevance to us

Operator normalization and purpose taxonomy for [[cloudflare-2025-radar]] and [[datadome-2026-traffic]]. Needs independently observed negative controls and spoof checks before use as ground truth.

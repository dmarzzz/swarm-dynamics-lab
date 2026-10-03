---
id: wiz-2026-hacking
type: blog
title: "Hacking Moltbook: The AI Social Network Any Human Can Control"
authors: [Gal Nagli]
year: 2026
url: https://www.wiz.io/blog/exposed-moltbook-database-reveals-millions-of-api-keys
site: Wiz Blog (security vendor)
topics: [swarm-detection, sybil-resistance, llm-agent-swarms]
added_by: dmarz/sd-informal
accessed: 2026-10-03
read_depth: full
relevance: 5
---

## Summary

Security-vendor research post (2 February 2026) on Moltbook, the viral Reddit-like social network for AI agents. Wiz found a Supabase key in the site's client-side JavaScript with no row-level security behind it, giving unauthenticated read and write access to about 4.75 million records. The exposed tables contradicted the platform's public picture: 1.5 million registered agents but only about 17,000 human owners, an average of 88 agents per owner. Anyone could register agents in a loop with no rate limiting, and a human could post as an "agent" with a plain POST request; the platform had no way to verify that an agent was an AI at all. Wiz also found 4,060 private agent-to-agent DM conversations, some carrying plaintext OpenAI API keys, 29,631 extra emails in an "observers" table, and write access that let anyone edit any post. Disclosure and fixes ran from 31 January 21:48 UTC to 1 February 01:00 UTC 2026. Jameson O'Reilly found the same misconfiguration independently (reported by 404 Media).

## Key claims

- "The revolutionary AI social network was largely humans operating fleets of bots" (Wiz's reading of the owner/agent ratio).
- "Agent internet" participation metrics are trivially inflatable without rate limits or identity checks.
- Write access means every post, vote and karma score during the exposure window is of uncertain integrity, including possible prompt-injection payloads consumed by other agents.

## Evidence quality

Primary investigation with request examples and a timeline; the 88:1 figure is a direct count from the database. What it does not show: how many agents were actually LLM-driven versus scripted, or the distribution of agents per owner (only the mean is given). Wiz is a commercial vendor; the post doubles as a vibe-coding security lesson.

## Relevance to us

The first measured operator-to-agent ratio for a large agent population in the wild, and it comes from a database leak rather than a detector. It is a Sybil measurement (one owner, many identities) on a platform built for agents, and it shows that work treating Moltbook activity as an emergent AI society (for example [[de-marzo-2026-collective]]) has to account for a heavy-tailed, human-steered population of unknown composition. Any swarm-detection method evaluated on Moltbook data should be checked against the owner table, which public scrapes do not have.

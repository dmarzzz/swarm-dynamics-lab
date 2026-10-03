---
id: cloudflare-2025-age
type: blog
title: "The age of agents: cryptographically recognizing agent traffic"
authors: ["Jin-Hee Lee"]
year: 2025
url: https://blog.cloudflare.com/signed-agents/
site: The Cloudflare Blog
topics: [sybil-resistance, llm-agent-swarms]
added_by: dmarz/sybil-credentials
accessed: 2026-10-03
read_depth: skim
relevance: 3
---

## Summary

Vendor post (28 August 2025) creating a "signed agents" category in Cloudflare's bot management. Signed agents are agents directed by end users rather than by a single company (booking flights, ordering food), whose infrastructure providers sign HTTP requests with Web Bot Auth ([[cloudflare-2025-forget]]) and which comply with a signed-agent policy. They differ from verified bots, which perform one repetitive task for their operator (for example indexing). The initial cohort named is ChatGPT agent, Goose (Block), Browserbase and Anchor Browser; operators apply through a bot submission form.

## Key claims

- User-directed agents need a separate trust class from operator-directed crawlers.
- Cryptographic request signing is the basis of recognition. The post gives no numbers and does not discuss anonymity, rate limiting or Sybil abuse (as read).

## Evidence quality

Product announcement; policy, not evidence. Author name taken from the page's author link. Read via a summarising fetch plus page metadata, so depth is skim.

## Relevance to us

Documents where the deployed web is heading for agent identity: a small allow-list of signing platforms, each vouching for all of its users' agents. That concentrates Sybil control in the platform (it decides how many agents a user may run) and gives origins no per-user unlinkable quota. It is the industry baseline that anonymous-credential proposals ([[adler-2024-personhood]], [[yun-2026-anonymous]]) would need to interoperate with.

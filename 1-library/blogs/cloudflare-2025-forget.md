---
id: cloudflare-2025-forget
type: blog
title: "Forget IPs: using cryptography to verify bot and agent traffic"
authors: ["Thibault Meunier", "Mari Galicer"]
year: 2025
url: https://blog.cloudflare.com/web-bot-auth/
site: The Cloudflare Blog
topics: [sybil-resistance, llm-agent-swarms, swarm-detection]
added_by: dmarz/sybil-credentials
accessed: 2026-10-03
read_depth: skim
relevance: 4
---

## Summary

Vendor post (15 May 2025) introducing Web Bot Auth: bots and AI agents sign HTTP requests with HTTP Message Signatures (RFC 9421) using Ed25519. A request carries a Signature-Agent header pointing to a directory of the operator's public keys, a Signature-Input header with created/expires times, a JWK-thumbprint key id and the tag web-bot-auth, and a Signature header. The signature covers the request authority and the signature-agent component, not the body. Origins verify against the published key instead of trusting IP ranges or User-Agent strings. A request-mTLS alternative using a TLS flag is described and deprioritised.

## Key claims

- User-Agent is spoofable; IP allow-lists break with shared infrastructure, changing IPs, privacy proxies and cloud CIDR churn; per-site bearer tokens do not scale.
- OpenAI had begun signing its Operator agent's requests with RFC 9421 (quoted in the post).
- Acknowledged costs: signature verification adds notable overhead at internet scale; RFC 9421 adoption is limited.
- Links IETF drafts (web-bot-auth architecture, HTTP message signatures directory) and the reference code ([[gh-cloudflare-web-bot-auth]]).

## Evidence quality

Vendor announcement and proposal, no measurements. Authors listed from the page's author links. Read via a summarising fetch plus page metadata, so depth is skim.

## Relevance to us

Web Bot Auth is the opposite design point to anonymous credentials: every agent request is attributable to a named operator key. It defends against impersonation (a bot claiming to be a well-known agent) but not against Sybils as such: an operator can mint many keys or many agents, and per-user accountability is absent because one operator signs for all its users. For agent swarms it gives operator-level accountability; combining it with per-principal anonymous rate limits ([[yun-2026-anonymous]], [[davidson-2024-privacy]]) is an open design question. Follow-on program: [[cloudflare-2025-age]].

## Notes from dmarz/sd-web-agents

Measured follow-up from the agent-fingerprinting papers: [[fayolle-2026-internet]] observed ChatGPT Agent sending `signature` and `signature-agent` headers, which made it trivially identifiable, and [[kang-2026-whose]] saw the same headers from OpenAI's agent. [[wang-2026-fp-agent]] reports that Web Bot Auth is voluntary and that Atlas Agent, Browser Use, Comet and Skyvern did not sign, so unsigned agent traffic still needs fingerprint-based detection. For swarm detection, a signature identifies the operator key, not the number of independent principals behind it.

---
id: gh-cloudflare-web-bot-auth
type: code
title: "web-bot-auth: libraries and examples for signing automated agent HTTP traffic with RFC 9421 HTTP Message Signatures"
repo: cloudflare/web-bot-auth
url: https://github.com/cloudflare/web-bot-auth
authors: ["Cloudflare Research"]
year: 2025
language: "Rust and TypeScript"
license: "Apache-2.0"
stars: 165
last_commit: 2026-09-19
topics: [sybil-resistance, llm-agent-swarms]
added_by: dmarz/sybil-code-data
accessed: 2026-10-03
read_depth: skim
relevance: 4
papers: []
---

## Summary

Reference code for draft-meunier-webbotauth-httpsig-protocol, an IETF draft for bots and AI agents to sign their HTTP requests so that origins can verify which operator sent them. Packages implement RFC 9421 HTTP Message Signatures, RFC 7638 JWK thumbprints, the web-bot-auth profile in TypeScript and Rust, and a validator for signed key directories at `/.well-known/http-message-signatures-directory`. Examples include a browser extension that signs every request, a Caddy verification plugin, a Cloudflare Workers verifier, and a Workers-hosted registry with a "Signature Agent Card". The README says the code has not been audited.

## What it can do for us

This is the emerging agent-identity layer on the open web: it binds requests to an operator key, which gives accountability but not Sybil resistance, since an operator can mint unlimited keys unless a registry or directory gates them. It frames a precise question for us: what admission cost should a signature-agent registry impose so that key directories carry reputation.

## Run notes

Not run. Cloudflare hosts a live test deployment at http-message-signatures-example.research.cloudflare.com that verifies requests signed with the published RFC 9421 test key.

## Limitations

Draft standard, unaudited code. Authentication of an operator, not uniqueness of an agent.

## Notes from dmarz/sybil-credentials

The announcing posts are catalogued as [[cloudflare-2025-forget]] (Web Bot Auth, May 2025, which notes OpenAI signing Operator traffic with RFC 9421) and [[cloudflare-2025-age]] (the "signed agents" category, August 2025, initial cohort ChatGPT agent, Goose, Browserbase, Anchor Browser). Design contrast for a survey: this stack gives attributable, operator-level identity; anonymous rate-limited credentials ([[yun-2026-anonymous]], [[davidson-2024-privacy]]) give unlinkable per-principal quotas. Neither alone bounds how many agents one principal can field.

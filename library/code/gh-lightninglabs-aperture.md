---
id: gh-lightninglabs-aperture
type: code
title: "aperture: L402 (Lightning HTTP 402) reverse proxy for paid APIs"
repo: lightninglabs/aperture
url: https://github.com/lightninglabs/aperture
authors: ["Lightning Labs"]
year: 2019
language: Go
license: MIT
stars: 271
last_commit: 2026-10-01
topics: [sybil-resistance, llm-agent-swarms]
added_by: dmarz/sybil-credentials
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: []
---

## Summary

A Go reverse proxy for gRPC and REST backends that implements L402: HTTP 402 plus macaroons plus Lightning. To get an API token the client pays a Lightning invoice; the preimage is part of the final L402 token, and the macaroon carries attributes and capabilities (enabling automated pricing and tier upgrades). The README says it is used in production by Lightning Loop. It also speaks the IETF Payment HTTP Authentication Scheme draft (charge and deposit-backed session intents) and supports metered pricing: pay once for a bundle, then draw down per request from usage reported by the upstream, motivated explicitly by variable LLM inference cost, including streamed responses.

## What it can do for us

An existing, production-used way to put a payment-backed, capability-scoped token in front of any agent-facing API. The bundle-then-meter model is the non-anonymous analogue of the refund tickets in [[crapis-2026-zk]].

## Run notes

Not run. Requires Go 1.25+, a reachable lnd node, TLS cert/key in `~/.aperture`, config in `~/.aperture/aperture.yaml`; `make build`.

## Limitations

Macaroon tokens are bearer tokens linkable across requests; Lightning payments give some payer privacy but the token itself is a persistent identifier. Needs Lightning infrastructure. Compare [[gh-x402-foundation-x402]].

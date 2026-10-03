---
id: gh-cloudflare-privacypass-issuer
type: code
title: "privacypass-issuer: Cloudflare Workers issuer for IETF Privacy Pass tokens (publicly verifiable, blind RSA)"
repo: cloudflare/privacypass-issuer
url: https://github.com/cloudflare/privacypass-issuer
authors: ["Cloudflare"]
year: 2023
language: "TypeScript"
license: "Apache-2.0 (per README; API reports NOASSERTION)"
stars: 27
last_commit: 2026-09-10
topics: [sybil-resistance]
added_by: dmarz/sybil-code-data
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: []
---

## Summary

A Privacy Pass issuer following draft-ietf-privacypass-protocol-16, running on Cloudflare Workers with keys in R2. It supports publicly verifiable blind-RSA tokens: a client that has passed some attestation (a CAPTCHA, a device check) obtains unlinkable tokens it can later redeem at origins without being tracked. The README covers deployment, public endpoints, Access protection for admin routes, automated key rotation by cron (at most 256 keys, ids chosen at random) and scheduled key clearing.

## What it can do for us

Privacy Pass is how the web already rate-limits anonymous clients: an attester decides who gets tokens, and tokens are spent per request. For agent swarms it is the natural way to give an agent a budget of anonymous actions backed by a single attestation, a centralised relative of [[gh-rate-limiting-nullifier-circom-rln]].

## Run notes

Not run. `pnpm run deploy:production`; local issuance test with `pnpm run test:e2e -- <issuer-name>`.

## Limitations

Sybil resistance depends entirely on the attester, which is outside this repo. Issuer is a trusted party; tokens are unlinkable but the issuer controls supply.

---
id: gh-privacypass-challenge-bypass-extension
type: code
title: "challenge-bypass-extension: original Privacy Pass browser client (deprecated)"
repo: privacypass/challenge-bypass-extension
url: https://github.com/privacypass/challenge-bypass-extension
authors: ["Privacy Pass team"]
year: 2017
language: JavaScript
license: BSD-3-Clause
stars: 1252
last_commit: 2024-08-30
topics: [sybil-resistance]
added_by: dmarz/sybil-credentials
accessed: 2026-10-03
read_depth: skim
relevance: 2
papers: [davidson-2018-privacy]
---

## Summary

The Chrome/Firefox extension that implemented the client side of the PoPETS 2018 Privacy Pass protocol ([[davidson-2018-privacy]]): solve a provider's CAPTCHA, receive blinded tokens, and spend one later to pass that provider's challenge without interaction. Providers listed were Cloudflare and hCaptcha. The README marks it deprecated in 2024: the IETF protocol ([[davidson-2024-privacy]]) diverged from the PoPETS version, CAPTCHA providers dropped the old flavour, and Cloudflare maintains a fork (Silk, cloudflare/pp-browser-extension) with IETF support.

## What it can do for us

Reference implementation of the issuance/redemption client flow and of the extension-side mitigations described in the paper (per-URL spend tracking against token drain). Useful for reading, not for building on.

## Run notes

Not run. README build: `nvm use 16 && npm ci && npm run build`; tests with `npm test`.

## Limitations

Deprecated and unsupported by any provider per the README. Implements only one-show tokens without rate limits. For current code use the IETF-aligned fork named in the README (not catalogued here).

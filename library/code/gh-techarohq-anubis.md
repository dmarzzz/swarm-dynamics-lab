---
id: gh-techarohq-anubis
type: code
title: "Anubis: proof-of-work challenge proxy that screens HTTP clients before they reach a site, aimed at AI scrapers"
repo: TecharoHQ/anubis
url: https://github.com/TecharoHQ/anubis
authors: ["TecharoHQ"]
year: 2025
language: Go
license: "MIT"
stars: 23028
last_commit: 2026-09-30
topics: [swarm-detection, sybil-resistance]
added_by: dmarz/sd-code-data
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: []
---

## Summary

Reverse proxy ('Web AI Firewall Utility') that makes clients solve a JavaScript proof-of-work challenge before passing requests upstream, with policy files to allowlist known good bots. Built to protect small sites from AI-company scrapers; the README calls it a nuclear option that also blocks small scrapers and the Internet Archive unless allowlisted. 23k stars in about a year indicates very wide deployment.

## What it can do for us

Cost-imposition rather than detection: it makes each additional client expensive, the same economics as Sybil resistance. Its logs (who solves the challenge, how fast) are a data source on headless agents that can run JavaScript.

## Run notes

Not run.

## Limitations

Browser agents that execute JavaScript pass the challenge, only paying compute; it filters cheap scrapers, not capable agents. Hurts legitimate archival bots.

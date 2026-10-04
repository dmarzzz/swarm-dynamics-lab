---
id: gh-shadow-tornettools
type: code
title: "tornettools: generate, run and analyse statistically sound private Tor network models in Shadow"
repo: shadow/tornettools
url: https://github.com/shadow/tornettools
authors: ["Rob Jansen", "Justin Tracey", "Ian Goldberg"]
year: 2020
language: "Python"
license: "Public-release distribution statement (NRL; GitHub reports NOASSERTION)"
stars: 42
last_commit: 2026-06-29
topics: [meta, sybil-resistance]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: [jansen-2021-once]
---

## Summary

Simulates: scaled-down or full Tor networks sampled from real Tor metrics (relay consensus, user counts by country, Markov traffic models via TGen). Interaction model: a pipeline (stage, generate, simulate, parse, plot) that feeds [[gh-shadow-shadow]]. Scale: up to 100% Tor (6,489 relays, 792k users) in the companion paper [[jansen-2021-once]]. LLM-driven: no. Adversarial hooks: none native; relays are just generated hosts, so malicious relays are added by editing the generated config. Weight: needs Shadow on Linux plus large RAM for large scales.

## What it can do for us

A worked template for the part every Sybil or swarm simulation gets wrong: sampling many independent synthetic networks from real data and reporting confidence intervals across them, rather than one run on one sample.

## Run notes

Not run. Stars, licence and last commit from the GitHub API on 2026-10-03; README read via the API.

## Limitations

Tor-specific. Versioning is self-described as "based on vibes rather than semver"; pin a commit. Requires Shadow (Linux).

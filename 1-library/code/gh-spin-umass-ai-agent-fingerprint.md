---
id: gh-spin-umass-ai-agent-fingerprint
type: code
title: "AI-agent-fingerprint: MARK multi-layer (timing, TLS/HTTP2, header, behaviour) fingerprinting testbed for AI web agents"
repo: SPIN-UMass/AI-agent-fingerprint
url: https://github.com/SPIN-UMass/AI-agent-fingerprint
authors: ["SPIN lab, UMass Amherst (Dayeon Kang et al.)"]
year: 2026
language: "Go and Python"
license: "none stated"
stars: 3
last_commit: 2026-06-18
topics: [swarm-detection, llm-agent-swarms]
added_by: dmarz/sd-web-agents
accessed: '2026-10-03'
read_depth: skim
relevance: 4
papers: [kang-2026-whose]
---

## Summary

Release for [[kang-2026-whose]]. The tree holds a Go server (`cmd/agent-scraper/main.go`, systemd and logrotate configs, a Dockerfile) that terminates TLS and logs ClientHello, HTTP/2 prelude and headers, baseline crawler configs for Heritrix, Nutch and Scrapy with a `run_trials.sh`, collected `fingerprint_data` including agent transcripts, and a copy of the paper PDF. The README is a title only; I read the file tree, not the code.

## What it can do for us

A ready server-side logger for an agent honeysite: TLS, JA4, Akamai HTTP/2 fingerprint, header order and Sec-Fetch checks, plus the five UX scenario pages. Pairs with [[gh-ethanbwang-fp-agent]] for behavioural features.

## Run notes

Not run. Needs a domain and a TLS certificate (the paper used Let's Encrypt on AWS EC2).

## Limitations

No licence file, so reuse terms are unclear. README is empty; documentation lives in the paper. Three stars, last commit 2026-06-18.

---
id: gh-0x4d31-galah
type: code
title: "Galah: LLM-powered web honeypot that generates a plausible response to any HTTP request"
repo: 0x4D31/galah
url: https://github.com/0x4D31/galah
authors: ["Adel Karimi"]
year: 2023
language: Go
license: "Apache-2.0"
stars: 669
last_commit: 2025-07-24
topics: [swarm-detection]
added_by: dmarz/sd-code-data
accessed: 2026-10-03
read_depth: skim
relevance: 2
papers: []
---

## Summary

Go web honeypot that sends each incoming HTTP request to an LLM (OpenAI, Google, Vertex, Anthropic, Cohere, Ollama) and returns a generated response mimicking whatever application the request targets; responses are cached per port, path and query, and requests can be matched against Suricata rules. The author calls it a weekend project and notes it can be fingerprinted (latency, network signatures). Cited as related work by [[reworr-2024-llm]].

## What it can do for us

Shows the opposite direction to agent detection: an LLM used to fool scanners. Useful as a responsive surface to embed canary content in, and as a caution that LLM latency itself fingerprints the honeypot.

## Run notes

Not run (needs an LLM API key).

## Limitations

Does not detect agents. Slow, costly per request and identifiable. Last commit 2025-07-24.

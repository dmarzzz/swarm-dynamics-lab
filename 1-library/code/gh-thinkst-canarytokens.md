---
id: gh-thinkst-canarytokens
type: code
title: "Canarytokens: self-hostable tripwire tokens (URLs, DNS names, documents, AWS keys) that alert when touched"
repo: thinkst/canarytokens
url: https://github.com/thinkst/canarytokens
authors: ["Thinkst Applied Research"]
year: 2015
language: Python
license: "see repo (custom)"
stars: 2172
last_commit: 2026-09-24
topics: [swarm-detection]
added_by: dmarz/sd-code-data
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: []
---

## Summary

Thinkst's open-source server behind canarytokens.org. It mints tokens of many kinds (web bug URLs, DNS hostnames, Word and PDF documents, AWS API keys, QR codes, cloned-site JavaScript and more); any use of a token triggers an alert by email or webhook with source IP and request details. Recommended deployment is the canarytokens-docker repo.

## What it can do for us

The general mechanism that agent-specific canaries ([[gh-peg-snare]], [[gh-tcotl-agentcapture]]) specialise. Tokens embedded in pages, documents or tool outputs are the cheapest way to detect an agent that reads and acts on content, and DNS tokens fire even when an agent only resolves a name.

## Run notes

Not run.

## Limitations

Tells you a token was used, not whether an LLM agent, a script or a human used it; attribution needs timing or behaviour on top. Licence is not a standard SPDX identifier on GitHub.

---
id: gh-beelzebub-labs-beelzebub
type: code
title: "Beelzebub: YAML-configured deception framework with LLM-backed decoys and MCP bait tools"
repo: beelzebub-labs/beelzebub
url: https://github.com/beelzebub-labs/beelzebub
authors: ["mariocandela (beelzebub-labs)"]
year: 2022
language: Go
license: "GPL-3.0"
stars: 2189
last_commit: 2026-10-01
topics: [swarm-detection]
added_by: dmarz/sd-code-data
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: []
---

## Summary

Go deception runtime: services and response rules are defined in YAML (18 example configurations), with static handlers or LLM-generated responses, for SSH, HTTP, TCP, Telnet and MCP. Events go to logs, RabbitMQ or Prometheus. The MCP decoy exposes bait tools whose invocation is evidence of prompt-injection-driven or unexpected agent behaviour; the README is careful to say this provides evidence and does not guarantee detection. A commercial platform is built on it.

## What it can do for us

The most mature open honeypot runtime with first-class MCP decoys, so the practical base for any agent-honeypot experiment we deploy, with logging infrastructure already in place.

## Run notes

Not run (install script starts many privileged-port listeners; README asks for an isolated lab host).

## Limitations

The LLM decoys serve attackers with LLM output, which is a honeypot realism tool, not an agent detector; agent detection must be built on top. GPL-3.0. No published detection statistics.

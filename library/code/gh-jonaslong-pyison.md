---
id: gh-jonaslong-pyison
type: code
title: "Pyison: Python tarpit that traps AI crawlers in an endless generated blog without using user-agent matching"
repo: JonasLong/Pyison
url: https://github.com/JonasLong/Pyison
authors: ["JonasLong"]
year: 2025
language: Python
license: "MIT"
stars: 125
last_commit: 2025-10-10
topics: [swarm-detection]
added_by: dmarz/sd-code-data
accessed: 2026-10-03
read_depth: skim
relevance: 2
papers: []
---

## Summary

Serves a realistic-looking blog whose pages link endlessly to more generated pages filled with random text (generated without Markov chains or LLMs), so crawlers that follow links get stuck and ingest junk. Deliberately does not discriminate by User-Agent, since crawlers disguise themselves; anything that keeps following links far into the maze self-identifies as a crawler. Lists Nepenthes and Iocaine as earlier tarpits.

## What it can do for us

Depth into an unlinked-from-humans maze is a behavioural detector that ignores headers: a human never goes 50 pages deep. Cheap to deploy as a sensor of crawler and agent traffic.

## Run notes

Not run.

## Limitations

Catches link-following crawlers, not goal-directed agents that stop after a few pages. Single-maintainer.

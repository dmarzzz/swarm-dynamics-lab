---
id: gh-camel-ai-oasis
type: code
title: "OASIS: open agent social-interaction simulator for up to one million LLM agents on Twitter/Reddit-like platforms"
repo: camel-ai/oasis
url: https://github.com/camel-ai/oasis
authors: ["CAMEL-AI"]
year: 2024
language: Python
license: "Apache-2.0"
stars: 5221
last_commit: 2026-09-30
topics: [llm-agent-swarms, collective-decision, sync-consensus]
added_by: shadow/sol-1
accessed: 2026-10-03
read_depth: skim
relevance: 4
papers: []
---

## Summary

Coordination model: platform simulation. Agents act on simulated Twitter or Reddit (post, repost, follow, like, comment) with recommendation systems and a time engine, scaling to a stated one million users, built to study information spread, group polarisation and herd behaviour (arXiv 2411.11581). Ships examples, a Hugging Face dataset, docs and a community. Apache-2.0, 5.2k stars, active (2026-09-30).

## What it can do for us

The most directly relevant off-the-shelf simulator for cascade and polarisation experiments with LLM agents at scale, and a controlled comparator for the in-the-wild wiki dynamics (does a false belief propagate the same way on a feed as on a shared answer board?).

## Run notes

Not run. Metadata (stars, licence, last commit) taken from the GitHub API on 2026-10-03; README read via the API.

## Limitations

Social-media affordances, not a shared wiki or task grader; cost scales with agent count and LLM calls. Not run here.

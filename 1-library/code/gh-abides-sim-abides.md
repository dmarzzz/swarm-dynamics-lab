---
id: gh-abides-sim-abides
type: code
title: "ABIDES (original): agent-based interactive discrete-event market simulator with per-agent latency"
repo: abides-sim/abides
url: https://github.com/abides-sim/abides
authors: ["David Byrd", "Tucker Balch"]
year: 2019
language: "Python"
license: "BSD-3-Clause (GitHub reports NOASSERTION)"
stars: 579
last_commit: 2020-11-19
topics: [meta]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: [byrd-2019-abides]
---

## Summary

Simulates: a NASDAQ-like exchange and many trading agents exchanging ITCH/OUCH-style messages. Interaction model: a kernel delivers messages between agents in nanosecond simulated time with configurable pairwise latency and per-agent computation delay. Scale: "tens of thousands of trading agents" per [[byrd-2019-abides]]. LLM-driven: not built in; an agent's wakeup or receive handler could call one. Adversarial hooks: none native; spoofing or manipulation agents are agent subclasses. Weight: pure Python, laptop. Superseded by the J.P. Morgan rewrite [[gh-jpmorganchase-abides-jpmc-public]].

## What it can do for us

Its kernel (message passing with explicit latency per agent pair) is the right abstraction for builder, relay and searcher latency races and for agents that wake, observe and act asynchronously.

## Run notes

Not run. Stars, licence and last commit from the GitHub API on 2026-10-03; README read via the API. The newer abides-jpmc-public was run instead.

## Limitations

Last commit 2020-11-19; use the JPMC version.

---
id: gh-flashbots-spam-inspect
type: code
title: "spam-inspect: trace-based classifier for on-chain MEV spam bots on OP-Stack rollups"
repo: flashbots/spam-inspect
url: https://github.com/flashbots/spam-inspect
authors: [Flashbots]
year: 2025
language: Python
license: MIT (stated in README; no licence file detected by the GitHub API)
stars: 13
last_commit: 2025-06-15
topics: [sybil-resistance]
added_by: dmarz/sybil-flashbots
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: []
---

## Summary

Python tool (repo created 2025-02-25) that traces every transaction in a block range and classifies "spamming bot activity": transactions that repeatedly call DEX state-reading functions (slot0, getReserves and similar) more than a threshold number of times (default 4) without any legitimate call such as mint, transferFrom or rebalance. It caches block data in Postgres, supports backfilling and parallel batches, and produces charts. It is the tooling behind the measurements in [[flashbots-2025-mev]].

## What it can do for us

- A reproducible behavioural classifier for one kind of wasteful agent: agents that pay to read shared state on-chain and act only occasionally.
- Gives the exact heuristic and threshold, so its gameability can be assessed: the README states that any transferFrom excludes a transaction, and the blog notes adding a token transfer would evade it.
- Needs a trace_block-capable node (OP-Reth or OP-Erigon per the blog), Postgres and Python.

## Run notes

Not run. Read the README; it gives `git clone`, a venv with `pip install -r requirements.txt`, a Postgres setup script (`scripts/setup_db.py`) and `python run.py charts <start_block> <end_block>`.

## Limitations

Heuristic is per transaction and identity-agnostic; attributing spam to operators (the "profit-taking address" grouping in the blog) is a separate analysis not described in the README. Small repository, last commit 2025-06-15.

## Relevance to us

Behavioural classification is the alternative to identity-based Sybil defence: judge each action by what it does rather than who sent it. The weakness, stated by the authors, is that a classifier with a published rule is easy to evade, which is why the accompanying blog argues for repricing the action instead ([[flashbots-2025-mev]], [[mazorra-2026-timing]]).

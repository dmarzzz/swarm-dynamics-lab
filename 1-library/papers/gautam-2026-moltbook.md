---
id: gautam-2026-moltbook
type: paper
title: "The Moltbook Observatory Archive: an incremental dataset of agent-only social network activity"
authors: ["Sushant Gautam", "Annika W. Olstad", "Klas H. Pettersen", "Michael A. Riegler"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2605.13860
doi: null
arxiv: '2605.13860'
cite: "Gautam, S., Olstad, A. W., Pettersen, K. H., & Riegler, M. A. (2026). The Moltbook Observatory Archive: An incremental dataset of agent-only social network activity. arXiv:2605.13860."
topics: [llm-agent-swarms, swarm-detection]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: null
code: [gh-kelkalot-moltbook-observatory]
---

## Summary

Dataset paper. Moltbook is a social network where all posts and comments are written by autonomous AI agents. The archive passively polls the Moltbook API and records agent profiles, posts, comments, community ('submolt') metadata, platform-level time-series snapshots and word-frequency trends into SQLite, exported as date-partitioned Parquet. The documented release covers 78 days (2026-01-27 to 2026-04-14): 2,615,098 posts and 1,213,007 comments from 175,886 unique posting agents across 6,730 communities. MIT licence.

## Contribution

Claims the first large-scale observational dataset of a social network populated only by autonomous agents, with collection code.

## Key results

- 2.6M posts, 1.2M comments, 175,886 posting agents, 6,730 communities over 78 days.

## Methods and models

Continuous API polling (posts every 2 min, profiles every 15 min, snapshots hourly per repo); HF dataset SimulaMet/moltbook-observatory-archive.

## Limitations and open questions

Abstract only. Observational, so agent identity and human steering behind accounts are not controlled; press coverage linked from the repo reports humans drove much of the growth.

## Relevance to us

Real-world ground truth to calibrate or validate an LLM social sim against (reply depth, cascade sizes, community growth). Related: [[de-marzo-2026-collective]], [[x-daveholtz-2017716355475124330]], [[x-kunmukh-2054965024863461739]] (MoltGraph), dataset [[data-moltbook-dataset-2026]].

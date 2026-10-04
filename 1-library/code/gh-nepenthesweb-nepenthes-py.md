---
id: gh-nepenthesweb-nepenthes-py
type: code
title: "nepenthes-py: Python rewrite of the Nepenthes anti-AI-crawler tarpit (infinite Markov-babble maze)"
repo: NEPENTHESWEB/nepenthes-py
url: https://github.com/NEPENTHESWEB/nepenthes-py
authors: ["NEPENTHESWEB"]
year: 2026
language: Python
license: "MIT"
stars: 36
last_commit: 2026-03-03
topics: [swarm-detection]
added_by: dmarz/sd-code-data
accessed: 2026-10-03
read_depth: skim
relevance: 2
papers: []
---

## Summary

Python reimplementation of Nepenthes, the tarpit that generates an endless sequence of pages of Markov-chain text, each with many links deeper into the maze, served slowly, to trap crawlers and poison training data. The README frames the goal as accelerating model collapse.

## What it can do for us

Same use as [[gh-jonaslong-pyison]]: a sensor whose hit pattern (depth, speed, link-following) separates crawlers from people.

## Run notes

Not run.

## Limitations

Small rewrite of a project hosted elsewhere (zadzmo.org, not opened); the poisoning claim is not measured. Wastes the operator's bandwidth too.

---
id: gh-buzz-lang-buzz
type: code
title: "Buzz: programming language for heterogeneous robot swarms (neighbour map/reduce, dynamic swarms, virtual stigmergy) running on ARGoS and ROS"
repo: buzz-lang/Buzz
url: https://github.com/buzz-lang/Buzz
authors: ["Carlo Pinciroli", "Giovanni Beltrame", "MIST Lab"]
year: 2015
language: C
license: "MIT"
stars: 319
last_commit: 2026-04-01
topics: [swarm-robotics, swarm-intelligence]
added_by: shadow/sol-1
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: []
---

## Summary

A scripting language and VM for swarm behaviour with bottom-up primitives (per-robot commands, neighbour data map/reduce/filter) and top-down primitives (dynamic swarm membership, virtual stigmergy for global shared data) whose runtime is fully distributed; extensible with new primitives and integrable with ROS. Whitepaper arXiv 1507.05946. MIT, 319 stars, last commit 2026-04-01 (repo moved from MISTLab to buzz-lang).

## What it can do for us

Virtual stigmergy is a formalised version of exactly what the wiki swarm improvised (a shared key-value store propagated by gossip); useful vocabulary and a reference design.

## Run notes

Not run. Metadata (stars, licence, last commit) taken from the GitHub API on 2026-10-03; README read via the API.

## Limitations

Needs ARGoS or ROS to run; small community. Not run.

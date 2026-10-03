---
id: gh-google-deepmind-hanabi-learning-environment
type: code
title: "Hanabi Learning Environment: DeepMind's cooperative imperfect-information card game platform (2-5 players)"
repo: google-deepmind/hanabi-learning-environment
url: https://github.com/google-deepmind/hanabi-learning-environment
authors: ["Google DeepMind"]
year: 2019
language: C++ / Python
license: "Apache-2.0"
stars: 669
last_commit: 2023-02-14
topics: [marl-emergence]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: skim
relevance: 2
papers: []
---

## Summary

Simulates the cooperative card game Hanabi, in which each of 2 to 5 players sees everyone's cards except their own and can only share information through costly hint actions; interaction is turn-based. Provides a Gym-like `rl_env.py` and a lower-level `pyhanabi.py` game interface for search methods. Scale is fixed at 2-5 agents; throughput not reported in the README. Because the state is a short symbolic description (hands, hints, discards), text rendering for LLM agents is straightforward. No population mechanics; partner swapping (ad hoc play) is the only identity manipulation. Light C++ build with pip. Archived by Google DeepMind (read-only) with last push February 2023; JAX re-implementations exist in [[gh-bold-lab-ai-jaxmarl]].

## What it can do for us

A clean testbed for implicit communication and theory of mind among few agents, and for detecting a partner that does not follow the shared convention (a 2-5 player analogue of spotting an outsider). Background only for swarm work.

## Run notes

Not run. README read via GitHub API on 2026-10-03.

## Limitations

Archived. Small fixed player count. Turn-based, so not a dynamics simulator.

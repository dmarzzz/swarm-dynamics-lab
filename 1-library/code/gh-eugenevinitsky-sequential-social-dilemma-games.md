---
id: gh-eugenevinitsky-sequential-social-dilemma-games
type: code
title: "Sequential Social Dilemma Games: open reimplementation of DeepMind's Harvest (commons) and Cleanup (public goods) gridworlds"
repo: eugenevinitsky/sequential_social_dilemma_games
url: https://github.com/eugenevinitsky/sequential_social_dilemma_games
authors: ["Eugene Vinitsky", "Natasha Jaques", "contributors"]
year: 2018
language: Python
license: "MIT"
stars: 416
last_commit: 2025-03-06
topics: [marl-emergence, collective-decision]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: [leibo-2017-multi]
---

## Summary

Simulates two gridworld social dilemmas from [[leibo-2017-multi]]: Harvest, a tragedy of the commons in which apple regrowth depends on nearby apples so greedy harvesting collapses the resource, and Cleanup, a public-goods game in which apples only grow if some agents spend time cleaning a river while others can free-ride. Interaction is simultaneous, partially observed (egocentric RGB windows), with a "tagging" beam that removes other agents temporarily. Typical runs use about 5 agents; throughput not reported. RL-only (gym and RLlib multi-agent API, pixel observations). Agent count is a constructor argument; no join/leave. Moderate install (pinned old Python 3.8 and patched Ray per README).

## What it can do for us

The canonical small "defector in the commons" setting: putting one exploiter or a coordinated group among cooperators and watching the resource collapse is the direct analogue of Sybil over-extraction. The repo's README itself recommends using [[gh-google-deepmind-meltingpot]] instead, which contains maintained versions of these substrates.

## Run notes

Not run. README read via GitHub API on 2026-10-03.

## Limitations

Deprecated by its author in favour of Melting Pot (README "Deprecation Warning"). Old pinned dependencies.

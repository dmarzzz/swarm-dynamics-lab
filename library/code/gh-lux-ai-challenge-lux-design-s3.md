---
id: gh-lux-ai-challenge-lux-design-s3
type: code
title: "Lux AI Season 3 (NeurIPS 2024 / Kaggle): JAX two-team partially observable unit-control game with meta-learning matches"
repo: Lux-AI-Challenge/Lux-Design-S3
url: https://github.com/Lux-AI-Challenge/Lux-Design-S3
authors: ["Lux AI Challenge organisers (Stone Tao et al.)"]
year: 2024
language: Python (JAX)
license: "Apache-2.0"
stars: 352
last_commit: 2025-02-05
topics: [marl-emergence]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: skim
relevance: 2
papers: []
---

## Summary

Simulates a 1v1 strategy game in which each player controls a fleet of units on a randomised map to gather points under partial observability, played as best-of-five match series on the same randomised map and game parameters so that bots must adapt within a series (the "meta-learning style" twist). Interaction is simultaneous per turn; bots are separate processes speaking a JSON protocol through starter kits in Python, JS and others, which makes it straightforward to plug in an LLM-driven bot. Throughput: the env is JAX and the README provides a benchmark script for 16,384 parallel envs on GPU; not measured here. Two players, each with many units; no open population. Moderate install (pip -e, JAX). Kaggle-hosted competition ended.

## What it can do for us

A worked example of the "bots as external processes over a JSON protocol" pattern, which is what an LLM-agent arena needs, combined with a JAX core for RL throughput. Also a source of strong competition bots as opponents.

## Run notes

Not run. README read via GitHub API on 2026-10-03. Documented smoke test: `luxai-s3 path/to/bot/main.py path/to/bot/main.py --output replay.json`.

## Limitations

Two-player only. Season-specific rules; previous seasons are separate repos. Last push February 2025.

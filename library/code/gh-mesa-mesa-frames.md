---
id: gh-mesa-mesa-frames
type: code
title: "mesa-frames: Mesa extension storing agents in Polars DataFrames for vectorised, large-population models"
repo: mesa/mesa-frames
url: https://github.com/mesa/mesa-frames
authors: ["Mesa project contributors"]
year: 2024
language: Python
license: "Apache-2.0"
stars: 43
last_commit: 2026-09-07
topics: [meta]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 3
papers: []
---

## Summary

One line: Mesa-style Model/AgentSet API where an AgentSet is a Polars DataFrame and agent rules are column operations (grid spaces; no continuous-space flocking example in the README); README claims up to 10x over classic Mesa on Boltzmann wealth and about 2x on Sugarscape, with practical populations of 10^6+ versus about 10^3; no LLM integration; no adversarial hooks; light to run (pip install mesa-frames).

The README is explicit that it is a poor fit for models needing strict per-agent sequencing or non-vectorisable methods.

## What it can do for us

If we stay in the Mesa ecosystem and need 10^5 simple agents (for example a population of mostly scripted agents with a few LLM-driven ones), this is the in-ecosystem route. Its synchronous, set-based updates also make update order explicit.

## Run notes

Not run.

## Limitations

Benchmarks self-reported. Vectorised rules mean simultaneous (synchronous) updates by default, which changes model behaviour for some models ([[radax-2010-timing]]).

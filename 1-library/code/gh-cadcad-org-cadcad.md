---
id: gh-cadcad-org-cadcad
type: code
title: "cadCAD: Python framework for complex adaptive dynamics simulations with Monte Carlo, A/B tests and parameter sweeps"
repo: cadCAD-org/cadCAD
url: https://github.com/cadCAD-org/cadCAD
authors: ["cadCAD.org", "BlockScience"]
year: 2018
language: "Python"
license: "MIT"
stars: 620
last_commit: 2024-04-19
topics: [meta, sybil-resistance]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: []
---

## Summary

Simulates: any discrete-time system written as a state dictionary updated by policy functions and state-update functions in partial state-update blocks, widely used for token-economy and mechanism design in crypto. Interaction model: synchronous timesteps, Monte Carlo runs and parameter sweeps; agents are entries in the state, not processes. Scale: not stated in the README. LLM-driven: a policy function could call an LLM, but nothing is built in. Adversarial hooks: none; an attacker is another policy. Weight: pure Python, laptop. Version 0.5.3 per the README.

## What it can do for us

The modelling vocabulary (policies, state updates, sweeps) that crypto mechanism designers already use; useful to write Sybil-cost or reputation-capture models that Flashbots and token-engineering readers will recognise. [[gh-cadlabs-radcad]] runs the same model shape faster.

## Run notes

Not run. Stars, licence and last commit from the GitHub API on 2026-10-03; README read via the API. The compatible re-implementation radCAD was run instead; see [[gh-cadlabs-radcad]].

## Limitations

Last commit 2024-04-19. Not a network or agent-process simulator: no messages, latency or identities. Slow on large sweeps compared with radCAD (per radCAD's own positioning; not measured here).

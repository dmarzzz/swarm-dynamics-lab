---
id: gh-ibm-amlsim
type: code
title: "AMLSim: IBM multi-agent anti-money-laundering transaction simulator (MASON-based) producing labelled synthetic financial graphs"
repo: IBM/AMLSim
url: https://github.com/IBM/AMLSim
authors: ["Toyotaro Suzumura", "Hiroki Kanezashi"]
year: 2018
language: Python/Java
license: "Apache-2.0"
stars: 399
last_commit: 2025-09-17
topics: [swarm-detection, sybil-resistance]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 3
papers: [gh-eclab-mason]
---

## Summary

Simulation model: account agents transact over a generated graph with injected money-laundering typologies, producing synthetic transaction logs with ground-truth labels for detection research. Built on Java 8 + MASON 20, with Python generators. Adversarial hooks: yes, laundering patterns are the adversary. Weight: Java toolchain plus manual jar downloads.

## What it can do for us

Template for injecting coordinated adversarial typologies into an agent population to produce labelled data for detectors, which is the shape of a Sybil-detection benchmark.

## Run notes

Not run. Stars, licence and last push from the GitHub API on 2026-10-03; README read via the API; source code not read.

## Limitations

Old stack; finance-specific typologies; master branch only per README.

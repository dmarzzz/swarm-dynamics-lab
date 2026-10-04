---
id: gh-nsnam-ns-3-dev-git
type: code
title: "ns-3: discrete-event packet-level network simulator for research and education (GitHub mirror)"
repo: nsnam/ns-3-dev-git
url: https://github.com/nsnam/ns-3-dev-git
authors: ["ns-3 project"]
year: 2013
language: "C++"
license: "GPL-2.0-only"
stars: 563
last_commit: 2026-10-03
topics: [meta]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 2
papers: []
---

## Summary

Simulates: packet-level networks (wired, wireless, LTE and more) with models of protocol stacks written for the simulator. Interaction model: C++ discrete-event scheduler; applications are model code, not real binaries (the Shadow README contrasts this as better control and scale but limited application realism). Scale: not stated in the README. LLM-driven: no. Adversarial hooks: none native; attacks are written as node models. Weight: C++ build, CPU-only, runs on macOS and Linux. GitHub is a read-only mirror of the GitLab repository; licence GPL-2.0-only.

## What it can do for us

Only useful if we need radio or link-layer realism (drone swarms, mesh radios). For P2P overlays and agent swarms, Shadow or a higher-level simulator fits better.

## Run notes

Not run. Stars, licence and last commit from the GitHub API on 2026-10-03; README read via the API.

## Limitations

Applications must be re-implemented as ns-3 models, which is the opposite of what we want for testing real agent or client code. GitHub mirror only; contributions go to GitLab.

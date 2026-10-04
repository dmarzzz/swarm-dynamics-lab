---
id: wild-identity
type: task
title: Identity churn and observable coordination across three swarms
kind: build
status: open
priority: p1
owner: null
for: shadow
created: 2026-10-04
created_by: shadow/sol-identity
depends_on: []
topics: [swarm-detection, sybil-resistance, llm-agent-swarms]
---

## Goal

Descriptive, post-hoc analysis requested by Shadow: observed label lifetimes, participation concentration, and sign-off/mention graphs in collusion.wiki and SwarmTraces versus swarm-lab commit agent ids. No model calls or causal identity claims.

## Done when

- Reproducible code takes an external --data path; raw datasets stay out of git.
- Derived aggregate tables, lifetime CDF, Lorenz curves and graph metrics are saved.
- One-page FINDING.md reports denominators, uncertainty and identity attribution limits.
- Novelty check against library and existing wiki copying analysis is documented.
- lab.py check passes and deliverables are pushed.

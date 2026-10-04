---
id: wild-identity
type: task
title: Identity churn and observable coordination across three swarms
kind: build
status: done
priority: p1
owner: shadow/sol-identity
for: shadow
created: 2026-10-04
created_by: shadow/sol-identity
depends_on: []
topics:
- swarm-detection
- sybil-resistance
- llm-agent-swarms
claimed_at: 2026-10-04T14:56Z
updated: 2026-10-04T15:23Z
outputs:
- researchers/shadow/notes/wild-identity/FINDING.md
- researchers/shadow/notes/wild-identity/README.md
- researchers/shadow/notes/wild-identity/results/summary.json
- researchers/shadow/notes/wild-identity/results/identity-observability.svg
---

## Goal

Descriptive, post-hoc analysis requested by Shadow: observed label lifetimes, participation concentration, and sign-off/mention graphs in collusion.wiki and SwarmTraces versus swarm-lab commit agent ids. No model calls or causal identity claims.

## Done when

- [x] Reproducible code takes an external --data path; raw datasets stay out of git.
- [x] Derived aggregate tables, lifetime CDF, Lorenz curves and graph metrics are saved as working material.
- [x] One-page FINDING.md reports denominators, uncertainty and identity attribution limits.
- [x] Novelty check against library and existing wiki copying analysis is documented.
- [x] lab.py check passes and deliverables are pushed.

## Coverage note

Every source row is accounted for: wiki 14,591 revisions, git 2,897 frozen commits, SwarmTraces 189,579 redacted rows. SwarmTraces identity metrics are not identifiable because actor fields and timestamp values are missing; not imputed. Ten fixtures and 25 aggregate checks pass. Working SVG is saved; formal Flight Deck publication was rolled back because of existing missing video paths, worktree strict validation, and tool rewrites of unrelated researchers' provenance. Those unrelated writes were restored. Evidence metadata records exploratory status with no causal churn claim.

---
id: wild-askswarm
type: task
title: 'AskSwarm: reusable descriptive questions across three observed swarms'
kind: build
status: done
priority: p0
owner: shadow/sol-askswarm
for: shadow
created: 2026-10-04
created_by: shadow/sol-askswarm
depends_on: []
topics:
- swarm-detection
- llm-agent-swarms
- meta
claimed_at: 2026-10-04T14:56Z
updated: 2026-10-04T15:25Z
outputs:
- researchers/shadow/notes/wild-askswarm/README.md
- researchers/shadow/notes/wild-askswarm/FINDING.md
- researchers/shadow/notes/wild-askswarm/results/comparison.html
---

## Goal

Build an offline, reusable table adapter and CLI under researchers/shadow/notes/wild-askswarm/.
Compare lexical reuse, observed participation and identity coverage across collusion.wiki,
SwarmTraces and this repository. Human-directed exploratory tooling, not a gated hypothesis test.
No paid calls. Never commit source dataset rows. Missing actors or clocks stay missing.

## Done when

- [x] Importable package, three source adapters, generic table adapter and 18 tests.
- [x] One HTML report per source plus cross-source comparison and aggregate JSON.
- [x] One-page FINDING.md, reproducible commands, source/code hashes and limitations.
- [x] Repository check passes and outputs pushed (tool 5afc526a, results d6463560).

## Coverage note

All three source adapters executed. SwarmTraces has 189,579 artifacts but zero explicit actors
and zero non-null clocks; social/temporal metrics are unavailable, not imputed. Wiki uses all
14,591 revision snapshots; git freezes 2,673 non-merge commits at 4959a80b. Seven baseline and
sensitivity reports pass aggregate arithmetic checks. Three hub reports read back as done.
The SVG is usable under notes/results; Flight Deck publication is deferred because its add
command rewrites unrelated researchers' attestations. All such side effects were restored.

---
id: build-soc07-private-judgments
type: task
title: Build and run the SOC-07 private-judgments development study (S0, S1)
kind: build
status: open
priority: p1
owner: null
for: dmarz
created: 2026-10-04
created_by: dmarz/soc07-private
depends_on:
- design-soc07-private-commitment
topics:
- llm-agent-swarms
- collective-decision
---

## Goal

Implement the plan in `researchers/dmarz/notes/soc07-private-judgments/` and take it to a running exploratory
study on the team hub: keep five agents' first judgments private or publish them before one discussion round,
with revision allowed. Exploratory S0 and S1 only; the 960-world S2 confirmation is closed. Requested by dmarz.
Cross-researcher review is waived by dmarz for this study; the reviewer is dmarz/fleet-monitor.

## Done when

- [ ] Phase 1: generator, protected scorer, controller with phase barriers, vault, board, budget ledger, journal,
      scripted policies, provider adapter and hub worker implemented under `src/`, with unit tests and the
      plan's S0 (60 offline fixtures plus fault injections) passing.
- [ ] Phase 1: scripted S0 run on a claimed server, reported to the hub, zero model calls.
- [ ] Phase 1: pre-run assessment for S1-Q, S1-R and S1-L committed (`reviews/s1-pre.md`).
- [ ] Phase 2 (after the reviewer's go): S1-Q, S1-R and S1-L run as separate hub runs with gates between them.
- [ ] Phase 2: analysis, post-run review with actual cost, results on main, server claim released.

## Coverage note

Not started.

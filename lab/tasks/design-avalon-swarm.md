---
id: design-avalon-swarm
type: task
title: 'Design brief (no build): swarm-scale Avalon benchmark layer'
kind: synthesis
status: open
priority: p2
owner: null
for: dmarz
created: 2026-10-03
created_by: dmarz/avalon
depends_on:
- survey-avalon-swarm
topics:
- llm-agent-swarms
- sybil-resistance
- fork-merge-security
---

## Goal

A one-page design brief in the style of `5-experiments/studies/dmarz/swarm-factory.md`, written only after the
survey: which base engine, which of A1-A6 survive the survey, the balance sweep needed per N, cost estimate
(seats x rounds x messages, local vs frontier split), and the metrics. Do not build the simulation; dmarz
decides that after reading the brief.

## Done when

- `researchers/dmarz/notes/avalon-swarm.md` written, linking the survey and the chosen base engine entry.
- Includes the BotSim pitfall check (honest agents must actually engage the Sybils).
- `check` passes.

---
id: run-market-split-api
type: task
title: Ship the neutral-agent market-splitting pilot
kind: build
status: claimed
priority: p1
owner: dmarz/market-split
for: dmarz
created: 2026-10-03
created_by: dmarz/market-split
depends_on: []
topics:
- sybil-resistance
- llm-agent-swarms
claimed_at: 2026-10-04T02:08Z
updated: 2026-10-04T03:11Z
---

## Goal

Qualify the paid model adapter offline, then run bounded neutral-agent competence and discovery tests through agentops with measured replays. Use the existing shared dmarz API authorization.

## Done when

- [x] Frozen neutral design and durable accounting pass mocked API tests.
- [x] Exclusive host and reviewed model qualification pass before discovery.
- [ ] Bounded discovery pilot reports all episodes, failures, cost and replay.
- [ ] Post-mortem, artifact verification and claim release completed.

## Coverage note

2026-10-04: user added a conditional parallel-model request. Sonnet V5 now passes15offline checks,12mockepisodes,6mechanics and4fresh profit episodes;independent Haiku qualification may proceed while Sonnet discovery runs. Both retain separate queues,ledgers and model-specific reports.

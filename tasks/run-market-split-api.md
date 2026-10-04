---
id: run-market-split-api
type: task
title: Ship the neutral-agent market-splitting pilot
kind: build
status: done
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
updated: 2026-10-04T06:58Z
outputs:
- researchers/dmarz/notes/market-split-api/RESULTS.md
- researchers/dmarz/notes/market-split-api/reviews/s1-002-post.md
- researchers/dmarz/notes/market-split-api/report/s1-002/closeout.json
- researchers/dmarz/notes/market-split-haiku/NEXT-EXPERIMENT.md
---

## Goal

Qualify the paid model adapter offline, then run bounded neutral-agent competence and discovery tests through agentops with measured replays. Use the existing shared dmarz API authorization.

## Done when

- [x] Frozen neutral design and durable accounting pass mocked API tests.
- [x] Exclusive host and reviewed model qualification pass before discovery.
- [x] Bounded discovery pilot reports all episodes, failures, cost and replay.
- [x] Post-mortem, artifact verification and claim release completed.

## Coverage note

2026-10-04: user added a conditional parallel-model request. Sonnet V5 now passes15offline checks,12mockepisodes,6mechanics and4fresh profit episodes;independent Haiku qualification may proceed while Sonnet discovery runs. Both retain separate queues,ledgers and model-specific reports.

2026-10-04 closeout:18original Sonnet bundles/36valid episodes/864calls complete; all126run and8analysis artifacts read back,864actions replayed, full results/post-mortem/records published. Claim released; existing host preserved. Haiku failure/teardown retained; next diagnostic plan published and unstarted. One unrelated missing shared-film artifact remains disclosed in the post-mortem.

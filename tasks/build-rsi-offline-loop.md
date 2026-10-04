---
id: build-rsi-offline-loop
type: task
title: Build a real-record offline trace to improvement to credit loop
kind: build
status: done
priority: p1
owner: shadow/sol-rsi2
for: shadow
created: 2026-10-04
created_by: shadow/sol-rsi2
depends_on: []
topics:
- llm-agent-swarms
claimed_at: 2026-10-04T14:07Z
updated: 2026-10-04T14:35Z
outputs:
- researchers/shadow/notes/rsi/DEMO.md
- researchers/shadow/notes/rsi/r1-results/summary.json
- researchers/shadow/notes/rsi/r1-results/replay.html
- researchers/shadow/notes/rsi/R1-POSTMORTEM.md
---

## Goal

Continue the owner-requested RSI tooling demo on shadow/rsi. Import approved metadata from saved research records, package agent-authored bounded improvements, replay a frozen reporting contract, and issue non-monetary attribution receipts. No research-effect claim, raw private trace export, upstream experiment edits or live settlement.

## Done when

- [x] A prospective engineering replay plan and source manifest are saved.
- [x] Real capture-memory records and explicitly scoped pool metadata become swarm-trace envelopes; public teammate trace import is included if usable.
- [x] The searcher supplies pinned declarative bundles, including a useful repair and a rejected alternative.
- [x] An offline builder recomputes decisions and conserving attribution credits against frozen records.
- [x] Tests, limitations, privacy audit, DEMO.md and a pull request are published on shadow/rsi only.

## Coverage note

Delivered [DEMO.md](../researchers/shadow/notes/rsi/DEMO.md), 566 validated envelopes and a deterministic real-record report/credit replay. Accepted lineage repair 195/195 accounting checks versus baseline 75/195; rejected shortcut 75/195. Eighteen R1 tests and fourteen protocol tests pass, as do desktop/mobile browser and local privacy checks. No paid calls, raw pool export or upstream deployment. [PR #84](https://github.com/dmarzzz/swarm-lab/pull/84) is open and unmerged, branch shadow/rsi.

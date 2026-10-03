---
id: build-discussion-dose
type: task
title: Build and deploy the SEC-47 discussion dose exploratory study
kind: build
status: done
priority: p1
owner: dmarz/discussion-dose
for: dmarz
created: 2026-10-03
created_by: dmarz/discussion-dose
depends_on: []
topics:
- fork-merge-security
- llm-agent-swarms
- collective-decision
claimed_at: 2026-10-03T23:24Z
updated: 2026-10-03T23:39Z
outputs:
- researchers/dmarz/notes/discussion-dose/README.md
- researchers/dmarz/notes/discussion-dose/ARCHITECTURE.md
- researchers/dmarz/notes/discussion-dose/TASKS-AND-EVALS.md
- researchers/dmarz/notes/discussion-dose/VALIDATION.md
---

## Goal

At the human's request, write an exploratory SEC-47 plan, link related atlas questions, implement a minimal reusable environment with mechanically validated tasks and scores, and deploy through swarm-labs-agentops. Register in the live hub experiment list as exploratory; preserve formal review gates. Use templates/experiment-worker as the starting point. S2 remains disabled.

## Done when

- [x] Plan, architecture, metrics and benchmark audit are linked and committed before pilot collection.
- [x] Offline tests cover task validity, access isolation, board barriers, merge, scoring and failure accounting.
- [x] Code is deployed to a claimed fleet server, registered in the live list, and an engineering smoke run is reported.
- [x] Execution limits, results, review status and remaining launch requirements are documented.

---
id: build-memory-handoff-qwen
type: task
title: Prepare program v5 line M (can successors repair inherited false memory) to launch-ready
kind: build
status: claimed
priority: p0
owner: dmarz/pipeline-memory
for: dmarz
created: 2026-10-04
created_by: dmarz/pipeline
depends_on: []
topics:
- llm-agent-swarms
claimed_at: 2026-10-04T10:30Z
updated: 2026-10-04T10:30Z
---

## Goal

Line M of research program v5: does binding inherited claims to original source contents repair false or stale memory without erasing useful knowledge? 24 roots x 6 memory states x 4 handoff policies, 576 main calls and 24 qualification calls on qwen/qwen3.7-flash, reusing the discussion benchmark v3 memory fixtures, resolver and scorer in new files. Study directory `researchers/dmarz/notes/memory-handoff-qwen/`. The program is dmarz's own (research program v5, 2026-10-04); this task implements the line as a ready-chain package. Preparation only: this task launches nothing and makes no model inference call. The run goes through the private run queue after the fleet monitor's same-researcher check.

## Done when

- [ ] Plan and frozen design (the program's design for this line) committed before implementation.
- [ ] Code, offline tests and a scripted zero-model-call stage that passes offline.
- [ ] Pre-run review on main with assignment manifest, call counts, gates, model settings, hard max_calls and the pinned commit.
- [ ] Chained launch per researchers/dmarz/notes/pipeline/READY-CHAIN.md with the server as a parameter.
- [ ] Run request filed in the private run queue after the fleet monitor's go.

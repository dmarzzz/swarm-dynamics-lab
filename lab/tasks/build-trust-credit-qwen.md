---
id: build-trust-credit-qwen
type: task
title: Prepare program v5 line T (trust credit, when verification amplifies capture) to launch-ready
kind: build
status: done
priority: p0
owner: dmarz/pipeline-split
for: dmarz
created: 2026-10-04
created_by: dmarz/pipeline
depends_on: []
topics:
- sybil-resistance
- llm-agent-swarms
claimed_at: 2026-10-04T10:30Z
updated: 2026-10-04T11:37Z
outputs:
- 5-experiments/studies/dmarz/trust-credit-qwen/reviews/chain-001-pre.md
---

## Goal

Line T of research program v5: does propagating a passed identity's trust credit to its neighbours cause extra attackers to be admitted? 24 fresh roots, 324 scripted identities, three admission rules replayed on one frozen audit sequence, 504 main calls and 24 qualification calls on qwen/qwen3.7-flash. Study directory `researchers/dmarz/notes/trust-credit-qwen/`. The program is dmarz's own (research program v5, 2026-10-04); this task implements the line as a ready-chain package. Preparation only: this task launches nothing and makes no model inference call. The run goes through the private run queue after the fleet monitor's same-researcher check.

## Done when

- [x] Plan and frozen design (the program's design for this line) committed before implementation.
- [x] Code, offline tests and a scripted zero-model-call stage that passes offline.
- [x] Pre-run review on main with assignment manifest, call counts, gates, model settings, hard max_calls and the pinned commit.
- [x] Chained launch per researchers/dmarz/notes/pipeline/READY-CHAIN.md with the server as a parameter.
- [x] Run request filed in the private run queue after the fleet monitor's go. (Filed and run by the operator as run queue 270, 2026-10-04.)

## Outputs after the run (added by dmarz/pipeline-split, 2026-10-04)

- researchers/dmarz/notes/trust-credit-qwen/RESULTS.md
- researchers/dmarz/notes/trust-credit-qwen/records/
- researchers/dmarz/notes/trust-credit-qwen/reviews/chain-001-post.md
- researchers/dmarz/notes/trust-credit-qwen/reporting/build_report.py

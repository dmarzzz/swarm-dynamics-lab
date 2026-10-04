---
id: design-compositional-safety-study
type: task
title: Design the Patchwork compositional safety study
kind: synthesis
status: done
priority: p1
owner: dmarz/patchwork-hypotheses
for: dmarz
created: 2026-10-03
created_by: dmarz/patchwork-hypotheses
depends_on: []
topics:
- fork-merge-security
- llm-agent-swarms
- swarm-detection
claimed_at: 2026-10-04T02:20Z
updated: 2026-10-04T02:26Z
outputs:
- researchers/dmarz/notes/compositional-safety-plan/README.md
- researchers/dmarz/notes/compositional-safety-plan/design.json
- researchers/dmarz/notes/compositional-safety-plan/src/check_plan.py
---

## Goal

User request: "design an experiment plan that would achieve the goal of impressing deepmind researchers after we have run it at scale". Design an explicitly unreviewed working plan for SEC-54, with causal controls, staged qualification, power and resource planning, transfer tests, falsifiers and a reproducible release. Planning only; no model calls, server allocation or formal hypothesis promotion.

## Done when

- [x] Save the complete working plan and its exact design matrix.
- [x] Check the closest prior work and state the limits of the novelty claim.
- [x] Validate sample arithmetic, planned inference and budget accounting.
- [x] Run repository checks and publish the plan with a clear entry point.

## Coverage note

Published a requested, explicitly unreviewed SEC-54 working plan. The 69,940-episode reference envelope distinguishes 500 independent main-study task roots from repeated model/variant/arm runs. It includes a 1,920-episode development stage, ordinary-goal tasks, shared-versus-fragmented specialist controls, receipt placebos, SafeFlow adaptation, global reference enforcement, held-out-family transfer, independent implementation, power/cost decisions, failure accounting and falsifiers. No formal hypothesis, experiment or model run was created. Arithmetic and local links passed; lab check had 0 errors and 5 inherited catalogue warnings; strict Flight Deck check passed.

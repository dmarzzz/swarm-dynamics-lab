---
id: survey-agent-budgets
type: task
title: 'Survey: agent budgets, budget visibility and self-allocation among agents'
kind: survey
status: claimed
priority: p1
owner: shadow/sol-budget
for: null
created: 2026-10-03
created_by: dmarz/budget
depends_on: []
topics:
- agent-budgets
claimed_at: 2026-10-04T14:27Z
updated: 2026-10-04T16:08Z
---

## Goal

Context from dmarz: in large multi-agent runs, are agents given resource allocations, can they see them, and
what happens when agents coordinate their budgets (divide and conquer, or splitting into more identities to
claim more quota)? Prior-art survey for topic `agent-budgets`, seeded by the 2026-10-03 scan (dmarz/budget-a,
-b, -c). Cover: visible versus hidden budgets (reasoning and tool use), budget misperception, orchestrator
effort scaling, peer versus coordinator versus market allocation of a shared budget, commons and public-goods
games, tacit collusion and market division, and false-name (Sybil) manipulation of per-identity quotas.
Search the vocabulary of economics (common-pool resources, false-name-proof mechanisms), operating systems
(fair queueing, quotas, rate limiting) and RL (constrained and budgeted MDPs) as well as LLM agents.

Candidate experiments B1-B5 are hunches in `researchers/dmarz/notes/agent-budgets-hunches.md`. They become
hypothesis files only after this survey passes the gate.

## Done when

- `python3 scripts/lab.py gate survey-agent-budgets` reports nothing missing.
- The Gaps section states, with search evidence, whether any study measures LLM agents spawning extra
  identities to claim per-identity quota (hunch B2).
- Review task opened for another researcher.

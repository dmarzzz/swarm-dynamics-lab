---
id: wild-halflife
type: task
title: 'Idea half-life: adoption curves on collusion.wiki vs swarm-lab commit history'
kind: build
status: done
priority: p0
owner: shadow/sol-halflife
for: shadow
created: 2026-10-04
created_by: shadow/sol-halflife
depends_on: []
topics:
- llm-agent-swarms
- swarm-detection
claimed_at: 2026-10-04T15:03Z
updated: 2026-10-04T16:07Z
outputs:
- 5-experiments/studies/shadow/wild-halflife/FINDING.md
- 5-experiments/studies/shadow/wild-halflife/README.md
- 5-experiments/studies/shadow/wild-halflife/results/summary.json
- 5-experiments/studies/shadow/wild-halflife/results/supplement.json
- 5-experiments/studies/shadow/wild-halflife/results/fig-adoption.png
---

## Goal

Hackathon project A (BRIEF-2026-10-03 section 4), human-directed exploratory observational analysis,
not a gated hypothesis test. Measure how fast reused text units (inserted lines, URLs) spread to new
identities in collusion.wiki (identity = label, alternatively /16 ip block) and in this repository's
own commit history (identity = agent id, alternatively researcher). Survival-style adoption curves
and adoption hazard / half-life as a function of the number of visible prior copies. Framed as a
cross-swarm extension of arXiv 2609.09150 (de-marzo-2026-copying), not a discovery of copying.
No model calls. Never commit source dataset rows; code takes a --data path.

## Done when

- [x] PLAN.md committed before outcomes are computed (2cb859a5).
- [x] Analysis code with seven offline tests under researchers/shadow/notes/wild-halflife/; 12/12 same-author reference checks pass.
- [x] Aggregate JSON, one three-panel figure, FINDING.md with 1,000-resample bootstrap CIs, sensitivity checks, limits and novelty check.
- [x] Repository check passes, zero errors; draft 48bc8a76 and completed report 6af65898 pushed to main. Hub retrospective display readback done. Whole-repo strict Flight Deck check has pre-existing missing-film/worktree-name errors, disclosed in the post-mortem.

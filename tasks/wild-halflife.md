---
id: wild-halflife
type: task
title: 'Idea half-life: adoption curves on collusion.wiki vs swarm-lab commit history'
kind: build
status: claimed
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
updated: 2026-10-04T15:03Z
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

- [ ] PLAN.md committed before outcomes are computed.
- [ ] Analysis code with offline tests under researchers/shadow/notes/wild-halflife/.
- [ ] Aggregate JSON, figure, one-page FINDING.md with numbers, uncertainty, limits, novelty check.
- [ ] Repository check passes and outputs pushed.

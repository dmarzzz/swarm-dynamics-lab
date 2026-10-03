---
id: review-llm-agent-swarms
type: task
title: 'Review survey: llm agent swarms (cross-researcher)'
kind: review
status: open
priority: p0
owner: null
for: dmarz  # or vishesh; any agent not belonging to shadow
created: '2026-10-03'
created_by: shadow/sol-1
depends_on: []
topics: [llm-agent-swarms]
---

## Goal

surveys/llm-agent-swarms.md is `status: complete` and passes `lab.py gate llm-agent-swarms` (60+ cites, 16 search rounds, 5 seminal). It needs a review from an agent of a researcher other than shadow before any hypothesis can be filed against it. This is the hackathon's home-turf survey (measurable swarm dynamics in LLM populations: consensus / polarisation crossover with N, Ringelmann ceilings, committed-minority tipping, copying in the wild), so unblocking it unblocks the first hypotheses.

Create `reviews/llm-agent-swarms--<your-researcher>.md` with `python3 scripts/lab.py new review llm-agent-swarms--<researcher> --agent <id>`.

Things the author (shadow/sol-1) would most like challenged:
- The "What is known" bullets: are any of them single-source claims dressed as replicated?
- The Gaps list: is any gap already closed by a paper dmarz's scan catalogued that the survey missed? dmarz's llm-agent-swarms agents read 110 papers; the survey cites about 60.
- The seven uncatalogued forward-citation items named at the end of Gaps (Moltbook network structure, Chirper.ai, "Does safety molt", etc.): if any is load-bearing, say so.

## Done when

- Five cited entries spot-checked against their sources.
- Three independent searches run; missed work listed.
- `reviews/llm-agent-swarms--<researcher>.md` committed with `verdict: pass` or `revise` and reasons.

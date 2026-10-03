---
id: survey-sybil-resistance
type: task
title: 'Survey: Sybil resistance in multi-agent and swarm systems'
kind: survey
status: open
priority: p1
owner: null
for: null  # set to a researcher name to direct the task at them
created: 2026-10-03
created_by: dmarz/sybil
depends_on: [scan-papers-sybil-foundations, scan-papers-sybil-robotics, scan-papers-sybil-llm-agents, scan-flashbots-sybil]
topics: [sybil-resistance]
---

## Goal

Prior-art survey across all sybil scan tasks, structured around the cost of an identity in each setting (robots, P2P, LLM agents, MEV).

## Done when

- `python3 scripts/lab.py gate survey-sybil-resistance` reports nothing missing.
- Review task opened for another researcher.

## Coverage note


Filled by dmarz/sybil, 2026-10-03.

Wrote [[sybil-resistance]] as `surveys/sybil-resistance.md` (status in-progress) from the library entries tagged sybil-resistance (271 at the time) and the lane reports of the nine sybil scan tasks and two gap fills. No new searches were run in this pass; the survey is a synthesis. The body cites well over 150 distinct library entries, including more than 10 papers read in full, more than 3 code repos, more than 2 blogs or talks and many from 2025 and 2026, so every citation floor of the gate passes. Seminal works: douceur-2002-sybil, yokoo-2004-effect, singh-2006-eclipse, davidson-2018-privacy, gil-2015-guaranteeing. The Landscape is organised by setting: P2P and social graphs, robot swarms and networked control, LLM agent collectives, mechanism design, cryptographic credentials, MEV and Flashbots.

The frontmatter search log was reconstructed only from the coverage notes in tasks/*sybil*.md. Only eight rounds had both a hit count and the entries produced: the Privacy Pass forward chase (100 hits, 2 new), writings.flashbots.net (17 read, 5 new), collective.flashbots.net (33 read, 8 new), the flashbots GitHub org (8 repos, 5 new) and four Semantic Scholar forward chases from the P2P gap fill (GossipSub 14/2, Singh 2006 15/0, Bankrupting Sybil 0/0, S/Kademlia 2/0). Every other lane recorded its queries but not per-query counts, so those rounds are described in prose in the Search log section and left out of the structured log.

Gate status (`python3 scripts/lab.py gate sybil-resistance`): still missing a counted scholarly-index round, a counted preprint round, a social round, a backward citation round, and saturation (the last round has 0 results, which the gate treats as not saturated). `lab.py check --agent dmarz/sybil` reports 0 errors.

Done when progress:
- [ ] gate reports nothing missing (blocked on the search-log items above; needs counted reruns, not more citations)
- [ ] review task opened for another researcher (not opened, since the survey is not complete)

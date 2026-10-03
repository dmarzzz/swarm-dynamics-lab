---
id: scan-code-collective-sims
type: task
title: Catalogue simulators for collective motion and active matter
kind: scan
status: open
priority: p0
owner: null
created: '2026-10-03'
created_by: dmarz/setup
depends_on: []
topics:
- collective-motion
- active-matter
- sync-consensus
- crowds-and-traffic
---

## Goal

Find the code we could build experiments on: agent-based simulators, GPU particle engines, and reference implementations of the classic models.

## Seeds

Seeds come from memory and are starting points, not citations. Open each one, confirm the details, and catalogue it only if it checks out.

- NetLogo (its Flocking model) and Mesa (projectmesa/mesa)
- JAX MD (jax-md/jax-md) for GPU particle simulation
- Reference implementations of Vicsek, Couzin, Cucker-Smale and swarmalator models
- Pedestrian simulators built on the social force model

## Search plan

- GitHub search by topic and by language, sorted by stars and by recent activity; GitHub topics pages (e.g. topics/swarm, topics/multi-agent).
- Papers With Code and paper project pages for implementations of catalogued papers.
- For each candidate, record stars, last commit date and licence from the repo page.

## Done when

- At least 15 repos catalogued with stars, last commit, licence and an honest read_depth.
- At least 3 installed and run (read_depth: ran) with the commands and results in Run notes, chosen as the most likely to be used in the hackathon.
- Coverage note filled, including a short ranked list of what we would build on.

## Coverage note

The agent that finishes this task writes here: what was searched, counts by type, what is still missing, and which follow-up tasks it opened.

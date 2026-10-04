---
id: scan-datasets
type: task
title: Catalogue trajectory and collective-behaviour datasets
kind: scan
status: open
priority: p1
owner: null
created: '2026-10-03'
created_by: dmarz/setup
depends_on: []
topics:
- collective-motion
- collective-decision
- crowds-and-traffic
- swarm-robotics
- llm-agent-swarms
---

## Goal

Find real data we can test models against: animal group trajectories, pedestrian and traffic tracks, robot swarm logs, and logs of multi-agent AI runs.

## Seeds

Seeds come from memory and are starting points, not citations. Open each one, confirm the details, and catalogue it only if it checks out.

- Tracking tools that publish data: idtracker.ai and TRex
- Starling flock reconstructions from the Cavagna and Giardina group
- Pedestrian benchmarks: ETH/UCY, Stanford Drone Dataset
- Traffic: highD and NGSIM
- Fish and insect datasets from collective behaviour labs (search their data repositories, Dryad and Zenodo)

## Search plan

- Search Zenodo, Dryad, Figshare, Hugging Face datasets and Kaggle with topic terms plus 'trajectories' or 'tracking'.
- Check the data availability statements of the catalogued empirical papers.

## Done when

- At least 12 datasets catalogued with size, format, licence and access steps.
- At least 2 downloaded and loaded (read_depth: ran) with a loader snippet in the entry.
- Coverage note filled.

## Coverage note

The agent that finishes this task writes here: what was searched, counts by type, what is still missing, and which follow-up tasks it opened.

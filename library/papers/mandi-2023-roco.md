---
id: mandi-2023-roco
type: paper
title: 'RoCo: Dialectic Multi-Robot Collaboration with Large Language Models'
authors:
- Zhao Mandi
- Shreeya Jain
- Shuran Song
year: 2023
venue: arXiv preprint
url: https://arxiv.org/abs/2307.04738
doi: null
arxiv: '2307.04738'
cite: 'Mandi, Z., Jain, S., & Song, S. (2023). RoCo: Dialectic multi-robot collaboration with large language models. arXiv preprint arXiv:2307.04738.'
topics:
- llm-agent-swarms
- swarm-robotics
added_by: dmarz/llm-agent-swarms
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: "11 (OpenAlex W4383994281, arXiv record, 2026-10-03); Semantic Scholar 303 same day"
code: []
---

## Summary

Each robot arm is equipped with an LLM agent; the agents discuss and collectively reason about task strategy, then generate sub-task plans and task-space waypoint paths for a multi-arm motion planner. Environment feedback (collision checks) is fed back for in-context plan refinement. RoCoBench, a 6-task benchmark, shows high success and adaptation to task variations; real-world experiments include a human in the loop.

## Contribution

Influential "dialectic" coordination of embodied LLM agents with grounding in motion planning.

## Key results

- High success across RoCoBench's six tasks (abstract; numbers not read).

## Methods and models

LLM dialogue for planning, waypoint generation, motion planner, environment feedback loop. Project website with code (not opened).

## Limitations and open questions

Two to three arms; not swarm scale. Venue: Semantic Scholar lists ICRA 2024; the arXiv record does not state it, so the cite uses the preprint.

## Relevance to us

Background for embodied LLM coordination; see [[li-2025-large]].

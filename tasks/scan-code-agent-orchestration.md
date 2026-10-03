---
id: scan-code-agent-orchestration
type: task
title: Catalogue LLM multi-agent and orchestration frameworks
kind: scan
status: claimed
priority: p0
owner: shadow/sol-1
created: '2026-10-03'
created_by: dmarz/setup
depends_on: []
topics:
- llm-agent-swarms
claimed_at: 2026-10-03T17:54Z
updated: 2026-10-03T17:54Z
---

## Goal

Map the frameworks people use to run many LLM agents together, what coordination model each one uses (handoffs, group chat, graphs, blackboards, markets, swarms), and what we could use to run our own experiments.

## Seeds

Seeds come from memory and are starting points, not citations. Open each one, confirm the details, and catalogue it only if it checks out.

- OpenAI Swarm and the OpenAI Agents SDK
- Microsoft AutoGen
- LangGraph
- CrewAI
- CAMEL
- MetaGPT and ChatDev
- Claude Agent SDK and community orchestrators built on Claude Code
- Google DeepMind Concordia for agent-based social simulation

## Search plan

- GitHub search by topic and by language, sorted by stars and by recent activity; GitHub topics pages (e.g. topics/swarm, topics/multi-agent).
- Papers With Code and paper project pages for implementations of catalogued papers.
- For each candidate, record stars, last commit date and licence from the repo page.
- For each framework, record the coordination model in the Summary in one sentence, so the coverage note can compare them.

## Done when

- At least 20 repos catalogued with stars, last commit, licence and an honest read_depth.
- At least 3 installed and run (read_depth: ran) with the commands and results in Run notes, chosen as the most likely to be used in the hackathon.
- Coverage note filled, including a short ranked list of what we would build on.

## Coverage note

The agent that finishes this task writes here: what was searched, counts by type, what is still missing, and which follow-up tasks it opened.

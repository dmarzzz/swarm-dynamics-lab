---
id: guertler-2025-textarena
type: paper
title: "TextArena"
authors: ["Leon Guertler", "Bobby Cheng", "Simon Yu", "Bo Liu", "Leshem Choshen", "Cheston Tan"]
year: 2025
venue: "arXiv"
url: https://arxiv.org/abs/2504.11442
doi: null
arxiv: "2504.11442"
cite: "Guertler, L., Cheng, B., Yu, S., Liu, B., Choshen, L., & Tan, C. (2025). TextArena. arXiv preprint arXiv:2504.11442."
topics: [llm-agent-swarms]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "7 (Semantic Scholar, 2026-10-03)"
code: [gh-textarena-textarena]
---

## Summary

Describes TextArena, an open collection of competitive text games (57+ environments at publication, single, two and multi-player) for evaluating and training LLM agents, with an online play system against humans and other models and real-time TrueSkill ratings. It targets social skills such as negotiation, theory of mind and deception that static benchmarks miss.

## Contribution

A shared, extensible Gym-style game substrate and leaderboard for LLM social and strategic skills.

## Key results

- 57+ environments at publication (abstract); the repo now lists 100+ games.
- Online TrueSkill leaderboard against humans and models (abstract).

## Methods and models

Gym-style env API, string observations and actions, wrappers for rendering and training. Not read beyond the abstract.

## Limitations and open questions

Leaderboard measures win rates rather than collective dynamics; small player counts.

## Relevance to us

Bootstrap substrate for small-group game experiments; I ran a public-goods game with an injected free-rider (see [[gh-textarena-textarena]]).

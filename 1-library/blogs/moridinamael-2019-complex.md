---
id: moridinamael-2019-complex
type: blog
title: "Complex Behavior from Simple (Sub)Agents"
authors: ["moridinamael"]
year: 2019
url: https://www.lesswrong.com/posts/3pKXC62C98EgCeZc4/complex-behavior-from-simple-sub-agents
site: LessWrong
topics: [fork-merge-security, collective-decision, collective-motion]
added_by: shadow/sol-w4
accessed: 2026-10-03
read_depth: skim
relevance: 1
---

## Summary

Curated 2019 post (114 points, 14 comments) with a toy Python simulation (github.com/moridinamael/subagents, not run by us) of a non-learning agent on a 2D plane whose only motivation comes from attached goal-like sub-agents, each wanting to reach or avoid a point and each re-arming at its own rate after satisfaction. Every step the agent samples ten unit moves and takes the one with the highest valence reported by any single sub-agent, winner-take-all. The post walks through emergent trajectories: stable circuits between three goals; an "ugh field" where a strong aversion permanently blocks a goal until an intermediate goal routes around it; a pinned low-valence "smartphone" sub-agent that makes the path distracted and zigzagging; a movement preference that produces chaotic exploration; sociable agents that orbit each other; and the finding that adding one strong new goal siphons attention from a previously stable set. The design note that matters: summing valences across sub-agents instead of taking the winner makes the agent descend to a local minimum and sit there, so the aggregation rule, not the sub-agents, determines whether behaviour stays alive. Future work sections (belief, bias, goal hierarchies) were not read. Explicitly labelled playful and speculative by the author; the human-behaviour analogies are illustrative.

## Key claims

- Qualitatively rich, path-dependent behaviour emerges from a handful of fixed-preference sub-agents under winner-take-all selection with no learning.
- Aggregation rule is decisive: winner-take-all gives circuits and detours, additive aggregation collapses to a local minimum.
- A persistent weak attractor near the agent (the "smartphone") degrades goal pursuit more than its valence would suggest; introducing a new strong goal destabilises existing ones.

## Evidence quality

Simulation anecdotes with plots, code public on GitHub, no quantitative analysis or parameter sweeps. Author states the epistemic status up front ("seriously but not literally"). Nothing here is a measured result in the sense the lab wants.

## Relevance to us

Low, background. The one transferable point is the aggregation-rule comparison: how sub-agent outputs are merged (max versus sum) changes the composite's dynamics more than any single sub-agent does, which is the fork-merge-security topic's merge-threshold question in miniature, and the "new goal is disruptive" plot is a toy of one injected sub-agent capturing the parent. Pairs with [[wentworth-2019-why]] (unanimity committees) as the two simplest aggregation rules at either extreme.

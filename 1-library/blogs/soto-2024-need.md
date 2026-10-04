---
id: soto-2024-need
type: blog
title: "The need for multi-agent experiments"
authors: ["Martín Soto"]
year: 2024
url: https://www.lesswrong.com/posts/gtLkvS6tDLstBd8uY/the-need-for-multi-agent-experiments-1
site: LessWrong
topics: [llm-agent-swarms, meta]
added_by: shadow/sol-w4
accessed: 2026-10-03
read_depth: skim
relevance: 3
---

## Summary

2024 position post (43 points, 3 comments) arguing that the alignment community should run large-scale experiments on populations of AI agents that approximate society-scale deployment. The a priori case: loss of control runs through two steps, introducing agents with certain properties into certain positions, then the agents interacting; alignment has focused on step one, and the burden is on sceptics to show step two does not matter. The main sceptical reply is a centralised software FOOM; Soto expects a more decentralised "hardware singularity" and argues we should not be near-certain of a singleton. Conditions for the work to matter: no singleton take-off, adequate single-agent alignment, and coordination problems that capable aligned AIs do not solve by default (he gives 65% to that last). Additional arguments: multi-agent work also reduces s-risk from conflict and improves deliberation; multi-agent problems have historical precedent and data; the single/multi-agent boundary is blurry (an LLM scaffold is already a small multi-agent system); and run-up dynamics can shape even an eventual singleton. The opportunity he emphasises is using AIs to scale experiments on dangerous societal dynamics, because emergent effects appear only at scale and purely game-theoretic analysis under-predicts (cites wargaming, agent-based models in virology, role-play prediction studies, and Leibo's Concordia as a prototype codebase). Example experiments: whether commitment credibility or transparency is net positive for fallible language agents; where the helpfulness-harmlessness trade-off should sit under different bad-actor assumptions; which single-agent changes most improve social welfare when applied to all agents versus a minority. Main tractability worry is generalisation from short, simple lab runs to the real trajectory. The remainder (neglectedness, further tractability discussion) was not read.

## Key claims

- Interaction dynamics (step two) are a neglected, independent lever on multi-agent AI risk.
- Scaled experiments on populations of actual AI agents can surface emergent dynamics that theory misses and let us test the agents we worry about directly.
- Generalisation from lab-scale multi-agent experiments to deployment is the central open methodological problem.

## Evidence quality

Argument and research agenda; no experiments of its own. Cites Critch's multipolar work, Concordia (arXiv 2312.03664), generative agents (arXiv 2304.03442) and a few empirical studies on role-play prediction. The 65% figure is a stated personal credence.

## Relevance to us

This is roughly the methodological charter for what this lab is doing in the llm-agent-swarms track: population-level experiments on real agents to find emergent coordination, with explicit attention to whether findings generalise. The three example experiments are candidate hypotheses once the survey gate is passed. Useful as a framing citation alongside [[critch-2021-what]] (processes over agents) and [[x-policytensor-2096383641064808902]] (measure the collective, not the individual); the Hugging Face and wiki incidents are, in his terms, uncontrolled versions of exactly the experiments he asked for ([[metr-2026-brief]], [[elasky-2026-encoded]]).

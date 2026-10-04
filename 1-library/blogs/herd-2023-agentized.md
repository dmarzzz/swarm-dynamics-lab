---
id: herd-2023-agentized
type: blog
title: "Agentized LLMs will change the alignment landscape"
authors: ["Seth Herd"]
year: 2023
url: https://www.lesswrong.com/posts/dcoxvEhAfYcov2LA6/agentized-llms-will-change-the-alignment-landscape
site: LessWrong
topics: [llm-agent-swarms, swarm-detection]
added_by: shadow/sol-w4
accessed: 2026-10-03
read_depth: full
relevance: 2
---

## Summary

April 2023 post (162 points, 102 comments), written days after Auto-GPT and BabyAGI appeared, as a ten-point list of predictions. The predictions: LLM-in-a-loop systems (goal decomposition, subtask prioritisation, progress checks) will substantially raise the effective intelligence of the core model by adding executive function, recursive thought and episodic task memory; this was easier than expected (BabyAGI in about three days, with GPT-4 writing the code); tool use (HuggingGPT, about 40 examples) and self-improvement loops (Reflexion) plug in easily; within a year the internet will be full of LLM bots thinking and acting; ChaosGPT (an Auto-GPT told to destroy humanity) is a visceral preview; watching agents think will shift public opinion; the world will be multilateral, with anyone able to spawn a "dumb AGI" and defence harder than offence, so indefinite defence against out-of-control agents is untenable; and yet interpretability and parts of alignment may be easier because these systems take goals in English and think in English, while outer alignment, alignment stability under recursive subgoals, and inner alignment under continued training remain unsolved. He closes by predicting the need for very strong global monitoring, "including breaking all encryption," to prevent hostile agent behaviour. Explicitly a rapid-reaction post ("head spinning"), not analysis.

## Key claims

- Agentic scaffolds would quickly produce a world of many autonomous LLM agents acting on the internet (prediction made April 2023).
- Multilateral deployment plus offence-defence asymmetry makes agent-level defence insufficient and pushes toward population-level monitoring.
- English-language reasoning traces are a major interpretability affordance for agents.

## Evidence quality

Opinion and forecast with no data; the value is historical. Several predictions (an internet of acting LLM agents, public reaction to visible agent reasoning, pressure toward broad monitoring) are now checkable against 2026 events, and the chain-of-thought interpretability claim has been partially undercut by later reports that CoT monitorability is degrading ([[brown-2026-agent]]).

## Relevance to us

Early statement of the premise behind swarm-detection: once agents are cheap and multilateral, the defensive problem becomes monitoring the population rather than aligning each system. Useful as a dated prior to compare against what actually happened in the Hugging Face and wiki incidents ([[metr-2026-brief]], [[collusion-wiki-2026-discovery]]). Herd's follow-up with more structure is the next item in this batch, [[herd-2023-capabilities]].

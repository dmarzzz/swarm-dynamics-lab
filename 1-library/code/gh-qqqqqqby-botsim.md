---
id: gh-qqqqqqby-botsim
type: code
title: "BotSim: LLM-powered malicious social botnet simulation on Reddit-like data, with the BotSim-24 detection dataset"
repo: QQQQQQBY/BotSim
url: https://github.com/QQQQQQBY/BotSim
authors: ["Boyu Qiao", "Kun Li", "Wei Zhou", "Shilong Li", "Qianqian Lu", "Songlin Hu"]
year: 2024
language: "Python"
license: "none stated"
stars: 23
last_commit: 2025-03-20
topics: [swarm-detection, llm-agent-swarms, sybil-resistance]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: skim
relevance: 4
papers: [qiao-2025-botsim]
---

## Summary

Simulates: LLM-driven bot accounts (GPT-4o-mini) posting, commenting, reposting and liking among replayed real Reddit users across six news subreddits, with a recommendation-ranked feed and per-bot timelines. Interaction model: timeline replay of human data plus an LLM agent decision centre (goal tasks, persona, background knowledge, memory). Scale: 1,000 bots and 1,907 humans in BotSim-24 [[qiao-2025-botsim]]. LLM-driven: yes. Adversarial hooks: native; the bots are the adversary, with metadata, text and interaction disguise strategies. Weight: Python plus OpenAI API keys; the README says the general BotSim code was partly lost and is incomplete, and only the RedditBotSim folder is stable.

## What it can do for us

A labelled LLM-botnet dataset and generator for testing swarm detectors, and a cautionary example: because replayed humans never reply to bots, detectors can exploit the missing human-to-bot edges (see [[qiao-2025-botsim]]).

## Run notes

Not run. Stars, licence and last commit from the GitHub API on 2026-10-03; README read via the API.

## Limitations

Incomplete code by the authors' own statement; no licence; humans are replayed, not reactive. Compare [[gh-camel-ai-oasis]] for a fully simulated population.

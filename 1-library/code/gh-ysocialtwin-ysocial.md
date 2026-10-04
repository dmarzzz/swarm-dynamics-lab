---
id: gh-ysocialtwin-ysocial
type: code
title: "Y Social: zero-code LLM-powered social media digital twin (microblog/forum) with recommender choices, Ollama/vLLM agents and an embedded analysis notebook"
repo: YSocialTwin/YSocial
url: https://github.com/YSocialTwin/YSocial
authors: ["Giulio Rossetti", "Massimo Stella", "Rémy Cazabet", "Katherine Abramski", "Erica Cau", "Salvatore Citraro", "Andrea Failla", "Riccardo Improta", "Virginia Morini", "Valentina Pansanella"]
year: 2024
language: JavaScript
license: "GPL-3.0"
stars: 33
last_commit: 2026-10-03
topics: [llm-agent-swarms, swarm-detection, sybil-resistance]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: skim
relevance: 4
papers: [rossetti-2024-y]
---

## Summary

Simulation model: a shared social feed (posts, comments, shares, likes, hashtags, mentions) served by a REST server (YServer) to LLM agent clients (YClient); feed ranking is a pluggable recommender (reverse-chronological, popularity, followers, comment count, common interests, common interactions); agents have demographics, political leaning, toxicity level, interests, activity profiles and engagement distributions (Poisson, geometric, Zipf). Humans can log in and post alongside agents. Scale: not stated in the README. LLM-native: yes, local Ollama or vLLM. Adversarial hooks: per-agent toxicity and leaning parameters and hybrid human-agent accounts; no explicit sybil module, but agent populations are fully configurable, so coordinated account groups can be injected. Weight: web app (Flask/JS) plus local LLM server; annotation via VADER, Perspective API and Autogen.

## What it can do for us

Closest open, actively maintained substrate for 'detect a coordinated LLM swarm inside a social feed': we control the recommender, can inject a block of coordinated accounts, and can export the interaction graph to the embedded Jupyter/ySights tooling. Runs on local models, so cost is hardware rather than API.

## Run notes

Not run. Stars, licence and last push from the GitHub API on 2026-10-03; README read via the API. I did not read the source code. Three repos: YSocial (web app, 33 stars), YServer (REST API, 12 stars) and YClient (agent client, 11 stars), all GPL-3.0.

## Limitations

GPL-3.0 (copyleft for anything we distribute). Small user base. Scale limits are undocumented. Validation of agent realism is limited (see [[larooij-2025-do]]).

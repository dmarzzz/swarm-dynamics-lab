---
id: gh-microsoft-autogen
type: code
title: "AutoGen: multi-agent conversation framework (group chat, event-driven agent runtime), now in maintenance mode"
repo: microsoft/autogen
url: https://github.com/microsoft/autogen
authors: ["Microsoft"]
year: 2023
language: Python
license: "CC-BY-4.0"
stars: 61250
last_commit: 2026-04-06
topics: [llm-agent-swarms]
added_by: shadow/sol-1
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: [wu-2023-autogen]
---

## Summary

Coordination model: multi-agent conversation. AgentChat offers group-chat patterns (round robin, selector, swarm-style handoff) over an event-driven, actor-like core runtime (autogen-core) that can be distributed. README now carries a maintenance-mode notice: no new features, community managed, with Microsoft Agent Framework as the successor. Licence shows CC-BY-4.0 at the repo level (code is MIT per the repo's LICENSE-CODE; the API reports the docs licence). Paper: AutoGen (Wu et al. 2023), already in the library as [[wu-2023-autogen]].

## What it can do for us

The group-chat abstraction is the most natural off-the-shelf way to put N LLM agents in a shared channel and log who says what. autogen-core's distributed runtime could scale to tens of agents. Maintenance mode is acceptable for a hackathon.

## Run notes

Not run. Metadata (stars, licence, last commit) taken from the GitHub API on 2026-10-03; README read via the API.

## Limitations

Frozen feature set; last commit 2026-04-06. Group chat is turn-based with a selector, not asynchronous, so timing dynamics are artificial.

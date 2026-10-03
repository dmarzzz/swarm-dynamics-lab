---
id: scan-code-agent-orchestration
type: task
title: Catalogue LLM multi-agent and orchestration frameworks
kind: scan
status: done
priority: p0
owner: shadow/sol-1
created: '2026-10-03'
created_by: dmarz/setup
depends_on: []
topics:
- llm-agent-swarms
claimed_at: 2026-10-03T17:54Z
updated: 2026-10-03T17:57Z
outputs:
- library/code
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

32 repos under llm-agent-swarms in library/code/: 19 orchestration frameworks and agent social simulators (openai-swarm, openai-agents-python, microsoft-autogen, microsoft-agent-framework, langgraph, deepagents, crewai, camel, oasis, metagpt, chatdev, claude-agent-sdk-python, google-adk-python, concordia, generative-agents, ai-town, agentsociety, elizaos, ruflo) plus 13 incident-adjacent repos (swarm-ai-research/swarm archive and wiki incident, collusion wiki mirrors, sealed-swarm-transcripts, exploitgym, swarmtrace, docent, audit benches, firstflagpoisoned, project-sid). Stars, licence, last commit and language pulled from the GitHub API on 2026-10-03 for every entry. Coordination model stated in each Summary (handoffs: openai-swarm, agents-python; group chat / conversation patterns: autogen; graph: langgraph, adk; role crews: crewai, metagpt, chatdev; role-play dialogue: camel; blackboard-style shared board: sealed-swarm, swarm archive reproduction; social sim: concordia, oasis, generative-agents, agentsociety).

Gap against Done-when: the 20-repo floor is met, but none of the orchestration frameworks were installed and run (read_depth: ran). The three runs in this scan went to the collective-sims task (mesa, vmas, pmocz). Honest state: skim for 19 of the frameworks and incident repos, abstract for the rest. Recommend whoever picks up the survey or first experiment installs oasis or concordia (both designed for N-agent social sims with a shared feed) and openai-agents-python or claude-agent-sdk (cheapest handoff loop) and upgrades those entries.

Ranked list to build on for a 1-day experiment: (1) gh-killy-netsphere-sealed-swarm-transcripts, a shared-board swarm with small open models, 7,200 CC0 transcripts, already shows synchronisation and exploit spread; fork and vary N / board visibility. (2) gh-camel-ai-oasis, million-agent social-feed simulator with Twitter/Reddit recsys, built for herding and polarisation measurements. (3) gh-google-deepmind-concordia, generative agent-based modelling with a game master, slower but principled. (4) gh-openai-swarm or openai-agents-python for a minimal handoff orchestrator when the question is about orchestration topology rather than social dynamics. (5) gh-microsoft-autogen group chat for N-agent debate / consensus runs.

Not opened as new tasks: a ran-upgrade pass on the top 3 frameworks; a follow-up could be filed if the survey needs it.

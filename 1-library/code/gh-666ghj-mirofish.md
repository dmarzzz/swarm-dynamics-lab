---
id: gh-666ghj-mirofish
type: code
title: "MiroFish: 'swarm intelligence' prediction engine that seeds an OASIS social simulation from documents and reports on it (75k stars)"
repo: 666ghj/MiroFish
url: https://github.com/666ghj/MiroFish
authors: ["666ghj"]
year: 2025
language: Python
license: "AGPL-3.0"
stars: 75684
last_commit: 2026-10-01
topics: [llm-agent-swarms]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 4
papers: []
---

## Summary

Pipeline: (1) extract seeds from uploaded material (news, policy drafts, financial signals, novels) and build a GraphRAG memory; (2) extract entities and relations, generate personas and configure agents; (3) run a 'dual-platform parallel simulation' with dynamic temporal memory (Zep Cloud); (4) a ReportAgent writes a prediction report; (5) users can chat with any simulated agent. The README credits OASIS ([[gh-camel-ai-oasis]]) as the simulation engine. Weight: Python 3.11-3.12 with uv, Node 18 frontend, LLM API and Zep API keys. Popular forks: nikmcfly/MiroFish-Offline (2.6k stars, offline/English), tt-a1i/MiroFish-local (Graphiti+Neo4j instead of Zep), SCTY-Inc/mirofish-cli; none catalogued.

## What it can do for us

Shows the product wrapper people actually adopt around OASIS (document-to-population seeding, report agent); the seeding pipeline is the reusable part. Its predictive validity is unestablished.

## Run notes

Not run. Stars, licence and last push from the GitHub API on 2026-10-03; README read via the API; source code not read.

## Limitations

AGPL; depends on paid Zep Cloud memory by default; 'predicting anything' is a marketing claim with no published validation found; prediction from LLM social sims faces the validation problems in [[larooij-2025-do]].

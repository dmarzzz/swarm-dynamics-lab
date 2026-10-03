---
id: gh-googlecloudplatform-race-condition
type: code
title: "Race Condition: Google Cloud Next '26 multi-agent marathon simulation (ADK + Gemini) with deterministic autopilot runners and NDJSON replay"
repo: GoogleCloudPlatform/race-condition
url: https://github.com/GoogleCloudPlatform/race-condition
authors: ["Google Cloud"]
year: 2026
language: Python/Go
license: "unspecified (GitHub NOASSERTION)"
stars: 234
last_commit: 2026-10-02
topics: [llm-agent-swarms]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 3
papers: []
---

## Summary

Simulation: agents plan a Las Vegas marathon route, simulate environment (weather, traffic, crowds) and run hundreds of runner agents. Reference patterns called out in README: cached vs live replay of recorded NDJSON agent streams; a deterministic 'runner_autopilot' that makes the same shape of decisions with zero API calls, for load testing; a planner ladder (plain, with eval gating, with AlloyDB memory); a Go hub routing WebSocket traffic to Python ADK agents over A2A with batching to avoid thundering herds when hundreds broadcast on one tick. Weight: GCP services (GKE, AlloyDB, Memorystore) for full deploy.

## What it can do for us

Two patterns to copy: a zero-cost deterministic stand-in for LLM agents (measure the simulator separately from the model) and record/replay of agent streams.

## Run notes

Not run. Stars, licence and last push from the GitHub API on 2026-10-03; README read via the API; source code not read.

## Limitations

Cloud-heavy; demo rather than research tool; licence unclear.

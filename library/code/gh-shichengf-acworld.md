---
id: gh-shichengf-acworld
type: code
title: "ACWorld: Agentic Commerce World, protocol-validated buyer/merchant market environment and benchmark"
repo: shichengf/ACWorld
url: https://github.com/shichengf/ACWorld
authors: ["Shicheng Fan", "et al."]
year: 2026
language: Python
license: "MIT"
stars: 6
last_commit: 2026-10-03
topics: [llm-agent-swarms]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 3
papers: [fan-2026-agentic]
---

## Summary

Simulation model: many-to-many market of Buyer and Merchant agents acting through the Vibe Commerce Protocol; a platform validates each action and the World records authorised transaction effects. Scale: 200 capability tasks plus 60 large-catalog tasks over 785,022 listings. LLM-native: yes. Adversarial hooks: none explicit; policy-refusal cases scored in v1.1.0. Weight: Python; Harbor adapter for hidden evaluation on 20 private configurations.

## What it can do for us

Validated-action market substrate with deterministic oracles; useful pattern for auditable agent markets.

## Run notes

Not run. Stars, licence and last push from the GitHub API on 2026-10-03; README read via the API; source code not read.

## Limitations

Benchmark-style tasks, not open-ended population dynamics; v1.1.0 scores are not comparable to the paper (v1.0.0).

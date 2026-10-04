---
id: gh-baselomari-ma-craftax
type: code
title: "Multi-Agent Craftax: Craftax-MA and Craftax-Coop open-ended survival/crafting MARL environments in JAX (JaxMARL API)"
repo: BaselOmari/MA-Craftax
url: https://github.com/BaselOmari/MA-Craftax
authors: ["Bassel Al Omari", "Michael Matthews", "Alexander Rutherford", "Jakob N. Foerster"]
year: 2025
language: Python (JAX)
license: "MIT"
stars: 18
last_commit: 2025-08-31
topics: [marl-emergence]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: [al-omari-2025-multi]
---

## Summary

Simulates the open-ended Crafter/NetHack-style survival and crafting world of Craftax (gather, craft tools, fight, descend floors) with several agents sharing a world: Craftax-MA keeps the original mechanics, while Craftax-Coop adds heterogeneous agent roles, trading and mechanics that require cooperation. Interaction is simultaneous via the JaxMARL interface (`make_craftax_env_from_name("Craftax-Coop-Symbolic")`), with symbolic observations. The paper reports a 250-million-interaction training run in under an hour on hardware accelerators [[al-omari-2025-multi]]; not measured here. RL-only, though the symbolic observation is decodable to text. Agent count is a config value; no join/leave. Moderate install (JAX; baselines for IPPO, MAPPO, PQN included).

## What it can do for us

Long-horizon, open-ended multi-agent world in JAX that composes with [[gh-bold-lab-ai-jaxmarl]] tooling; trading in Craftax-Coop gives an exchange channel to abuse.

## Run notes

Not run. README read via GitHub API on 2026-10-03.

## Limitations

New, 18 stars, last push August 2025. Separate from the related "Multi-Agent Craftax (MAC)" environment of Ye, Tao and Jaques (arXiv 2508.15679), which shares the name; not catalogued.

## Notes from dmarz/factory-scan

For the planned swarm-factory environment (Factorio-like production feeding Cournot markets): A GPU-fast multi-agent crafting world with built-in trade requests, usable as an RL baseline substrate or as a template for adding a priced market on top of crafting.

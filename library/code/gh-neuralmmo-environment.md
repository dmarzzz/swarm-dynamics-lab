---
id: gh-neuralmmo-environment
type: code
title: "Neural MMO 2: massively multi-agent survival/combat/trade MMO world for RL, 128+ agents per world, PettingZoo API"
repo: NeuralMMO/environment
url: https://github.com/NeuralMMO/environment
authors: ["Joseph Suarez", "Neural MMO contributors (CarperAI, Parametrix.AI)"]
year: 2019
language: Python
license: "MIT"
stars: 578
last_commit: 2024-08-30
topics: [marl-emergence]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: ran
relevance: 4
papers: [suarez-2023-neural]
---

## Summary

Simulates a procedurally generated MMO-style tile world (default 160x160 map, 1024-tick horizon) where 128 agents (configurable; PLAYER_N=512 ran fine) forage food and water, fight each other and NPCs with three combat styles, level eight professions, and trade items on a global market; interaction is simultaneous-move through a PettingZoo ParallelEnv with structured dict observations (Tile, Entity, Inventory, Market, Communication) and a dict action space (Move, Attack, Use, Give, GiveGold, Buy, Sell, Comm, Destroy). Measured here at about 6,100-6,400 random-action agent-steps/s in one Python process on an M1 Max CPU. RL-first, but the step API is plain Python with structured, nameable observations, so an LLM policy can be dropped in per agent (slowly). Population is a config knob, agents die and are removed (closed population per episode, no respawn into an open population by default), and the 2.0 task system lets one agent be rewarded on another agent's state, which is a direct hook for adversarial or colluding agents. Lightweight: pip install, no GPU. The GitHub repo is effectively frozen since August 2024; development moved to the C rewrite "nmmo3" inside [[gh-pufferai-pufferlib]].

## What it can do for us

The richest open many-agent social world that runs on a laptop CPU: resources, combat, gifting (Give/GiveGold) and a market give natural channels for collusion, Sybil-style coordinated accounts and resource funnelling. Because `PLAYER_N` is a config value and the task API can assign one agent's reward to another agent's outcome (`create_task(assignee=...)`), we can inject a coordinated sub-population (e.g. 16 agents run by one controller that funnel gold to one "principal") and test whether detectors on trade and movement traces spot them.

## Run notes

Ran on 2026-10-03, M1 Max, Python 3.10 via uv.

```
uv venv -p 3.10 .venv && uv pip install -p .venv/bin/python nmmo   # 13 s, installs nmmo 2.1.2
```

Script (scratchpad `run_nmmo.py`): `env = nmmo.Env(Default()); obs,_ = env.reset(seed=1)`; then loop `env.step({a: env.action_space(a).sample() for a in env.agents})` for 60 s.

- Default config: PLAYER_N 128, MAP_SIZE 160, HORIZON 1024. Reset 0.09 s.
- Random actions: all 128 agents dead after 272 ticks; 8,414 agent-steps in that run, 197 env-steps/s, 6,105 agent-steps/s.
- Second run, 150 ticks: N=128 gave 6,243 agent-steps/s (123 env-steps/s, 12 alive at end); N=512 gave 6,409 agent-steps/s (43 env-steps/s, 14 alive at end). Throughput per agent stays flat as N grows.
- Passing an empty action dict (`env.step({})`) killed all agents by tick 25 in both N=128 and N=512; cause not investigated (likely starvation or combat with no movement). Treat no-op as non-trivial.
- The paper reports about 3,000 agent-steps per CPU core per second with mortality removed [[suarez-2023-neural]]; our higher figure includes cheap dead/dying agents and is not a like-for-like comparison.

## Limitations

Repo last pushed August 2024; the active successor is nmmo3 (C, inside PufferLib), which has a different API. Random agents die fast, so meaningful long-horizon runs need a trained or scripted policy. Observations are large structured tensors (about 10 KB per agent-step per the paper), so feeding them to an LLM needs a text summariser. No built-in respawn of new identities mid-episode.

## Notes from dmarz/sim-envs

2026-10-03: Meta MMO ([[choe-2024-massively]], code [[gh-kywch-meta-mmo]]) packages five short many-agent minigames on Neural MMO 2 for generalist-policy training with Elo evaluation; unmaintained since 2024-08.

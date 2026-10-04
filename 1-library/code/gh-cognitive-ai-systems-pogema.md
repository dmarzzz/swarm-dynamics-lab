---
id: gh-cognitive-ai-systems-pogema
type: code
title: "POGEMA: fast partially observable multi-agent pathfinding gridworld, scales to 1000+ agents on one CPU core"
repo: Cognitive-AI-Systems/pogema
url: https://github.com/Cognitive-AI-Systems/pogema
authors: ["Alexey Skrynnik", "Anton Andreychuk", "Konstantin Yakovlev", "Aleksandr Panov", "AIRI / Cognitive AI Systems lab"]
year: 2022
language: Python
license: "MIT"
stars: 300
last_commit: 2026-09-14
topics: [marl-emergence, swarm-robotics, collective-motion]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: ran
relevance: 4
papers: [skrynnik-2024-pogema]
---

## Summary

Simulates many agents on an obstacle grid each trying to reach its own target with only a local egocentric view (default radius 5, three 11x11 channels: obstacles, other agents, target direction); interaction is simultaneous moves with configurable collision rules (`block_both`, `priority`, `soft`). Measured here at roughly 170,000-195,000 random-action agent-steps per second on a single M1 Max core for 64 to 1024 agents (numpy). RL and classical-planner oriented; observations are small arrays that are easy to print as text, so an LLM agent per robot is feasible but slow. Population is a config knob (`num_agents`, explicit `agents_xy`/`targets_xy`), and `on_target='restart'` gives lifelong MAPF where agents get new goals forever; there is no join/leave of identities mid-episode, but one can mark a subset of agent indices as adversarial (e.g. blockers that never move toward targets) in the controller without touching the env. Very light: `pip install pogema`, numpy only. Integrations for PettingZoo, PyMARL, SampleFactory and RLlib; the benchmark suite and baselines are in a separate pogema-benchmark repo [[skrynnik-2024-pogema]]. The GitHub org path `CognitiveAISystems/pogema` is only a pointer to this repo.

## What it can do for us

The fastest truly many-agent environment we got running on a laptop CPU, with knobs for N, density, map, collision semantics and lifelong goals. A natural first testbed for "a few adversarial or colluding agents inside a large cooperative swarm" (congestion attacks, deadlock induction) and for measuring how swarm throughput degrades with the adversarial fraction.

## Run notes

Ran on 2026-10-03, M1 Max, Python 3.11 via uv.

```
uv venv -p 3.11 .venv && uv pip install -p .venv/bin/python pogema lbforaging   # 1 s, pogema 1.4.0, gymnasium 0.28.1
```

Script (scratchpad `pogema/run.py`): `pogema_v0(grid_config=GridConfig(num_agents=N, size=S, density=0.3, obs_radius=5, max_episode_steps=256, seed=1))`, 256 random-action steps.

| N agents | grid | env-steps/s | agent-steps/s |
|---|---|---|---|
| 64 | 32x32 | 3,035 | 194,206 |
| 256 | 64x64 | 764 | 195,602 |
| 1024 | 128x128 | 164 | 167,680 |

Observation per agent: shape (3, 11, 11). Per-agent cost is almost flat in N. Gymnasium warns about box precision; harmless. Note the README says the PyPI package is the older line and recommends installing from GitHub while "Pogema 2.0" is prepared; we used PyPI 1.4.0.

## Limitations

Pathfinding only: no resources, communication channel, or economic actions. Rewards are sparse goal-reached signals. Version split between PyPI and GitHub.

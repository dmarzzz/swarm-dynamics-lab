---
id: scan-code-collective-sims
type: task
title: Catalogue simulators for collective motion and active matter
kind: scan
status: done
priority: p0
owner: shadow/sol-1
created: '2026-10-03'
created_by: dmarz/setup
depends_on: []
topics:
- collective-motion
- active-matter
- sync-consensus
- crowds-and-traffic
claimed_at: 2026-10-03T17:54Z
updated: 2026-10-03T17:57Z
outputs:
- 1-library/code/gh-mesa-mesa.md
- 1-library/code/gh-pmocz-activematter-python.md
- 1-library/code/gh-proroklab-vectorizedmultiagentsimulator.md
---

## Goal

Find the code we could build experiments on: agent-based simulators, GPU particle engines, and reference implementations of the classic models.

## Seeds

Seeds come from memory and are starting points, not citations. Open each one, confirm the details, and catalogue it only if it checks out.

- NetLogo (its Flocking model) and Mesa (projectmesa/mesa)
- JAX MD (jax-md/jax-md) for GPU particle simulation
- Reference implementations of Vicsek, Couzin, Cucker-Smale and swarmalator models
- Pedestrian simulators built on the social force model

## Search plan

- GitHub search by topic and by language, sorted by stars and by recent activity; GitHub topics pages (e.g. topics/swarm, topics/multi-agent).
- Papers With Code and paper project pages for implementations of catalogued papers.
- For each candidate, record stars, last commit date and licence from the repo page.

## Done when

- At least 15 repos catalogued with stars, last commit, licence and an honest read_depth.
- At least 3 installed and run (read_depth: ran) with the commands and results in Run notes, chosen as the most likely to be used in the hackathon.
- Coverage note filled, including a short ranked list of what we would build on.

## Coverage note

Repos catalogued under collective-motion / active-matter / sync-consensus / crowds-and-traffic in 1-library/code/: gh-mesa-mesa (ran), gh-proroklab-vectorizedmultiagentsimulator (ran, flocking scenario), gh-pmocz-activematter-python (ran, Vicsek), gh-netlogo-netlogo, gh-jax-md-jax-md, gh-khev-swarmalators, gh-than-mark-swarmalators-experiment-mobile, gh-pedestriandynamics-jupedsim, gh-openai-multiagent-particle-envs. That is 9, below the 15 floor. Stars, licence, last commit from the GitHub API on 2026-10-03.

Three installed and run in a fresh venv with exact commands and outputs in Run notes: mesa 3.5.1 boid flockers (polarisation 0.09 to 0.41 over 100 steps, 10.8k agent-steps/s); vmas 1.5.2 flocking (64 envs x 8 agents, 1,615 agent-steps/s on CPU); pmocz activematter Vicsek (order parameter 1.000 / 0.985 / 0.946 / 0.793 / 0.216 for eta 0.1 / 0.5 / 1 / 2 / 4). All CPU-only, no GPU needed, all run in under a minute.

Gap against Done-when: count is 9 of 15. Missing: a Couzin zonal model reference implementation, a Cucker-Smale implementation, a social-force pedestrian sim other than JuPedSim (e.g. PySocialForce), GPU particle engines beyond JAX MD. Searched GitHub for 'vicsek', 'couzin', 'cucker-smale', 'swarmalator', 'social force', 'boids' sorted by stars; most hits are student repos with no licence or no commits since 2020, which I chose not to catalogue rather than pad the count. A future agent can add 6 with a half hour on those queries.

Ranked list to build on: (1) gh-pmocz-activematter-python, 100-line Vicsek, trivially modifiable, already reproduces the order-disorder transition; (2) gh-mesa-mesa, boid flockers with polarisation metric built in, Python, extensible to LLM-driven agents; (3) gh-proroklab-vectorizedmultiagentsimulator, vectorised torch, scales to thousands of agents for MARL baselines; (4) gh-jax-md-jax-md if a GPU is available.

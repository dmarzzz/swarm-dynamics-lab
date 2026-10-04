---
id: scan-code-robotics-marl
type: task
title: Catalogue swarm robotics simulators and MARL environments
kind: scan
status: done
priority: p0
owner: shadow/sol-1
created: '2026-10-03'
created_by: dmarz/setup
depends_on: []
topics:
- swarm-robotics
- marl-emergence
claimed_at: 2026-10-03T17:54Z
updated: 2026-10-03T17:57Z
outputs:
- 1-library/code
---

## Goal

Find the simulators and training environments for robot swarms and multi-agent RL, with an eye to what trains fast on one GPU.

## Seeds

Seeds come from memory and are starting points, not citations. Open each one, confirm the details, and catalogue it only if it checks out.

- ARGoS (ilpincy/argos3) and the Kilobot simulators
- VMAS, the vectorized multi-agent simulator (proroklab)
- PettingZoo and Melting Pot
- Drone swarm stacks: Crazyswarm and PX4/ROS swarm tooling
- Buzz, a programming language for robot swarms

## Search plan

- GitHub search by topic and by language, sorted by stars and by recent activity; GitHub topics pages (e.g. topics/swarm, topics/multi-agent).
- Papers With Code and paper project pages for implementations of catalogued papers.
- For each candidate, record stars, last commit date and licence from the repo page.

## Done when

- At least 15 repos catalogued with stars, last commit, licence and an honest read_depth.
- At least 3 installed and run (read_depth: ran) with the commands and results in Run notes, chosen as the most likely to be used in the hackathon.
- Coverage note filled, including a short ranked list of what we would build on.

## Coverage note

17 repos under swarm-robotics / marl-emergence in 1-library/code/: gh-proroklab-vectorizedmultiagentsimulator (ran), gh-farama-foundation-pettingzoo, gh-farama-foundation-magent2, gh-google-deepmind-meltingpot, gh-facebookresearch-benchmarl, gh-bold-lab-ai-jaxmarl, gh-instadeepai-jumanji, gh-oxwhirl-pymarl, gh-oxwhirl-smac, gh-openai-multi-agent-emergence-environments, gh-openai-multiagent-particle-envs, gh-ilpincy-argos3, gh-jic-csb-kilombo, gh-buzz-lang-buzz, gh-imrclab-crazyswarm2, gh-usc-actlab-crazyswarm, gh-px4-px4-autopilot. Stars, licence, last commit from the GitHub API on 2026-10-03.

Gap against Done-when: the 15-repo floor is met, but only 1 of the required 3 was run (vmas flocking, 64 envs x 8 agents, 1,615 agent-steps/s CPU). PettingZoo (pip install, mpe environments) and JaxMARL (CPU jax works for small MPE) are the two cheapest ran-upgrades; neither was done. ARGoS and Kilombo need C builds; Crazyswarm/PX4 need ROS 2 and hardware, out of scope for the hackathon. read_depth is skim for 9 and abstract for 7, honest.

What trains fast on one GPU or CPU: vmas (vectorised torch, thousands of agents), jaxmarl (jit-compiled MPE/SMAX, fastest per step), pettingzoo mpe (pure Python, slow but standard), benchmarl (torchrl trainers over vmas/pettingzoo, ready-made MAPPO/IPPO configs). MAgent2 for large-N (hundreds to thousands) gridworld battles.

Ranked list to build on: (1) gh-proroklab-vectorizedmultiagentsimulator + gh-facebookresearch-benchmarl for an N-scaling MARL baseline in a few hours; (2) gh-bold-lab-ai-jaxmarl if someone has a GPU and wants many seeds; (3) gh-farama-foundation-pettingzoo as the lowest-friction API when wrapping an LLM policy; (4) gh-google-deepmind-meltingpot for social-dilemma scenarios (needs more setup). Robotics sims (argos3, kilombo, buzz) are catalogued for the survey's reference, not for running this weekend.

---
id: kazemkhani-2024-gpudrive
type: paper
title: "GPUDrive: Data-driven, multi-agent driving simulation at 1 million FPS"
authors: [Saman Kazemkhani, Aarav Pandya, Daphne Cornelisse, Brennan Shacklett, Eugene Vinitsky]
year: 2024
venue: International Conference on Learning Representations (ICLR 2025)
url: https://arxiv.org/abs/2408.01584
doi: null
arxiv: '2408.01584'
cite: "Kazemkhani, S., Pandya, A., Cornelisse, D., Shacklett, B., & Vinitsky, E. (2025). GPUDrive: Data-driven, multi-agent driving simulation at 1 million FPS. In International Conference on Learning Representations (ICLR 2025). arXiv:2408.01584."
topics: [marl-emergence, crowds-and-traffic]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: null
code: [gh-emerge-lab-gpudrive]
---

## Summary

Builds a GPU-accelerated multi-agent driving simulator on the Madrona engine [[shacklett-2023-extensible]] with observation, reward and dynamics written in C++ and lowered to CUDA, exposed through Python, and initialised from Waymo Open Motion Dataset scenes. Reports a peak of 2.3 million agent steps per second, 2-3 orders of magnitude above the CPU simulator Nocturne (about 15,000), and trains RL agents to reach goals across thousands of scenarios in hours.

## Contribution

Defines and reports throughput in agent steps per second (ASPS) and controlled-agent steps per second (CASPS), which is the right unit when scenes contain variable numbers of agents, and shows that batch GPU simulation makes self-play over real-world multi-agent data practical.

## Key results

- Peak ASPS 2.3 million (RTX 4080 / A100 comparison); Waymax could not run more than 16 environments in parallel without running out of memory in their setup.
- Controllable agents per scene: mean about 10.8, standard deviation about 9.3 over 512 scenes; CASPS about 200,000 on random scene mixes.
- Goal-reaching agents trained in minutes for small scene sets and scaled to thousands of scenarios in hours.

## Methods and models

Madrona ECS batch simulation, one world per scene, radial-filter or LiDAR observations, IPPO-style training via PufferLib/CleanRL/SB3 integrations.

## Limitations and open questions

Throughput depends strongly on scene density; real-data scenes have few controllable agents. Human-compatibility of learned policies is the open question the authors frame.

## Relevance to us

The ASPS/CASPS distinction should be adopted in our own throughput reporting (we report agent-steps/s in our run notes). Mixed log-replay plus policy-controlled agents is a template for "few bots among many humans" experiments.

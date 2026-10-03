---
id: schuck-2025-swarmgpt
type: paper
title: "SwarmGPT: Combining Large Language Models With Safe Motion Planning for Drone Swarm Choreography"
authors: ["Martin Schuck", "Dinushka Orrin Dahanaggamaarachchi", "Ben Sprenger", "Vedant Vyas", "Siqi Zhou", "Angela P. Schoellig"]
year: 2025
venue: "IEEE Robotics and Automation Letters"
url: https://arxiv.org/abs/2412.08428
doi: "10.1109/lra.2025.3619745"
arxiv: "2412.08428"
cite: "Schuck, M., Dahanaggamaarachchi, D. O., Sprenger, B., Vyas, V., Zhou, S., & Schoellig, A. P. (2025). SwarmGPT: Combining Large Language Models With Safe Motion Planning for Drone Swarm Choreography. IEEE Robotics and Automation Letters, 10(11), 12237-12244."
topics: [swarm-robotics, llm-agent-swarms]
added_by: dmarz/swarm-robotics-recent
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "7 (OpenAlex W4415002936, 2026-10-03); 10 (Crossref, 2026-10-03); 20 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

SwarmGPT uses an LLM as a choreographer for drone-swarm performances set to music. Non-experts refine choreographies in natural language, and a safety filter makes minimal corrections whenever safety or feasibility constraints (collisions, actuator limits) are violated, decoupling high-level design from low-level motion planning. Validated in simulation with up to 200 drones and in real-world experiments with up to 20 drones across diverse songs.

## Contribution

An early, peer-reviewed example of the 'LLM proposes, verified planner disposes' pattern for robot swarms. It is centralised, unlike the per-robot LLM agents of [[strobel-2024-llm2swarm]].

## Key results

- Safe, synchronised choreographies in simulation with up to 200 drones and in real flights with up to 20 drones (per the abstract).

## Methods and models

LLM prompt-to-waypoint generation, a safety filter via constrained motion planning, real drone deployment (per the abstract).

## Limitations and open questions

Abstract-depth entry. Choreography is open-loop and centrally planned, so there is no emergent collective dynamics. The LLM's role is design, not control.

## Relevance to us

A reference point for LLM-plus-swarm work at the hackathon. Contrast with decentralised LLM controllers in [[strobel-2024-llm2swarm]] and [[ji-2026-genswarm]], and with the critique in [[rahman-2025-llm-powered]].

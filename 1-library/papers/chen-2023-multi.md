---
id: chen-2023-multi
type: paper
title: "Multi-Agent Consensus Seeking via Large Language Models"
authors:
- "Huaben Chen"
- "Wenkang Ji"
- "Lufeng Xu"
- "Shiyu Zhao"
year: 2023
venue: "arXiv preprint"
url: https://arxiv.org/abs/2310.20151
doi: null
arxiv: "2310.20151"
cite: "Chen, H., Ji, W., Xu, L., & Zhao, S. (2023). Multi-agent consensus seeking via large language models. arXiv preprint arXiv:2310.20151."
topics:
- llm-agent-swarms
- sync-consensus
- swarm-robotics
added_by: dmarz/llm-agent-swarms-audit
accessed: '2026-10-03'
read_depth: full
relevance: 5
citations: "14 (OpenAlex W4388184526, arXiv record, 2026-10-03); Semantic Scholar 68 same day"
code: []
---

## Summary

The paper asks whether LLM agents, left to choose their own strategy, solve the textbook consensus problem of networked control. Each of n GPT-3.5-turbo agents starts with a random number in [0, 100], sees the states of its neighbours each round, writes a short "Reasoning" and a new "Position", and the group is asked to agree on a common value. Without being told how, agents mostly use the average strategy (set your next state to the mean of the observed states), which is exactly DeGroot / average consensus. Stubborn and suggestible personalities, the number of agents and directed vs undirected topologies then reproduce the qualitative phenomena of consensus theory: leader-follower structure, clustering, oscillation and slower convergence on sparse graphs. The same prompt, with [x] replaced by [x, y], drives a multi-robot aggregation task in the plane.

## Contribution

The first explicit bridge between LLM multi-agent negotiation and the Jadbabaie / Olfati-Saber / Ren-Beard consensus literature, showing that the emergent default update rule of an LLM agent is approximately linear averaging. It sits upstream of the robot-swarm work of the same group ([[ji-2026-genswarm]]) and of the statistical-physics treatments of LLM opinion dynamics ([[de-marzo-2024-ai]], [[el-2026-physics]]).

## Key results

- Strategy: the average strategy dominates (sometimes excluding the agent's own state); minor strategies are "suggestible" (copy a neighbour), "stubborn" (stay put) and erroneous moves from hallucination, which other agents then follow (error propagation). Measured qualitatively from transcripts.
- Final consensus value sits near the mean of the initial states; its variance across runs falls as n grows (n = 2, 4, 6, 8; temperature 0 and 0.7; 2,400 runs in total). Temperature 0 gives tighter consensus than 0.7. Measured (Monte Carlo, Fig. 4; numbers shown only graphically).
- Two suggestible agents can oscillate forever (period-two swapping); ten suggestible agents reach consensus without oscillation, because they follow the local majority. Multiple stubborn agents among 10 produce stable clusters (no consensus). Measured, example runs.
- Topology: fully connected undirected graphs converge fastest; non-complete graphs converge more slowly; directed graphs produce leader-follower consensus where the root agent sets the final value. Measured on 3-agent examples; the generalisation to larger graphs is the authors' belief, not tested.
- Multi-robot aggregation in 2D: LLM planner updates every 2 s, a velocity controller every 0.1 s, all-to-all communication; robots converge to a common point. Demonstration only.

## Methods and models

Single model (GPT-3.5-turbo-0613). States are scalars (or 2D positions for robots). Personalities set by prompt. Topologies: complete, path-like undirected and directed trees on 3 agents; up to 10 agents for personality tests. Comparison point is the ODE model x_i(t+1) = mean of x_j over N_i. Project page and code: https://windylab.github.io/ConsensusLLM/

## Limitations and open questions

One old model, scalar states, tiny topologies (mostly 3 agents), and convergence speeds reported only as example trajectories, so no convergence-rate measurement against the spectral gap. The low planner update rate limits real robot use. Open: does the implied averaging weight matrix match the graph Laplacian prediction, and how does it change with model, N and prompt? That is a cheap, well-posed hackathon measurement.

## Relevance to us

A minimal, reproducible bridge from LLM agents to classical consensus control (topic sync-consensus): fitting the implied update matrix on larger random graphs and comparing convergence time with the algebraic connectivity would be a clean experiment. Compare [[de-marzo-2024-ai]] (binary majority following), [[han-2026-conformity]] (confidence-weighted pooling on topologies), [[li-2025-llm]] and [[strobel-2024-llm2swarm]] (LLMs in robot swarms), and [[chen-2023-scalable]] (centralised vs decentralised multi-robot planning).

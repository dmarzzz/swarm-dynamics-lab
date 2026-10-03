---
id: kolling-2016-human
type: paper
title: "Human Interaction With Robot Swarms: A Survey"
authors: ["Andreas Kolling", "Phillip Walker", "Nilanjan Chakraborty", "Katia Sycara", "Michael Lewis"]
year: 2016
venue: "IEEE Transactions on Human-Machine Systems"
url: https://api.openalex.org/works/doi:10.1109/thms.2015.2480801
doi: "10.1109/thms.2015.2480801"
arxiv: null
cite: "Kolling, A., Walker, P., Chakraborty, N., Sycara, K., & Lewis, M. (2016). Human Interaction With Robot Swarms: A Survey. IEEE Transactions on Human-Machine Systems, 46(1), 9–26."
topics: ["swarm-robotics"]
added_by: dmarz/swarm-robotics-audit
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "424 (OpenAlex, 2026-10-03)"
code: []
---
## Summary

The first survey of human-swarm interaction (HSI). It introduces swarm robotics basics, then looks at HSI
from the operator's side: the cognitive complexity of tasking a swarm, the interface between swarm and
operator (communication, state estimation and visualisation of the swarm), and how humans can control a
swarm. It proposes a taxonomy of control methods and lists open problems. (From the abstract; the full text
was not reachable.)

## Contribution

The standard citation for HSI as a subfield, and the source of the control-method taxonomy that later work
on steering swarms through a few user-driven or "stubborn" agents builds on (see [[dorigo-2021-swarm]],
section III-G).

## Key results

- Taxonomy of human control methods for swarms (details not checked).
- Identifies challenges in communication, state estimation, visualisation and control (from abstract).

## Methods and models

Narrative survey of the literature up to about 2015. No experiments.

## Limitations and open questions

Abstract-level entry. It predates learning-based and LLM-based swarm interfaces ([[strobel-2024-llm2swarm]])
and recent augmented-reality work.

## Relevance to us

Background for any demo where a human steers a swarm (for example by a few informed agents, as in
[[sun-2023-mean]]). It fills the human-swarm interaction gap the scan listed.

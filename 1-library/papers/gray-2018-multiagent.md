---
id: gray-2018-multiagent
type: paper
title: "Multiagent Decision-Making Dynamics Inspired by Honeybees"
authors: ["Rebecca Gray", "Alessio Franci", "Vaibhav Srivastava", "Naomi Ehrich Leonard"]
year: 2018
venue: "IEEE Transactions on Control of Network Systems"
url: "https://arxiv.org/abs/1711.11578"
doi: "10.1109/tcns.2018.2796301"
arxiv: "1711.11578"
cite: "Gray, R., Franci, A., Srivastava, V., & Leonard, N. E. (2018). Multiagent Decision-Making Dynamics Inspired by Honeybees. IEEE Transactions on Control of Network Systems, 5(2), 793–806. https://doi.org/10.1109/tcns.2018.2796301"
topics: ["collective-decision", "sync-consensus", "swarm-robotics"]
added_by: dmarz/collective-decision
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "100 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Designs distributed multiagent network dynamics that reproduce the honeybee value-sensitive decision with a pitchfork bifurcation, proves how the agent-level dynamics recover the swarm's behaviour on networks, and adds an adaptive bifurcation control law that improves decision performance beyond that observed in swarms.

## Contribution

Bridge from the mean-field bee model [[pais-2013-mechanism]] to networked control; precursor of [[bizyaeva-2023-nonlinear]] and [[leonard-2024-fast]].

## Key results

- Agent-based network dynamics recover value-sensitive decisions (analysis).
- Adaptive bifurcation control improves performance (proved and simulated).
- Abstract-level reading only; numbers beyond the abstract were not checked.

## Methods and models

Nonlinear dynamics on graphs; bifurcation and singular perturbation analysis.

## Limitations and open questions

Theory and simulation only.

## Relevance to us

Provides a controller we could deploy directly on networked agents. Related: [[reina-2015-design]].

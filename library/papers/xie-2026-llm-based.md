---
id: xie-2026-llm-based
type: paper
title: LLM-Based Penetration Testing in the Presence of Honeypots
authors:
- Xinhong Xie
- Piyush Nagasubramaniam
- Neeraj Karamchandani
- Sencun Zhu
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2609.08093
doi: null
arxiv: '2609.08093'
cite: 'Xie, X., Nagasubramaniam, P., Karamchandani, N., & Zhu, S. (2026). LLM-Based Penetration Testing in the Presence of Honeypots. arXiv preprint arXiv:2609.08093.'
topics:
- swarm-detection
added_by: dmarz/sd-honeypots
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Studies an LLM attack agent that must spend a finite LLM execution budget across a pool of hosts, some of which are honeypots. The attacker's choice is formalised as a budgeted decision process (continue exploiting or skip a host when honeypot suspicion arises). The authors report that a detector-guided skip policy lets the agent allocate budget efficiently and compromise real hosts in a mixed testbed. Defences are explicitly out of scope.

## Contribution

Frames honeypot avoidance as an economic problem for the agent operator, showing that LLM agents can reason about deception artefacts and route around them, which removes much of the trap's value as a sensor.

## Key results

- A detector-guided budget policy lets LLM attack agents compromise hosts in a mixed honeypot/real pool more efficiently (abstract; no numbers stated there).

## Methods and models

Controlled mixed-host testbed; budgeted decision process; honeypot-suspicion detector feeding the agent. Abstract-level read.

## Limitations and open questions

Abstract only. Testbed composition and the specific honeypots used are not known from the abstract.

## Relevance to us

Another evasion data point, alongside [[cordeiro-2026-rouxii]]: rational swarm operators will price traps into their budget. Detection designs should make "skip" costly or indistinguishable from real targets. Contrast [[reworr-2024-llm]], [[pasquini-2024-hacking]].

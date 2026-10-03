---
id: zhang-2025-exposing
type: paper
title: "Exposing LLM User Privacy via Traffic Fingerprint Analysis: A Study of Privacy Risks in LLM Agent Interactions"
authors: ["Yixiang Zhang", "Xinhao Deng", "Zhongyi Gu", "Yihao Chen", "Ke Xu", "Qi Li", "Jianping Wu"]
year: 2025
venue: "arXiv preprint"
url: https://arxiv.org/abs/2510.07176
doi: null
arxiv: "2510.07176"
cite: "Zhang, Y., Deng, X., Gu, Z., Chen, Y., Xu, K., Li, Q., & Wu, J. (2025). Exposing LLM User Privacy via Traffic Fingerprint Analysis: A Study of Privacy Risks in LLM Agent Interactions. arXiv:2510.07176."
topics: [swarm-detection]
added_by: dmarz/sd-attribution
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

Shows that LLM agents' tool invocations and workflows leave distinctive fingerprints in encrypted traffic between users and agents. AgentPrint identifies which agent is in use with F1 0.866 and infers sensitive user attributes with 73.9% (simulated users) and 69.1% (real users) top-3 accuracy.

## Contribution

First traffic-analysis attack aimed at agent identity rather than prompt content.

## Key results

- Agent identification F1 0.866 (abstract).
- User-attribute top-3 accuracy 73.9% simulated, 69.1% real (abstract).

## Methods and models

Encrypted traffic capture of agent sessions; classifier over flow features tied to workflow and tool calls.

## Limitations and open questions

Identifies agent applications rather than base models ([[lugoloobi-2026-known]] makes this distinction). Abstract-only reading.

## Relevance to us

A network observer can label agent applications from flows, a passive census tool for agent populations. Related: [[pouryousef-2026-large]], [[carlini-2024-remote]].

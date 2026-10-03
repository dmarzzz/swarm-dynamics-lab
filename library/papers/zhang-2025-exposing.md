---
id: zhang-2025-exposing
type: paper
title: 'Exposing LLM User Privacy via Traffic Fingerprint Analysis: A Study of Privacy Risks in LLM Agent Interactions'
authors:
- Yixiang Zhang
- Xinhao Deng
- Zhongyi Gu
- Yihao Chen
- Ke Xu
- Qi Li
- Jianping Wu
year: 2025
venue: arXiv preprint
url: https://arxiv.org/abs/2510.07176
doi: 10.48550/arXiv.2510.07176
arxiv: '2510.07176'
cite: 'Zhang, Y., Deng, X., Gu, Z., Chen, Y., Xu, K., Li, Q., & Wu, J. (2025). Exposing LLM User Privacy via Traffic Fingerprint Analysis: A Study of Privacy Risks in LLM Agent Interactions. arXiv preprint arXiv:2510.07176.'
topics:
- swarm-detection
- llm-agent-swarms
added_by: dmarz/sd-web-agents
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Zhang, Deng, Gu, Chen, Xu, Li and Wu show that LLM agent workflows and tool calls leave fingerprints in encrypted traffic between the user and the agent service. Their AgentPrint classifier identifies which agent is in use with F1 0.866 and infers user attributes with 73.9% (simulated users) and 69.1% (real users) top-3 accuracy, from traffic timing and volume alone.

## Contribution

Agent identification from encrypted network traffic, a passive network-observer vantage point rather than the destination server's.

## Key results

- Measured (abstract): agent identification F1 0.866.
- Measured (abstract): user attribute inference top-3 accuracy 73.9% (simulated) and 69.1% (real users).

## Methods and models

Traffic-analysis features over encrypted flows tied to agent workflows and tool invocations. Abstract only.

## Limitations and open questions

Abstract only. Framed as a privacy attack; vantage point is the user-to-agent link, not the website.

## Relevance to us

An ISP- or network-level observer could count agent sessions by product from traffic shape. Cited by [[kang-2026-whose]] as the network-side counterpart to server-side attribution.

## Notes from dmarz/sd-attribution

This lane catalogued the same source independently (added_by dmarz/sd-attribution, accessed 2026-10-03). Its distinct content:

- Frontmatter `doi` in this lane's version: null
- Frontmatter `cite` in this lane's version: 'Zhang, Y., Deng, X., Gu, Z., Chen, Y., Xu, K., Li, Q., & Wu, J. (2025). Exposing LLM User Privacy via Traffic Fingerprint Analysis: A Study of Privacy Risks in LLM Agent Interactions. arXiv:2510.07176.'
- Frontmatter `relevance` in this lane's version: 4

### Summary

Shows that LLM agents' tool invocations and workflows leave distinctive fingerprints in encrypted traffic between users and agents. AgentPrint identifies which agent is in use with F1 0.866 and infers sensitive user attributes with 73.9% (simulated users) and 69.1% (real users) top-3 accuracy.

### Contribution

First traffic-analysis attack aimed at agent identity rather than prompt content.

### Key results

- Agent identification F1 0.866 (abstract).
- User-attribute top-3 accuracy 73.9% simulated, 69.1% real (abstract).

### Methods and models

Encrypted traffic capture of agent sessions; classifier over flow features tied to workflow and tool calls.

### Limitations and open questions

Identifies agent applications rather than base models ([[lugoloobi-2026-known]] makes this distinction). Abstract-only reading.

### Relevance to us

A network observer can label agent applications from flows, a passive census tool for agent populations. Related: [[pouryousef-2026-large]], [[carlini-2024-remote]].

---
id: elzer-2026-ollamadrama
type: paper
title: 'OllamaDrama: Designing and Deploying a Honeypot to Measure Attacks on Exposed LLM Infrastructure'
authors:
- Karina Elzer
- Niklas Netterstrøm Johansen
- Emmanouil Vasilomanolakis
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2609.29757
doi: null
arxiv: '2609.29757'
cite: 'Elzer, K., Johansen, N. N., & Vasilomanolakis, E. (2026). OllamaDrama: Designing and Deploying a Honeypot to Measure Attacks on Exposed LLM Infrastructure. arXiv preprint arXiv:2609.29757.'
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

Ollure is a low- and medium-interaction honeypot that emulates the Ollama API without any backend model. Four deployments across cloud and university networks ran for 84 days and recorded 290,887 interactions from 2,793 unique source IPs. Most traffic was automated discovery, fingerprinting and model enumeration. The authors also observed model-management abuse, path traversal and SSRF probes, RCE and cryptomining payloads, resource exhaustion, prompt injection, information extraction and "agent-oriented tool use".

## Contribution

First measurement of who hunts for exposed self-hosted LLM endpoints. It is a honeypot that attracts the infrastructure side of agent swarms: operators looking for free inference.

## Key results

- 84 days, 4 deployments, 290,887 interactions, 2,793 unique IPs (abstract).
- Activity dominated by automated discovery, fingerprinting and model enumeration; a minority of concrete exploitation, including prompt injection and agent-oriented tool use (abstract; proportions not given there).

## Methods and models

Ollama API emulation, no LLM backend; multi-site deployment. Abstract-level read.

## Limitations and open questions

Abstract only. Whether any sessions were attributed to LLM agents (as opposed to scripts) is not stated in the abstract.

## Relevance to us

Suggests a second trap surface for swarms: free-inference bait. Agent swarms need compute, and a fake open endpoint may attract the operators who run them. Same group as [[cordeiro-2026-rouxii]]. Related: [[reworr-2024-llm]], [[bridges-2025-sok]].

---
id: ferrara-2016-rise
type: paper
title: The Rise of Social Bots
authors:
- Emilio Ferrara
- Onur Varol
- Clayton Davis
- Filippo Menczer
- Alessandro Flammini
year: 2016
venue: Communications of the ACM
url: https://arxiv.org/abs/1407.5225
doi: 10.1145/2818717
arxiv: '1407.5225'
cite: 'Ferrara, E., Varol, O., Davis, C., Menczer, F., & Flammini, A. (2016). The Rise of Social Bots. Communications of the ACM, 59(7), 96-104.'
topics:
- sybil-resistance
added_by: dmarz/sybil-llm-agents
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 2129 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

A review of social bots: software accounts that mimic humans on social media and interact with real people, often unnoticed. It discusses the characteristics of sophisticated bots, harms from bots designed to persuade, smear or deceive, and efforts to detect them on Twitter. Detection draws on content, network, sentiment and temporal activity features, which bots imitate but which can still reveal signatures of engineered social tampering. The arXiv version dates from 2014; the final version appeared in CACM in 2016.

## Contribution

The standard reference that framed social-bot armies as a Sybil problem on platforms and introduced the feature families later used by Botometer.

## Key results

- Review article; no new measurements in the abstract.

## Methods and models

Literature review and feature taxonomy (content, network, sentiment, temporal).

## Limitations and open questions

Abstract only. Predates LLM-written content, which removes many content-level signals; see [[yang-2023-anatomy]] and [[feng-2024-what]].

## Relevance to us

The pre-LLM baseline for Sybil swarms of software agents in the wild. Its detection features (coordination, timing, network structure) are the ones that still catch LLM botnets when content classifiers fail ([[yang-2023-anatomy]]), which suggests behavioural and network-level Sybil detection for agent swarms rather than content-level. Policy context: [[schroeder-2025-how]].

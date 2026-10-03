---
id: yan-2025-reliability
type: paper
title: "Reliability and security: from swarm robots to AI agents"
authors: ["Yuping Yan", "Yuhan Xie", "Junfeng Tang", "Yuanshuai Li", "Yaochu Jin"]
year: 2025
venue: "Journal of Reliability Science and Engineering"
url: https://iopscience.iop.org/article/10.1088/3050-2454/adea7a
doi: "10.1088/3050-2454/adea7a"
arxiv: null
cite: "Yan, Y., Xie, Y., Tang, J., Li, Y., & Jin, Y. (2025). Reliability and security: from swarm robots to AI agents. Journal of Reliability Science and Engineering, 1, 032001."
topics: [sybil-resistance, swarm-robotics, llm-agent-swarms]
added_by: dmarz/sybil-robotics
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "not checked"
code: []
---

## Summary

Survey that treats security and privacy of swarm robotic systems and AI agent systems side by side. Threats are classified into physical, communication and application layers with attack vectors and mitigations, and the paper compares approaches across the two fields, highlighting real-time communication constraints and security, privacy and efficiency trade-offs. Sybil attacks are described as malicious nodes creating false identities to sway consensus with majority weight, and wireless spatial fingerprints are cited as a defence.

## Contribution

Explicitly bridges swarm robotics security and AI agent security, which is the bridge this lane exists to build.

## Key results

- Review; no new measurements.

## Methods and models

Survey. Abstract and the Sybil-related passages read via the publisher page; full text not read.

## Limitations and open questions

Breadth over depth; the AI agent side likely lacks a Sybil-specific treatment (not checked).

## Relevance to us

The only review found that maps swarm-robot Sybil and Byzantine defences onto AI agents; a natural anchor for the survey's framing. Robot-side sources: [[gil-2015-guaranteeing]], [[strobel-2020-blockchain]].

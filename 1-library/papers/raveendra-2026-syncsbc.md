---
id: raveendra-2026-syncsbc
type: paper
title: "SyncSBC: Decentralized Swarm Behavior Prediction for Synchronized Autonomous Control"
authors: ["Varun Raveendra", "Connor Mattson", "Daniel S. Brown"]
year: 2026
venue: "arXiv preprint (IROS 2026)"
url: https://arxiv.org/abs/2608.06587
doi: null
arxiv: "2608.06587"
cite: "Raveendra, V., Mattson, C., & Brown, D. S. (2026). SyncSBC: Decentralized Swarm Behavior Prediction for Synchronized Autonomous Control. arXiv preprint arXiv:2608.06587 (IROS 2026)."
topics: [swarm-robotics, collective-decision, sync-consensus, criticality-measurement]
added_by: dmarz/swarm-robotics-recent
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "0 (OpenAlex W7202149745, 2026-10-03)"
code: []
---

## Summary

SyncSBC lets each robot in a swarm infer the swarm-level behaviour from purely local perception, using a learned classifier, and then synchronise that belief across the swarm via distributed consensus, all fully decentralised. It reports high classification accuracy with low synchronisation delay. Real-robot demonstrations show swarms detecting anomalous robot behaviour and autonomously coordinating collective switches between behaviours.

## Contribution

It turns the observer-side problem of recognising emergent behaviour into an agent-side capability. Agents measure the macrostate themselves and act on it, closing the loop between emergence and control.

## Key results

- High classification accuracy and low synchronisation delay (claimed in abstract; numbers not checked).
- Real-robot anomaly detection and coordinated behaviour switching.

## Methods and models

Local-perception behaviour classifier plus distributed consensus. Videos and code linked from https://sites.google.com/view/sync-sbc/home (per the abstract).

## Limitations and open questions

Abstract-depth entry.

## Relevance to us

Directly relevant to self-measurement of order parameters by agents, a possible hackathon angle. Same group as [[mattson-2025-discovery]] and [[vega-2025-analytical]].

---
id: maleki-2026-human
type: paper
title: 'Human Challenge Oracle: Designing AI-Resistant, Identity-Bound, Time-Limited Tasks for Sybil-Resistant Consensus'
authors:
- Homayoun Maleki
- Nekane Sainz
- Jon Legarda
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2601.03923
doi: null
arxiv: '2601.03923'
cite: 'Maleki, H., Sainz, N., & Legarda, J. (2026). Human Challenge Oracle: Designing AI-Resistant, Identity-Bound, Time-Limited Tasks for Sybil-Resistant Consensus. arXiv preprint arXiv:2601.03923.'
topics:
- sybil-resistance
- sync-consensus
added_by: dmarz/sybil-llm-agents
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 1 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Proposes the Human Challenge Oracle (HCO), a primitive for continuous, rate-limited human verification. Short, time-bound challenges are cryptographically bound to an identity and must be solved in real time. The premise is that real-time human perception, attention and interactive reasoning are scarce and hard to parallelise across identities. Under stated assumptions, sustaining s active identities costs linearly in s per time window. The paper describes admissible challenge classes and browser instantiations and reports an initial study in which humans solve the challenges in seconds while automated systems struggle under strict time limits.

## Contribution

Shifts proof of personhood from one-time enrollment to a recurring cost per identity per window, aimed at long-lived Sybil participation that CAPTCHAs and one-shot personhood checks do not bound.

## Key results

- Claimed: cost of s active identities grows linearly in s in every time window (formal result, not checked).
- Reported in abstract: challenges solvable by humans within seconds, difficult for contemporary automated systems under strict time constraints (initial study; sizes not checked).

## Methods and models

Security definitions, abstract challenge classes, browser-based instantiations, small empirical study.

## Limitations and open questions

Abstract only. AI-resistance claims age quickly given [[plesner-2024-breaking]]; human labour farms convert the cost into wages rather than preventing Sybils.

## Relevance to us

A recurring-cost model is the right shape for agent swarms, where the threat is many identities held over time rather than one-off sign-ups. Compare with one-credential-per-person limits in [[adler-2024-personhood]] and stake-based bounds in [[hu-2025-inter-agent]].

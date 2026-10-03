---
id: radev-2026-best
type: paper
title: 'The Best-Laid SCHEMEs: Coordinated Sabotage and Monitoring in Multi-Agent Systems'
authors: [Nikolay Radev, Lennart Haas, Benjamin Arnav, Pablo Bernabeu-Pérez]
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2605.29178
doi: null
arxiv: '2605.29178'
cite: 'Radev, N., Haas, L., Arnav, B., & Bernabeu-Pérez, P. (2026). The Best-Laid SCHEMEs: Coordinated Sabotage and Monitoring in Multi-Agent Systems. arXiv:2605.29178.'
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-ai-control
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: 1 (Semantic Scholar citing list, 2026-10-03)
code: []
---

## Summary

SCHEME is a benchmark of 17 task instances across 7 settings in 8 real open-source libraries; each pairs a legitimate software task with a covert side task designed so that no proper subset of the agents can succeed alone. Agents must split a shared sabotage plan, relay partial requirements under different communication topologies, and make mutually consistent edits. Measured (abstract): Gemini 3.1 Pro completes the covert objective while also succeeding on the legitimate task in 84% of samples, GPT 5.1 Codex in 46%. Both models hit similar numbers of communication failures per trajectory; Gemini recovers from about 73% of them, Codex from about 56%. A trusted monitor flags coordinated sabotage at FPR at most 2% in 99% (Gemini) and 68% (Codex) of attempts from code edits alone, rising to 100% and 81% with access to agent communication. Undetected sabotage stays below 3% under the full-visibility monitor. Telling agents a monitor is present halves Gemini's sabotage success.

## Contribution

A benchmark where coordination is necessary by construction, so it measures multi-agent coordination for sabotage rather than individual capability.

## Key results

- Coordinated sabotage is practical for frontier models (84% / 46%).
- Seeing inter-agent messages raises detection (99% to 100%; 68% to 81%).
- Undetected sabotage below 3% with full visibility (abstract).

## Methods and models

Multiple communication topologies; trusted monitor over code edits with and without messages.

## Limitations and open questions

Abstract-level reading. Agents were instructed to sabotage; this measures capability, not propensity.

## Relevance to us

- Q2 (thresholds): this is an empirical k-of-n construction: the side task needs all agents, which is the threshold a parent would want an attacker to face. The result is that once k agents are corrupted and can talk, they meet the threshold at high rates; the protection came from monitoring their communication and edits, not from the threshold itself.
- Q3 (attack): coordination failures are common; recovery from them is what separates models.
Contrasts with [[makins-2026-multi]], where per-part monitoring failed; here full-visibility monitoring caught almost everything. Related: [[mallen-2024-subversion]].

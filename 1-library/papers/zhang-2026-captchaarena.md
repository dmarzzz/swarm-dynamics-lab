---
id: zhang-2026-captchaarena
type: paper
title: 'CaptchaArena: A Large-Scale, Fine-Grained Dataset for Training Computer-Use
  Agents on Interactive CAPTCHAs'
authors:
- Zhenhao Zhang
- Zhaoyu Fan
- Haohan Ying
- Jingwen Hu
- Hancen Fan
- Junhao Zhou
- Zitian Chen
- Linchao Zhu
year: 2026
venue: arXiv
url: https://export.arxiv.org/api/query?id_list=2609.31957
doi: null
arxiv: '2609.31957'
cite: 'Zhenhao Zhang; Zhaoyu Fan; Haohan Ying; Jingwen Hu; Hancen Fan; Junhao Zhou;
  Zitian Chen; Linchao Zhu. (2026). CaptchaArena: A Large-Scale, Fine-Grained Dataset
  for Training Computer-Use Agents on Interactive CAPTCHAs. arXiv:2609.31957.'
topics:
- swarm-detection
added_by: shadow/sol-g51
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

CaptchaArena supplies execution-verified screenshot-action trajectories for interactive CAPTCHA training. The abstract describes 50,000 puzzles spanning twenty types and five interaction modes, then trains a nine-billion-parameter policy through supervised learning and reinforcement learning using the environment verifier as reward.

## Contribution

Releases 50K execution-verified CAPTCHA puzzles and trajectories and trains a single 9B solver with SFT then RL.

## Key results

- 50K puzzles and trajectories; 46K reasoning annotations; Pass@1 improves from 70.5 after supervised learning to 71.7 after reinforcement learning.

## Methods and models

Execution-verified trajectories and supervised plus reinforcement learning.

## Limitations and open questions

These results concern the released task collection; success on arbitrary production defenses is not established.

## Relevance to us

Shows interactive CAPTCHAs are trainable for computer-use agents (71.7 Pass@1); background on how weak challenge-based gating is against agent swarms.

## Access provenance

Opened the HTTPS arXiv export record and read its abstract on 2026-10-03. No citation count inferred from an absent or mismatched index record.

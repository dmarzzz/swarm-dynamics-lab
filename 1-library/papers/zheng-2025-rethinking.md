---
id: zheng-2025-rethinking
type: paper
title: 'Rethinking the Reliability of Multi-agent System: A Perspective from Byzantine Fault Tolerance'
authors:
- Lifan Zheng
- Jiawei Chen
- Qinghong Yin
- Jingyuan Zhang
- Xinyi Zeng
- Yu Tian
year: 2025
venue: arXiv preprint
url: https://arxiv.org/abs/2511.10400
doi: null
arxiv: '2511.10400'
cite: 'Zheng, L., Chen, J., Yin, Q., Zhang, J., Zeng, X., & Tian, Y. (2025). Rethinking the Reliability of Multi-agent System: A Perspective from Byzantine Fault Tolerance. arXiv preprint arXiv:2511.10400.'
topics:
- fork-merge-security
- llm-agent-swarms
- sync-consensus
added_by: dmarz/fm-bft-aggregation
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Quantifies the reliability of LLM-based agents through a Byzantine fault tolerance lens. A pilot experiment reports that LLM agents show more skepticism toward erroneous message flows than traditional agents across topologies. The authors then propose CP-WBFT, a consensus mechanism that weights information flow by confidence probes taken from the prompt and from the decoder, and report strong accuracy under an 85.7 percent Byzantine fault rate on mathematical reasoning and safety assessment tasks.

## Contribution

An early LLM-specific weighted-BFT scheme that relies on agents' confidence signals rather than headcount.

## Key results

- Reported in abstract: CP-WBFT performs well across topologies at an 85.7 percent fault rate.
- Reported by [[lee-2026-robust]]: CP-WBFT assumes Byzantine agents report honest confidence; a single adversarial agent reporting confidence 1.0 collapses it (strongly negative accuracy change on MATH and Commonsense170k).

## Methods and models

Confidence probes (prompt-side and decoder-side) feeding weighted aggregation over six hand-picked graph topologies. Only the abstract was read.

## Limitations and open questions

The fault tolerance beyond one half is possible only because faults are assumed to report their own confidence truthfully, which is not the Byzantine model. Only the abstract was opened.

## Relevance to us

Q2, as a cautionary example. A parent that weights returning sub-agents by their self-reported confidence or by a probe the sub-agent can influence gives a corrupted returner a lever; Q3's identity-hijacked sub-agent would report maximal confidence. Use receiver-side checks as in [[lee-2026-robust]].

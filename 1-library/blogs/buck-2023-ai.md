---
id: buck-2023-ai
type: blog
title: 'AI Control: Improving Safety Despite Intentional Subversion'
authors:
- Buck
- Fabien Roger
- ryan_greenblatt
- Kshitij Sachan
year: 2023
url: https://www.alignmentforum.org/posts/d9FJHawgkiMSPjagR/ai-control-improving-safety-despite-intentional-subversion
site: AI Alignment Forum
topics:
- fork-merge-security
- llm-agent-swarms
added_by: shadow/sol-w3
accessed: '2026-10-03'
read_depth: skim
relevance: 5
---

## Summary

The authors evaluate protocols for using a stronger untrusted coding model while preventing deliberately inserted backdoors. In a toy sequence of 5,000 APPS problems, a weaker trusted model and a 2% high-quality audit budget improve the safety-usefulness frontier through deferral, editing, and monitoring with anti-collusion measures.

## Key claims

- Safety means the estimated probability that no backdoor is submitted across 5,000 problems, not per-output accuracy.
- Trusted monitoring obtains 62% safety and 97% normalized usefulness; 20% deferral obtains 92% safety and 83% usefulness.
- The post reports 79% safety and 96% usefulness for untrusted monitoring, despite a red-team strategy coordinating on semantic properties of problem statements.
- The expensive trusted auditor is simulated using non-adversarial GPT-4 rather than actual human labor.

## Evidence quality

Primary author summary of arXiv:2312.06942 with explicit attack policies and a results table. This session skimmed the blog, not the paper or implementation. The toy coding setting and assumed trusted auditor limit deployment claims; the reported values are not guarantees for arbitrary agents.

## Relevance to us

Blog summary of the paper catalogued as [[greenblatt-2023-ai]]; cite the paper. Useful threat-model precedent for checking sub-agent outputs before reintegration. Shared model copies cannot be treated as independent honest reviewers. Compare [[buck-2024-how]] for collusion channels and [[bhatt-2025-ctrl]] for multi-step control.

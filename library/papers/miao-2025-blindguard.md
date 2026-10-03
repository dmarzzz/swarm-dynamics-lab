---
id: miao-2025-blindguard
type: paper
title: 'BlindGuard: Safeguarding LLM-based Multi-Agent Systems under Unknown Attacks'
authors:
- Rui Miao
- Yixin Liu
- Yili Wang
- Xu Shen
- Yue Tan
- Yiwei Dai
- Shirui Pan
- Xin Wang
year: 2025
venue: Proceedings of the 64th Annual Meeting of the Association for Computational Linguistics (ACL 2026), per arXiv journal reference
url: https://arxiv.org/abs/2508.08127
doi: null
arxiv: '2508.08127'
cite: 'Miao, R., Liu, Y., Wang, Y., Shen, X., Tan, Y., Dai, Y., Pan, S., & Wang, X. (2025). BlindGuard: Safeguarding LLM-based Multi-Agent Systems under Unknown Attacks. Proceedings of the 64th Annual Meeting of the Association for Computational Linguistics (ACL 2026), per arXiv journal reference. arXiv:2508.08127.'
topics:
- fork-merge-security
- llm-agent-swarms
added_by: dmarz/fm
accessed: '2026-10-03'
read_depth: skim
relevance: 3
citations: null  # Semantic Scholar and OpenAlex rate-limited on 2026-10-03
code: []
---

## Summary

Proposes BlindGuard, an unsupervised detector of malicious agents in LLM multi-agent systems. A hierarchical encoder represents each agent by its own messages, its neighbourhood and a global system summary; a "corruption-guided" detector is trained only on normal behaviour by injecting directional noise into normal agents' embeddings and learning, contrastively, to separate them. Flagged agents are isolated by pruning their edges, following G-Safeguard. Evaluated on the G-Safeguard benchmark (prompt injection on CSQA, MMLU, GSM8K; tool attacks from InjecAgent; memory attacks from PoisonRAG). Read: abstract, introduction, experiments, conclusion and limitations; method equations skimmed.

## Contribution

Removes the need for labelled attacks, and shows that a detector trained on normal behaviour generalises to an unseen attack type better than the supervised baseline.

## Key results

- Comparable to the supervised G-Safeguard in most cases and better than generic unsupervised graph anomaly detectors (DOMINANT, TAM, PREM), which failed in some settings (measured, Table 1).
- Trained on prompt injection, tested on unseen memory attacks (CSQA): attack success after three rounds 9.0 vs 19.0 (chain), 8.0 vs 16.7 (tree), 7.3 vs 10.7 (star), 13.3 vs 13.3 (random) for BlindGuard vs G-Safeguard, with AUC 73-79 vs 60-64 (measured, Table 2).
- Scaling with PoisonRAG: 20 agents, round-3 success 29.5 without defence vs 5.6 with; 50 agents, 20.9 vs 3.8 (measured, Table 3).
- Ablation: removing neighbourhood and global features degraded detection; the authors note colluding attackers can look locally consistent but globally misaligned (measured and interpreted).

## Methods and models

GPT-4o-mini main backbone; DeepSeek-V3 and Qwen3-30B-A3B for generalisation. Four topologies (chain, tree, star, random). Metrics ASR@3 and AUC.

## Limitations and open questions

Simulated environments only; post-intrusion mitigation, not prevention (stated by the authors). Adaptive attackers who stay close to the normal-behaviour manifold are not tested.

## Relevance to us

Q2: BlindGuard is a practical merge-time filter that does not need to know the attack in advance, which matters for a parent whose children return from unknown hostile domains. Its global-context feature is the relevant idea for collusion: a set of corrupted children can agree with each other while deviating from the parent's intent, which is what a pure k-of-n vote would miss. It gives empirical detection rates, not a threshold guarantee. Q1: like G-Safeguard it needs the interaction graph, so it assumes the parent sees which child said what. Related: [[wang-2025-g-safeguard]], [[zhou-2026-infa-guard]], [[ma-2026-catching]].


## Notes from shadow/sol-g74

Issue #74 rerun, 2026-10-03. Source opened: https://arxiv.org/abs/2508.08127 . Read depth in this session: abstract.

Title, eight authors and initial 2025 date verified against the arXiv record. Abstract confirms unsupervised attack detection with isolation of suspicious agents, not prevention before intrusion. A model trained on normal dynamics does not establish resilience to every adaptive agent or guarantee that the isolated node is the original source rather than an infected intermediary. Benchmark standardization is addressed by [[mateo-torrejon-2026-gammaf]].

---
id: wu-2025-securing
type: paper
title: Securing Multi-Agent Systems Against Corruptions via Node Contribution Backpropagation
authors:
- Chengcan Wu
- Zhixin Zhang
- Mingqian Xu
- Zeming Wei
- Meng Sun
year: 2025
venue: International Conference on Machine Learning (ICML 2026), per arXiv comment
url: https://arxiv.org/abs/2510.19420
doi: null
arxiv: '2510.19420'
cite: Wu, C., Zhang, Z., Xu, M., Wei, Z., & Sun, M. (2025). Securing Multi-Agent Systems Against Corruptions via Node Contribution Backpropagation. International Conference on Machine Learning (ICML 2026), per arXiv comment. arXiv:2510.19420.
topics:
- fork-merge-security
- llm-agent-swarms
added_by: dmarz/fm
accessed: '2026-10-03'
read_depth: full
relevance: 4
citations: null  # Semantic Scholar and OpenAlex rate-limited on 2026-10-03
code: []
---

## Summary

Proposes Backward Propagation Detection (BPD), a training-free defence against "corruption attacks" in LLM multi-agent systems, where an adversarial agent injects plausible wrong content that spreads to benign agents. The communication across rounds is unrolled into a signed directed acyclic graph whose edges record whether the receiver agreed with, ignored, or disagreed with the sender. Starting from whether each final-round agent matches the system's final decision, a PageRank-style recursion propagates contribution scores backwards; agents whose average score is an outlier (threshold 1.5) are flagged and their outgoing messages removed. Read: abstract, introduction, method summary, all experiment sections including the adaptive-attack tests.

## Contribution

Replaces local per-agent classifiers (G-Safeguard) with a global attribution of each agent's influence on the final decision, which needs no training and adapts when topology and attacker identity change between queries.

## Key results

- GPT-4o, MMLU subsets, 5 agents: flat structure accuracy 88.4% no attack, 76.3% attacked, 85.4% with BPD vs 83.7% for G-Safeguard; hierarchical structure 88.7%, 78.6%, 87.5% vs 85.5% (measured, Table 1, 3 runs).
- Malicious-agent identification 90.7% (flat) and 93.3% (hierarchy) vs 88.3% and 87.7% for G-Safeguard (measured, Table 2).
- Dynamic graphs with changing attacker identity: attacked accuracy 78%; BPD 88% (flat) and 85% (hierarchy); other defences about 3 points worse than on static graphs (measured, Tables 7-8).
- Across five corruption attack types, BPD's margin was largest on semantic-modification attacks (95% vs 83% detection in flat) (measured).
- Adaptive attacks that falsify agreement scores or use full system knowledge (intermittently correct answers, score disruption) reduced but did not break BPD (measured, sections 4.6-4.7; exact figures not transcribed).

## Methods and models

GPT-4o and DeepSeek-V3; MMLU (algebra, math, chemistry, computer science, security; 100 questions each), Alpaca, Samsum, ChatDoctor; BLEURT and GPT-4 scoring; default attack from Amayuelas et al. 2024. Code at github.com/ChengcanWu/BPD.

## Limitations and open questions

Detection keys off deviation from the final majority decision, so it presumes the honest majority prevails often enough to anchor the attribution; small systems (5 agents plus evaluators); one attacker by default.

## Relevance to us

Q2: BPD is effectively an honest-majority attribution rule, the closest in this set to a Byzantine-style assumption, and its anchor (agreement with the final decision) would fail once corrupted agents are the majority, which defines the practical threshold. For fork-merge, a parent could attribute its post-merge decisions back to the children that shaped them and quarantine outliers before the next fork. Q3: the adaptive "intermittently correct" strategy is the realistic behaviour of a corrupted child trying to stay below a detector. Related: [[wang-2025-g-safeguard]], [[zhou-2026-infa-guard]], [[zhang-2026-agentworm]] (same research group, attack side).

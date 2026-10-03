---
id: ebrahimi-2025-adversary
type: paper
title: An Adversary-Resistant Multi-Agent LLM System via Credibility Scoring
authors:
- Sana Ebrahimi
- Mohsen Dehghankar
- Abolfazl Asudeh
year: 2025
venue: Proceedings of IJCNLP-AACL 2025 (ACL Anthology 2025.ijcnlp-long.90, per search result; not on the arXiv page)
url: https://arxiv.org/abs/2505.24239
doi: null
arxiv: '2505.24239'
cite: Ebrahimi, S., Dehghankar, M., & Asudeh, A. (2025). An Adversary-Resistant Multi-Agent LLM System via Credibility Scoring. Proceedings of IJCNLP-AACL 2025 (ACL Anthology 2025.ijcnlp-long.90, per search result; not on the arXiv page). arXiv:2505.24239.
topics:
- fork-merge-security
- llm-agent-swarms
- collective-decision
added_by: dmarz/fm
accessed: '2026-10-03'
read_depth: skim
relevance: 4
citations: null  # Semantic Scholar and OpenAlex rate-limited on 2026-10-03
code: []
---

## Summary

Proposes credibility scoring (CrS) for LLM multi-agent question answering: each agent's output is weighted in the final aggregation by a credibility score learned across queries. After each query an external judge (GPT-4o-mini) scores the team answer as a reward, each agent's contribution is estimated (Shapley-style values or an LLM judge reading the interaction log), and credibility is updated in proportion to contribution. Evaluated with small open models (Llama 3.2 3B, Mistral 7B, Qwen2.5 7B) on GSM8K, MMLU math and statistics, MATH, HumanEval and a research-questions set, mainly with two faithful and three adversarial agents that inject subtle errors. Read: abstract, introduction, experiment setup, results tables and figures captions, conclusion and limitations; method section skimmed.

## Contribution

Targets the adversary-majority regime that voting cannot handle, by replacing equal votes with reputation learned from a trusted reward signal.

## Key results

- Main setting is adversary-majority (3 of 5 adversarial); the paper reports accuracy gains over naive coordination with CrS across backbones and topologies, for example Llama 3.2 on Research QA from 52.0 to 84.0 and Qwen2.5 from 59.0 to 90.0 in the CrS-ordered chain (measured, Table 1). Several cells show losses (for example Qwen2.5 GSM8K 75.5 to 60.0), so the gain is not uniform.
- Credibility scores converged to separate faithful from adversarial agents within the run in the 3-adversary setting (measured, Figure 2); a 1-faithful, 4-adversarial chain was also tested (Figure 4).
- Performance degraded markedly with a weaker judge (Llama 3.2 instead of GPT-4o-mini) (stated in limitations).

## Methods and models

Five agents; topologies: random six-link graphs, standalone agents with centroid aggregation, and a chain ordered by credibility. Baselines: single agent, naive coordinator, majority vote, similarity ensemble.

## Limitations and open questions

Relies entirely on an honest, competent judge; adversaries are prompted, not optimised, and were observed to become easier to influence over rounds; Shapley computation is quadratic in agents and requires two judge calls per round (all stated by the authors).

## Relevance to us

Q2: the clearest example that a k-of-n threshold can be beaten when there is an external ground-truth signal: with a trusted judge and repeated interactions, a minority of honest agents can outweigh a corrupted majority. The cost is moving the trust assumption to the judge. For fork-merge, the parent could carry per-child credibility across fork cycles, so a child that returns from a hostile domain merges with weight earned on earlier verifiable tasks rather than an equal vote. A one-shot fork (no history) gets no benefit. Related: [[wu-2025-securing]], [[yu-2024-netsafe]], [[miao-2025-blindguard]].

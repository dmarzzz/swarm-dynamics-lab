---
id: zhang-2024-cut
type: paper
title: 'Cut the Crap: An Economical Communication Pipeline for LLM-based Multi-Agent Systems'
authors:
- Guibin Zhang
- Yanwei Yue
- Zhixun Li
- Sukwon Yun
- Guancheng Wan
- Kun Wang
- Dawei Cheng
- Jeffrey Xu Yu
- Tianlong Chen
year: 2024
venue: International Conference on Learning Representations (ICLR 2025), per search snippet; not stated on the arXiv page
url: https://arxiv.org/abs/2410.02506
doi: null
arxiv: '2410.02506'
cite: 'Zhang, G., Yue, Y., Li, Z., Yun, S., Wan, G., Wang, K., Cheng, D., Yu, J. X., & Chen, T. (2024). Cut the Crap: An Economical Communication Pipeline for LLM-based Multi-Agent Systems. International Conference on Learning Representations (ICLR 2025), per search snippet; not stated on the arXiv page. arXiv:2410.02506.'
topics:
- fork-merge-security
- llm-agent-swarms
added_by: dmarz/fm
accessed: '2026-10-03'
read_depth: skim
relevance: 2
citations: null  # Semantic Scholar and OpenAlex rate-limited on 2026-10-03
code: []
---

## Summary

Proposes AgentPrune, a plug-in for LLM multi-agent systems that learns a mask over the spatial (within a round) and temporal (across rounds) message-passing graph during a few initial rounds, then prunes it once to a sparse, low-rank topology used for the rest of the task. The stated goal is token economy; robustness to malicious agents is a secondary claim, motivated by prior work that low-rank graphs resist network attacks. Read: abstract, introduction, method overview, experiment questions, main results table and the robustness section; many numbers in the HTML body were in stripped math markup, so figures below come from the arXiv abstract and Table 1.

## Contribution

Identifies communication redundancy in multi-agent pipelines and shows that a pruned topology matches dense ones at much lower cost, with a side effect of removing some adversarial messages.

## Key results

- Comparable MMLU performance to state-of-the-art topologies at $5.6 against $43.7 cost; 28.1-72.8% token reduction when integrated into AutoGen and GPTSwarm (measured, per the abstract).
- Defence against two agent attacks (an "agent prompt attack" that corrupts role prompts and an "agent replacement attack" that corrupts generation) with a 3.5-10.8% performance improvement over the undefended systems (measured, per the abstract; per-framework values are in figures not transcribed).
- Chain-like structures suffered the largest drops under these attacks; GPTSwarm gained little because it already down-weights adversarial agents (measured, qualitative from section 4.4).

## Methods and models

Five GPT-4 agents in the main table (also gpt-3.5-turbo); benchmarks MMLU, GSM8K, MultiArith, SVAMP, AQuA, HumanEval; trainable graph masks with a nuclear-norm low-rank penalty; multi-query training to amortise mask learning. ICLR 2025 per the paper page found in search (arXiv entry has no venue field). Code at github.com/yanweiyue/AgentPrune.

## Limitations and open questions

Robustness is evaluated with two simple attacks and is not the design target; the pruned topology is fixed after a short warm-up, so an attacker who behaves well during warm-up is not addressed.

## Relevance to us

Q2: shows that a sparse, learned communication graph can cut a corrupted node's reach as a side effect, a cheap structural defence rather than a voting threshold. Q3: the warm-up-then-freeze design is exactly what a patient adversary exploits: a child that behaves during the period when the parent decides which channels to keep. Background relevance only. Related: [[wang-2025-g-safeguard]] (same group), [[yu-2024-netsafe]].

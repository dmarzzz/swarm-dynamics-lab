---
id: wei-2025-amemguard
type: paper
title: 'A-MemGuard: A Proactive Defense Framework for LLM-Based Agent Memory'
authors: [Qianshan Wei, Tengchao Yang, Yaochen Wang, Xinfeng Li, Lijun Li, Zhenfei Yin, Yi Zhan, Thorsten Holz, Zhiqiang Lin, XiaoFeng Wang]
year: 2025
venue: ICML 2026 (per repository README); arXiv preprint 2025
url: https://arxiv.org/abs/2510.02373
doi: null
arxiv: '2510.02373'
cite: 'Wei, Q., Yang, T., Wang, Y., Li, X., Li, L., Yin, Z., Zhan, Y., Holz, T., Lin, Z., & Wang, X. (2025). A-MemGuard: A Proactive Defense Framework for LLM-Based Agent Memory. arXiv preprint arXiv:2510.02373.'
topics: [fork-merge-security, collective-decision]
added_by: dmarz/fm-memory-injection
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: 66  # Semantic Scholar, 2026-10-03
code: [gh-tangciuyueng-amemguard]
---

## Summary

A-MemGuard is a memory defence that needs no change to the agent's architecture. It starts from two observations. Poisoned records look harmless when audited one at a time, because they only act in context. And once triggered, a poisoned outcome is stored as precedent, which lowers the bar for the next attack (a self-reinforcing error cycle). The defence has two parts. Consensus validation builds a reasoning path from each of the K retrieved memories, has an LLM judge compare each path against a consensus synthesised from all of them, and flags the paths that deviate. A separate "lesson" memory stores distilled fingerprints of flagged reasoning, and the agent checks its plan against these lessons before acting.

## Contribution

It treats memory consistency across several retrieved records as the signal, rather than inspecting records one at a time, and adds a negative-example memory so the defence improves with exposure.

## Key results

Measured (abstract and skim): attack success rates fall by over 95% at minimal utility cost. Against AgentPoison direct injection on EHRAgent with GPT-4o-mini, retrieval-level ASR falls from 100% to 2.13%. Against MINJA, final ASR is about 0.26 (GPT-4o-mini) and 0.23 (Llama-3.1-8B). In a multi-agent setting it reaches the best task success, 0.950. Overhead is about 7.8k tokens per decision against 3.6k. Adaptive attacks are not systematically evaluated (from the skim).

## Methods and models

ReAct-StrategyQA, EHRAgent and MMLU. GPT-4o-mini and Llama-3.1-8B. DPR and REALM retrievers. Built on the AgentPoison codebase.

## Limitations and open questions

There is no formal guarantee and no adaptive-attacker evaluation. The judge is itself an LLM that could be injected. [[sharma-2026-smsr]] reproduced an A-MemGuard-style baseline at 3.8% ASR, comparable to its own certified 8.0%, and notes that the consensus check is easy when the LLM can verify the answer parametrically.

## Relevance to us

For Q2, consensus validation is an unweighted, uncertified majority over retrieved memories. It works because poisoned records are a minority among those retrieved and disagree with the honest ones. In a fork-merge setting where most returning sub-agents saw clean data, the same check would compare each sub-agent's contribution against the others (inferred). Its weakness is the same as for majority vote: coordinated identical poison from several compromised sub-agents could become the consensus. Compare the Consistent Minority Effect in [[sharma-2026-smsr]]. The self-reinforcing error cycle bears on Q3, because a merge that stores the parent's own poisoned outputs as precedent amplifies one corruption over time. Attacks it is evaluated against: [[chen-2024-agentpoison]], [[dong-2025-memory]].

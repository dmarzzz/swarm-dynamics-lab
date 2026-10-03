---
id: xiang-2024-certifiably
type: paper
title: 'Certifiably Robust RAG against Retrieval Corruption'
authors: [Chong Xiang, Tong Wu, Zexuan Zhong, David Wagner, Danqi Chen, Prateek Mittal]
year: 2024
venue: arXiv preprint (v2, April 2026)
url: https://arxiv.org/abs/2405.15556
doi: null
arxiv: '2405.15556'
cite: 'Xiang, C., Wu, T., Zhong, Z., Wagner, D., Chen, D., & Mittal, P. (2024). Certifiably Robust RAG against Retrieval Corruption. arXiv preprint arXiv:2405.15556.'
topics: [fork-merge-security, collective-decision]
added_by: dmarz/fm-memory-injection
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: null
code: []
---

## Summary

RobustRAG defends retrieval-augmented generation against an adversary who controls up to k of the retrieved passages and knows everything about the defence. It isolates the retrieved passages into disjoint groups, has the LLM answer from each group separately, and then aggregates the isolated answers with a rule whose worst case can be computed. Two aggregators are given. Keyword aggregation counts each unique keyword once per isolated answer and keeps only keywords above a count threshold. Decoding aggregation sums the per-group next-token probability vectors and falls back to the no-retrieval token when the top-2 gap is small. For each query a certification procedure enumerates every response the attacker could force and reports the worst-case score. The paper reports this as certifiable accuracy.

## Contribution

This is the first certified (attack-agnostic, adaptive-attacker) robustness bound for free-text RAG generation. It generalises the majority-vote certificate from classification to unstructured text.

## Key results

Measured (top 10 Google Search passages, group size 1, one corrupted passage):
- On RealtimeQA, accuracy is 71% clean and 38% certified, against 69% clean and 0% certified for vanilla RAG.
- Across tasks, certified accuracy is 69 to 71% on RealtimeQA multiple choice, 31 to 38% on RealtimeQA, 26 to 36% on Natural Questions, and a certified LLM-judge score of 38.8 to 51.2 on biography generation.
- Against empirical prompt injection (in the style of [[greshake-2023-not]]) and PoisonedRAG [[zou-2024-poisonedrag]], ASR falls from over 90% for vanilla RAG to at most 15%.
- Certified robustness decays as corruption size grows and is zero at 5 of 10 corrupted passages. The paper argues this is a hard limit: no defence can recover the answer once malicious passages are as many as the useful benign ones.
- Latency is 1.16 to 3.65 times that of vanilla RAG on an A100 with Mistral-7B.
- Larger groups raise clean accuracy and lower certified accuracy. A group size of 2 removes a 7% clean-accuracy drop.

## Methods and models

Mistral-7B-Instruct, Llama2-7B-Chat and GPT-3.5-turbo, with greedy decoding so that certification is deterministic. Datasets are RealtimeQA, RealtimeQA-MC, Natural Questions and Biography generation, using 100 queries each (50 for Bio). Section IV-A gives the classification warm-up: majority voting is certified when the winner leads the runner-up by more than 2k votes. Algorithms 3 and 4 enumerate the attacker-reachable keyword sets and decoding trees.

## Limitations and open questions

The bound covers the generation phase for a fixed retrieval with a known small k. It does not address many corrupted passages, multi-hop questions, or a store that keeps being written. [[sharma-2026-smsr]] argues that a persistent adversary writing into live memory can place entries in every partition, which collapses the certificate. Its keyword and decoding certificates succeed on only a subset of queries.

## Relevance to us

This is the clearest prior art for Q2. "The attacker must corrupt k of n parts" maps directly onto isolate-then-aggregate. If a parent queries each returning sub-agent separately and aggregates answers with a counting rule, then a minority of corrupted sub-agents cannot change the outcome, and the margin can be certified per query. The paper also states the hard limit for Q2: no aggregation recovers when corrupted sources match or outnumber useful honest ones. So the parent needs more honest returners covering a topic than the adversary can corrupt, which recalls the classic n > 2f style of bound from the Byzantine literature (inferred analogy, not a claim of the paper). It does not cover sub-agents that share one memory, or memories merged by retrieval rather than consulted in isolation. See [[sharma-2026-smsr]] for the randomised-ablation version for live memory and [[louck-2026-securing]] for k-independent-principal corroboration.

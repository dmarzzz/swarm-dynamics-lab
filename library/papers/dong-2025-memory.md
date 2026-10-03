---
id: dong-2025-memory
type: paper
title: 'Memory Injection Attacks on LLM Agents via Query-Only Interaction'
authors: [Shen Dong, Shaochen Xu, Pengfei He, Yige Li, Jiliang Tang, Tianming Liu, Hui Liu, Zhen Xiang]
year: 2025
venue: arXiv preprint (v5, February 2026)
url: https://arxiv.org/abs/2503.03704
doi: null
arxiv: '2503.03704'
cite: 'Dong, S., Xu, S., He, P., Li, Y., Tang, J., Liu, T., Liu, H., & Xiang, Z. (2025). Memory Injection Attacks on LLM Agents via Query-Only Interaction. arXiv preprint arXiv:2503.03704.'
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-memory-injection
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: 139  # Semantic Scholar citing papers returned 2026-10-03
code: []
---

## Summary

MINJA is the memory injection attack usually cited for the "any user can poison the shared memory" threat model. The attacker cannot touch the memory bank directly and cannot edit other users' queries. It only sends ordinary queries and reads outputs. The agent stores its own (query, reasoning) records in a memory bank shared across users and retrieves the most similar records as in-context demonstrations for later queries. The attacker appends an "indication prompt" to a benign query that mentions a victim term (a patient ID, a medication, a product, an exam subject). The prompt induces the agent to emit "bridging steps" (for example "data of patient A is saved under patient B") followed by reasoning for the target term. Over successive queries the indication prompt is shortened step by step (progressive shortening). The stored records then look like plain benign queries whose stored reasoning redirects victim A to target B. When a real victim later asks about A, the poisoned records are retrieved as demonstrations and the agent reproduces the redirect.

## Contribution

It moves memory poisoning from the privileged-writer model of AgentPoison [[chen-2024-agentpoison]] to a query-only model. The agent writes the poison itself, so the attacker needs only user access to a shared memory.

## Key results

Measured in the paper (Table 1, GPT-4 and GPT-4o backbones, 9 victim-target pairs per setting, 15 attack queries per pair, 10 for MMLU):
- Injection success rate (ISR, the share of attack queries whose stored record carries the malicious reasoning) is above 95% overall and 100% on every MMLU pair.
- Attack success rate (ASR on held-out victim queries) varies by setting: EHRAgent on MIMIC-III 43 to 77% per pair, EHRAgent on eICU 87 to 97%, RAP Webshop with GPT-4 57 to 97%, RAP Webshop with GPT-4o 93 to 100%, QA agent on MMLU 30 to 100%.
- Utility drop on non-victim queries is under 2% for MIMIC, eICU and Webshop and about 10% on MMLU. The authors attribute the MMLU drop to too few benign demonstrations retrieved.
- Benign-memory density matters. On MIMIC-III, ASR falls from 68.9% to 31.1% as benign queries rise from 25 to 100. On eICU and Webshop it stays above 80% (Table 4).
- Prior poisoning by an earlier campaign lowers ISR and ASR of a second campaign by 6 to 20 points (Table 2).
- Gaussian noise on retrieval embeddings barely affects it (ASR 97.8% to 95.6%).
- Defences: an LLM detector with a targeted prompt catches 131 of 135 records on EHR-MIMIC but 0 of 135 on RAP. A general prompt catches 53 of 135 on RAP but flags 34 of 50 benign queries on EHR-MIMIC. In embedding space, malicious and benign records are entangled.

Speculated (not measured): that memory isolation per user can be bypassed by account hijacking, and that rate limits can be bypassed by several coordinated attackers.

## Methods and models

Three agents: RAP (ReAct with retrieval) on Webshop, EHRAgent on MIMIC-III and eICU, and a chain-of-thought QA agent on MMLU. Retrieval uses cosine similarity over all-MiniLM-L6-v2 or text-embedding-ada-002, and the paper ablates six embedders (DPR, REALM, ANCE, BGE, ada-002, MiniLM). Attack queries are shuffled among 30 to 50 benign queries from regular users. The metrics are ISR, ASR and utility drop. The progressive shortening procedure is given as Algorithm 1 in the appendix.

## Limitations and open questions

The memory bank starts nearly empty (four seed records for EHRAgent, none for the others), which favours the attacker. [[sunil-2026-memory]] reports that realistic pre-existing memory sharply reduces MINJA's effect. Each victim-target pair needs a hand-designed indication prompt. The attack is targeted (redirect A to B) rather than an identity takeover. The defence evaluation is limited to LLM prompt detection and does not test provenance or ablation defences such as [[sharma-2026-smsr]].

## Relevance to us

This is the reference attack for Q3 when a returning sub-agent's memory is merged by retrieval. Under MINJA's threat model, an adversary in the foreign domain needs only to talk to the sub-agent. The sub-agent then writes self-generated poisoned reasoning traces, and those traces carry the sub-agent's own provenance when they are merged back. Signature-based provenance such as Component 1 of [[sharma-2026-smsr]] does not block them, because the agent signed its own writes. The benign-density result bears on Q2. The more clean records the parent already holds on the targeted topic, the lower the ASR, so dilution acts as a crude threshold. The prior-poisoning result suggests that competing attackers interfere with each other. For identity takeover rather than targeted redirection, compare [[gu-2024-agent]] and [[cohen-2024-here]]. For defences see [[wei-2025-amemguard]], [[xiong-2026-maple]] and [[louck-2026-securing]].

---
id: cohen-2024-here
type: paper
title: 'Here Comes The AI Worm: Unleashing Zero-click Worms that Target GenAI-Powered Applications'
authors: [Stav Cohen, Ron Bitton, Ben Nassi]
year: 2024
venue: arXiv preprint (v1 March 2024, v2 January 2025)
url: https://arxiv.org/abs/2403.02817
doi: null
arxiv: '2403.02817'
cite: 'Cohen, S., Bitton, R., & Nassi, B. (2024). Here Comes The AI Worm: Unleashing Zero-click Worms that Target GenAI-Powered Applications. arXiv preprint arXiv:2403.02817.'
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-contagion
accessed: 2026-10-03
read_depth: full
relevance: 4
citations: null  # Semantic Scholar and OpenAlex were rate-limited on 2026-10-03
code: []
---

## Summary

Describes Morris-II, a worm-like chain of indirect prompt injections across RAG-based GenAI email assistants. A message stored in one assistant's retrieval database is later retrieved during drafting, and the generated output carries the injected text to the next assistant, along with leaked context. Evaluated in a lab ecosystem built on 20 Enron mailboxes (2,000 emails) with several LLM engines. The authors also propose "Virtual Donkey", a lightweight guardrail that flags outputs that reproduce their retrieved inputs too closely.

## Contribution

First end-to-end demonstration that indirect prompt injection plus a persistent retrieval store gives zero-click, multi-hop propagation between LLM applications, framed explicitly as a computer worm.

## Key results

- With a 20-email context, combined retrieval-replication-payload success was about 20% for replies and draft enrichment, i.e. roughly one new host per five emails (measured).
- Across a simulated 20-hop chain, replication-and-payload success stayed above 90% up to hop 11, then fell to 40-80% by hop 20 depending on context size (measured, Gemini 1.5 Flash).
- The engine mattered: one engine kept near 100% over 20 hops, another fell to 64% (measured).
- Retrieval rate depended strongly on the content of the carrier message and on the embedding model (measured).
- Virtual Donkey: TPR 1.0 at FPR 0.015 in distribution; AUC 0.96-1.0 on unseen jailbreak styles and payloads, 0.79-0.97 on a different email corpus. Not tested against adaptive attackers (authors' caveat).

## Methods and models

LangChain client, vector store with cosine similarity, five embedding models, three generation modes (new email, enrichment, reply). Hop chains simulated by passing one hop's output as the next hop's input across random permutations of the 20 mailboxes. Guardrail: logistic regression, naive Bayes and decision stump on BLEU, METEOR and ROUGE-L overlap scores.

## Limitations and open questions

The injected text and leaked data are visible to a human reader. The guardrail relies on near-verbatim copying, so paraphrasing propagation would weaken it. Lab ecosystem only, not deployed products.

## Relevance to us

Q3: this is the canonical "persistent store plus self-replication" mechanism. A fork that explores a hostile domain and caches what it reads in a retrieval memory is structurally one of these assistants; if the parent merges that memory, the injected item is retrieved during the parent's later work. The measured per-hop decay is a data point for how much an injection degrades across one fork-to-parent hop. Q2: an input/output overlap check is a cheap per-merge filter for returning memories, but it assumes verbatim replication, which [[papadopoulos-2026-mind]] shows is only one of several propagation styles. Successors: [[zhang-2026-agentworm]] (configuration-file persistence in a production framework), [[lee-2024-prompt]] (within one multi-agent system), [[gu-2024-agent]] (image-based infectious jailbreak).

## Notes from dmarz/fm-memory-injection

Abstract re-read 2026-10-03 for the memory-injection lane. The worm spreads because each compromised assistant writes the self-replicating prompt into the RAG store of the next application, so memory is the transmission medium. The Virtual Donkey guardrail (TPR 1.0, FPR 0.015 per the abstract) is a detector on the propagation path. In fork-merge terms that corresponds to inspecting what a sub-agent returns before merge (Q2 gate), and the abstract claims it is robust to out-of-distribution worms. For the memory-side mechanics of how a payload gets stored, see [[dong-2025-memory]] and [[srivastava-2025-memorygraft]]. For defences that gate private-to-shared promotion, see [[xiong-2026-maple]].

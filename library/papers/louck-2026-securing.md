---
id: louck-2026-securing
type: paper
title: 'Securing LLM-Agent Long-Term Memory Against Poisoning: Non-Malleable, Origin-Bound Authority with Machine-Checked Guarantees'
authors: [Yedidel Louck]
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2606.24322
doi: null
arxiv: '2606.24322'
cite: 'Louck, Y. (2026). Securing LLM-Agent Long-Term Memory Against Poisoning: Non-Malleable, Origin-Bound Authority with Machine-Checked Guarantees. arXiv preprint arXiv:2606.24322.'
topics: [fork-merge-security, sybil-resistance]
added_by: dmarz/fm-memory-injection
accessed: 2026-10-03
read_depth: skim
relevance: 5
citations: 16  # Semantic Scholar, 2026-10-03
code: []
---

## Summary

The paper argues that memory-poisoning defences which decide a memory item's authority from its content (detectors, trust scores) or from its derivation lineage are unsound. An attacker can launder an untrusted origin through three channels: the agent's own summarisation of the content, a trusted tool echoing it, and "manufactured corroboration" (several planted untrusted items that look like independent agreement). A machine-checked separation theorem in TLA+ follows. T1: no content- or lineage-based defence is sound under laundering. T2: binding origin at write time is necessary. T3: non-malleable origin-bound authority plus Sybil-resistant, corroboration-gated elevation is sufficient. The construction, TMA-NM, labels each write by authenticated channel (untrusted ingestion gets no authority to act) and propagates untrust through tool calls. It lets an untrusted-origin value drive a consequential action only if at least k=2 independent trusted principals corroborate it, or the user gives a fresh authorisation bound to that action. Writes and verdicts go to a hash-chained log.

## Contribution

It names corroboration as a laundering channel and makes corroboration Sybil-resistant. Corroborators must come from distinct authenticated channels and administrative domains with no shared upstream source, and repeated untrusted items never count.

## Key results

Measured (8 frontier models from 6 vendors, pooled):
- Undefended ASR is 84% direct and 68% laundering. A content trust score gives 0% direct but 68% laundering. A lineage defence (MemLineage) gives 0% and 47%. Capability IFC in the style of CaMeL/Fides gives 84% and 68%. TMA-NM gives 0% and 0%, with 100% legitimate utility.
- 0 of 192 per laundering channel for TMA-NM.
- On reproduced published attacks (MemMorph, MemoryGraft, Trojan Hippo, Conversational Trojan), ASR is 38.2% undefended and 0% for TMA-NM.
- The gate decision takes about 1.3 microseconds with no model call.

## Methods and models

The proof covers a finite model (3 slots, at most 2 sessions, k=2) with an inductive invariant, not a fully mechanised unbounded proof. A cross-defence, cross-attack, cross-model benchmark and the TLA+ models are released (not opened).

## Limitations and open questions

It relies on a correct origin-labelling oracle (assumption A1). Untrusted memory can still colour free-text answers, because only the retrieval-to-action path is gated. Value attribution uses a text proxy that an obfuscating adversary might evade. A value reconstructed in context from fragments may escape tracking. Single author.

## Relevance to us

Directly relevant to Q2, and the closest to a Byzantine-style k-of-n rule for memory. A value carried home by one sub-agent would have no authority to act until k independent principals corroborate it. The paper's independence test (distinct administrative domain, no shared upstream source) is the crux for fork-merge. Sub-agents forked from the same parent and exploring the same hostile domain share both a domain and an upstream source, so under this rule they would not count as independent corroborators of each other. For Q2 this means the threshold has to be over independent evidence channels, not over sub-agent count (inference from the paper's definition). The laundering result also bears on Q3. A compromised sub-agent's own summary is exactly the "self-summarisation" channel, so a parent that trusts a sub-agent's digest of what it learned is laundering by construction. Compare [[sharma-2026-smsr]] (randomised threshold) and [[zhan-2026-when]] (authority lost at consolidation). On manufactured consensus see the sybil-resistance notes on [[lee-2024-prompt]].

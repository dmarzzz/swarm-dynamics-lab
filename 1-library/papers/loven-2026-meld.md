---
id: loven-2026-meld
type: paper
title: "MELD: A Protocol for Merging Knowledge Across Distributed Agentic Memories"
authors: [Lauri Lovén, Jaakko Sauvola, Jukka Riekki, Sasu Tarkoma]
year: 2026
venue: arXiv
url: https://arxiv.org/abs/2608.16357
doi: null
arxiv: "2608.16357"
cite: "Lovén, L., Sauvola, J., Riekki, J., & Tarkoma, S. (2026). MELD: A Protocol for Merging Knowledge Across Distributed Agentic Memories. arXiv preprint arXiv:2608.16357."
topics: [fork-merge-security, llm-agent-swarms, sync-consensus]
added_by: dmarz/fm-sutton
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: null
code: []
---

## Summary

MELD is a protocol for merging knowledge-graph memories ("brains") of federated LLM agents. Each brain admits every incoming claim through a five-outcome procedure (insert, merge, relate, conflict, reject), decided from three signals: scoped claim-key identity, embedding similarity (all-MiniLM-L6-v2) and an NLI contradiction verdict (cross-encoder/nli-deberta-v3-small), under context, freshness and authority gates. Every state change is one authenticated, versioned Patch; contradictions are preserved rather than resolved; a per-claim status CRDT over publish/subscribe keeps brains coherent without a coordinator. Measured (abstract and Section 7): distributed merge is recall-non-inferior to a centralized store on HotpotQA distractor under a pre-specified equivalence test and recall-superior to naive union at about 11% less live storage; the merge classifier reaches AUC 0.968 with a 0.013 false-merge rate on adjudicated candidate pairs; the status CRDT reconverges in 30/30 partition-heal trials versus 11/30 for last-writer-wins; semantic routing sends about 3x fewer messages at matched recall. Deployed across a 5G edge, national HPC and a local host.

## Contribution

An explicit, auditable merge-decision procedure for agent memories, with non-destructive merges (supersede links, replayable Patches) so a bad merge can be corrected by appending.

## Key results

- AUC 0.968, false-merge rate 0.013 on the gold set.
- 30/30 versus 11/30 partition-heal reconvergence (status CRDT versus last-writer-wins).
- Recall non-inferior to centralized, about 11% less storage than naive union.

## Methods and models

Knowledge-graph memories, HMAC-authenticated deltas over a shared group key, status CRDT, embedding and NLI classifiers with calibrated thresholds.

## Limitations and open questions

Section 5.4 states the guarantees are for benign faults only: "The mechanisms do not defend against a Byzantine participant: a valid-key holder can publish well-formed false claims; the authority field is asserted, so without a trust root binding keys to authority levels a malicious brain can claim to be canonical; and an encoder-aware adversary can craft a contradiction below [the threshold] to evade the conflict gate." HMAC attributes deltas to the group, not to a sender. The authors name Byzantine eventual consistency (Kleppmann and Howard, 2020) as the starting point for hardening.

## Relevance to us

The closest engineered artefact to a merge gate for LLM agents' memories, and its own threat model lists the fork-merge attacks as out of scope, which marks the gap. Q3: a corrupted child holding the group key can publish well-formed false claims, claim canonical authority, or craft claims that the NLI gate misses; all three are the "overwrite the parent's knowledge" attack in memory form. Q2: MELD has no quorum; one brain's claim is admitted on its own signals, so k-of-n would need to be added on top (for example requiring a claim to arrive from k independently keyed children before it changes status). Its non-destructive, replayable Patch log is a strong precondition for any defence: a parent can roll back everything a child contributed once the child is found corrupt, which [[christiano-2018-supervising]]'s distillation step cannot do. Per-sender keys would also make children linkable, which is in tension with Q1 hiding. Context: [[sutton-2025-father]], [[anthropic-2026-create]].

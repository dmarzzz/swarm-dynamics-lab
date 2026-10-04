---
id: kleppmann-2022-making
type: paper
title: "Making CRDTs Byzantine Fault Tolerant"
authors: ["Martin Kleppmann"]
year: 2022
venue: "9th Workshop on Principles and Practice of Consistency for Distributed Data (PaPoC '22)"
url: https://martin.kleppmann.com/papers/bft-crdt-papoc22.pdf
doi: "10.1145/3517209.3524042"
arxiv: null
cite: "Kleppmann, M. (2022). Making CRDTs Byzantine fault tolerant. In Proceedings of the 9th Workshop on Principles and Practice of Consistency for Distributed Data (PaPoC '22), pp. 8-15. ACM."
topics: [fork-merge-security, sync-consensus, sybil-resistance]
added_by: dmarz/fm-mobile-agents
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: "16 (Crossref, 2026-10-03)"
code: []
---

## Summary

A short position paper showing how operation-based CRDTs can be retrofitted to keep Strong Eventual Consistency when any number of peers are Byzantine. Two mechanisms do the work. First, every update is identified by the hash of its bytes and names its causal predecessors by hash, so updates form a Merkle DAG like a Git history; two correct nodes that exchange head hashes and find them equal have provably delivered the same set of updates, and equivocation (one sender, one sequence number, two different updates) can no longer fool version vectors. Second, any validity check on an update must be a deterministic function of the update and of before(u), the set of its hash-reachable ancestors, never of the receiver's full local state, so all correct replicas reach the same accept or reject decision. No experiments; correctness of the full scheme is stated as a conjecture.

## Contribution

Moves the "how many faulty peers can a merge tolerate" question out of the 3f+1 regime: for state that only needs convergence (not agreement on a single total order), merging can be made safe with no bound on the number of Byzantine contributors and hence no Sybil defence. Builds directly on [[kleppmann-2020-byzantine]].

## Key results

- Shows by example (Figure 1) that version vectors are unsafe under equivocation: two correct nodes can hold identical vectors over different update sets.
- Byzantine reliable broadcast gives a stronger property than CRDTs need and costs the n > 3f bound; CRDT eventual delivery needs no quorum vote.
- With 256-bit hashes and up to three heads, a node's whole delivered set is summarised in under 100 bytes.
- Hash-of-update IDs make duplicate IDs impossible without a hash collision.
- Validity decisions based only on before(u) guarantee convergence; updates from correct nodes are always valid under this rule (argued, not proven for specific CRDTs).
- Related work comparison: Zhao et al. and ASPAS need 3f+1 replicas; Matrix Event Graph and Merkle Search Trees also tolerate arbitrary Byzantine counts.

## Methods and models

Asynchronous P2P model with unknown, changing membership, fair-loss links, authenticated pairwise channels, and unbounded Byzantine nodes. Correctness is Strong Eventual Consistency (eventual delivery, convergence, termination). Analysis is by construction and argument, with a forward reference to the proofs in [[kleppmann-2020-byzantine]] for the hash-graph reconciliation.

## Limitations and open questions

The guarantee is convergence, not safety of content. A Byzantine peer's update that passes the validity predicate is merged by every correct replica; the scheme ensures everyone agrees, including on the poison. The author leaves proofs for specific CRDTs, performance measurement, and the general claim (any op-based CRDT can be fixed this way) as conjecture. Eventual delivery still requires that correct nodes are connected through correct nodes (eclipse is out of scope).

## Relevance to us

Q2: this is the cleanest statement that a merge does not need a k-of-n threshold when the merged state is append-only and conflict-free; the threshold question only arises for non-monotone decisions (overwrite a belief, change a goal). For a parent re-absorbing sub-agents, it suggests splitting state into a grow-only evidence log (mergeable from any number of corrupted children, with provenance by hash) and a small set of decisions that need quorum. Q3: it also shows the residual attack surface precisely: anything that passes the deterministic validity predicate gets in everywhere, so the attacker's target is the predicate, which for LLM memory is a semantic check rather than a syntactic one. Q1: content-addressed DAGs make provenance of each merged item checkable, which is the opposite of hiding; hiding would need to sit at the transport layer. See also [[jacob-2021-conflict-free]], [[mahajan-2010-depot]], [[li-2004-secure]], [[douceur-2002-sybil]], [[castro-1999-practical]].

## Notes from dmarz/fm-code-bench

An instructional Rust implementation is catalogued as [[gh-jackyzha0-bft-json-crdt]]; I ran its byzantine tests (3 passed: equivocation, forged update, path update). Running it made one boundary concrete for Q2: hash-chained, signed ops stop forgery and equivocation, but a validly signed malicious op from a compromised replica is applied like any other, so BFT CRDTs guarantee convergence, not content integrity. A quorum-based alternative is [[gh-davidrusu-bft-crdts]] (secure broadcast layer).

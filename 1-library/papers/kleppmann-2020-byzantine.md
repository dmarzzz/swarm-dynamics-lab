---
id: kleppmann-2020-byzantine
type: paper
title: "Byzantine Eventual Consistency and the Fundamental Limits of Peer-to-Peer Databases"
authors: ["Martin Kleppmann", "Heidi Howard"]
year: 2020
venue: "arXiv preprint (cs.DC)"
url: https://arxiv.org/pdf/2012.00472
doi: null
arxiv: "2012.00472"
cite: "Kleppmann, M., & Howard, H. (2020). Byzantine Eventual Consistency and the Fundamental Limits of Peer-to-Peer Databases. arXiv:2012.00472 [cs.DC]."
topics: [fork-merge-security, sync-consensus, sybil-resistance]
added_by: dmarz/fm-mobile-agents
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: null
code: [gh-ept-byzantine-eventual]
---

## Summary

Defines Byzantine Eventual Consistency (BEC): self-update, eventual update, convergence, atomicity, authenticity, causal consistency and invariant preservation, required only of correct replicas, with any subset of replicas Byzantine. The main theorem (3.1) says a fault-tolerant replication algorithm that ensures BEC exists if and only if the set of transactions run by correct replicas is I-confluent with respect to every application invariant (Bailis et al.'s invariant confluence, carried into the Byzantine setting). The positive side is a Byzantine causal broadcast built on a signed hash DAG with a reconciliation protocol (Algorithm 1) and a Bloom-filter optimisation (Algorithm 2), proved correct in appendices. The negative side is a partition-style impossibility proof: if two concurrent transactions each preserve an invariant but their merge violates it, Byzantine replicas can withhold information until both commit. Measured in a 4-replica in-memory simulation (600 reconciliations per point): Algorithm 2 needs 1.03 round trips on average (96.7% in one round trip, 3.2% two, 0.04% three or more) and about 1 kB overhead per reconciliation over an optimal algorithm, using 10 bits per Bloom entry and 7 hash functions. The prototype runs only correct replicas; Byzantine behaviour is not simulated in the evaluation.

## Contribution

A characterisation result: exactly the I-confluent part of an application can be merged safely from arbitrarily many Byzantine peers, and anything non-I-confluent (for example a balance that must stay non-negative) needs consensus and therefore an honest-fraction bound and Sybil defence. Prior Byzantine CRDT and secure broadcast work assumed 3f+1 replicas; Depot ([[mahajan-2010-depot]]) and OldBlue tolerated arbitrary faults but without invariants.

## Key results

- Theorem 3.1: BEC with invariant preservation is achievable with any number of Byzantine replicas iff all transactions are I-confluent with respect to all invariants (proved in both directions).
- Version vectors are corruptible by an equivocating replica (Figure 4); hash-of-predecessor DAGs are not, assuming collision resistance.
- A faulty replica in a reconciliation can at worst omit heads or add well-formed signed messages; it cannot stop two correct replicas from later converging (argued in Section 5.4, proved in Appendix A).
- Table 1 classifies updates as safe or unsafe per invariant type (check constraint, non-negative value, foreign key, uniqueness, materialised view).
- Evaluation numbers as in the summary; performance under actual Byzantine behaviour is left open.

## Methods and models

Asynchronous model, signatures with distinct per-replica keys, no central membership control, correct replicas assumed to form one connected component (otherwise eclipse attacks block delivery). Proofs by construction plus an indistinguishability argument for the impossibility direction. Prototype in a single process simulating the network; source at [[gh-ept-byzantine-eventual]].

## Limitations and open questions

Open questions the authors list: how to guarantee correct replicas stay connected, how to formalise the safety table, and whether "coordination-free in the crash model" equals "Sybil-immune in the Byzantine model" in general. Unbounded log growth unless every replica's heads are known. No adversarial evaluation.

## Relevance to us

Q2: the most directly useful formal result in this lane. It converts "how many sub-agents must an attacker corrupt before the merge corrupts the parent?" into "which of the parent's updates are I-confluent?". For I-confluent state (add-only observations, provenance-tagged facts) the answer is that no threshold is needed because no number of corrupted children can break the invariants; for non-I-confluent state (goal changes, deletions, identity or key rotation) a quorum is unavoidable and the classic n > 3f style bounds come back ([[castro-1999-practical]]). Q3: an attacker who controls a returning child wants to push non-I-confluent updates through a path the parent treats as mergeable; the theorem says where to look. Q1: the connectivity assumption is an eclipse condition; an attacker who controls all paths between a returning child and the parent can block or reorder delivery. Related: [[kleppmann-2022-making]], [[jacob-2021-conflict-free]], [[li-2004-secure]], [[douceur-2002-sybil]].

## Notes from dmarz/fm-code-bench

Two code bases implement related ideas: [[gh-jackyzha0-bft-json-crdt]] (signed, hash-linked ops over a JSON CRDT; tests run) and [[gh-davidrusu-bft-crdts]] (CRDTs and AT2 over a secure broadcast layer). The second adds acknowledgement quorums, trading the any-number-of-faults convergence guarantee for agreement, which is the trade a fork-merge parent faces if it wants children's contributions co-signed by siblings (Q2).

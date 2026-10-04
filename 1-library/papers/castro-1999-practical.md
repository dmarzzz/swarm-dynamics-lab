---
id: castro-1999-practical
type: paper
title: Practical Byzantine Fault Tolerance
authors:
- Miguel Castro
- Barbara Liskov
year: 1999
venue: Proceedings of the Third Symposium on Operating Systems Design and Implementation (OSDI 1999)
url: https://web.archive.org/web/2020/http://pmg.csail.mit.edu/papers/osdi99.pdf
doi: null
arxiv: null
cite: 'Castro, M., & Liskov, B. (1999). Practical Byzantine Fault Tolerance. In Proceedings of the Third Symposium on Operating Systems Design and Implementation (OSDI), New Orleans, USA, February 1999.'
topics:
- fork-merge-security
- sync-consensus
added_by: dmarz/fm-bft-aggregation
accessed: '2026-10-03'
read_depth: skim
relevance: 4
citations: 3282  # OpenAlex cited_by_count, 2026-10-03; shadow/sol-g51
code: []
---

## Summary

PBFT, a state machine replication algorithm that tolerates Byzantine faults in asynchronous networks such as the Internet. It provides safety (linearizability) and liveness when at most floor((n-1)/3) of n replicas are faulty, does not rely on synchrony for safety, uses MACs instead of public-key signatures in normal operation, and needs one round trip for read-only and two for read-write operations. A Byzantine-fault-tolerant NFS built on it was only 3 percent slower than unreplicated NFS on the Andrew benchmark. The system model explicitly assumes independent node failures and notes that under malicious attack this requires different implementations, operating systems, root passwords and administrators per replica, citing N-version programming.

## Contribution

Made BFT replication practical and fast in asynchronous settings, with the 3f + 1 bound as an engineering parameter.

## Key results

- Measured: BFS (Byzantine-fault-tolerant NFS) 3 percent slower than standard NFS in normal operation.
- Design: safety holds regardless of message delays; liveness needs eventual synchrony.
- Stated in the conclusion: the approach cannot mask a software error that occurs at all replicas, only errors that occur independently.
- Noted in related work: earlier systems that exclude replicas via failure detectors can be attacked by slowing correct replicas until they are misclassified, so an attacker controlling one replica can push the faulty count past one third.

## Methods and models

State machine replication with a primary, view changes and checkpoints. Skimmed: abstract, system model, introduction, related work and conclusions; protocol details not read.

## Limitations and open questions

The f < n/3 guarantee rests on the independent-failure assumption the authors state; the conclusion concedes common-mode errors are not masked.

## Relevance to us

Q2. The practical template for "an attacker must corrupt more than a third of the parts": it works only if parts fail independently, and the authors' own recipe for independence is diversity of implementation and administration. For a parent forking copies of one LLM, that recipe is unavailable by construction unless the forks use different models, prompts or tools. The failure-detector attack in their related work also maps onto fork-merge: an attacker who can make honest returning sub-agents look faulty (late, inconsistent) can get them excluded and gain a relative majority. See [[knight-1986-experimental]], [[avizienis-1985-n-version]], [[lamport-1982-byzantine]].

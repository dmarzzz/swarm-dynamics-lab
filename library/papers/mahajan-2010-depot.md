---
id: mahajan-2010-depot
type: paper
title: "Depot: Cloud storage with minimal trust"
authors: ["Prince Mahajan", "Srinath Setty", "Sangmin Lee", "Allen Clement", "Lorenzo Alvisi", "Mike Dahlin", "Michael Walfish"]
year: 2010
venue: "9th USENIX Symposium on Operating Systems Design and Implementation (OSDI 2010)"
url: https://www.usenix.org/legacy/event/osdi10/tech/full_papers/Mahajan.pdf
doi: null
arxiv: null
cite: "Mahajan, P., Setty, S., Lee, S., Clement, A., Alvisi, L., Dahlin, M., & Walfish, M. (2010). Depot: Cloud storage with minimal trust. In Proceedings of the 9th USENIX Symposium on Operating Systems Design and Implementation (OSDI '10). USENIX Association. Extended version: ACM Transactions on Computer Systems 29(4), 2011, doi:10.1145/2063509.2063512."
topics: [fork-merge-security, sync-consensus]
added_by: dmarz/fm-mobile-agents
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "117 (Crossref, TOCS 2011 version, 2026-10-03)"
code: []
---

## Summary

Depot is a key-value cloud store that tolerates buggy or malicious behaviour by any number of clients or servers while still giving correct clients safety and liveness guarantees. Its key move is to "reduce misbehaviour to concurrency": every update is signed and names its antecedents and the state its writer saw, so the only thing a faulty node can do undetectably is fork, showing divergent histories to different nodes. Unlike earlier fork-consistent systems that detect forks and then stall, Depot lets correct clients join forks, treating the two branches as logically concurrent updates by two virtual nodes and resolving them with the same machinery used for disconnected operation. The resulting contract is Fork-Join-Causal (FJC) consistency, a slight weakening of causal consistency. Other properties (bounded staleness, durability, integrity via authorisation, snapshotting against spurious updates by faulty clients, garbage collection, eviction of faulty nodes) are layered on FJC. It adds a few hundred bytes of metadata per update and object. I read the abstract, introduction, design overview and the list of layered properties; I did not read the evaluation in detail.

## Contribution

The first storage system I found that explicitly treats a Byzantine fork as something to merge rather than only detect, with a named consistency model for that merge.

## Key results

- Safety for correct clients regardless of how many other nodes are faulty (claimed and argued in the paper).
- Faulty behaviour reduced to forking; forks joined as concurrent virtual nodes.
- Metadata overhead of a few hundred bytes per update (reported).
- Teapot variant gives many of the guarantees on an unmodified S3 (reported).

## Methods and models

System design, protocol specification, prototype and evaluation under injected faults (evaluation not read in detail).

## Limitations and open questions

Kleppmann and Howard note that the published descriptions were not detailed enough for them to reproduce Depot's algorithm and that FJC is specific to a key-value model and does not handle invariants ([[kleppmann-2020-byzantine]]). Reads can still be unavailable if no correct reachable node holds the object.

## Relevance to us

Q2 and Q3: the "fork-join" vocabulary maps directly onto Sutton's split-and-merge. Depot's answer to a corrupted branch is not a k-of-n vote but to merge it as a separate virtual participant with its own provenance, keep all branches, and use snapshots and eviction to limit damage. For a parent agent this suggests keeping each child's contribution as a separately attributed branch that can be later quarantined or evicted, instead of folding it irreversibly into one shared memory. Q1: not addressed. Related: [[li-2004-secure]], [[kleppmann-2022-making]], [[jacob-2021-conflict-free]].

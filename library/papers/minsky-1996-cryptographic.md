---
id: minsky-1996-cryptographic
type: paper
title: "Cryptographic Support for Fault-Tolerant Distributed Computing"
authors: ["Yaron Minsky", "Robbert van Renesse", "Fred B. Schneider", "Scott D. Stoller"]
year: 1996
venue: "Cornell University Department of Computer Science Technical Report TR96-1600"
url: https://ecommons.cornell.edu/items/058b3547-d988-4e20-bc1b-2a2c123571d9
doi: null
arxiv: null
cite: "Minsky, Y., van Renesse, R., Schneider, F. B., & Stoller, S. D. (1996). Cryptographic Support for Fault-Tolerant Distributed Computing. Technical Report TR96-1600, Department of Computer Science, Cornell University, July 1996."
topics: [fork-merge-security, sync-consensus, collective-decision]
added_by: dmarz/fm-mobile-agents
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: null
code: []
---

## Summary

A short Cornell report (read from the PostScript bitstream on eCommons) on making an agent computation that visits a pipeline of hosts tolerant to malicious hosts. Each pipeline stage is replicated; a host in stage i takes the majority of the inputs it receives from stage i-1 and forwards to all of stage i+1, so the computation "heals" and tolerates faulty values from a minority of replicas in each stage. Voting alone fails: any two faulty hosts can claim to be the last stage and push a majority of bogus agents to the actuator, so agents must carry a privilege known only to source and actuator. Carrying it as an (n, k) threshold secret share fails too, because faulty minorities before and after a vote can steal different shares and pool them; the fix is to re-split (re-share) the fragments at every vote, with chained authentication or proactive renewal to avoid exponential message growth, and verifiable secret sharing so a faulty host cannot destroy the secret. Measured on 14 SparcStation 20s over 10 Mbit Ethernet with 1, 3, 5, 7 replicas: voting every N hosts amortises synchronisation, with most gain by N = 10; with a 2% chance per host of being 350 times slower, an unreplicated agent slowed about sixfold, 3 replicas cut the slowdown to about 20%, and 7 replicas made it negligible.

## Contribution

The first concrete k-of-n construction for agents that leave and must come back: per-stage majority voting combined with threshold secret sharing that is re-split at each vote, so corruption cannot accumulate across stages. Precursor of the Schneider-Zhou distributed-trust line ([[schneider-2005-implementing]]).

## Key results

- With 2k-1 replicas per stage, tolerates faulty values from a minority (up to k-1) in each stage, not just overall (argued).
- Naive per-replica share forwarding lets faulty hosts on both sides of a vote combine shares; resharing at each vote prevents this.
- Resharing by concatenation multiplies message size by 2k-1 per stage; two alternative protocols give linear or constant message size.
- Performance measurements as in the summary (300-round averages, variance about 0.1%). Replication can make the computation faster than a single copy because voters wait for the median correct replica, not the slowest.

## Methods and models

Deterministic stage computations, faulty hosts that can lie and masquerade as other faulty hosts but cannot forge correct hosts' identities or read their secrets. Cluster experiment simulating agent moves as UDP messages.

## Limitations and open questions

Assumes replicas fail independently; [[yee-1997-sanctuary]] argues this is unrealistic when replicas share an operator or software. Requires deterministic stages so outputs can be compared byte for byte. Protocols are outlined, not proved.

## Relevance to us

Q2: this is the closest prior design to a Byzantine threshold on fork-merge. Read as: send n sub-agents, merge only what a majority agree on at each checkpoint, and refresh any shared credential at each checkpoint so a corruption in one leg cannot be combined with one in another. Two transfer problems for LLM sub-agents: outputs are not deterministic, so majority voting needs a semantic equivalence test, and copies of the same model are not independent, so the minority-per-stage bound may be optimistic. Q3: the attack on naive sharing (collusion across a vote boundary) is a template for an attacker who corrupts one child early and another late. Q1: not addressed. Related: [[sander-1998-protecting]], [[jansen-1999-mobile]] (summarises this as itinerary recording with replication and voting), [[castro-1999-practical]], [[blanchard-2017-byzantine]].

---
id: schneider-2005-implementing
type: paper
title: "Implementing Trustworthy Services Using Replicated State Machines"
authors: ["Fred B. Schneider", "Lidong Zhou"]
year: 2005
venue: "IEEE Security & Privacy"
url: https://www.cs.cornell.edu/fbs/publications/TrustSurvey.pdf
doi: "10.1109/msp.2005.125"
arxiv: null
cite: "Schneider, F. B., & Zhou, L. (2005). Implementing Trustworthy Services Using Replicated State Machines. IEEE Security & Privacy, 3(5), 34-43."
topics: [fork-merge-security, sync-consensus, sybil-resistance]
added_by: dmarz/fm-mobile-agents
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: "15 (Crossref, 2026-10-03)"
code: []
---

## Summary

A survey article (headed "Distributed Trust" in the PDF) on what has to change when Byzantine-fault-tolerant replicated state machines are asked to resist attacks rather than random failures. The plain approach (2t+1 replicas, majority output) silently assumes processor independence: the probability that m replicas are compromised is about Pr1^m. Under attack, a vulnerability in one replica is usually in all, so the probability that more than t are compromised is closer to Pr1 and replication does not improve trustworthiness; replication also multiplies the places a secret is stored. The article walks through the repairs: proactive recovery that turns "at most t compromised over the lifetime" into "at most t per window of vulnerability"; (n, t+1) secret sharing and threshold signatures so the service key is never materialised at one server (properties TC1 and TC2); proactive secret sharing against a mobile adversary that moves from server to server; server key refresh via trusted hardware, offline keys, or attack awareness; adversary structures that replace the threshold t with explicit sets of servers assumed jointly corruptible (for example all replicas on one OS or under one operator); diversity by multiple implementations, pre-existing diverse components, or automatic randomisation; and three ways around FLP for coordination (abandon consensus, randomise, or sacrifice liveness). It closes with tables of systems (BFS, COCA, CODEX, E-Vault) and toolkits (BFT, ITTC, Phalanx, IBM proactive toolkit, Sintra).

## Contribution

Names and organises the "distributed trust" paradigm: trust an ensemble more than any member, but only to the extent that member compromises are independent. This is the conceptual answer to whether a k-of-n threshold helps.

## Key results

- Independence argument: with shared vulnerabilities, P(more than t compromised) is about Pr1, not Pr1^m (stated, not measured).
- A mobile adversary defeats fixed secret shares over time; periodic independent resharing with deletion forces it to compromise more than t servers within one window.
- Adversary structures generalise thresholds; protocols for thresholds usually generalise, but identifying the right structure needs knowledge of common vulnerabilities in COTS components.
- Cites Knight and Leveson's finding that independent teams from one spec produce the same bugs, as a limit on design diversity.
- Asynchronous proactive secret sharing (APSS) avoids consensus by having servers keep all new sharings.

## Methods and models

Survey and synthesis; no new experiments. Model: hosts and channels, compromised components fully controlled by the adversary, asynchronous versus synchronous assumptions treated explicitly because DoS can break timing assumptions.

## Limitations and open questions

Short survey with a limited literature review by the authors' own statement. Does not address whether the single state machine's semantics can be abused, which the authors call open.

## Relevance to us

Q2: the core caution for any Byzantine merge threshold over sub-agents. Sub-agents forked from the same parent share weights, prompts and tools, so they share vulnerabilities; a prompt injection that works on one child likely works on all children that read the same content. A k-of-n merge rule then gives security close to that of a single child unless children are made diverse (different models, prompts, tool stacks, sources) or assigned to disjoint information domains, in which case an adversary structure (corruptible sets per domain) is the right model, not a count. Proactive recovery maps to periodically re-forking children from a clean parent snapshot rather than letting them accumulate state. Q1: the mobile adversary is the attacker who hops between children; resharing with deletion is a defence that does not need hiding. Related: [[minsky-1996-cryptographic]], [[yee-1997-sanctuary]], [[castro-1999-practical]], [[kleppmann-2020-byzantine]].

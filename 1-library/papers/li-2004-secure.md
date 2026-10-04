---
id: li-2004-secure
type: paper
title: "Secure Untrusted Data Repository (SUNDR)"
authors: ["Jinyuan Li", "Maxwell Krohn", "David Mazières", "Dennis Shasha"]
year: 2004
venue: "6th Symposium on Operating Systems Design and Implementation (OSDI '04)"
url: https://www.usenix.org/legacy/event/osdi04/tech/full_papers/li_j/li_j.pdf
doi: null
arxiv: null
cite: "Li, J., Krohn, M., Mazières, D., & Shasha, D. (2004). Secure Untrusted Data Repository (SUNDR). In Proceedings of the 6th Symposium on Operating Systems Design and Implementation (OSDI '04), pp. 121-136. USENIX Association."
topics: [fork-merge-security, sync-consensus]
added_by: dmarz/fm-mobile-agents
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: null
code: []
---

## Summary

SUNDR is a network file system that stores data on untrusted servers and lets clients detect unauthorised modification by malicious server operators or users. Instead of distributing trust over a threshold of honest servers, it vests write authority in users' public keys, so even an attacker with full control of the server cannot make clients accept altered contents of files the attacker cannot write. The protocol achieves fork consistency: a malicious server can show different clients divergent histories (fork them), but once forked, two clients can never again see each other's updates without detecting the fork. Motivated by real compromises of source repositories (Debian 2003, Apache, Gnome) and hosting sites such as SourceForge. The implementation performs comparably with NFS, sometimes better and sometimes worse. I read the abstract, introduction and the definition of fork consistency.

## Contribution

Introduced fork consistency, the strongest property achievable with a single untrusted server, and the template that Depot ([[mahajan-2010-depot]]) and Byzantine CRDTs later extend from "detect forks" to "join forks".

## Key results

- Fork consistency: integrity or consistency failures are detectable as soon as forked clients exchange any information (proved in the paper's model).
- Write authority bound to user keys rather than server honesty.
- Performance comparable with NFS (reported).

## Methods and models

Protocol design with version structures signed by users, file-system implementation and benchmarks.

## Limitations and open questions

A faulty server can keep forked clients permanently partitioned (no liveness for cross-fork visibility), which Depot and BEC later address.

## Relevance to us

Q1 and Q3: fork consistency formalises an attack the parent must expect when its children communicate through infrastructure the adversary controls: the adversary can partition children into separate views so that each looks internally consistent, and the corruption is detected only when the parent compares their histories. A merge protocol that compares signed histories across children gets this detection for free; one that merges summaries does not. Related: [[torres-arias-2016-omitting]], [[kleppmann-2020-byzantine]], [[jacob-2021-conflict-free]].

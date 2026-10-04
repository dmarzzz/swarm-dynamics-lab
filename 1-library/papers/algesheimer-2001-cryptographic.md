---
id: algesheimer-2001-cryptographic
type: paper
title: "Cryptographic Security for Mobile Code"
authors: ["Joy Algesheimer", "Christian Cachin", "Jan Camenisch", "Günter Karjoth"]
year: 2001
venue: "Proceedings 2001 IEEE Symposium on Security and Privacy (S&P 2001)"
url: https://people.cs.vt.edu/~kafura/cs6204/Readings/MobileAgents/CrytographicSecurityForMobileCode.pdf
doi: "10.1109/secpri.2001.924283"
arxiv: null
cite: "Algesheimer, J., Cachin, C., Camenisch, J., & Karjoth, G. (2001). Cryptographic security for mobile code. In Proceedings 2001 IEEE Symposium on Security and Privacy (S&P 2001), pp. 2-11. IEEE."
topics: [fork-merge-security]
added_by: dmarz/fm-mobile-agents
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "37 (Crossref, 2026-10-03)"
code: []
---

## Summary

IBM Zurich paper (read from a course-hosted author version dated August 2003; I read the introduction, model, impossibility argument and architecture overview). It formalises a mobile computation as an originator plus a sequence of hosts, each updating the agent state with a function g_j and producing a host output with h_j, all non-interactively. Proposition 1 shows that non-interactive secure mobile computing is impossible whenever a host learns anything that depends on the agent's state: the host can rerun the agent on different inputs and, for a shopping agent with a secret price threshold, recover the threshold by binary search. Encrypted-function approaches (Sander and Tschudin; later log-depth and polynomial-circuit extensions) only work when the originator alone receives output. The paper's fix is a minimally trusted generic "secure computation service" that evaluates Yao garbled circuits on behalf of agents, learns nothing about the computation, and must only be trusted not to collude with originator or host; it is presented as cheaper than tamper-proof hardware at every host. Applications sketched: comparison shopping and a generalised auction.

## Contribution

An impossibility result for software-only protection of "active" mobile code, and an architecture that replaces per-host trusted hardware with one generic, non-colluding third party.

## Key results

- Proposition 1: non-interactive secure mobile computing schemes do not exist when a host gets state-dependent output (proof by re-execution and binary search).
- Prior CEF schemes protect only state updates and final results, not outputs to hosts.
- The trusted-hardware alternative (Yee; Wilhelm et al.) requires all users to trust the hardware manufacturer and each module to execute code exactly once.
- The secure computation service is practical for small functions (claimed; I did not check their cost figures).

## Methods and models

Cryptographic model with simulation-based privacy definitions; construction from Yao's encrypted circuits and oblivious transfer. No large-scale measurement read.

## Limitations and open questions

Requires a party that does not collude; garbled circuits scale poorly with function size. Does not address integrity of what a host feeds in as input.

## Relevance to us

Q3: the re-execution argument is the formal core of a strong attack on a sub-agent in a hostile domain: the host controls the sub-agent's inputs and can reset and replay it as many times as it likes, so any decision rule the sub-agent carries (what to trust, when to report home, what to merge) can be learned and then targeted. This maps to an adversary iterating prompt injections offline against a captured copy until one works. Q2: the "one-execution" requirement on trusted hardware and the non-collusion assumption on the computation service are both threshold-style assumptions worth reusing (a third party that verifies a child's output before merge). Q1: if the parent's merge criteria are secret, this result says a host that can query the child repeatedly will learn them; hiding is not robust against a host with replay. Related: [[sander-1998-protecting]], [[yee-1997-sanctuary]], [[menetrey-2022-attestation]].

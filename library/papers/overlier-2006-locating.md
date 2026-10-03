---
id: overlier-2006-locating
type: paper
title: Locating Hidden Servers
authors: [Lasse Overlier, Paul Syverson]
year: 2006
venue: 2006 IEEE Symposium on Security and Privacy (S&P'06)
url: https://www.freehaven.net/anonbib/cache/hs-attack06.pdf
doi: 10.1109/sp.2006.24
arxiv: null
cite: Overlier, L., & Syverson, P. (2006). Locating hidden servers. 2006 IEEE Symposium on Security and Privacy (S&P'06). IEEE.
topics: [fork-merge-security, sybil-resistance]
added_by: dmarz/fm-unlinkability
accessed: 2026-10-03
read_depth: skim
relevance: 5
citations: 165 (Crossref, 2026-10-03)
code: []
---

## Summary

Overlier and Syverson attack the deployed Tor hidden-service protocol. An attacker runs one relay and repeatedly connects to the hidden server as a client, forcing the server to build fresh circuits; whenever the server happens to pick the attacker's relay as its first hop, a timing signature links the circuit to the server's IP. Using a single hostile node they located deployed hidden servers "in a matter of minutes". They propose entry guard nodes (a small, persistent set of first hops) and show that with three permanent preferred guards the attacker only ever sees the guards, though identifying the guards themselves "never took more than a few hours".

## Contribution

The first intersection attacks demonstrated on a deployed public anonymity network, and the origin of Tor's entry guard design.

## Key results

- One hostile relay plus a client that triggers repeated circuit construction is enough to locate a hidden server within minutes (measured on the live network).
- The attack works because the server re-randomises its first hop every circuit; a persistent guard set stops it unless the attacker owns a guard.
- With guards, all identified connections pointed to the three guards (Table 2), so the attacker learns the guards rather than the server; locating the guards took at most a few hours.
- Trade-off stated: a smaller guard set lowers the chance the attacker owns one but raises the chance all guards are monitored, DoSed, or fail.

## Methods and models

Live experiments on the 2006 Tor network (about 450 relays) with an attacker-controlled relay and client, plus timing-signature matching; analysis of guard-set size, layering, and permanence options.

## Limitations and open questions

Guards move the problem rather than removing it: an attacker who can DoS or compromise the guards returns to the original attack. The paper's results are for 2006 Tor; parameters differ today.

## Relevance to us

Q1, directly. A parent that reintegrates a freshly chosen sub-agent each cycle is in the hidden server's position: every fresh choice is another draw an attacker can wait for, so rotating which part returns leaks the parent over repeated rounds (the intersection logic formalised in [[wright-2004-predecessor]]). The guard result says the counter-intuitive defence is to keep a small, stable, trusted set of merge points or couriers and route all returns through them, and that this concentrates risk on the guards. Q3: the attack template, owning one relay and inducing repeated reconnection until the target routes through you, is the network-layer analogue of corrupting one sub-agent and waiting for it to be selected for merge. Builds on [[dingledine-2004-tor]].

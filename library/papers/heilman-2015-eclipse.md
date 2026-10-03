---
id: heilman-2015-eclipse
type: paper
title: "Eclipse Attacks on Bitcoin's Peer-to-Peer Network"
authors: ["Ethan Heilman", "Alison Kendler", "Aviv Zohar", "Sharon Goldberg"]
year: 2015
venue: "24th USENIX Security Symposium (USENIX Security 15), Washington, D.C., pp. 129-144"
url: https://www.usenix.org/system/files/conference/usenixsecurity15/sec15-paper-heilman.pdf
doi: null
arxiv: null
cite: "Heilman, E., Kendler, A., Zohar, A., & Goldberg, S. (2015). Eclipse Attacks on Bitcoin's Peer-to-Peer Network. In Proceedings of the 24th USENIX Security Symposium, Washington, D.C., August 12-14, 2015, pp. 129-144. USENIX Association. ISBN 978-1-939133-11-3."
topics: [sybil-resistance, sync-consensus]
added_by: dmarz/sybil-foundations
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: "869 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

The paper shows that an off-path attacker controlling enough IP addresses can monopolise all eight outgoing and up to 117 incoming connections of a public bitcoind 0.9.3 node. The attacker repeatedly connects from its addresses to fill the victim's "tried" table, floods the "new" table with unroutable "trash" addresses via ADDR messages, and waits for the victim to restart; the bias toward fresh timestamps then makes the victim pick attacker addresses. Probabilistic analysis, Monte Carlo simulation, measurements of live nodes and attacks on the authors' own mainnet nodes all agree, and the proposed countermeasures were partly deployed in bitcoind 0.10.1.

## Contribution

The first measured eclipse attack on a deployed cryptocurrency p2p network, with a cost model in IP addresses and attack time, and a set of countermeasures borrowed from botnet design (test-before-evict, feeler and anchor connections) that bound the attacker's success no matter how many addresses it controls. It moves the eclipse problem of [[singh-2006-eclipse]] from structured DHTs to unstructured gossip networks.

## Key results

- An infrastructure attacker with 32 distinct /24 blocks (8,192 addresses) or a botnet of 4,600 bots eclipses a victim with at least 85% probability in the attacker's worst case, independent of network size; 400 bots sufficed against the authors' live nodes.
- If those 8,192 nodes joined honestly, the chance of eclipsing a target would be about (8192/(7200+8192))^8 = 0.6%; for 3,000 bots about 0.006%. The attack works because of protocol details, not raw share.
- Freshness bias: with 72% of tried filled and 48 hours of attack, success is 90%; with uniform random selection 90% success would need 98.7% of tried.
- Holding 117 incoming connections costs about 4 bytes per second, because bitcoind accepted all incoming connections from one IP.
- Measured churn: live nodes' tried tables were at most about 8% full after 43 days; 17% of tried addresses were over 30 days old; only 5-28% of tried addresses were online.
- Experiments (Table 2): worst-case infrastructure attack 98% wins; worst-case 4,600-bot attack 100%; live 400-bot attack 84%.
- Countermeasures 1, 2 and 6 (deterministic random eviction, random selection, more buckets) shipped in bitcoind 0.10.1; after that, a botnet needs about 163K addresses for 50% success and 284K for 90% when tried is full of legitimate addresses. With test-before-evict, success is bounded by (1 - p*h/4096)^8 regardless of attacker size, where h is legitimate addresses and p their liveness.

## Methods and models

Reverse-engineered bitcoind 0.9.3 address management (tried: 64 buckets of 64, keyed on /16 group; new: 256 buckets keyed on source group). Analytical success probability q(f, f', tau_a, tau)^8; binomial and recurrence models for table filling; Monte Carlo (100 trials per point); 43-day measurement of five public nodes; attack experiments with reserved IP ranges against instrumented victims (worst case, transplant and live), 50 restarts each.

## Limitations and open questions

Requires the victim to restart (the authors argue restarts are common: upgrades, DoS, crashes). Only public-IP nodes are attacked directly. Network-level (BGP) attackers are out of scope. Countermeasures 3 and 4 were proposed as a patch, not deployed at publication.

## Relevance to us

This is the empirical anchor for "eclipse as isolating one agent's view" in any open agent gossip layer. Three lessons carry over to agent swarms and to Flashbots p2p infrastructure. Peer selection that favours recency lets an attacker win with a minority; uniform selection plus test-before-evict bounds influence regardless of identity count. Diversity limits on address groups (/16 buckets, at most a few connections per IP) act as a crude identity bound. Anchor connections (peers kept across restarts) are the agent analogue of trusted long-lived contacts. Churn, here node restarts, is the window of vulnerability; continuous agent spawning creates the same window. Bounds influence (test-before-evict, anchors) more than identities (/16 grouping). Related: [[marcus-2018-low-resource]], [[singh-2006-eclipse]], [[castro-2002-secure]], [[vyzovitis-2020-gossipsub]], [[gh-flashbots-buildernet-orderflow-proxy]], [[babaioff-2012-bitcoin]].

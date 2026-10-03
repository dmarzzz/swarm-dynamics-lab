---
id: dingledine-2004-tor
type: paper
title: 'Tor: The Second-Generation Onion Router'
authors: [Roger Dingledine, Nick Mathewson, Paul Syverson]
year: 2004
venue: 13th USENIX Security Symposium
url: https://svn.torproject.org/svn/projects/design-paper/tor-design.pdf
doi: 10.21236/ada465464
arxiv: null
cite: 'Dingledine, R., Mathewson, N., & Syverson, P. (2004). Tor: The second-generation onion router. Proceedings of the 13th USENIX Security Symposium, San Diego, CA.'
topics: [fork-merge-security, sybil-resistance]
added_by: dmarz/fm-unlinkability
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: 4051 (OpenAlex, 2026-10-03)
code: []
---

## Summary

The design paper for Tor, a low-latency circuit-based onion routing overlay. Clients build circuits hop by hop (telescoping) with per-hop ephemeral keys for forward secrecy, multiplex TCP streams over circuits, and use a small set of directory servers that sign a threshold consensus on which relays exist. It introduces location-hidden services reached through introduction points and rendezvous points, so a server can offer a service without revealing its IP. The paper reports an alpha network of 32 nodes (May 2004) and informal latency tests (cnn.com front page median 2.8 s through Tor versus 0.3 s direct).

## Contribution

Showed a deployable anonymity design that deliberately gives up protection against a global passive adversary and end-to-end timing confirmation in exchange for interactive latency, and gave a concrete rendezvous design for responder anonymity.

## Key results

- Threat model: an adversary who observes some fraction of the network and controls some fraction of relays; explicitly not secure against end-to-end timing correlation.
- Hidden services: Bob advertises introduction points; Alice picks a rendezvous point; neither learns the other's location. Bob can give different clients different (unadvertised) introduction points so an attacker must disable all of them.
- If an adversary controls m of N relays, it can correlate at most (m/N)^2 of traffic (as stated in the attack list).
- Directory authorities: clients trust a directory signed by a threshold (majority) of directory servers; subverting more than half lets an attacker list arbitrary relays.
- "Iterated compromise" is limited by circuit lifetime and forward secrecy; "jurisdictional arbitrage" makes legal coercion of a whole path harder.

## Methods and models

System design and attack-by-attack analysis (Section 7); deployment notes and informal timing measurements (Section 8). I read the goals, threat model, rendezvous, directory, attacks, deployment and open-problem sections and skimmed the cell and circuit mechanics.

## Limitations and open questions

No cover traffic, no mixing; end-to-end confirmation defeats it by design. Path-rotation frequency is left open (frequent rotation invites predecessor and intersection attacks, see [[wright-2004-predecessor]]); hidden-service location was later broken by exactly that route ([[overlier-2006-locating]]). Directory servers are a small trusted set.

## Relevance to us

Q1. A parent agent that wants to receive work back from field sub-agents without exposing its own location maps onto a hidden service: sub-agents report to rendezvous points, never to the parent's address, and different sub-agents can be handed different introduction points so that capturing one sub-agent reveals one entry point only. The paper's own analysis shows what this hides (location, linkage) and what it does not (timing correlation by an observer at both ends). Q2: the directory-authority majority signature is a k-of-n threshold on who is admitted, and the (m/N)^2 correlation figure shows how hiding degrades with the fraction of compromised relays. Builds on [[chaum-1981-untraceable]]; contrasts with mix-based [[piotrowska-2017-loopix]]; the latency-anonymity-bandwidth bound is [[das-2018-anonymity]]. Tor's later DoS work is in [[torproject-2021-res]].

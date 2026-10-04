---
id: jansen-1999-mobile
type: paper
title: "Mobile Agent Security"
authors: ["Wayne Jansen", "Tom Karygiannis"]
year: 1999
venue: "NIST Special Publication 800-19 (withdrawn August 1, 2018)"
url: https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-19.pdf
doi: "10.6028/nist.sp.800-19"
arxiv: null
cite: "Jansen, W., & Karygiannis, T. (1999). Mobile Agent Security. NIST Special Publication 800-19. National Institute of Standards and Technology, Gaithersburg, MD."
topics: [fork-merge-security]
added_by: dmarz/fm-mobile-agents
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "91 (Crossref, 2026-10-03)"
code: []
---

## Summary

NIST's review of mobile agent security, now archived and withdrawn as outdated. It models a system as agents plus agent platforms (the home platform being most trusted) and sorts threats into four classes: agent-to-platform, platform-to-agent, agent-to-agent, and other-to-agent-system (masquerading, denial of service, unauthorized access, eavesdropping, alteration, repudiation). It then reviews countermeasures. For protecting agents from platforms it covers partial result encapsulation (sliding encryption; Yee's PRACs with forward integrity; Karjoth et al.'s chained, signed, hash-linked platform entries that also bind the next hop), mutual itinerary recording by a cooperating peer agent, itinerary recording with replication and voting (the Minsky et al. scheme), execution tracing (Vigna), environmental key generation, computing with encrypted functions (Sander and Tschudin), and time-limited obfuscation (Hohl). It also lists anonymity of the agent's principal as an area for future research. I read the threat sections, the agent-protection countermeasures, future research and summary.

## Contribution

A compact reference map of the 1995-1999 mobile-agent defence literature, which is the closest classical analogue of protecting a sub-agent that visits a hostile domain and returns.

## Key results

- PRAC limitation: a malicious platform that keeps copies of keys or key-generating functions, or colludes with a later platform, can modify earlier entries undetected.
- Karjoth-style chaining prevents a revisited or colluding platform from altering its own earlier entry without breaking the chain (as described by NIST).
- Mutual itinerary recording assumes few malicious platforms and that a platform will not collude with one visited by the peer; it cannot tell which of two platforms killed an agent.
- Replication and voting suits tasks that are multi-stage and duplicable; it costs extra resources.
- CEF does not stop denial of service, replay or experimental extraction.

## Methods and models

Literature review and taxonomy; no experiments.

## Limitations and open questions

Coverage ends in 1999; secure coprocessor and TEE work, later replication schemes and later attacks on these protocols are not included. Withdrawal note says today's environment is significantly more complex.

## Relevance to us

A checklist of mechanisms to port. Q2: replication and voting ([[minsky-1996-cryptographic]]) and mutual itinerary recording (two cooperating agents checking each other's routes) are the classical k-of-n and 2-of-2 designs for returning parts. Q3: the stated limitations (key retention, collusion of two hosts, revisits) describe what a capable attacker on a returning sub-agent would do. Q1: the anonymity item points at hiding the principal behind an agent, which is the reverse of dmarz's question (hiding which agent belongs to which principal and returns home) and is listed as unstudied in 1999. Related: [[yee-1997-sanctuary]], [[sander-1998-protecting]], [[farmer-1996-security]].

---
id: farmer-1996-security
type: paper
title: "Security for Mobile Agents: Issues and Requirements"
authors: ["William M. Farmer", "Joshua D. Guttman", "Vipin Swarup"]
year: 1996
venue: "Proceedings of the 19th National Information Systems Security Conference (NISSC 1996)"
url: http://web.archive.org/web/20170318005049/http://csrc.nist.gov/nissc/1996/papers/NISSC96/paper033/SWARUP96.PDF
doi: null
arxiv: null
cite: "Farmer, W. M., Guttman, J. D., & Swarup, V. (1996). Security for Mobile Agents: Issues and Requirements. In Proceedings of the 19th National Information Systems Security Conference (NISSC), 1996."
topics: [fork-merge-security]
added_by: dmarz/fm-mobile-agents
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: 196  # OpenAlex cited_by_count, 2026-10-03; shadow/sol-g51
code: []
---

## Summary

A short MITRE paper (read from the archived NIST conference PDF) that sorts mobile-agent security goals into impossible, easy, and possible-but-not-easy. Its central claim is that the new complication of mobility is that "as an agent traverses multiple hosts that are trusted to different degrees, its state can change in ways that adversely impact its functionality". Two examples carry the argument. In the competing-airlines case, the second airline can rewrite the first airline's fares in the agent's environment or advance its program counter into a preferred branch, and the first airline can change "reserve 2 seats" to "reserve 100" at its competitor. In the distributed intrusion-detection case, an untrusted interpreter swaps two stored host addresses and resets the program counter so that the agent collects data from its trusted home and delivers it to the attacker, so "a migrating agent can become malicious by virtue of its state getting corrupted". Declared impossible in the generic case: authenticating an interpreter as untampered, ensuring correct or complete execution, keeping code or carried keys private, and distinguishing an agent from its clone. Declared possible with new work: a signed, application-specific state appraisal function that each interpreter runs on arrival to decide whether the agent's state is safe and what privileges it gets.

## Contribution

States three design principles still useful today: critical decisions must be made on neutral (trusted) hosts; unchanging parts of state must be sealed cryptographically; and an agent's privileges should depend on an appraisal of its current state. The state appraisal idea is developed in the authors' ESORICS 1996 paper (not catalogued here; not opened).

## Key results

- Principle: "An agent's critical decisions should be made on neutral (trusted) hosts."
- Principle: "Unchanging components of the state should be sealed cryptographically."
- A corrupted agent can be turned against its own home without any code change, by editing mutable state (address swap example).
- Clones cannot be reliably distinguished from the original because agents cannot carry usable private keys.
- Faithful execution cannot be checked in general: if the result were known, the agent would not need to be sent.

## Methods and models

Conceptual analysis with worked scenarios; agent model of code plus execution state (program counter, registers, environment, stack, store) run by interpreters connected by host-to-host channels. No implementation or measurement.

## Limitations and open questions

Requirements paper; offers no mechanism beyond outlines. Assumes many hosts are run by adversaries or competitors, which makes several goals impossible by construction.

## Relevance to us

Q3: the clearest early statement that the payload of the attack is state, not code: the returning agent runs the parent's own trusted code on attacker-edited memory and goals, which is the mobile-agent analogue of an LLM memory or context injection that makes a sub-agent "become" the attacker's agent while keeping its credentials. The address-swap example shows the corrupted agent using its legitimate home privileges to exfiltrate. Q2: state appraisal on re-entry is a merge gate; combined with the neutral-host rule it suggests the parent should only merge conclusions re-derived on its own trusted substrate from sealed evidence, never adopt a child's decisions. Q1: the clone indistinguishability result cuts both ways: an attacker cannot tell which clone the parent will trust, but neither can the parent tell a returned clone from a substitute without keys bound to hardware ([[menetrey-2022-attestation]]). Related: [[harrison-1995-mobile]], [[sander-1998-protecting]], [[yee-1997-sanctuary]], [[dong-2025-memory]].

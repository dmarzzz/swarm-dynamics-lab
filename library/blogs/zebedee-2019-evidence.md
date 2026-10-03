---
id: zebedee-2019-evidence
type: blog
title: "Evidence-Based Subjective Logic and Sybil-resistance"
authors: [Liam Zebedee]
year: 2019
url: https://ethresear.ch/t/evidence-based-subjective-logic-and-sybil-resistance/5075
site: ethresear.ch
topics: [sybil-resistance, collective-decision]
added_by: dmarz/sybil-flashbots-informal
accessed: 2026-10-03
read_depth: full
relevance: 3
---

## Summary

Forum post (1 March 2019) proposing evidence-based subjective logic (EBSL), from the paper "Flow-based reputation with uncertainty: evidence-based subjective logic", as a Sybil-resistant reputation algorithm. Subjective logic represents opinions as (belief, disbelief, uncertainty) summing to 1, with discounting for transitive trust and fusion for combining opinions; EBSL works with integer evidence counts and fixes a flaw in how trust flows through arbitrary networks, converging to a reputation matrix by a PageRank-like fixed point. The author reimplemented the algorithm and simulated Sybil networks: in a highly connected honest network attached to a Sybil cluster, the honest network's view of the Sybils' reputation grows only linearly with each honest node the attacker convinces. Replies raise bribery (citing Phil Daian's enclave-based bribery work), local versus global reputation (Yondon Fu), and insurance-based trust as an alternative.

## Key claims

- Flow-based subjective reputation limits Sybil influence to the trust edges an attacker can obtain from honest nodes.
- Reputation providers (for example a ride-hailing operator attesting identity) can be modelled as replaceable nodes in the trust graph.
- Bought reputation turns subjective trust networks into plutocratic consensus unless bribery resistance is added.

## Evidence quality

Hobbyist simulation with linked code; no formal bound beyond the cited paper. The "linear in convinced honest nodes" result is from the author's simulation, not checked.

## Relevance to us

Agent swarms that rate each other need exactly this kind of attack-edge-limited reputation; EBSL is one concrete algorithm to put in a Sybil experiment alongside EigenTrust-style baselines. The replies connect it to bribery and encumbrance, which link to [[austgen-2023-complete]]. The wash-collusion limit in [[glynn-2026-wash]] applies: flow-based trust bounds fake identities, not real colluding ones.

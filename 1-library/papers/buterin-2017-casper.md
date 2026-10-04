---
id: buterin-2017-casper
type: paper
title: "Casper the Friendly Finality Gadget"
authors: ["Vitalik Buterin", "Virgil Griffith"]
year: 2017
venue: "arXiv preprint (cs.CR), v4 January 2019; Ethereum Foundation"
url: https://arxiv.org/pdf/1710.09437
doi: null
arxiv: "1710.09437"
cite: "Buterin, V., & Griffith, V. (2017). Casper the Friendly Finality Gadget. arXiv:1710.09437 (v4, 22 January 2019)."
topics: [sybil-resistance, sync-consensus]
added_by: dmarz/sybil-foundations
accessed: 2026-10-03
read_depth: full
relevance: 4
citations: "692 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

Casper FFG is a proof-of-stake finality overlay on top of a block-proposal mechanism (initially Ethereum's proof-of-work chain). Validators lock deposits and vote on checkpoint pairs (source, target) every 100 blocks; a supermajority link needs 2/3 of validators weighted by deposit, a checkpoint is justified by a supermajority link from a justified checkpoint and finalized when its direct child is justified from it. Two slashing conditions (no two votes for the same target height; no vote surrounding another) make any safety failure attributable: two conflicting checkpoints cannot both be finalized unless validators holding at least 1/3 of deposits are provably slashable. The paper adds dynamic validator sets with forward and rear sets, a withdrawal delay against long-range revisions, and an inactivity leak against catastrophic crashes.

## Contribution

States the stake-weighting principle in one line: "Proof of stake's security derives from the size of the deposits, not the number of validators", so all fractions are deposit-weighted. Accountable safety turns Sybil resistance into an economic bound: an attacker needs 1/3 of deposits and loses them if it equivocates.

## Key results

- Theorem 1 (accountable safety): two conflicting checkpoints cannot both be finalized unless at least 1/3 of validators by deposit violate a slashing condition.
- Theorem 2 (plausible liveness): if at least 2/3 follow the protocol, a new checkpoint can always be finalized without anyone violating a slashing condition.
- Fork choice: follow the chain containing the justified checkpoint of greatest height.
- A validator that has left can never rejoin with the same key; deposits stay locked for a withdrawal delay (about four months of blocks) during which slashing still applies.
- Long-range revisions are handled by clients refusing to revert finalized blocks and logging on regularly (for example once per 1-2 months); the informal argument needs withdrawal delay omega > 4*delta.
- The inactivity leak drains deposits of non-voting validators so that the online set regains a supermajority, at the cost of allowing two conflicting finalizations without explicit slashing after a partition; validators then favour the first finalized checkpoint they saw.

## Methods and models

Formal definitions and proofs for the fixed-validator case; informal arguments for dynamic validator sets, long-range attacks and crashes. Read in full.

## Limitations and open questions

The authors list a fully compromised proposal mechanism (which can block finality), an open recovery algorithm for some attacks (handled for now by "minority soft forks"), and unproven safety under changing weights. Incentive analysis is deferred.

## Relevance to us

Casper shows how to make many identities pointless by weighting every vote by a slashable deposit, and how to make misbehaviour attributable to a specific key so the deposit can be taken. For agent swarms, the transferable pattern is bonded agents whose signed votes or messages are checked against simple equivocation rules, with automatic slashing on proof. It bounds influence by stake and makes Sybils costly only through the bond, not through identity checks; correlated operators behind several bonded seats remain a risk, which is what [[obol-2026-deployment]] addresses in practice. Related: [[gilad-2017-algorand]], [[castro-1999-practical]], [[lamport-1982-byzantine]], [[burianova-2025-secret]], [[heimbach-2024-deanonymizing]].

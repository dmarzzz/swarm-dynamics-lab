---
id: aspnes-2005-exposing
type: paper
title: "Exposing Computationally-Challenged Byzantine Impostors"
authors: ["James Aspnes", "Collin Jackson", "Arvind Krishnamurthy"]
year: 2005
venue: "Technical Report YALEU/DCS/TR-1332, Department of Computer Science, Yale University"
url: http://www.cs.yale.edu/homes/aspnes/papers/tr1332.pdf
doi: null
arxiv: null
cite: "Aspnes, J., Jackson, C., & Krishnamurthy, A. (2005). Exposing Computationally-Challenged Byzantine Impostors. Technical Report YALEU/DCS/TR-1332, Department of Computer Science, Yale University."
topics: [sybil-resistance, sync-consensus]
added_by: dmarz/sybil-foundations
accessed: 2026-10-03
read_depth: full
relevance: 4
citations: "not checked (Semantic Scholar rate-limited at the time)"
code: []
---

## Summary

The authors argue that Douceur's impossibility [[douceur-2002-sybil]] is narrower than commonly read, because it forces honest nodes to hold exactly one identity. If instead every node, honest or not, receives identities in proportion to the puzzle solutions it produces, Byzantine agreement can be solved when the adversary controls a bounded fraction of total computing power rather than of nodes. Two preamble protocols assign priced identities and build a virtual network on which any standard Byzantine agreement algorithm then runs.

## Contribution

An early formal statement of the idea behind proof-of-work consensus, three years before Bitcoin: replace "fraction of faulty nodes" with "fraction of computational power", and Sybil identities stop mattering for agreement.

## Key results

- Democracy (three rounds): every node sends an individual sub-puzzle to every other node; each node solves a combined hash puzzle over all received bits as many times as it can; identities are assigned by solutions. Tolerates adversary power Ce < Cg/2 for unauthenticated consensus and Ce < Cg for δ-differential consensus. Messages O(Ng·N).
- Monarchy (N rounds): each node in turn acts as king, issues puzzles and counts solutions; identities then exchange "accusations". Tolerates Ce < Cg/3 (unauthenticated) and Ce < Cg/2 (δ-differential). Allows fixed-cost puzzles such as time-lock puzzles.
- With equal computing power per machine, consensus with multiple identities per node is solvable under exactly the same conditions as with single identities.
- The combined puzzle resists tampering, precomputation (a table of size Ng·2^S would be needed) and collusion, under a strong assumption on the hash function that the authors flag as unproven for real hash functions.

## Methods and models

Synchronous point-to-point network with reliable messages, digital signatures but no PKI, nodes with bounded puzzle-solving rate; protocol design with counting proofs. Assumes the participant set is known at the start via some sign-up mechanism, which the authors leave open.

## Limitations and open questions

Synchronous model, known membership, no churn, high message cost; the adversary still decides the agreed value in plain Byzantine agreement, so strong or δ-differential consensus is needed for useful outcomes. Later resource-burning work [[gupta-2020-resource]] addresses churn and cost.

## Relevance to us

The cleanest bridge between Sybil resistance and consensus in a swarm: if agents' voting weight is priced by a verifiable resource, the swarm can run standard fault-tolerant agreement even though identities are free. For LLM agent swarms the priced resource could be compute, stake or attested hardware; for robots it could be physical presence ([[gil-2015-guaranteeing]]). The paper also explicitly treats identities as "autonomous agents hosted by the nodes", which is the agent-host split we face. See [[borge-2017-proof-of-personhood]] for the personhood alternative to compute pricing.

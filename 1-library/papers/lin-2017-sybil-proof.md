---
id: lin-2017-sybil-proof
type: paper
title: "Sybil-proof incentive mechanisms for crowdsensing"
authors: [Jian Lin, Ming Li, Dejun Yang, Guoliang Xue, Jian Tang]
year: 2017
venue: IEEE INFOCOM 2017, IEEE Conference on Computer Communications, Atlanta, pp. 1-9
url: https://ieeexplore.ieee.org/document/8057175
doi: 10.1109/infocom.2017.8057175
arxiv: null
cite: "Lin, J., Li, M., Yang, D., Xue, G., & Tang, J. (2017). Sybil-proof incentive mechanisms for crowdsensing. In IEEE INFOCOM 2017, IEEE Conference on Computer Communications, pp. 1-9. IEEE. https://doi.org/10.1109/INFOCOM.2017.8057175"
topics: [sybil-resistance, collective-decision]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "39 (Crossref, 2026-10-03)"
code: []
---

## Summary

Crowdsensing platforms recruit smartphone users through reverse auctions (users bid costs for sensing tasks, the platform selects winners and pays them). The authors point out that none of the existing auction-based incentive mechanisms consider a Sybil attack, in which one user bids under several identities to win more tasks or extract higher payments, and that this can undermine the mechanisms' truthfulness and budget properties. They design Sybil-proof mechanisms for two settings: SPIM-S for single-minded users (each bids on one task bundle), which is computationally efficient, individually rational, truthful and Sybil-proof; and SPIM-M for multi-minded users (bids on several bundles), which keeps individual rationality, truthfulness and Sybil-proofness but drops the efficiency guarantee. Properties are validated in extensive simulations. Abstract only (IEEE paywalled, no OA copy; abstract from the ASU repository record). The construction (payment rules that make splitting a bid across identities weakly dominated, in the spirit of false-name-proof auctions) and the simulation metrics are not visible from the abstract; a follow-up by the same group covers Sybil-proof online (dynamic arrival) mechanisms.

## Contribution

Brings false-name-proofness into crowdsensing procurement auctions, with separate mechanisms for single- and multi-minded bidders.

## Key results

- SPIM-S: efficient + IR + truthful + Sybil-proof (single-minded).
- SPIM-M: IR + truthful + Sybil-proof (multi-minded), efficiency not guaranteed.
- Simulation validation of these properties (figures not visible).

## Methods and models

Reverse-auction mechanism design for task allocation, Sybil-proofness as an extended incentive-compatibility notion, simulation. Details not read.

## Limitations and open questions

Abstract-level read. Sybil-proofness here is about bidding identities within the auction; it does not stop one phone from submitting many sensing reports under many accounts outside the auction. Efficiency loss of SPIM-M is unquantified from the abstract.

## Relevance to us

Directly analogous to task allocation among LLM agents: a platform procuring work from agents by auction must assume one operator can enter many agent-bidders, and this is the closest off-the-shelf design for that case. Theory roots: [[sakurai-1999-limitation]], [[yokoo-2003-characterization]] (NSA condition is what SPIM-style payments enforce), [[yokoo-2005-robust]] (two-sided case); verifiable allocation for robots in [[lavaur-2024-verifiable]]. Root: [[douceur-2002-sybil]].

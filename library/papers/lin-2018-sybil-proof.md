---
id: lin-2018-sybil-proof
type: paper
title: "Sybil-Proof Online Incentive Mechanisms for Crowdsensing"
authors: [Jian Lin, Ming Li, Dejun Yang, Guoliang Xue]
year: 2018
venue: IEEE INFOCOM 2018, IEEE Conference on Computer Communications, Honolulu, pp. 2438-2446
url: https://par.nsf.gov/biblio/10076448-sybil-proof-online-incentive-mechanisms-crowdsensing
doi: 10.1109/infocom.2018.8486418
arxiv: null
cite: "Lin, J., Li, M., Yang, D., & Xue, G. (2018). Sybil-Proof Online Incentive Mechanisms for Crowdsensing. In IEEE INFOCOM 2018, IEEE Conference on Computer Communications, pp. 2438-2446. IEEE. https://doi.org/10.1109/INFOCOM.2018.8486418"
topics: [sybil-resistance, collective-decision]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "33 (Crossref, 2026-10-03)"
code: []
---

## Summary

Follow-up to the same group's offline SPIM mechanisms, moving to the online crowdsensing setting where users arrive and depart over time and the platform must decide on the fly. The authors observe that the online setting gives a Sybil attacker one extra dimension, active time: a user can split not only its task bids but also its declared arrival/departure windows across fake identities, which breaks the online auction mechanisms proposed so far. They design SOS (single-minded users) achieving computational efficiency, individual rationality, truthfulness and Sybil-proofness, and SOM (multi-minded users) achieving individual rationality, truthfulness and Sybil-proofness, and evaluate both in extensive simulations. Abstract only (IEEE paywalled; abstract and page number from the NSF Public Access record, which lists the accepted manuscript but the PDF link did not resolve from this box). Mechanism details (presumably threshold-price online rules with per-identity monotone payments) and simulation results are not visible.

## Contribution

First Sybil-proof online (dynamic arrival) incentive mechanisms for crowdsensing, closing an open problem stated in the offline paper, and identifying time-splitting as an additional Sybil strategy.

## Key results

- SOS: efficient + IR + truthful + Sybil-proof online (single-minded).
- SOM: IR + truthful + Sybil-proof online (multi-minded).
- Time (arrival/departure) is a new axis for false-name manipulation in online mechanisms.

## Methods and models

Online reverse auction with arrivals and departures, Sybil-proofness over identity, bid and time splitting, simulation evaluation; details not read.

## Limitations and open questions

Abstract-level; efficiency loss of SOM unquantified; Sybil-proofness is within the auction (identities per bidder), not against duplicate sensing accounts outside it.

## Relevance to us

Relevant because agent marketplaces are inherently online: agents come and go, and an operator can fragment both bids and presence windows across many agents. This is the closest existing treatment of that case. Builds on [[lin-2017-sybil-proof]]; theory roots [[yokoo-2003-characterization]], [[todo-2009-characterizing]]; procurement setting [[suyama-2005-strategy]]. Root: [[douceur-2002-sybil]].

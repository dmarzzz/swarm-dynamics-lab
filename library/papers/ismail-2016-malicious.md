---
id: ismail-2016-malicious
type: paper
title: "Malicious peers eviction for P2P overlays"
authors: [Hatem Ismail, Daniel Germanus, Neeraj Suri]
year: 2016
venue: 2016 IEEE Conference on Communications and Network Security (CNS), Philadelphia, pp. 216-224
url: https://ssg.lancs.ac.uk/wp-content/uploads/hatem-malcious.pdf
doi: 10.1109/cns.2016.7860488
arxiv: null
cite: "Ismail, H., Germanus, D., & Suri, N. (2016). Malicious peers eviction for P2P overlays. In 2016 IEEE Conference on Communications and Network Security (CNS), pp. 216-224. IEEE. https://doi.org/10.1109/CNS.2016.7860488"
topics: [sybil-resistance, swarm-detection]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: "1 (Crossref, 2026-10-03)"
code: []
---

## Summary

Targets "localized attacks" (LAs) on structured P2P overlays: a small set of malicious peers positioned around a popular or critical victim peer p_v intercept the lookups meant to resolve it, a family that the authors' generic attack model covers uniformly, including Sybil, eclipse, index poisoning and DDoS variants. Malicious insertion of only 5-10% of the overlay size is enough to intercept most lookups for a target and pollute 20-26% of replies, dropping lookup success for the victim to about 1%. Prior countermeasures are specific to one network or one attack and, critically, lack an eviction step, so a malicious peer detected by one benign peer stays unknown to the rest. The proposed two-fold mechanism first lets each peer detect suspicious peers from lookup behaviour (fake or inconsistent replies against a configurable fake-reply probability FR of 50% or 80%), then runs an eviction protocol in which a querying peer compares its own verdicts with those reported by neighbours and propagates confirmed malicious entries into blacklists, so eviction spreads beyond the detector's local view. OMNeT++ simulations on a service overlay (80% of lookups aimed at the popular subset) with malicious insertion ratios of 5% and 10%: lookup reliability improves by up to 97% under attack and malicious peers are successfully evicted in up to 99% of cases, including for the stealthier attack variants that trade immediate severity for detection hardness. Read: abstract, introduction and localized-attack background, the generic attack model (strategies vs behaviours), detection and eviction mechanism, simulation set-up (Table of parameters: MI 5/10%, FR 50/80%) and headline results, conclusion; detailed per-figure results skimmed.

## Contribution

A network-agnostic detect-and-evict mechanism for localized overlay attacks, evaluated against a unified attack model that subsumes Sybil and eclipse variants, with explicit propagation of blacklists so detections become overlay-wide.

## Key results

- 5-10% malicious insertion pollutes 20-26% of replies and fails ~99% of lookups to the victim without countermeasures.
- With the mechanism: reliability up by as much as 97%; eviction success up to 99% at <= 10% malicious peers.
- Covers EA, Sybil, index poisoning and DDoS strategies in one attack model.

## Methods and models

OMNeT++ overlay simulation, generic LA model parameterised by placement strategy and misbehaviour, local detection plus neighbour cross-checking and blacklist dissemination.

## Limitations and open questions

Simulation only; detection relies on observable fake replies, so a passive Sybil (correct replies, only counting or eclipsing) is harder; blacklist propagation is itself a slander vector if malicious peers report honest ones, which the cross-check only partly addresses; eviction assumes identities are stable enough that a blacklisted peer cannot trivially rejoin (the whitewashing gap).

## Relevance to us

A reasonable template for the "detect locally, confirm with peers, propagate eviction" loop that an agent network would need against a coordinated cluster, and a reminder that eviction without identity cost just forces re-registration. Closely related to [[puttaswamy-2009-securing]] (self-certifying detection and malice-aware routing), [[araujo-2011-maximum]] (collusion detection with the same whitewashing caveat), the live measurements in [[eisenbarth-2022-ethereum]] and the taxonomy [[urdaneta-2011-survey]]. Root: [[douceur-2002-sybil]].

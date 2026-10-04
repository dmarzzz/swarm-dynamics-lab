---
id: el-mouhib-2021-analysis
type: paper
title: "Analysis of the Impact of Traffic Density on the Compromised CAV Rate : a Multi-Agent Modeling Approach"
authors: [Manal El Mouhib, Kamal Azghiou, Abdelwahed Tahani]
year: 2021
venue: 2021 IEEE International IOT, Electronics and Mechatronics Conference (IEMTRONICS), Toronto, pp. 1-6
url: https://ieeexplore.ieee.org/document/9422630/
doi: 10.1109/iemtronics52119.2021.9422630
arxiv: null
cite: "El Mouhib, M., Azghiou, K., & Tahani, A. (2021). Analysis of the Impact of Traffic Density on the Compromised CAV Rate : a Multi-Agent Modeling Approach. In 2021 IEEE International IOT, Electronics and Mechatronics Conference (IEMTRONICS), pp. 1-6. IEEE. https://doi.org/10.1109/iemtronics52119.2021.9422630"
topics: [sybil-resistance, crowds-and-traffic, fork-merge-security]
added_by: shadow/sol-p2
accessed: 2026-10-03
read_depth: abstract
relevance: 2
citations: "0 (Crossref, 2026-10-03)"
code: []
---

## Summary

Short conference paper modelling how an attack that spreads over vehicle-to-vehicle (V2V) links propagates through a population of connected and autonomous vehicles (CAVs). The authors propose a threat model for attacks exploiting the V2V channel, then abstract away the specific exploit and run a NetLogo multi-agent simulation (1000 runs per scenario) to study the macroscopic effect of road traffic density on the fraction of CAVs that end up compromised. The headline finding in the abstract is that the denser the traffic a CAV is engaged in, the more likely it is to be compromised, i.e. contact rate drives contagion in the same way as in epidemic models. The paper closes with countermeasures proposed for inclusion in Intelligent Transportation System security policy. Section headings visible on the IEEE page include "Agent Based Simulation of V2V Penetration Rate". Abstract and table of contents only; the body is paywalled and no open copy was found, so the threat model details, infection rule, density values and the quantitative compromise rates are not recorded here. The same first author has a 2022 follow-up framing the problem as stochastic malware spread among CAVs (not catalogued).

## Contribution

Positions V2V compromise as a density-dependent contagion in a mobile multi-agent population and quantifies it by agent-based simulation rather than closed-form epidemic models.

## Key results

- Compromised-CAV rate increases with traffic density (abstract; magnitudes not visible).
- 1000 NetLogo simulations per scenario (abstract).

## Methods and models

NetLogo agent-based simulation; CAVs as mobile agents with V2V contact; abstracted attack that spreads on contact; scenarios parameterised by traffic density. Details not visible.

## Limitations and open questions

Abstract-level read. The abstract does not say whether compromised vehicles forge identities (Sybil) or simply relay the exploit, so the sybil-resistance tag rests on the collector's placement and the V2V trust context rather than on confirmed content. Zero Crossref citations; short paper; simulation only.

## Relevance to us

Low. Relevant only as a reminder that in a mobile swarm the rate of member-to-member contact is itself a security parameter: denser interaction means faster spread of a compromised member's influence, which is the same mechanism the bounded-time-interaction framing in [[gandhi-2025-roborebound]] tries to cap. Could serve as a trivial baseline (SI-style contagion in a moving population) when designing experiments on corruption spreading through an agent collective.

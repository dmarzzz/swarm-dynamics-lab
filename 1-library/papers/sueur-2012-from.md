---
id: sueur-2012-from
type: paper
title: "From Social Network (Centralized vs. Decentralized) to Collective Decision-Making (Unshared vs. Shared Consensus)"
authors: ["Cédric Sueur", "Jean-Louis Deneubourg", "Odile Petit"]
year: 2012
venue: "PLoS ONE"
url: "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3290558/"
doi: "10.1371/journal.pone.0032566"
arxiv: null
cite: "Sueur, C., Deneubourg, J.-L., & Petit, O. (2012). From Social Network (Centralized vs. Decentralized) to Collective Decision-Making (Unshared vs. Shared Consensus). PLoS ONE, 7(2), e32566. https://doi.org/10.1371/journal.pone.0032566"
topics: ["collective-decision", "collective-motion"]
added_by: dmarz/collective-decision-audit
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: "100 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Agent-based model of group departures in which an individual's probability of joining a collective movement depends on its affiliative ties to those already moving, run on artificial 10-member social networks ranging from a star (fully centralised) to an equal network (fully decentralised). Centralised networks make the central individual a de facto leader (unshared consensus), while decentralised networks give every initiator a similar following (shared consensus). Model patterns are compared with departure data from five semi-free-ranging primate groups.

## Contribution

Links the primate literature on unshared versus shared consensus (despotic rhesus versus egalitarian Tonkean macaques) to network structure through an explicit mimetic joining model, rather than attributing the difference to dominance per se. It is one of the few modelling papers on primate collective departures, a thin area in our library next to [[strandburg-peshkin-2015-shared]].

## Key results

- Mean number of joiners fell with network centralisation following an inverse exponential (R^2 = 0.81, p = 0.015); star and highly decentralised networks had fewer joiners than the others.
- Departure latency of the first joiner rose exponentially with the centrality index (R^2 = 0.82, p = 0.013, y = 48.37 e^{0.81 x}).
- In centralised networks, movements initiated by the central individual recruited more joiners than those initiated by others (star network: about 9.99 versus 5.1 joiners, Mann-Whitney Z = -27.17, p < 0.0001); the difference vanished in decentralised networks.
- The authors report that observed primate groups match the model networks that best represent their social structure (I did not read this comparison in detail).

## Methods and models

Markov-chain mimetism model in NetLogo: initiator departs with a constant probability; resting individual i joins with probability psi_i = lambda_i + M sum_k r(i,k) over moving individuals k, with lambda_i = 0.00007 and M = 0.002 per 1-s step; each individual distributes a fixed total of affiliation (sum r(i,k) = 1). N = 10, eight network types (star, highly to very low centralised, equal, chain, random), 10,000 simulations each; a run stops when nobody joins for 300 s. Primate data from five groups (macaque species) at the Strasbourg Primatology Centre.

## Limitations and open questions

Only affiliative ties, no dominance or need asymmetries; N = 10; no spatial or directional component (a single departure decision). Comparison with primates is qualitative and on captive, semi-free-ranging groups.

## Relevance to us

A minimal, implementable model of how influence-network topology turns shared into unshared consensus; the same question as hub effects in [[becker-2017-network]] and leadership hierarchies in [[nagy-2010-hierarchical]]. Field counterpart: [[strandburg-peshkin-2015-shared]] and [[papageorgiou-2024-compromise]].

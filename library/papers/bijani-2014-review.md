---
id: bijani-2014-review
type: paper
title: "A review of attacks and security approaches in open multi-agent systems"
authors: [Shahriar Bijani, David Robertson]
year: 2014
venue: Artificial Intelligence Review, vol. 42, no. 4, pp. 607-636 (online 16 May 2012)
url: https://link.springer.com/article/10.1007/s10462-012-9343-1
doi: 10.1007/s10462-012-9343-1
arxiv: null
cite: "Bijani, S., & Robertson, D. (2014). A review of attacks and security approaches in open multi-agent systems. Artificial Intelligence Review, 42(4), 607-636. https://doi.org/10.1007/s10462-012-9343-1"
topics: [sybil-resistance, llm-agent-swarms]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "62 (Crossref, 2026-10-03)"
code: []
---

## Summary

Review of security in open multi-agent systems (MAS), where agents built by different parties join and leave a peer-to-peer style society that is not pre-engineered to cooperate, so conventional perimeter security does not apply. The authors introduce and classify the main attacks on open MAS, survey security techniques from the literature, split them into prevention and detection approaches, and finish by matching each attack class to the countermeasures they consider appropriate. The abstract (from the Edinburgh group page and RIS export; the Springer page served only the reference list through the reader proxy) does not list the attack classes themselves. The reference list, which did load, shows the review draws on Douceur's Sybil attack, Cheng and Friedman's Sybilproof reputation mechanisms, Sit and Morris on DHT security, Braynov and Jadliwala "Detecting malicious groups of agents" (2004), mobile-agent security (Jansen and Karygiannis NIST SP 800-19), electronic institutions (Esteva et al.) and attack-tree / attack-graph modelling, so the attack taxonomy spans Sybil and collusion, mobile-agent tampering, information leakage and denial of service. Bijani's 2013 Edinburgh PhD thesis ("Securing Open Multi-agent Systems Governed by Electronic Institutions") restates the review's taxonomy and extends it with information-flow analysis for the LCC choreography language. Abstract plus reference list only; the body is paywalled and Unpaywall finds no OA copy.

## Contribution

One of the few surveys that treats security of open agent societies (rather than P2P overlays or single robots) as its object, and organises defences as prevention versus detection, with a mapping from attack class to countermeasure.

## Key results

- Attack taxonomy for open MAS and a prevention/detection split of defences (abstract; classes not visible).
- Reference base shows Sybil, colluding-group detection, mobile-agent and electronic-institution attacks are all in scope (inferred from the bibliography, not from the body).

## Methods and models

Literature review; companion thesis uses the Lightweight Coordination Calculus (LCC) and electronic institutions as the governed-MAS model.

## Limitations and open questions

Abstract-level read. Pre-LLM (2012 online); agents are BDI/FIPA style, not language models. Whether the review's detection approaches (e.g. Braynov and Jadliwala's malicious-group detection) have been evaluated at scale is not checkable from what loaded.

## Relevance to us

Bridge between the P2P Sybil literature ([[douceur-2002-sybil]], [[cheng-2005-sybilproof]], [[urdaneta-2011-survey]]) and agent societies, which is the closer analogue to LLM agent swarms than DHTs are. The "detecting malicious groups of agents" lineage it cites is a direct ancestor of coordinated-agent detection and would be worth chasing for the swarm-detection survey. Compare the much later LLM-era framings in [[hammond-2025-multi]] and [[lin-2026-treacherous]].

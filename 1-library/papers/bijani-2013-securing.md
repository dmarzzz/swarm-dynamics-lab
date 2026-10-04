---
id: bijani-2013-securing
type: paper
title: "Securing open multi-agent systems governed by electronic institutions"
authors: [Shahriar Bijani]
year: 2013
venue: PhD thesis, School of Informatics, The University of Edinburgh (supervisors Dave Robertson, David Aspinall)
url: https://era.ed.ac.uk/items/2e730153-d6ed-49b7-aaa1-5a5b34a83edf
doi: null
arxiv: null
cite: "Bijani, S. (2013). Securing open multi-agent systems governed by electronic institutions. PhD thesis, The University of Edinburgh. http://hdl.handle.net/1842/8268"
topics: [sybil-resistance, fork-merge-security]
added_by: shadow/sol-p2
accessed: 2026-10-03
read_depth: abstract
relevance: 2
citations: "not checked (thesis, no DOI)"
code: []
---

## Summary

Edinburgh PhD thesis (issued 2013-11-28) that expands the attack-and-defence review published as [[bijani-2014-review]] and then goes deep on one problem: information leakage in open multi-agent systems whose interaction protocols are specified as electronic institutions in the Lightweight Coordination Calculus (LCC), a choreography language based on logic programming and the pi-calculus. Per the abstract: the thesis first introduces and classifies the main attacks on open MAS in a taxonomy, surveys security techniques and sorts them into prevention versus detection, and suggests countermeasures per attack class. It then argues that conventional mechanisms (access control, encryption) cannot stop information from propagating once released, and proposes two frameworks for detecting insecure information flows in LCC interaction models: conceptual modelling of interaction models, and language-based information-flow analysis via a new security-typed LCC with both static (design-time) and dynamic (run-time) type checking, formally evaluated by proving the type system's properties. The acknowledged limitation of both is the difficulty of expressing realistic policies as annotations. A cloud-computing case study applies security-typed LCC to virtual machine migration management and analyses leaks. Abstract and repository metadata only; the PDF was not opened in this session.

## Contribution

The full-length version of the open-MAS attack taxonomy plus a language-based (type-system) approach to preventing information leakage in agent choreographies, which is a different defence family from the reputation and identity mechanisms that dominate Sybil work.

## Key results

- Attack taxonomy for open MAS and a prevention/detection classification of countermeasures (abstract; details in the companion review).
- Security-typed LCC with static and dynamic checking, with proven properties (abstract).
- Case study on VM migration choreography (abstract).

## Methods and models

Literature classification; LCC choreography language; information-flow type systems; formal proofs; case study. No empirical evaluation visible.

## Limitations and open questions

Abstract-level. The Sybil connection is through the taxonomy chapter (the review cites Douceur and Sybilproof reputation), not through the type-system contribution, which concerns confidentiality rather than identity. Annotation burden admitted by the author. Pre-LLM agents.

## Relevance to us

Low to moderate. Useful mainly as the primary source behind [[bijani-2014-review]] if the survey needs the full taxonomy, and as an example of treating agent interaction protocols as typed programs, which is one way to think about preventing a corrupted sub-agent from exfiltrating state on merge. See also the same group's reputation-as-selection work [[chatzinikolaou-2012-use]].

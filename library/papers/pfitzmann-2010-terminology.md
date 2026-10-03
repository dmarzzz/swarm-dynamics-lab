---
id: pfitzmann-2010-terminology
type: paper
title: 'A terminology for talking about privacy by data minimization: Anonymity, Unlinkability, Undetectability, Unobservability, Pseudonymity, and Identity Management'
authors: [Andreas Pfitzmann, Marit Hansen]
year: 2010
venue: Technical report, TU Dresden and ULD Kiel (version v0.34, 10 August 2010)
url: https://dud.inf.tu-dresden.de/literatur/Anon_Terminology_v0.34.pdf
doi: null
arxiv: null
cite: 'Pfitzmann, A., & Hansen, M. (2010). A terminology for talking about privacy by data minimization: Anonymity, Unlinkability, Undetectability, Unobservability, Pseudonymity, and Identity Management (Version v0.34). TU Dresden and ULD Kiel.'
topics: [fork-merge-security, sybil-resistance]
added_by: dmarz/fm-unlinkability
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: null
code: []
---

## Summary

Pfitzmann and Hansen give the standard vocabulary of the anonymity field. Anonymity of a subject from an attacker's perspective means the attacker cannot sufficiently identify the subject within a set of subjects, the anonymity set. Unlinkability of two or more items of interest means the attacker cannot sufficiently distinguish whether they are related. Undetectability means the attacker cannot sufficiently distinguish whether an item exists; unobservability adds anonymity of the subjects involved even against other participants. They define anonymity delta (a-posteriori minus a-priori anonymity, never positive) and classify pseudonyms by linkability, from person pseudonyms to role-relationship and one-time transaction pseudonyms.

## Contribution

A precise, widely cited glossary that separates hiding who (anonymity), hiding relations (unlinkability) and hiding existence (undetectability, unobservability).

## Key results

- Definitions are relative to an attacker and to an anonymity set; anonymity can only stay the same or decrease as the attacker observes more.
- Unobservability implies anonymity; undetectability is only possible with respect to subjects not involved in the item.
- Transaction pseudonyms (fresh per transaction) maximise unlinkability; role-relationship pseudonyms trade some linkability for accountability.

## Methods and models

Conceptual definitions with set diagrams; no experiments.

## Limitations and open questions

Informal ("sufficiently"); quantitative and game-based versions are in [[kuhn-2018-privacy]].

## Relevance to us

Q1 vocabulary. dmarz's question splits cleanly: hiding which sub-agent will be merged is sender anonymity within the anonymity set of returners; hiding that a given outgoing part and a given returning part are the same is unlinkability; hiding that a real return happened at all is undetectability, which is what cover loops in [[piotrowska-2017-loopix]] buy. The pseudonym taxonomy suggests sub-agents should travel under transaction pseudonyms unlinkable to the parent, re-identified only at merge, which is the commitment-and-reveal structure of [[boneh-2020-single]].

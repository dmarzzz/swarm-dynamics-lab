---
id: pawlick-2019-game
type: paper
title: A Game-theoretic Taxonomy and Survey of Defensive Deception for Cybersecurity and Privacy
authors: [Jeffrey Pawlick, Edward Colbert, Quanyan Zhu]
year: 2019
venue: ACM Computing Surveys
url: https://arxiv.org/abs/1712.05441
doi: 10.1145/3337772
arxiv: '1712.05441'
cite: Pawlick, J., Colbert, E., & Zhu, Q. (2019). A Game-theoretic Taxonomy and Survey of Defensive Deception for Cybersecurity and Privacy. ACM Computing Surveys, 52(4), 1-28.
topics: [fork-merge-security]
added_by: dmarz/fm-unlinkability
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: null
code: []
---

## Summary

The authors survey 24 game-theoretic papers (2008-2018) on defensive deception and define six mutually exclusive species by four game-theoretic differences (private information, actors, actions, duration). Cryptic deception hides: perturbation (intensive, informational: noise on the valuable data itself), moving target defense (intensive, motive: randomise or change the configuration), obfuscation (extensive, informational: add decoy data or traffic outside the valuable item), mixing (extensive, motive: exchange identities with other users, as in mix networks and mix zones). Mimetic deception imitates: honey-x (static: honeypots, honeynets, honeytokens) and attacker engagement (dynamic). Most surveyed models are Nash or Stackelberg games and static.

## Contribution

A precise taxonomy that separates decoys, movement, noise and mixing, and maps each to the game structures used to analyse it.

## Key results

- Six species: perturbation, moving target defense, obfuscation, mixing, honey-x, attacker engagement.
- Mixing is distinguished because it needs other users' participation (for example Tor is classified as mixing).
- Obfuscation and MTD differ by one property (Hamming distance one in the taxonomy's binary lattice), likewise obfuscation and perturbation.
- No one-to-one mapping between deception species and game types in the literature.

## Methods and models

Literature survey and taxonomy construction; I read the abstract, taxonomy section and the classification discussion.

## Limitations and open questions

Covers only game-theoretic papers to 2018; most models static.

## Relevance to us

Q1 design space. The six species give a checklist for how a parent can hide which sub-agent returns: MTD (re-designate the returner), obfuscation (send decoy returners and decoy traffic, as in [[piotrowska-2017-loopix]]), mixing (pool sub-agents with other agents' sub-agents so identities are exchanged, as in [[chaum-1981-untraceable]]), honey-x (deliberately expose bait sub-agents to detect who is trying to capture them), attacker engagement (feed a captured sub-agent misleading state). Q3: honey-x is also a detection tool for the memory-hijack attack, since a corrupted bait that tries to merge exposes the attacker. Companions: [[cho-2020-toward]], [[sengupta-2020-survey]], [[fugate-2019-artificial]].

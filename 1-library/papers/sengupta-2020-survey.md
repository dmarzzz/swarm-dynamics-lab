---
id: sengupta-2020-survey
type: paper
title: A Survey of Moving Target Defenses for Network Security
authors: [Sailik Sengupta, Ankur Chowdhary, Abdulhakim Sabur, Adel Alshamrani, Dijiang Huang, Subbarao Kambhampati]
year: 2020
venue: IEEE Communications Surveys & Tutorials
url: https://arxiv.org/abs/1905.00964
doi: 10.1109/comst.2020.2982955
arxiv: '1905.00964'
cite: Sengupta, S., Chowdhary, A., Sabur, A., Alshamrani, A., Huang, D., & Kambhampati, S. (2020). A Survey of Moving Target Defenses for Network Security. IEEE Communications Surveys & Tutorials, 22(3), 1909-1941.
topics: [fork-merge-security]
added_by: dmarz/fm-unlinkability
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: 247 (Crossref, 2026-10-03)
code: []
---

## Summary

Sengupta and colleagues survey moving target defenses for networks and organise them by three questions: what to move (which element of the system, mapped to stages of the cyber kill chain and APT phases), when to move (fixed or event-triggered timing), and how to move (the movement strategy, often chosen with domain knowledge or game theory such as Stackelberg games where the defender commits to a randomised policy). They review implementations, noting that virtualisation and software-defined networking make movement cheaper, and discuss qualitative and quantitative evaluation including performance costs.

## Contribution

A what-when-how framework for MTD with an explicit link from the moved element to the attack phase it disrupts, especially reconnaissance.

## Key results

- MTD's purpose is to make information gathered in reconnaissance stale before it can be used.
- Stackelberg security games are the common model for choosing randomised movement policies.
- SDN and virtualisation lower the cost of implementing movement.

## Methods and models

Survey with a formal notation for MTDs; I read the abstract, introduction and the categorisation sections.

## Limitations and open questions

Network-centric; costs are discussed qualitatively more than measured.

## Relevance to us

Q1. The what-when-how framing transfers to a fork-merge agent: what to move (which sub-agent is designated to return, which courier carries it, which merge endpoint), when to move (per fork, per round, on suspicion), and how (a randomised commitment the attacker can know but not predict, as in a Stackelberg game). It complements [[cho-2020-toward]] and the game-theoretic taxonomy in [[pawlick-2019-game]]; the repeated-round leak in [[wright-2004-predecessor]] is a reason to choose "when" carefully.

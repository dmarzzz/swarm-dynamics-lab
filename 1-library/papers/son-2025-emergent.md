---
id: son-2025-emergent
type: paper
title: "Emergent functional dynamics of link-bots"
authors: ["Kyungmin Son", "Kimberly Bowal", "Kwanwoo Kim", "L. Mahadevan", "Ho-Young Kim"]
year: 2025
venue: "Science Advances"
url: https://doi.org/10.1126/sciadv.adu8326
doi: "10.1126/sciadv.adu8326"
arxiv: null
cite: "Son, K., Bowal, K., Kim, K., Mahadevan, L., & Kim, H.-Y. (2025). Emergent functional dynamics of link-bots. Science Advances, 11(19), eadu8326."
topics: [swarm-robotics, active-matter]
added_by: dmarz/swarm-robotics-recent
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "3 (OpenAlex W4410227268, 2026-10-03); 3 (Crossref, 2026-10-03)"
code: []
---

## Summary

Link-bots are single-stranded chains of self-propelled bots joined by V-shaped links whose geometry constrains relative motion. With no computation, only steric and geometric constraints, the active polymer-like chain shows locomotion, navigation, transport and competitive or cooperative interactions. Tuning a few link parameters switches between traversing or blocking narrow spaces, passing or enclosing objects, and pushing loads in different directions.

## Contribution

It shows that mechanical constraint design alone can program functional collective behaviour, an embodied-intelligence counterpart to algorithmic swarm control.

## Key results

- Diverse tasks (traverse or obstruct gaps, pass or enclose objects, propel loads) selected by link parameters such as notch angle and spread angle (measured experimentally).
- Single bots on an 80 Hz, 70 um vibrating plate (45 cm arena) move at about 8 cm/s with active-Brownian MSD (ballistic at short times, diffusive at long times) (measured).

## Methods and models

Vibration-driven bristle bots (tilted legs) linked by rigid links of length L with notch angle theta and spread angle alpha into a symmetric V-shaped chain. A Python model updates each bot's velocity as self-propulsion v0 plus rotational noise plus bot-bot overlap forces, rigid-link length forces and notch-constraint forces (skimmed via the Europe PMC full text).

## Limitations and open questions

Skimmed. Small chains in a bounded arena; the scaling of behaviours with chain length was only partly explored.

## Relevance to us

Same 'embodied rule' theme as [[casiulis-2025-geometric]] and [[arbel-2024-mechanical]]; a simulation of active chains is a cheap hackathon option.

## Notes from dmarz/swarm-robotics-recent-audit

Audited 2026-10-03 against the Europe PMC full text (PMC12063647). The 45 cm arena, 80 Hz and 70 um vibration, 8 cm/s single-bot speed and the link parameters (length, notch angle, spread angle) match. No corrections needed. Citation count now from OpenAlex.

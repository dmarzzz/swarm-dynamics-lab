---
id: li-2025-reverse
type: paper
title: "Reverse engineering the control law for schooling in zebrafish using virtual reality"
authors: ["Liang Li", "Máté Nagy", "Guy Amichay", "Ruiheng Wu", "Wei Wang", "Oliver Deussen", "Daniela Rus", "Iain D. Couzin"]
year: 2025
venue: "Science Robotics"
url: https://doi.org/10.1126/scirobotics.adq6784
doi: "10.1126/scirobotics.adq6784"
arxiv: null
cite: "Li, L., Nagy, M., Amichay, G., Wu, R., Wang, W., Deussen, O., Rus, D., & Couzin, I. D. (2025). Reverse engineering the control law for schooling in zebrafish using virtual reality. Science Robotics, 10(101), eadq6784."
topics: [collective-motion, swarm-robotics]
added_by: dmarz/collective-motion-recent
accessed: 2026-10-03
read_depth: abstract
relevance: 5
citations: "17 (OpenAlex W4409982789, 2026-10-03)"
code: []
---
## Summary

Juvenile zebrafish in networked virtual reality interact with virtual robot fish and with each other in a shared virtual world, allowing models of social response to be tested in situ. The key social response is single- and multi-target pursuit based on an egocentric representation of conspecific positions (not their speed), robust to incomplete sensory input. A simple experimentally derived proportional-derivative law, "BioPD", accounts for the behaviour, passing a Turing-style test and a scalability test. Applied to terrestrial, aerial and water robots it gave close-to-optimal pursuit with little tuning.

## Contribution

A causally tested, minimal control law for following behaviour extracted from a vertebrate and transferred to robots.

## Key results

- Measured (abstract): pursuit uses positional, egocentric information; robust to incomplete input.
- Measured (abstract): BioPD reproduces all key features; passes Turing and scalability tests.
- Robots (abstract): near-optimal pursuit across vehicle types.

## Methods and models

Immersive VR for freely swimming fish, closed-loop virtual conspecifics, PD control model (details not read).

## Limitations and open questions

Abstract only. Pursuit of one or few targets; group-level emergence is only partly addressed. Note the contrast with the allocentric claim in [[salahshour-2025-allocentric]].

## Relevance to us

Directly implementable controller for a hackathon robot or sim demo. Same rig: [[amichay-2024-revealing]]. Closed-loop VR validation in another species: [[escobedo-2026-closed]].

## Notes from dmarz/collective-motion-recent-audit

Spot-checked metadata against Crossref (10(101), eadq6784; eight authors): matches. citations replaced with the OpenAlex cited_by_count (2026-10-03) in place of the Crossref count.

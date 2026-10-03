---
id: ko-2023-role
type: paper
title: The role of hydrodynamics in collective motions of fish schools and bioinspired underwater robots
authors: [Hungtang Ko, George Lauder, Radhika Nagpal]
year: 2023
venue: Journal of The Royal Society Interface
url: https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10598440/fullTextXML
doi: 10.1098/rsif.2023.0357
arxiv: null
cite: 'Ko, H., Lauder, G., & Nagpal, R. (2023). The role of hydrodynamics in collective motions of fish schools and bioinspired underwater robots. Journal of The Royal Society Interface, 20(207), 20230357.'
topics: [collective-motion, swarm-robotics]
added_by: dmarz/collective-motion-audit
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "59 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

A review spanning fluid mechanics, fish biology and underwater robotics that asks how fluid forces shape
aquatic collectives and how fish use flow sensing (the lateral line) to coordinate. The authors propose
"fluid stigmergy" as the organizing idea: the water is a shared medium that both couples agents physically
and stores information (wakes encode a neighbour's position, phase and tail-beat frequency) that others can
read. They survey wake physics, the energetics of school formations, sensing experiments and robot
platforms with flow sensors. Read: abstract, introduction, the formation-energetics and robotics sections
of the PMC full text; the remaining sections skimmed.

## Contribution

The most recent broad review (2023) of hydrodynamics in fish schooling, filling a gap left by the
"dry" behavioural reviews ([[lopez-2012-behavioural]], [[herbert-read-2016-understanding]]) and connecting
it to swarm robotics. It reframes stigmergy, usually a social-insect concept, for fluid environments.

## Key results

- The Weihs-Lighthill conjecture that a diamond formation is hydrodynamically optimal is challenged by
  animal experiments and simulations; side-by-side ("phalanx") formations can be more efficient, and
  tetras in phalanx formation reached faster speeds at lower tail-beat frequencies (reviewed, not new data).
- Simulations reviewed find schools more efficient than solitary swimmers regardless of formation
  (diamond, rectangular, side-by-side, inline); for up to four swimmers more than a dozen equilibrium
  formations exist, including the diamond.
- Fluctuations of the flow field preserve information about a neighbour's relative position, phase
  difference and tail-beat frequency.
- Most current robot swarms use social-force models with radio or external tracking; underwater robots
  lack those channels, and a vision-based underwater swarm has achieved milling; flow sensing could add
  energy saving and coordination.

## Methods and models

Narrative review with figures synthesizing computational fluid dynamics, particle image velocimetry
experiments, lateral-line ablation studies and robotic fish platforms. No new data.

## Limitations and open questions

- Open (as stated by the authors): whether diamond formations are optimal or preferred in nature; how fish
  integrate visual and flow cues; scaling of hydrodynamic benefits to large schools.
- A perspective piece: claims are as strong as the cited primary studies, which the entry does not
  re-check.

## Relevance to us

Points to an under-explored coordination channel: agents coupled through a shared physical medium rather
than explicit messages, which is a design option for robot swarms and an analogy for agents coupled through
a shared workspace. Related: [[filella-2018-model]] (model with dipole hydrodynamics),
[[huang-2024-collective]], [[wang-2025-collective]], [[vasarhelyi-2018-optimized]].

---
id: fersula-2026-leveraging
type: paper
title: "Leveraging design for collective phototaxis in morphological swarm robotics"
authors: ["Jeremy Fersula", "Nicolas Bredeche", "Olivier Dauchot"]
year: 2026
venue: "Nature Communications"
url: https://www.nature.com/articles/s41467-026-77743-2
doi: "10.1038/s41467-026-77743-2"
arxiv: null
cite: "Fersula, J., Bredeche, N., & Dauchot, O. (2026). Leveraging design for collective phototaxis in morphological swarm robotics. Nature Communications (published online 16 September 2026; volume and article number not yet assigned in Crossref). https://doi.org/10.1038/s41467-026-77743-2"
topics: [swarm-robotics, active-matter, collective-motion]
added_by: dmarz/swarm-robotics-recent-audit
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "0 (Crossref is-referenced-by-count, 2026-10-03; OpenAlex search budget exhausted during this audit)"
code: []
---

## Summary

Kilobots are fitted with passive exoskeletons whose geometry sets whether each robot tends to align or anti-align its heading with the external force it feels, the self-alignment mechanism of polar active matter. The authors compare the two morphologies on a simple phototaxis task, in experiments and in simulations of a physical model of the robots' self-aligning dynamics. The abstract reports that the success of morphological computation depends jointly on the control policy and the body design: the gap between the two morphologies becomes dramatic when robots may only slow down and never stop, and efficient phototaxis needs the self-alignment strength tuned to a sweet spot. Varying that one parameter also produces a range of other collective behaviours.

## Contribution

It turns the "morphological computation" idea in swarm robotics into a quantitative statement: one physical parameter of active-matter theory, the self-alignment strength, controls task success, and its useful range depends on the controller. It extends the exoskeleton Kilobot work of [[ben-zion-2023-morphological]] and the self-aligning active matter framework (see [[baconnier-2025-self]]) from emergent motion to a goal-directed task.

## Key results

- Experiments (per the abstract): two exoskeleton morphologies (aligning vs anti-aligning) give very different phototaxis success, and the contrast is largest when the policy forbids stopping and only allows slowing down.
- Simulations of a calibrated self-aligning model (per the abstract): phototaxis efficiency peaks at an intermediate self-alignment strength; outside that sweet spot it falls.
- Varying self-alignment strength produces "a rich repertoire" of collective behaviours (not enumerated in the abstract).
- Numbers (swarm sizes, success rates, the optimal alignment value) were not available to me; the full text was not accessible in this session.

## Methods and models

Kilobot swarm in exoskeletons designed by M. Y. Ben Zion (acknowledged as first presented in their earlier paper), light-seeking control policies with and without stopping, and numerical simulations of an active-particle model with a self-alignment torque coupling heading to velocity/force. Funding acknowledgements name ANR projects on morphological swarm robotics.

## Limitations and open questions

Only the abstract and front matter were read. Whether the sweet spot coincides with a collective transition (for example the onset of collective actuation) and how it scales with N are the questions to check in the full text. Kilobots are slow, stick-slip vibration robots; transfer to other platforms is open.

## Relevance to us

A clean hackathon-scale idea: one active-matter parameter (self-alignment strength) as a design knob for a task, testable in a simple self-aligning particle simulator. Pairs with [[ben-zion-2023-morphological]], [[baconnier-2025-self]], [[loi-2025-pogobot]] and the physics-of-robot-swarms strand ([[casiulis-2025-geometric]], [[alonso-llanes-2024-single]]).

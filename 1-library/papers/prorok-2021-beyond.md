---
id: prorok-2021-beyond
type: paper
title: "Beyond Robustness: A Taxonomy of Approaches towards Resilient Multi-Robot Systems"
authors: ["Amanda Prorok", "Matthew Malencia", "Luca Carlone", "Gaurav S. Sukhatme", "Brian M. Sadler", "Vijay Kumar"]
year: 2021
venue: "arXiv preprint (survey)"
url: https://arxiv.org/abs/2109.12343
doi: null
arxiv: "2109.12343"
cite: "Prorok, A., Malencia, M., Carlone, L., Sukhatme, G. S., Sadler, B. M., & Kumar, V. (2021). Beyond Robustness: A Taxonomy of Approaches towards Resilient Multi-Robot Systems. arXiv:2109.12343."
topics: [sybil-resistance, swarm-robotics, meta]
added_by: dmarz/sybil-robotics
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "101 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

Survey distinguishing robustness (needs known adversaries, over-provisioning, predictive models) from resilience (enduring and recovering from unexpected disruption by exploiting complementarity, diversity and redundancy, often via reconfiguration). Gives a formal taxonomy of approaches across perception, control, planning and learning, discusses stressors and how resilience can be defined and measured, and lists open problems.

## Contribution

The standard taxonomy paper for resilient multi-robot systems; the 2022 T-RO special section on resilience in networked robotic systems (Prorok, Kumar, Sadler, Sukhatme, doi:10.1109/TRO.2022.3143013) collects 17 papers in the same framing, including [[mallmann-trenn-2021-crowd]] and [[yemini-2021-characterizing]].

## Key results

- Review; no new measurements.

## Methods and models

Survey. Abstract read only; details beyond the abstract not checked.

## Limitations and open questions

Broad scope; adversarial identity is one stressor among many.

## Relevance to us

Useful vocabulary for our survey: Sybil resistance is a robustness method (bound the adversary) whereas trust-adaptive schemes are resilience methods (recover when the bound fails).

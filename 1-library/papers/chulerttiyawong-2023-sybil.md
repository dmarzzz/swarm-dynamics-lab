---
id: chulerttiyawong-2023-sybil
type: paper
title: "Sybil Attack Detection in Internet of Flying Things-IoFT: A Machine Learning Approach"
authors: ["Donpiti Chulerttiyawong", "Abbas Jamalipour"]
year: 2023
venue: "IEEE Internet of Things Journal"
url: https://api.openalex.org/works/doi:10.1109/jiot.2023.3257848
doi: "10.1109/jiot.2023.3257848"
arxiv: null
cite: "Chulerttiyawong, D., & Jamalipour, A. (2023). Sybil Attack Detection in Internet of Flying Things-IoFT: A Machine Learning Approach. IEEE Internet of Things Journal, 10(14), 12854-12866."
topics: [sybil-resistance, swarm-robotics]
added_by: dmarz/sybil-robotics
accessed: 2026-10-03
read_depth: abstract
relevance: 2
citations: "48 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Sybil detection for UAV flying ad hoc networks using physical-layer features of UAV radio signals measured by two ground nodes: received signal strength difference and time difference of arrival. Several supervised classifiers in Weka are compared in simulation, including malicious nodes with power control at levels not seen in training.

## Contribution

Representative of the UAV/FANET Sybil literature, which uses ground infrastructure plus ML rather than swarm-internal trust.

## Key results

- Average correct classification above 91% in simulation, including power-controlling attackers (abstract).
- No extra communication overhead for the UAVs (claimed).

## Methods and models

RSSD and TDoA features, supervised classifiers, simulation. Abstract read only; details beyond the abstract not checked.

## Limitations and open questions

Needs fixed ground nodes; simulation only.

## Relevance to us

Shows the UAV swarm community's default: external infrastructure as identity anchor, the opposite of fully decentralised defences like [[mallmann-trenn-2021-crowd]].

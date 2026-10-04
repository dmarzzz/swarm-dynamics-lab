---
id: adams-2025-can
type: paper
title: "Can a Single Human Supervise a Swarm of 100 Heterogeneous Robots?"
authors: ["Julie A. Adams", "Joshua Hamell", "Phillip Walker"]
year: 2025
venue: "IEEE Transactions on Field Robotics"
url: https://arxiv.org/html/2308.00102
doi: "10.1109/tfr.2024.3502316"
arxiv: "2308.00102"
cite: "Adams, J. A., Hamell, J., & Walker, P. (2025). Can a Single Human Supervise a Swarm of 100 Heterogeneous Robots? IEEE Transactions on Field Robotics, 2, 46-80. https://doi.org/10.1109/tfr.2024.3502316 (preprint arXiv:2308.00102, 2023)."
topics: [swarm-robotics]
added_by: dmarz/swarm-robotics-recent-audit
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: "9 (Crossref is-referenced-by-count, 2026-10-03; OpenAlex search budget exhausted during this audit)"
code: []
---

## Summary

Field study from DARPA's OFFensive Swarm-Enabled Tactics (OFFSET) programme. The CCAST integrator team (about 200 hardware UGVs and UAVs plus 250 simulated vehicles over the programme) let one "swarm commander" deploy a heterogeneous swarm of up to 100 robots in urban missions at US Army training sites through an immersive interface. During the final field exercise (FX-6) the team recorded wearable physiological and environmental metrics and subjective ratings, and estimated workload components (cognitive, speech, auditory, physical, visual) and overall workload with a multi-dimensional workload algorithm.

## Contribution

The first human-subjects data set of a single person deploying a hardware swarm of this size in a real urban environment. It answers the scale question for human-swarm interaction empirically rather than in lab studies with small swarms.

## Key results

- Workload estimates crossed the overload threshold frequently but the commander still completed the missions, often in difficult conditions (abstract).
- Over twelve shifts (eight at the urban training facility), overall workload was generally manageable and rose with task load; perceived stress spiked on critical shifts (such as distinguished-visitor day); fatigue varied with shift duration (Conclusions).
- Earlier OFFSET exercises showed a trained commander could run shifts of up to three hours.
- Qualitative findings: live video feeds were of little use outdoors because of low image quality, limited bandwidth and frequent loss of communication, and none were possible indoors.

## Methods and models

CCAST system with the I3 immersive interface and tactic-level commands; AprilTags stand in for mission artefacts; workload algorithm from Heard et al. combining wearable physiological metrics and an environmental metric. I skimmed the structure, abstract, discussion and conclusions; I did not check the per-shift statistics.

## Limitations and open questions

Few subjects (the team's own trained commanders), so this is a feasibility demonstration, not a controlled study. The robots are tactic-driven rather than self-organising, so "swarm" here means a large heterogeneous fleet. AprilTag artefacts sidestep perception errors that would raise workload.

## Relevance to us

The reference point for human-swarm interaction at scale, a gap the scan flagged. Contrast with LLM-mediated operation in [[strobel-2026-how]] and [[schuck-2025-swarmgpt]], and with the self-organised hierarchy of [[zhu-2024-self]].

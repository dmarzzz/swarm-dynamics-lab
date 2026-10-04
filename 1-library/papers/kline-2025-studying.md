---
id: kline-2025-studying
type: paper
title: "Studying collective animal behaviour with drones and computer vision"
authors: ["Jenna Kline", "Saadia Afridi", "Edouard G. A. Rolland", "Guy Maalouf", "Lucie Laporte-Devylder", "Christopher Stewart", "Margaret Crofoot", "Charles V. Stewart", "Daniel I. Rubenstein", "Tanya Berger-Wolf"]
year: 2025
venue: "Methods in Ecology and Evolution"
url: https://kops.uni-konstanz.de/bitstream/123456789/74478/1/Kline_2-hbqt5sr7yhl53.pdf
doi: "10.1111/2041-210x.70128"
arxiv: null
cite: "Kline, J., Afridi, S., Rolland, E. G. A., Maalouf, G., Laporte-Devylder, L., Stewart, C., Crofoot, M., Stewart, C. V., Rubenstein, D. I., & Berger-Wolf, T. (2025). Studying collective animal behaviour with drones and computer vision. Methods in Ecology and Evolution, 16(10), 2229–2259."
topics: [collective-motion, meta]
added_by: dmarz/collective-motion-recent-audit
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: "11 (OpenAlex W4413447615, 2026-10-03)"
code: []
---

## Summary

A methods review of 'AI-driven animal ecology' for collective behaviour from drone imagery. It walks the pipeline from mission planning and flight mode (manual, automatic waypoint, autonomous) through detection, classification, tracking, pose estimation and behaviour inference, maps computer-vision tasks to ecological questions, and argues that analysis success often depends on mission planning choices made with downstream computation in mind, which current studies often neglect.

## Contribution

The first systematic map of drone plus computer-vision work for collective animal behaviour, with practical guidelines; useful as an entry point to field data collection for wild groups (ungulates, primates, birds).

## Key results

- Review finding: studies focus mostly on detection and classification; CNNs dominate, while transformer models and video networks (X3D, I3D, SlowFast) are gaining ground for pose and behaviour.
- Review finding: reported model accuracy varies widely by task, species, habitat and metric, so cross-study comparison is hard.
- Practical numbers: in the KABR project (zebras and giraffes, Kenya) each 4K flight produced about 20.5 GB; about six missions a day for three weeks yielded about 1 TB.
- Prediction: semi-autonomous, edge-AI drone missions will become standard for collective-behaviour studies.

## Methods and models

Narrative and structured review with tables of flight modes, pipelines and tasks; examples from the KABR dataset and WildDrone network. Tools cited include CVAT and Ultralytics YOLO.

## Limitations and open questions

Read at skim depth (abstract, introduction, tables and data-management section). Focus is on detection and behaviour classification; there is little on extracting individual trajectories for interaction-rule inference, which is what most collective-motion modelling needs.

## Relevance to us

Guide for anyone proposing field data for the hackathon; complements lab tracking tools [[waldmann-2024-3d]], [[itoh-2024-fish]], [[phurtivilai-2026-trackfish3d]] and the analysis package [[papadopoulou-2024-swarmverse]]. Field context for [[jadhav-2024-collective]].

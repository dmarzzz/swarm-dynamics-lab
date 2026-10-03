---
id: gh-jacopopan-aerial-autonomy-stack
type: code
title: "aerial-autonomy-stack: PX4/ArduPilot + ROS2 multi-drone simulation and deployment stack with faster-than-real-time perception"
repo: JacopoPan/aerial-autonomy-stack
url: https://github.com/JacopoPan/aerial-autonomy-stack
authors: ["JacopoPan"]
year: 2025
language: C++/Python
license: "MIT"
stars: 610
last_commit: 2026-10-03
topics: [swarm-robotics]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 3
papers: []
---

## Summary

Stack for developing, simulating and deploying multi-drone autonomy: PX4 and ArduPilot multi-vehicle SITL (quadrotors, quadplane VTOLs, tailsitters), ROS2 action-based autopilot interface (XRCE-DDS or MAVROS), YOLO perception on ONNX GPU runtimes and LiDAR odometry (KISS-ICP), faster-than-real-time simulation, deployment on NVIDIA Orin/JetPack. Compare the lighter [[gh-learnsyslab-gym-pybullet-drones]].

## What it can do for us

Realistic path from simulated drone swarm to hardware; far heavier than needed for abstract swarm studies.

## Run notes

Not run. Stars, licence and last push from the GitHub API on 2026-10-03; README read via the API; source code not read.

## Limitations

Docker/ROS2/GPU heavy; disk-hungry; aimed at flight-realistic autonomy, not large swarms.

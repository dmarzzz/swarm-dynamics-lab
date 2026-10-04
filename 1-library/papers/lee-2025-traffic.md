---
id: lee-2025-traffic
type: paper
title: 'Traffic Control via Connected and Automated Vehicles (CAVs): An Open-Road Field Experiment with 100 CAVs'
authors:
- Jonathan W. Lee
- Han Wang
- Kathy Jang
- Nathan Lichtlé
- Amaury Hayat
- Matthew Bunting
- Arwa Alanqary
- William Barbour
- Zhe Fu
- Xiaoqian Gong
- George Gunter
- Sharon Hornstein
- Abdul Rahman Kreidieh
- Mat-Thew W. Nice
- William A. Richardson
- Adit Shah
- Eugene Vinitsky
- Fangyu Wu
- Shengquan Xiang
- Sulaiman Almatrudi
- Fahd Althukair
- Rahul Bhadani
- Joy Carpio
- Raphael Chekroun
- Eric Cheng
- Maria Teresa Chiri
- Fang-Chieh Chou
- Ryan Delorenzo
- Marsalis Gibson
- Derek Gloudemans
- Anish Gollakota
- Junyi Ji
- Alexander Keimer
- Nour Khoudari
- Malaika Mahmood
- Mikail Mahmood
- Hossein Nick Zinat Matin
- Sean Mcquade
- Rabie Ramadan
- Daniel Urieli
- Xia Wang
- Yanbing Wang
- Rita Xu
- Mengsha Yao
- Yiling You
- Gergely Zachár
- Yibo Zhao
- Mostafa Ameli
- Mirza Najamuddin Baig
- Sarah Bhaskaran
- Kenneth Butts
- Manasi Gowda
- Caroline Janssen
- John Lee
- Liam Pedersen
- Riley Wagner
- Zimo Zhang
- Chang Zhou
- Daniel B. Work
- Benjamin Seibold
- Jonathan Sprinkle
- Benedetto Piccoli
- Maria Laura Delle Monache
- Alexandre M. Bayen
year: 2025
venue: IEEE Control Systems
url: https://arxiv.org/abs/2402.17043
doi: 10.1109/mcs.2024.3498552
arxiv: '2402.17043'
cite: 'Lee, J. W., Wang, H., Jang, K., Lichtlé, N., Hayat, A., Bunting, M., Alanqary, A., Barbour, W., Fu, Z., Gong, X., et al. (2025). Traffic Control via Connected and Automated Vehicles (CAVs): An Open-Road Field Experiment with 100 CAVs. IEEE Control Systems, 45(1), 28–60. https://doi.org/10.1109/mcs.2024.3498552'
topics:
- crowds-and-traffic
- swarm-robotics
- sync-consensus
added_by: dmarz/crowds-and-traffic
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 47 (Crossref, 2026-10-03)
code: []
---

## Summary

Describes the CIRCLES project's control system for its open-road field experiment (the "MegaVanderTest") with a heterogeneous fleet of 100 longitudinally controlled vehicles acting as Lagrangian traffic actuators on a real freeway to reduce stop-and-go waves. A centralised Speed Planner ingests live traffic data and assigns speed targets over the cellular network; on each car a local controller overrides the stock adaptive cruise control using on-board sensors. The architecture accommodates optimal control, MPC, kernel methods and deep RL controllers.

## Contribution

Scales the ring-road single-AV demonstration ([[stern-2018-dissipation]]) to the largest open-road traffic-smoothing experiment reported, with a hierarchical (central plus local) architecture for controlling a swarm embedded in human traffic.

## Key results

- Reported (abstract): deployment of 100 controlled vehicles with a two-layer MegaController architecture; most configurations tested during ramp-up.
- Quantitative effects on traffic are not given in the abstract (not extracted).

## Methods and models

Hierarchical control; LTE communication; stock ACC override; data from third-party feeds and the fleet. IEEE Control Systems Magazine 45(1), 28–60. 64 authors (first ten listed in cite).

## Limitations and open questions

Abstract-level read; impact measurement relies on the I-24 MOTION instrument ([[gloudemans-2023-i24]]) and companion papers.

## Relevance to us

A real-world swarm-control deployment with documented architecture choices (central planner versus local control), informative for any hackathon design that mixes coordination layers. Companion RL paper: [[jang-2025-reinforcement]].

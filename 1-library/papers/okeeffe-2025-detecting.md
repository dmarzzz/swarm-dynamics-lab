---
id: okeeffe-2025-detecting
type: paper
title: "Detecting and diagnosing faults in autonomous robot swarms with an artificial antibody population model"
authors: ["James O’Keeffe"]
year: 2025
venue: "Royal Society Open Science"
url: https://doi.org/10.1098/rsos.251252
doi: "10.1098/rsos.251252"
arxiv: null
cite: "O'Keeffe, J. (2025). Detecting and diagnosing faults in autonomous robot swarms with an artificial antibody population model. Royal Society Open Science, 12(10), 251252. https://doi.org/10.1098/rsos.251252"
topics: [swarm-robotics]
added_by: dmarz/swarm-robotics-recent-audit
accessed: 2026-10-03
read_depth: skim
relevance: 2
citations: "3 (Crossref is-referenced-by-count, 2026-10-03; OpenAlex search budget exhausted during this audit)"
code: []
---

## Summary

Most swarm fault-tolerance work assumes sudden, complete failures in a few robots. This paper targets gradual wear, which is harder to notice. Inspired by Farmer et al.'s model of antibody population dynamics, the artificial antibody population dynamics (AAPD) model lets robots compare their behaviour features against peers, grow "antibody" populations against abnormal ones, and so detect and diagnose degrading motors or sensors. It runs distributed, in unsupervised (zeroth-order) or supervised, repertoire-based (higher-order) forms, and is tested on simulated foraging swarms of 2 to 20 robots in which much of the swarm degrades at once.

## Contribution

Extends immune-inspired swarm fault detection from step failures to gradual degradation, and adds diagnosis (which robot, which hardware, and for motors which side). It fills a gap the scan flagged next to [[shefi-2025-bugs]].

## Key results

- Foraging swarms using AAPD operate on average at 70-97% of their fault-free performance under gradual degradation and avoid most in-field failures (abstract).
- Gradual motor degradation: zeroth-order model detects at median degradation delta = 0.53 with true-positive score 0.78; first-order improves to 0.6 and 0.86. Gradual sensor degradation: zeroth-order 0.61 and 0.85; second-order up to 0.74 and 1.0 (Conclusions; target was delta = 0.75 and Psi_T = 1).
- Sudden complete failure: median Psi_T = 1 and Psi_F = 0 for swarms with as few as five robots.
- Fine diagnosis: first-order model identifies left, right or both motors correctly in 87% of tested cases.
- Stable performance for swarms of 5-10 robots even while much of the swarm degrades simultaneously.

## Methods and models

Simulated differential-drive robots (max wheel speed 0.22 m/s, 16 cm axle, 4 m max sensing range, 5% Gaussian noise), power-consumption model, degradation severities d_l, d_r, d_S on motors and sensor; 2 <= N <= 20. Single-author paper. I skimmed methods notation, results figures text and conclusions.

## Limitations and open questions

Simulation only. Performance depends on a majority of robots being in the normal range, the usual weakness of peer-comparison methods. Recovery strategies beyond detection are only sketched.

## Relevance to us

Background for any experiment on robustness of collective behaviour to degrading agents. Related: [[shefi-2025-bugs]] (fault-tolerant collective motion), [[raveendra-2026-syncsbc]] (decentralised behaviour classification for anomaly detection).

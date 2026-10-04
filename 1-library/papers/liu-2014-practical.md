---
id: liu-2014-practical
type: paper
title: "Practical User Authentication Leveraging Channel State Information (CSI)"
authors: [Hongbo Liu, Yan Wang, Jian Liu, Jie Yang, Yingying Chen]
year: 2014
venue: Proceedings of the 9th ACM Symposium on Information, Computer and Communications Security (ASIA CCS '14), Kyoto, pp. 389-400
url: https://mosis.uga.edu/jianliu/publications/liu2014practical.pdf
doi: 10.1145/2590296.2590321
arxiv: null
cite: "Liu, H., Wang, Y., Liu, J., Yang, J., & Chen, Y. (2014). Practical User Authentication Leveraging Channel State Information (CSI). In Proceedings of the 9th ACM Symposium on Information, Computer and Communications Security (ASIA CCS '14), pp. 389-400. ACM. https://doi.org/10.1145/2590296.2590321"
topics: [sybil-resistance]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: "88 (Crossref, 2026-10-03)"
code: []
---

## Summary

Non-cryptographic user/device authentication for Wi-Fi using channel state information (CSI, the per-subcarrier complex channel response exposed by commodity Intel 5300 cards, 30 subcarriers per antenna pair) instead of scalar RSS. The framework has two parts. An attack-resilient profile builder clusters the CSI samples collected while enrolling a user and, if the clusters are farther apart than a distance threshold tau, concludes a spoofer was present during profile building and discards the contaminated samples; with tau = 17 dB the CSI builder detects spoofer presence with an average ratio of 0.92, versus at most 0.40 for the RSS equivalent (tau = 2 dB). A machine-learning authenticator (SVM-style classification on CSI features, with outlier filtering) then decides whether incoming frames come from the enrolled user and flags spoofers, and can separate two users even when their RSS fingerprints coincide (a known failure mode of RSS: distant positions with similar RSS). Experiments in an office laboratory and an apartment: average authentication accuracy above 0.984 for CSI vs 0.92 for RSS; worst-case accuracy stays above 0.95 for CSI while RSS collapses to 0.27 (apartment) and 0.36 (laboratory) when two users share similar RSS. Read: abstract, introduction, framework overview, CSI vs RSS motivation, Section 7 evaluation (Figures 8 and 10 discussion), conclusion; feature extraction details skimmed.

## Contribution

Moves physical-layer identity from scalar RSS to full CSI on off-the-shelf hardware and shows the gain is largest exactly where RSS fails (users with coincident RSS signatures, and spoofers present during enrolment).

## Key results

- Spoofer-during-enrolment detection: 0.92 (CSI, tau 17 dB) vs 0.40 max (RSS).
- Average authentication accuracy: >0.984 (CSI) vs 0.92 (RSS).
- Worst-case accuracy with similar-RSS users: >0.95 (CSI) vs 0.27-0.36 (RSS).

## Methods and models

Intel 5300 CSI tool, 30 subcarriers; clustering with distance threshold for profile hygiene; supervised classifier for authentication; two indoor testbeds; comparison against RSS baselines from the authors' earlier work.

## Limitations and open questions

Static indoor settings; CSI profiles drift with environment and body movement, so re-enrolment policy matters; a spoofer within the channel coherence distance is not addressed; single-AP. Identity here means "same physical transmitter at the same place", not a person.

## Relevance to us

Fills the gap between RSS-based ([[sheng-2008-detecting]], [[yang-2013-detection]]) and array-based ([[xiong-2013-securearray]]) physical-layer identity: richer per-message fingerprints make it much harder for one device to pass as several, or several as one, and the enrolment-poisoning check is a useful idea for any fingerprint-based agent registry (verify the enrolment sample is unimodal before trusting the profile). Robotics transfer: [[gil-2015-guaranteeing]]. Taxonomy: [[urdaneta-2011-survey]].

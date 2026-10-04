---
id: yang-2013-detection
type: paper
title: "Detection and Localization of Multiple Spoofing Attackers in Wireless Networks"
authors: [Jie Yang, Yingying Chen, Wade Trappe, Jerry Cheng]
year: 2013
venue: IEEE Transactions on Parallel and Distributed Systems, vol. 24, no. 1, pp. 44-58 (extends INFOCOM 2009 paper "Determining the Number of Attackers and Localizing Multiple Adversaries in Wireless Spoofing Attacks")
url: https://ieeexplore.ieee.org/document/6175890
doi: 10.1109/tpds.2012.104
arxiv: null
cite: "Yang, J., Chen, Y., Trappe, W., & Cheng, J. (2013). Detection and Localization of Multiple Spoofing Attackers in Wireless Networks. IEEE Transactions on Parallel and Distributed Systems, 24(1), 44-58. https://doi.org/10.1109/TPDS.2012.104"
topics: [sybil-resistance, swarm-detection]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "166 (Crossref, 2026-10-03)"
code: []
---

## Summary

Treats identity spoofing in wireless networks as a spatial problem: several adversaries at different locations transmit under one legitimate node's identity, and the defender wants to (1) detect that spoofing is happening, (2) count how many distinct attackers share the identity, and (3) localise each of them, all from received signal strength (RSS) measured at a few landmarks, with no cryptography. GADE (Generalized Attack Detection modEl) clusters the RSS vectors observed for one identity with Partitioning Around Medoids; if the medoids are farther apart in signal space than a threshold tau the identity is being spoofed. Counting attackers is cast as multi-class detection: silhouette-plot and a system-evolution method pick the cluster count, and SILENCE adds minimum-distance testing between clusters to fix the silhouette method's tendency to undercount when attackers are close; with training data an SVM classifier improves counting further (TPDS version). IDOL feeds the clusters into standard RSS localisation algorithms (RADAR-style nearest neighbour, area-based probability, Bayesian networks) to position each attacker. Experiments on two office testbeds, an 802.11 network and an 802.15.4 ZigBee network: detection rate above 98% at under 10% false positives with tau around 10 dB, still above 95% at zero false positives; silhouette-plot counting hit rate 99.59% / 89.81% / 80.52% for 2 / 3 / 4 attackers on 802.11 (precision 91.85 / 87.29 / 99.33%), similar on ZigBee; SILENCE and SVM raise hit rate and precision above 90% across attacker counts; localisation accuracy comparable to the single-node case. Read from the open INFOCOM 2009 PDF (abstract, intro, GADE, Table I, detection-rate discussion) plus the TPDS abstract via IEEE Xplore for the journal additions (SVM).

## Contribution

First wireless spoofing detector that counts and localises multiple simultaneous impostors behind one identity, using only RSS clustering, and shows it works on two radio technologies in real buildings.

## Key results

- Spoofing detection >98% at <10% FPR (tau ~ 10 dB), >95% at 0% FPR (Fig. 4 of INFOCOM version).
- Counting attackers via silhouette: hit rate 99.6% (2), 89.8% (3), 80.5% (4) on 802.11; SILENCE/SVM push both hit rate and precision above 90%.
- Localisation of multiple attackers achieved with existing RSS algorithms once clusters are separated.

## Methods and models

RSS vectors from n landmarks; PAM clustering; thresholds on medoid distance; silhouette plot, system-evolution and SILENCE for K; SVM with training (TPDS); IDOL localisation pipeline. Testbeds: 802.11 and 802.15.4 in two office buildings.

## Limitations and open questions

Attackers must be spatially separated from the victim and each other by more than the RSS resolution; attackers varying transmit power are only partly handled; indoor static testbeds. The inverse problem, one radio claiming many identities (classic Sybil), is the natural complement and is not evaluated here.

## Relevance to us

The clearest "how many distinct physical sources are behind this identity" method in the library, which is structurally the swarm-detection question in reverse (we usually ask how many identities share one source). The clustering-plus-count-estimation pipeline is directly reusable for operator attribution from behavioural fingerprints. Sits with [[sheng-2008-detecting]] (GMM RSS profiles) and [[xiong-2013-securearray]] (angle-of-arrival signatures) in the physical-layer family, and with [[gil-2015-guaranteeing]] for the robotics transfer; taxonomy context in [[urdaneta-2011-survey]].

---
id: xiong-2013-securearray
type: paper
title: "SecureArray: Improving WiFi Security with Fine-Grained Physical-Layer Information"
authors: [Jie Xiong, Kyle Jamieson]
year: 2013
venue: Proceedings of the 19th Annual International Conference on Mobile Computing and Networking (MobiCom '13), Miami, pp. 441-452
url: https://www.cs.princeton.edu/~kylej/papers/p441-xiong.pdf
doi: 10.1145/2500423.2500444
arxiv: null
cite: "Xiong, J., & Jamieson, K. (2013). SecureArray: Improving WiFi Security with Fine-Grained Physical-Layer Information. In Proceedings of the 19th Annual International Conference on Mobile Computing and Networking (MobiCom '13), pp. 441-452. ACM. https://doi.org/10.1145/2500423.2500444"
topics: [sybil-resistance]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: "98 (Crossref, 2026-10-03)"
code: []
---

## Summary

Defence-in-depth for Wi-Fi against spoofing and session-hijack attacks by an adversary who may already hold the victim's keys. A multi-antenna access point (eight-antenna WARP radio) runs MUSIC-style angle-of-arrival (AoA) estimation on every received frame to obtain a multipath AoA spectrum, a signature of the exact client-AP channel at that instant that is very hard to forge from a different location. When the AP overhears a frame whose signature does not match the client's recent signatures beyond a similarity threshold eta, client and AP run a short AoA-signature challenge-response: the AP asks the legitimate client to transmit again and compares signatures, so an attacker cannot provoke false alarms by sending junk (sigma_2 guard) and the AP can drop the hijack. The paper also discusses mitigating deauthentication-style DoS against 802.11w. Evaluation in a busy office with static and mobile clients: 100% of spoofing attempts detected at a 0.6-0.67% false-alarm rate on legitimate traffic (L = 15 recent signatures, eta = 0.7); detection stays high when the attacker is only 5 cm from the client, with fewer AP antennas, and when both client and attacker walk at about 5 km/h. Read: abstract, introduction, threat model, overview of the AoA signature and challenge-response, evaluation headline figures and the mobility section; signal-processing derivations skimmed.

## Contribution

Shows that commodity-MIMO-era APs can extract a per-frame physical-layer signature fine-grained enough to separate transmitters 5 cm apart, and wraps it in a protocol that keeps false alarms low under mobility.

## Key results

- 100% attack detection with 0.6% false alarms in a busy office (static); ROC shows 100% detection at 0.67% false alarm with L = 15.
- Detection remains high at 5 cm client-attacker separation and with reduced antenna count.
- Mobile experiments (client and attacker both moving ~5 km/h) keep detection high after calibrated AoA.
- "Orders of magnitude" more accurate than RSS-based prior techniques (authors' comparison).

## Methods and models

8-antenna WARP AP, MUSIC AoA spectra, signature similarity with window L and threshold eta, challenge-response confirmation, one-time cable-phase calibration; office floor-plan testbed with line-of-sight and non-line-of-sight placements.

## Limitations and open questions

Requires AP-side antenna arrays and raw channel access, not available on most consumer APs in 2013 (less true now). An attacker co-located within a wavelength could in principle match; the paper's 5 cm result bounds this. Does not treat one radio claiming many identities (Sybil), though the same signatures would collapse them to one source.

## Relevance to us

Upper end of the physical-layer identity family: where [[sheng-2008-detecting]] uses coarse RSS and [[yang-2013-detection]] clusters RSS vectors, SecureArray uses full multipath AoA and reaches near-perfect separation, which is also the primitive behind the robot Sybil work in [[gil-2015-guaranteeing]] and [[gil-2018-resilient]] (synthetic aperture instead of a fixed array). For agent swarms the analogue is a high-dimensional per-message fingerprint plus a challenge-response step, rather than a single scalar feature. Taxonomy: [[urdaneta-2011-survey]].

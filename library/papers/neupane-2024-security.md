---
id: neupane-2024-security
type: paper
title: "Security Considerations in AI-Robotics: A Survey of Current Methods, Challenges, and Opportunities"
authors: [Subash Neupane, Shaswata Mitra, Ivan A. Fernandez, Swayamjit Saha, Sudip Mittal, Jingdao Chen, Nisha Pillai, Shahram Rahimi]
year: 2024
venue: IEEE Access, vol. 12, pp. 22072-22097
url: https://arxiv.org/abs/2310.08565
doi: 10.1109/access.2024.3363657
arxiv: "2310.08565"
cite: "Neupane, S., Mitra, S., Fernandez, I. A., Saha, S., Mittal, S., Chen, J., Pillai, N., & Rahimi, S. (2024). Security Considerations in AI-Robotics: A Survey of Current Methods, Challenges, and Opportunities. IEEE Access, 12, 22072-22097. https://doi.org/10.1109/ACCESS.2024.3363657"
topics: [swarm-robotics, sybil-resistance]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: skim
relevance: 2
citations: "72 (Crossref, 2026-10-03)"
code: []
---

## Summary

Broad survey of security for AI-driven robots organised around a three-layer architecture (perception, navigation and planning, control) and three dimensions: attack surfaces, ethical and legal concerns, and human-robot interaction (HRI) security. The attack-surface part tabulates jamming and spoofing of cameras, GPS, LiDAR and ultrasonics (Table II), adversarial examples against perception models, attacks on planners (including a cited work that uses deep RL to launch Sybil attacks with spoofed beacons against UAV path planning) and on controllers, plus communication and firmware vectors, with mitigations such as sensor fusion, filtering, randomization, anomaly detection and adversarial training. Authentication and access control are flagged as "often overlooked" in robotic systems, with the Sybil attack named as the example. Swarms appear only in the future-work section (VII-B "Securing Swarm Robotics and Knowledge Transfer"), which says a swarm can become inoperative if one constituent is attacked and points to secured federated learning and cybersecurity knowledge graphs as emerging defences; no swarm-specific attack analysis is given. Read from the arXiv HTML (v3, Jan 2024): abstract, structure, searched the text for Sybil, swarm, multi-robot and spoofing passages, and the future-research section. Middle sections (ethics, HRI) skimmed by heading only.

## Contribution

A one-stop taxonomy of attack surfaces across the perception-planning-control stack with an unusual pairing of technical attacks and ethical/legal/HRI concerns; useful as an orientation map rather than for any specific result.

## Key results

- Taxonomy across three architectural layers and three concern dimensions; Table II maps sensor attacks (jamming, spoofing, blinding) to defences (filters, fusion, randomization, anomaly detection).
- Seven future-research domains (Fig. 9): attack-surface mitigation, securing swarm robotics and knowledge transfer, human-robot ecosystems, explainability, safe robot learning, V&V of AI-robotics, education.
- No quantitative results of its own; all numbers come from cited work.

## Methods and models

Narrative literature survey (no systematic search protocol stated in the parts read). ~245 references.

## Limitations and open questions

Swarm and multi-robot security gets a few paragraphs; Sybil and identity attacks are mentioned, not analysed. Heavy on single-robot sensor attacks. As a 2023/24 survey it predates most LLM-agent-in-robots work.

## Relevance to us

Low: background context linking the robotics-security vocabulary (spoofing, jamming, adversarial perception) to the swarm and Sybil threads. The useful pointer is its admission that multi-robot/swarm security and sensor-fusion under faulty or malicious members are open, which is where [[gil-2015-guaranteeing]] and [[tang-2026-passivity]] sit. For an actual swarm-security survey use [[bijani-2014-review]] (open MAS attacks) or the Sybil-specific [[urdaneta-2011-survey]] instead.

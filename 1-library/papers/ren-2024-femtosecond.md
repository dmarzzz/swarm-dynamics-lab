---
id: ren-2024-femtosecond
type: paper
title: "Femtosecond laser writing of ant-inspired reconfigurable microbot collectives"
authors: ["Zhongguo Ren", "Chen Xin", "Kaiwen Liang", "Heming Wang", "Dawei Wang", "Liqun Xu", "Yanlei Hu", "Jiawen Li", "Jiaru Chu", "Dong Wu"]
year: 2024
venue: "Nature Communications"
url: https://doi.org/10.1038/s41467-024-51567-4
doi: "10.1038/s41467-024-51567-4"
arxiv: null
cite: "Ren, Z., Xin, C., Liang, K., Wang, H., Wang, D., Xu, L., Hu, Y., Li, J., Chu, J., & Wu, D. (2024). Femtosecond laser writing of ant-inspired reconfigurable microbot collectives. Nature Communications, 15(1), 7253. https://doi.org/10.1038/s41467-024-51567-4"
topics: [swarm-robotics]
added_by: dmarz/swarm-robotics-recent-audit
accessed: 2026-10-03
read_depth: skim
relevance: 2
citations: "44 (Crossref is-referenced-by-count, 2026-10-03; OpenAlex search budget exhausted during this audit)"
code: []
---

## Summary

Ant-shaped microbots (tens of micrometres) are printed by two-photon polymerisation from a magnetic photoresist, a hydrogel and silver nanoparticles. Magnetic fields drive them, and near-infrared light heats the nanoparticles so asymmetric hydrogel joints open the "mandibles", letting microbots grip each other. Combining the two fields, the microbots assemble reversibly and selectively into connected architectures (90 and 180 degree assemblies) that, unlike field-induced clusters, stay connected without a continuous stimulus. Assemblies cross a one-body-length gap, squeeze through a constriction and carry micro-cargo, including a drug-loaded hydrogel block tested on HeLa cells.

## Contribution

Physical (mechanical) linkage for microrobot collectives, addressing the weak, field-maintained connections of most magnetic/light/electric microrobot swarms. It is the microrobot analogue of the ant-bridge and self-assembly ideas in macroscale swarm robotics.

## Key results

- Mandible opening under NIR light with a response time of about 8 ms (measured); laser spot radius about 3.3 um under a 5x objective.
- Reversible, selective 90 and 180 degree assemblies; gap crossing of one body length; passage through a constriction; micro-cargo transport (measured demonstrations).
- Drug-delivery demonstration with a doxorubicin hydrogel block (fluorescence statistics, n = 3).

## Methods and models

Femtosecond-laser two-photon polymerisation of a multi-material microbot; magnetic actuation plus NIR photothermal actuation of asymmetric-crosslink hydrogel joints; finite-element simulation of the photothermal deformation. I skimmed the abstract, figure captions and discussion.

## Limitations and open questions

Collectives are small and centrally actuated by global fields, so this is externally steered assembly rather than decentralised swarm control. Individual addressability is limited.

## Relevance to us

Fills the microrobot gap of the scan. For the swarm-dynamics hackathon it is background only; see [[yang-2024-machine]] for the microrobot ML review and the micro/nanomotor swarming review [[patino-padial-2025-swarming]] and the microrobot collective-transport paper [[heuthe-2024-counterfactual]].

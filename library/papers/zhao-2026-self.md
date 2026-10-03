---
id: zhao-2026-self
type: paper
title: "Self-organized criticality in aquatic robot swarm"
authors: ["Shiji Zhao", "Jiajun Huang", "Chaoqun Li", "Shengli Mi"]
year: 2026
venue: "Science Advances"
url: https://doi.org/10.1126/sciadv.aec6153
doi: "10.1126/sciadv.aec6153"
arxiv: null
cite: "Zhao, S., Huang, J., Li, C., & Mi, S. (2026). Self-organized criticality in aquatic robot swarm. Science Advances, 12(20), eaec6153."
topics: [swarm-robotics, criticality-measurement, active-matter]
added_by: dmarz/swarm-robotics-recent
accessed: 2026-10-03
read_depth: skim
relevance: 5
citations: "0 (OpenAlex W7161009362, 2026-10-03); 0 (Crossref, 2026-10-03)"
code: []
---

## Summary

An aquatic robot swarm whose units are propelled by vibrating TPU films (4 cm discs). The robots interact through optical attraction (visible-light signals) and hydrodynamic wave repulsion, a physical nonlinear feedback loop. The swarm shows hallmarks of self-organised criticality: power-law distributions of correlated-cluster ('avalanche') sizes and durations, 1/f-like spectra, exponents stable under system upscaling, and evolution to a steady state independent of parameters. With external stimuli it stays critical and forms directed structures with adaptive behaviours such as collective pushing.

## Contribution

A rare physical, programmable realisation of SOC in a robot swarm, with measured exponents, complementing tuned-criticality robot studies such as [[verdoucq-2025-flocking]].

## Key results

- Cluster-size exponent tau = 1.68(3) (MLE), duration exponent alpha = 1.54(2), size-duration exponent gamma = 0.74(4), spectral exponent beta = 1.26(3) over 0.01-1 Hz (measured in experiments; values from the full text I skimmed).
- Lattice-model simulations give tau = 1.16(2), alpha = 2.67(1), gamma = 0.11(1): power laws, but different exponents from experiment.
- Under strong parameter changes, tau_exp = 1.35(2) and tau_sim = 1.23(1), still power-law (measured).
- The avalanche statistics come from physical experiments with N = 64 robots placed uniformly on the water surface and started simultaneously (Methods; Fig. 2B shows the cluster composition of this stable 64-robot system).

## Methods and models

Vibration-propelled floating robots with light emission and sensing, hydrodynamic repulsion, correlated-cluster detection, MLE power-law fits and a 2-D lattice simulation for finite-size analysis (skimmed via Europe PMC full text).

## Limitations and open questions

Skimmed. Power-law claims over limited ranges with finite-size cutoffs; experiment and simulation exponents disagree substantially; 'avalanche' depends on the cluster definition.

## Relevance to us

A key empirical paper for any hackathon claim about criticality in swarms; its methods (cluster statistics, MLE exponents, 1/f spectra) are directly reusable. See [[cavagna-2010-scale]] and [[verdoucq-2025-flocking]].

## Notes from dmarz/swarm-robotics-recent-audit

Audited 2026-10-03 against the Europe PMC full text (PMC13170653). Exponents tau = 1.68(3), alpha = 1.54(2), gamma = 0.74(4), beta = 1.26(3), the lattice-model values 1.16(2)/2.67(1)/0.11(1) and the perturbed tau_exp = 1.35(2), tau_sim = 1.23(1) all match the paper. Corrected the open N = 64 bullet: the 64-robot system is the physical experiment. Note the paper is internally inconsistent on film size: the text gives 4 cm TPU films, the Fig. 1A caption 3 cm. Replaced the Crossref-only citation count with OpenAlex.

---
id: berner-2023-adaptive
type: paper
title: Adaptive dynamical networks
authors: [Rico Berner, Thilo Gross, Christian Kuehn, Jürgen Kurths, Serhiy Yanchuk]
year: 2023
venue: Physics Reports
url: https://arxiv.org/abs/2304.05652
doi: 10.1016/j.physrep.2023.08.001
arxiv: '2304.05652'
cite: "Berner, R., Gross, T., Kuehn, C., Kurths, J., & Yanchuk, S. (2023). Adaptive dynamical networks. Physics Reports, 1031, 1-59."
topics: [sync-consensus, collective-decision]
added_by: dmarz/sync-consensus-audit
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: "132 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

A review of networks whose connectivity changes in response to the dynamical states of their nodes, so that
structure shapes dynamics and dynamics reshapes structure. It classifies adaptive networks (event-based versus
continuous adaptation, slow versus fast adaptation), surveys applications (synaptic plasticity, physiology,
machine learning, control, power grids, social and animal behaviour, epidemics, transport, climate tipping
elements, adaptive delays), catalogues the dynamical phenomena they produce (frequency clusters, solitary states,
recurrent and explosive synchronisation, chimeras, multistability), and reviews mathematical methods
(mean-field Vlasov-Fokker-Planck and moment equations, continuum limits, multiscale decompositions).

## Contribution

The reference review for co-evolving network dynamics, from the groups that developed adaptive phase-oscillator
theory. For swarms, it is the formal home of "who I listen to depends on what we are doing", which is the
situation of mobile agents whose interaction graph depends on their own positions (cf. [[ghosh-2022-synchronized]]
for externally time-varying networks, and swarmalators [[okeeffe-2017-oscillators]] where coupling depends on
state).

## Key results

- Canonical adaptive phase-oscillator model (Section 3.4): dphi_i/dt = omega_i + sum_j a_ij kappa_ij g(phi_i - phi_j),
  dkappa_ij/dt = -epsilon (kappa_ij + h(phi_i - phi_j)), with g and h 2 pi-periodic and epsilon << 1 a slow adaptation
  rate (Kuramoto-Sakaguchi type coupling and plasticity-like adaptation).
- Phenomena specific to adaptive coupling (Section 14): frequency clusters and multicluster states, solitary states,
  recurrent synchronisation, self-organised noise resistance, explosive (first-order) synchronisation with
  hysteresis, heterogeneous nucleation, chimeras.
- The Kuramoto model with inertia can be rewritten as an adaptive network (Section 8), linking power-grid models
  to adaptivity.
- Animal and social behaviour (Section 9): adaptive voter models; the review notes work interpreting animal
  swarming experiments as opinion formation with adaptive networks, including a prediction later verified in
  fish experiments (cited, not opened here).
- Open problems (Section 16): when event-based adaptation can be approximated by continuous rules, extending
  time-scale-separation results from small to large networks, and mean-field theories for adaptive networks.

## Methods and models

Review. Methods covered: slow-fast decomposition, master stability function for adaptive networks, mean-field
and moment closures, continuum limits, bifurcation analysis. Read: abstract, contents, Sections 3.4, 9 (part),
14.7 and the conclusions from the arXiv preprint; most application chapters not read.

## Limitations and open questions

- Very broad; physical motion as the source of adaptivity (agents moving changes who is connected) is not a
  central theme.
- Many results are for small networks or phase oscillators with simple adaptation rules.

## Relevance to us

Gives the vocabulary and known phenomena for swarms whose communication links strengthen or weaken with
agreement (e.g., robots that preferentially listen to in-phase neighbours, or LLM agents that weight peers by past
agreement). Expect frequency clusters and hysteresis rather than a single sync state. Related:
[[hegselmann-2002-opinion]] (state-dependent links in opinion dynamics), [[boccaletti-2023-structure]].

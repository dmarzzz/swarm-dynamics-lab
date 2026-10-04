---
id: helbing-2000-simulating
type: paper
title: Simulating dynamical features of escape panic
authors:
- Dirk Helbing
- Illés Farkas
- Tamás Vicsek
year: 2000
venue: Nature
url: https://arxiv.org/abs/cond-mat/0009448
doi: 10.1038/35035023
arxiv: cond-mat/0009448
cite: Helbing, D., Farkas, I., & Vicsek, T. (2000). Simulating dynamical features of escape panic. Nature, 407(6803), 487–490. https://doi.org/10.1038/35035023
topics:
- crowds-and-traffic
- collective-motion
- collective-decision
added_by: dmarz/crowds-and-traffic
accessed: '2026-10-03'
read_depth: full
relevance: 5
citations: 4955 (OpenAlex, 2026-10-03)
code: []
---

## Summary

Extends the social force model with granular-style body compression and sliding friction to simulate escape from a room through a 1 m door. Above a desired speed of about 1.5 m/s the outflow becomes intermittent, with arches clogging the exit and avalanche-like bursts, so that trying to move faster empties the room more slowly ("faster-is-slower"). A Vicsek-style herding parameter shows that neither pure individualism nor pure herding finds hidden exits efficiently; a mixture does best.

## Contribution

Introduced to a broad audience the idea that crowd disasters can be studied as self-driven many-particle physics, and coined or popularised three effects that structure later work: faster-is-slower at bottlenecks, clogging/arching as in granular hoppers, and the herding versus individualism trade-off for exit choice. The model (social force plus contact forces) is still the most-used evacuation model. Its "panic" framing has since been criticised on empirical grounds ([[haghani-2024-revisiting]]).

## Key results

- Simulated: 200 pedestrians, 15 m x 15 m room, 1 m wide exit. For v0 ≥ 1.5 m/s outflow becomes irregular (arch-like blockings and bursts); the leaving time for 200 people first decreases with v0 and then increases above about 1.5 m/s (faster-is-slower), clearest when flow J is divided by v0 (figure 1c,d).
- Simulated: above about v0 = 5 m/s some pedestrians are "injured" (radial force over circumference exceeds 1600 N/m, a threshold taken from the literature) and become obstacles.
- Simulated: jamming also occurs at widenings of corridors; asymmetric columns in front of exits improve outflow and reduce pressure (shown via figure 2 and online material).
- Simulated: with e_i = N[(1 − p) e_i^own + p ⟨e_j⟩_i] (herding weight p), the fraction escaping a smoky room with hidden exits is maximal at intermediate p (figure 3).
- Calibration: A = 2000 N, B = 0.08 m chosen to reproduce 0.73 persons/s through an effectively 1 m wide door at v0 ≈ 0.8 m/s (literature value). No data on real escape panics were available; the authors explicitly call for such data.

## Methods and models

m_i dv_i/dt = m_i (v_i^0 e_i^0 − v_i)/τ_i + Σ_j f_ij + Σ_W f_iW, with f_ij = {A e^{(r_ij − d_ij)/B} + k g(r_ij − d_ij)} n_ij + κ g(r_ij − d_ij) Δv_ji^t t_ij, g(x) = x if touching else 0. Parameters: m = 80 kg, τ = 0.5 s, k = 1.2 x 10^5 kg s^-2, κ = 2.4 x 10^5 kg m^-1 s^-1, diameters uniform in [0.5, 0.7] m. Impatience: v_i^0(t) = [1 − p_i(t)] v_i^0(0) + p_i(t) v_max with p_i = 1 − v̄_i/v_i^0. Simulation software described in arXiv cond-mat/0302021 (not checked).

## Limitations and open questions

- No quantitative validation against escape data; "panic" behaviours (pushing, herding) are assumed from social-psychology literature that later empirical work disputes (people rarely panic; [[haghani-2024-revisiting]]).
- Faster-is-slower was later observed in granular, sheep, and controlled competitive-egress experiments and reframed as a clogging transition ([[zuriguel-2014-clogging]]), but whether it occurs in real human evacuations is debated.
- Identical parameters for all agents; injury criterion and contact constants are not calibrated on humans.

## Relevance to us

A swarm-level example where increasing individual drive degrades collective throughput, the same structure as congestion collapse in robot swarms passing a doorway. The herding parameter is literally Vicsek alignment ([[vicsek-1995-novel]]) mixed with private information, linking to collective decision-making and the individual versus social information trade-off. Baseline for any bottleneck or evacuation experiment; compare [[helbing-1995-social]], [[helbing-2000-freezing]], [[zuriguel-2014-clogging]].

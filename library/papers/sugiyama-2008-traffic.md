---
id: sugiyama-2008-traffic
type: paper
title: Traffic jams without bottlenecks—experimental evidence for the physical mechanism of the formation of a jam
authors:
- Yuki Sugiyama
- Minoru Fukui
- Macoto Kikuchi
- Katsuya Hasebe
- Akihiro Nakayama
- Katsuhiro Nishinari
- Shin-ichi Tadaki
- Satoshi Yukawa
year: 2008
venue: New Journal of Physics
url: https://iopscience.iop.org/article/10.1088/1367-2630/10/3/033001/pdf
doi: 10.1088/1367-2630/10/3/033001
arxiv: null
cite: Sugiyama, Y., Fukui, M., Kikuchi, M., Hasebe, K., Nakayama, A., Nishinari, K., Tadaki, S.-i., & Yukawa, S. (2008). Traffic jams without bottlenecks—experimental evidence for the physical mechanism of the formation of a jam. New Journal of Physics, 10(3), 033001. https://doi.org/10.1088/1367-2630/10/3/033001
topics:
- crowds-and-traffic
- criticality-measurement
- collective-motion
added_by: dmarz/crowds-and-traffic
accessed: '2026-10-03'
read_depth: full
relevance: 5
citations: 751 (OpenAlex, 2026-10-03); 641 (Crossref, 2026-10-03)
code: []
---

## Summary

Twenty-two human-driven cars were placed on a 230 m circular track at a density chosen (from the optimal velocity model) to sit just above the instability threshold of free flow. Starting from uniform spacing at about 30 km/h, small headway fluctuations grew until, within a few minutes, a cluster of stopped cars formed and propagated backwards as a solitary wave at roughly 20 km/h, the same backward speed measured for jams on real highways. The paper is the first controlled demonstration that a jam can arise purely as a collective instability of a many-particle system, with no bottleneck, lane change or geometric trigger.

## Contribution

It moves the "phantom jam" from a model prediction (Nagel–Schreckenberg cellular automata, Bando's optimal velocity model, Kerner–Konhäuser fluid models) to an experimentally reproduced phenomenon, and frames traffic jam formation as a dynamical, non-equilibrium phase transition in a system of self-driven particles with asymmetric (look-ahead only) interactions. It became the standard ring-road protocol later reused for control experiments ([[stern-2018-dissipation]]) and for the larger Nagoya Dome follow-up ([[tadaki-2013-phase]]).

## Key results

- Measured: 22 cars on a 230 m circumference circuit; free flow persisted for a while, then a jam of about 5 cars formed roughly 3 minutes into the run (figure 3). Cars outside the jam moved at about 40 km/h; cars inside stopped completely.
- Measured: the jam cluster moved backwards at roughly 20 km/h and kept its size and speed (space-time traces, figure 4), matching the backward speed traced from Treiterer and Myers' 1967 aerial highway data (figure 5).
- Measured: with 23 cars a jam also formed with the same backward velocity (footnote; details deferred to later papers).
- Context data (not from this experiment): a month of Japanese freeway detector data gives a fundamental diagram with a sharp free/congested split at a critical density near 25 vehicles/km (figure 1).
- Claimed/interpreted: a bottleneck is only a trigger that raises density above critical; the essential origin of a jam is the instability of homogeneous flow above a critical density.

## Methods and models

Outdoor circular track at Nakanihon Automotive College; 360-degree camera at the centre records positions; drivers instructed to cruise at about 30 km/h and to follow the car in front safely. Density was set using the optimal velocity (OV) model criterion for linear instability of uniform flow (Bando et al. 1995, PRE 51, 1035; the OV model is dv_n/dt = a[V(Δx_n) − v_n]). Analysis is visual and trajectory-based (space-time diagram); no statistical estimate of the critical density is attempted here (that is done in [[tadaki-2013-phase]]). Supplementary movies at stacks.iop.org/NJP/10/033001/mmedia.

## Limitations and open questions

- Essentially one run reported in detail at one density (22 cars) plus a mention of 23 cars; no density sweep, no error bars, no estimate of the critical density or of metastability.
- Short circuit makes the conditions demanding for drivers; the authors say a longer circuit would be easier. Finite-size effects on a ring (only one jam fits) are not discussed.
- Driver heterogeneity and reaction times are not measured, so the experiment cannot discriminate between OV, IDM ([[treiber-2000-congested]]), cellular automaton or three-phase theories; it only rules out "bottleneck required".

## Relevance to us

The cleanest real-world demonstration that a homogeneous swarm of identical, locally coupled agents can lose stability and self-organise a travelling wave. The ring-road setup is a ready-made benchmark for any swarm controller (see [[stern-2018-dissipation]], [[wu-2022-flow]], [[lee-2025-traffic]]) and for string-stability analyses. The jam speed (about 20 km/h) is a quantitative invariant that a simulated vehicle swarm should reproduce. Broader physics context in [[helbing-2001-traffic]] and [[chowdhury-2000-statistical]].

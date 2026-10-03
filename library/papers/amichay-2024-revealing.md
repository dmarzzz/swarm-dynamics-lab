---
id: amichay-2024-revealing
type: paper
title: "Revealing the mechanism and function underlying pairwise temporal coupling in collective motion"
authors: ["Guy Amichay", "Liang Li", "Máté Nagy", "Iain D. Couzin"]
year: 2024
venue: "Nature Communications"
url: https://www.nature.com/articles/s41467-024-48458-z
doi: "10.1038/s41467-024-48458-z"
arxiv: null
cite: "Amichay, G., Li, L., Nagy, M., & Couzin, I. D. (2024). Revealing the mechanism and function underlying pairwise temporal coupling in collective motion. Nature Communications, 15(1), 4356."
topics: [collective-motion, sync-consensus, collective-decision]
added_by: dmarz/collective-motion-recent
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: "35 (OpenAlex W4398222988, 2026-10-03)"
code: []
---
## Summary

Juvenile zebrafish (24-26 days post fertilisation, about 1 cm long) swim in burst-and-glide bouts. The authors tracked 29 freely swimming pairs (TRex, 100 fps) and found that when close (< 4 cm) and fast (> 6 cm/s) the pair's bursts alternate out of phase with a shared lag. A phase response curve (PRC) measured from the data shows an unresponsive window (neighbour burst within 0.1 s of own burst is ignored) and then a roughly linear response, next bout length T = 2 tau, with tau the delay to the partner's burst (per-pair regression slope 1.71, R^2 = 0.48). Using immersive volumetric virtual reality (VR) with a virtual fish, they show that one-way coupling (open loop, virtual fish beating like a metronome at 240-360 ms) only yields a constant lag of about 0.32 s, not alternation; a closed-loop virtual fish driven by the PRC rule recovers the out-of-phase pattern. Temporal coupling also matters functionally: real fish that were in the specific temporal relation before a 60 degree turn of the virtual partner stayed in proximity more often afterwards (N = 423 vs 144 turn events, p <= 0.002 in 0.5-2 s windows).

## Contribution

Moves the study of collective motion from purely spatial interaction rules (metric, topological, visual) to temporal coupling, and shows experimentally, with a "dynamic social clamp", that reciprocity of interaction is necessary and sufficient for the observed rhythm. It gives a real-world example of a swarmalator-like system where the internal oscillator is speed and is non-isochronous.

## Key results

- Measured: out-of-phase burst alternation in close pairs; KS test vs shuffled pairs p < 0.001.
- Measured: unresponsive window of about 0.1 s after own burst; responsive window up to about 0.4 s with T approx 2 tau.
- Measured (open-loop VR, 74 fish no-turn, 77 fish turn): constant lag 311.8-332.9 ms across virtual-fish periods 240-360 ms, i.e. no alternation under one-way coupling.
- Measured (closed-loop VR, 67 fish): two symmetric correlation peaks like real pairs when the virtual fish follows the PRC rule.
- Measured: out-of-phase pairs swim side by side more often (circular Kuiper test p = 0.001).
- Model claim: a three-rule stochastic oscillator model (unresponsive window, PRC response with probability beta, else draw bout length from the empirical distribution) reproduces both regimes; results robust to beta and PRC slope; noise stabilises alternation.

## Methods and models

Two arenas (30 x 30 cm square, 28.7 cm circular, 0.5 cm water depth). Burst times from speed minima (Savitzky-Golay smoothed). Cross-correlation of Gaussian-cushioned burst trains. VR rig from loopbio (Stowers et al. 2017) with a virtual fish swimming straight paths, burst speed profile v = a t + b for t <= 0.12 s and exp(c t + d) after (a = 0.88, b = 0.188, c = -10.5, d = -0.823). Closed-loop rule: T = 2 tau if 100 ms <= tau <= 400 ms, else random draw from the natural bout distribution. Simulations: 20 realisations of 101,000 steps (step about 0.01 s). Data and code on figshare (10.6084/m9.figshare.c.7123501.v1 and 10.6084/m9.figshare.25398523.v1), MATLAB and Python.

## Limitations and open questions

Pairs only; how temporal coupling scales to schools of tens or hundreds is untested. The space and time parts of the model are not coupled (the simulation has no spatial motion). The analysis needs close, fast swimming; about 25% (open loop) and 14% (closed loop) of VR windows were discarded for VR artefacts. Neural basis of the unresponsive window (sensory suppression during bursts) is hypothesised, not measured.

## Relevance to us

A clean, testable rule for temporal coupling that a swarm simulator can add on top of spatial rules; suggests that synchronised intermittent motion (burst-and-coast) is part of the interaction, not noise. Pairs with [[li-2025-reverse]] (same lab, VR control law), [[de-lamo-2025-data]] (burst-and-coast synchrony emerging in a data-driven model) and the swarmalator line in sync-consensus. Same group's theory: [[heins-2024-collective]], [[salahshour-2025-allocentric]].

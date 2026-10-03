---
id: pastor-2015-experimental
type: paper
title: Experimental proof of faster-is-slower in systems of frictional particles flowing through constrictions
authors:
- José M. Pastor
- Angel Garcimartín
- Paula A. Gago
- Juan P. Peralta
- César Martín-Gómez
- Luis M. Ferrer
- Diego Maza
- Daniel R. Parisi
- Luis A. Pugnaloni
- Iker Zuriguel
year: 2015
venue: Physical Review E
url: https://arxiv.org/abs/1507.05110
doi: 10.1103/physreve.92.062817
arxiv: '1507.05110'
cite: Pastor, J. M., Garcimartín, A., Gago, P. A., Peralta, J. P., Martín-Gómez, C., Ferrer, L. M., Maza, D., Parisi, D. R., Pugnaloni, L. A., & Zuriguel, I. (2015). Experimental proof of faster-is-slower in systems of frictional particles flowing through constrictions. Physical Review E, 92(6), 062817. https://doi.org/10.1103/physreve.92.062817
topics:
- crowds-and-traffic
- active-matter
- collective-motion
- criticality-measurement
added_by: dmarz/crowds-and-traffic-audit
accessed: '2026-10-03'
read_depth: full
relevance: 4
citations: 161 (Crossref is-referenced-by-count, 2026-10-03; OpenAlex budget exhausted)
code: []
---

## Summary

Tests the faster-is-slower (FIS) prediction of [[helbing-2000-simulating]] experimentally in three systems that pass through a narrow door: about 95 people evacuating a room through a 69 cm door at three instructed levels of competitiveness, a herd of about 75 sheep entering a barn through a 94 cm door on warm versus cool days, and 500 glass beads leaving a quasi-2D hopper on a vibrated incline whose angle sets the driving force. In all three, stronger drive raises the mean time lapse between successive passages (lower flow), and the survival function of time lapses has a power-law tail whose exponent falls as drive rises. The granular data show the mechanism: drive speeds up the flowing regime but lengthens clogs.

## Contribution

The first controlled experimental demonstration of faster-is-slower, nearly 15 years after it was predicted in simulation, and the argument that it is a generic property of driven, frictional, discrete flows through constrictions rather than something specific to human "panic". It complements the clogging-transition picture of [[zuriguel-2014-clogging]] (same group) and supplies a benchmark for pedestrian models. Note that the arXiv title ("...in multi-particle systems flowing through bottlenecks") differs from the published PRE title used here.

## Key results

All measured:
- Humans (95 ± 3 participants, 69 cm door, three competitiveness levels, measured approach speeds 0.410 ± 0.071, 0.497 ± 0.077 and 0.717 ± 0.075 m/s): mean time lapse ⟨τ⟩ rises with competitiveness, so the flow rate falls; power-law tail exponents of the survival function P(τ) ~ τ^-α are α = 6.8 ± 1 (low), 5.5 ± 0.8 (medium), 4.2 ± 0.4 (high). Doorpost pressure sensors (128 cells, threshold 3 kg/cm^2) register more high-pressure events with competitiveness.
- Sheep (75 ± 10 animals, 94 cm door; 15 warm days at 25 ± 2 °C versus 20 cool days at 10 ± 5 °C): faster (cool-day) herds have larger ⟨τ⟩; α = 4.5 ± 0.3 (low) and 3.3 ± 0.2 (high).
- Granular hopper (500 beads, outlet three bead diameters, six incline angles): P(τ) has a kink at τ ≈ 0.05 s separating a flowing regime, where larger drive shortens τ (faster-is-faster), from a clogging regime with a power-law tail, where larger drive lengthens τ. Their combination produces the non-monotonic flow-rate curve.
- In all human runs α > 2, so mean flow is well defined; the effect on ⟨τ⟩ in humans is described by the authors as mild while the effect on α is strong.
- Claimed: necessary conditions for FIS are a discrete driven flow, a constriction, frictional contacts that stabilise arches, and an energy input that can break them.

## Methods and models

Time lapses τ_i = t_i − t_{i−1} between successive passages, extracted from spatio-temporal diagrams (one pixel line stacked over video frames, about 0.1 s precision for humans and sheep). Evacuation time T_N = Σ τ_i, flow W = 1/⟨τ⟩. Power-law tails fitted with the Clauset–Shalizi–Newman method; 95% confidence intervals by bootstrapping. Competitiveness quantified by the maximum group speed during initial approach to the door and by doorpost pressure. No model is fitted.

## Limitations and open questions

- Human competitiveness is set by instruction (avoid contact, soft contact, soft pushing), not by real urgency; only three levels, so the full non-monotonic FIS curve (with its minimum) is not resolved in humans or sheep, only the rising branch.
- The sheep manipulation (temperature) is indirect and confounded with other day-to-day variation.
- Later work (for example [[haghani-2024-revisiting]]) debates whether FIS occurs in real evacuations, where people rarely push competitively.

## Relevance to us

A rare cross-system experiment (humans, animals, grains) showing that more individual drive can reduce collective throughput, with a measurable signature (heavy-tailed inter-passage times whose exponent tracks drive). The same analysis applies directly to a robot swarm passing a doorway. Pairs with [[helbing-2000-simulating]] (prediction), [[zuriguel-2014-clogging]] (clogging transition), [[seyfried-2009-new]] (bottleneck flow at normal motivation) and [[poissonnier-2019-experimental]] (ants, which avoid clogging).

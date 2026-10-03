---
id: strogatz-2005-crowd
type: paper
title: Crowd synchrony on the Millennium Bridge
authors: [Steven H. Strogatz, Daniel M. Abrams, Allan McRobie, Bruno Eckhardt, Edward Ott]
year: 2005
venue: Nature
url: https://www.stevenstrogatz.com/articles/crowd-synchrony-on-the-millennium-bridge
doi: 10.1038/438043a
arxiv: null
cite: "Strogatz, S. H., Abrams, D. M., McRobie, A., Eckhardt, B., & Ott, E. (2005). Crowd synchrony on the Millennium Bridge. Nature, 438(7064), 43-44."
topics: [sync-consensus, crowds-and-traffic]
added_by: dmarz/sync-consensus-audit
accessed: 2026-10-03
read_depth: full
relevance: 4
citations: "590 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

A two-page Brief Communication explaining the wobble of London's Millennium Bridge on its opening day. The
authors couple a damped, driven harmonic oscillator for the bridge's lateral mode to a Kuramoto-type
population of pedestrians whose gait phases are nudged by the bridge's motion. Wobbling and crowd synchrony
then appear together, as one instability, once the number of walkers exceeds a critical crowd size N_c, which
they compute analytically. With one fitted sensitivity constant, the model reproduces the timescale and amplitude
of the wobbles seen in a controlled crowd test on the bridge.

## Contribution

The best-known demonstration that Kuramoto-style collective synchronisation, developed for fireflies and neurons
([[kuramoto-1984-chemical]], [[strogatz-2000-kuramoto]]), predicts a quantitative engineering failure in a human
crowd. It frames bridge and crowd as a feedback loop (environment-mediated coupling) rather than a structural
defect, and it is the anchor of the pedestrian-bridge synchronisation literature (later partly disputed, see
Limitations).

## Key results

- Model: M X'' + B X' + K X = G sum_{i=1..N} sin(Theta_i) for bridge displacement X; pedestrians
  dTheta_i/dt = Omega_i + C A sin(Psi - Theta_i + alpha), where A and Psi are the bridge amplitude and phase and
  Omega_i is drawn from a footfall-frequency density P(Omega).
- Analytic threshold (eq. 3, worst case alpha = pi/2 and P symmetric about Omega_0): N_c is proportional to the
  damping ratio zeta = B / (4MK)^(1/2) and inversely proportional to G C P(Omega_0); the PDF text extraction lost
  the Greek symbols, but the visible pieces are consistent with N_c = (4 zeta / pi) sqrt(K M) / (G C P(Omega_0)).
  Check the printed formula before relying on the prefactor.
- Fitted: C of about 16 m^-1 s^-1 from crowd tests on the bridge; with no further free parameters the model gives
  the synchronisation timescale and characteristic wobble amplitude (simulated test with the crowd increased
  stepwise to about 200 people, Fig. 2; wobble amplitude reaches several cm).
- Explains the empirical observation that the crowd's lateral force grows linearly with bridge velocity: the order
  parameter R and amplitude A rise together with a nearly constant ratio. Below N_c, R decays like N^(-1/2).

## Methods and models

Mass-spring-damper modal model of the bridge's resonant lateral mode coupled to N phase oscillators (sinusoidal
pedestrian forcing), Kuramoto order parameter R = |N^-1 sum_j exp(i Theta_j)|, self-consistency analysis
following [[strogatz-2000-kuramoto]] in the Supplementary Information, numerical simulation of the December 2000
diagnostic crowd test on the north span. Main text and figure read; Supplementary Information not read.

## Limitations and open questions

- The pedestrian phase-response equation (2) is hypothetical (the authors say so) and was not measured directly.
- A 2021 Nature Communications paper, "Emergence of the London Millennium Bridge instability without
  synchronisation" (doi 10.1038/s41467-021-27568-y; title seen in search, not opened), argues the instability can arise from
  foot-placement balance control without crowd synchrony, so the mechanism is disputed.
- Single lateral mode, global coupling through the bridge, no spatial crowd structure.

## Relevance to us

A compact example of indirect (environment-mediated) coupling producing synchrony, which is the same structure as
robots coupling through a shared floor, channel or medium. The threshold-crowd-size result is a testable
prediction for any swarm in which individuals respond to a common signal that they themselves drive. Links
sync-consensus to crowds-and-traffic (see [[helbing-2000-simulating]] for crowd dynamics without internal
oscillators) and to [[okeeffe-2017-oscillators]] for oscillators whose coupling depends on space.

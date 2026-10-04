---
id: sarfati-2021-self
type: paper
title: Self-organization in natural swarms of Photinus carolinus synchronous fireflies
authors: [Raphaël Sarfati, Julie C. Hayes, Orit Peleg]
year: 2021
venue: Science Advances
url: https://pmc.ncbi.nlm.nih.gov/articles/PMC8262802/
doi: 10.1126/sciadv.abg9259
arxiv: null
cite: "Sarfati, R., Hayes, J. C., & Peleg, O. (2021). Self-organization in natural swarms of Photinus carolinus synchronous fireflies. Science Advances, 7(28), eabg9259."
topics: [sync-consensus, collective-decision, criticality-measurement]
added_by: dmarz/sync-consensus-audit
accessed: 2026-10-03
read_depth: skim
relevance: 5
citations: "86 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Field study of synchronous fireflies (Photinus carolinus) in the Great Smoky Mountains during peak mating season
in June 2020. Using stereoscopic 360-degree video, the authors reconstruct flashes in 3D over a swarm region about
30 m long, with up to half a million space-time flash coordinates per night. At low density flashes are
uncorrelated; above a density threshold the swarm produces synchronous flashes in periodic bursts. Bursts
nucleate at a location and propagate through the swarm like a relay, which the authors explain by local
line-of-sight interactions shaped by occlusion from terrain and vegetation.

## Contribution

The first spatiotemporal, three-dimensional description of the onset of synchrony in a natural firefly swarm. It
replaces the all-to-all picture behind classic pulse-coupled models ([[mirollo-1990-synchronization]]) with
measured local, environment-dependent visual networks, and reports intermittent (burst) synchrony that standard
models of asymptotic phase locking do not produce.

## Key results

- Density-driven transition (measured): with few active fireflies (3-5 June, early or late at night) collective
  flashing is incoherent; on peak nights the swarm flashes synchronously. The standard deviation of the number of
  flashes per frame scales sublinearly with the mean at low density (random flashes) and linearly above a
  threshold (clustering).
- Rhythm (measured): synchronous flashes about every 0.55 s within bursts lasting about 10 s, bursts repeating
  every ~12 s. The authors note this intermittent synchrony is incompatible with many models of continuous phase
  convergence.
- Propagation (measured): within a burst, flashes spread at a roughly constant speed of about 0.5 m/s; early
  flashes are spatially localised. Early "streaks" move faster than late ones (0.31-0.51 m/s versus 0.19-0.28 m/s
  across peak nights), echoing earlier controlled experiments in which burst leaders flew farther than
  followers; the authors read this motion asymmetry as evidence that some fireflies perceive the swarm's global
  state (their relative delay in the burst), not only their local surroundings.
- Interpretation (claimed, supported by reconstruction of what a single firefly can see): interactions follow a
  line-of-sight network that is peaked at short distance but long-tailed, defined by occlusion from vegetation.

## Methods and models

Two GoPro Fusion 360-degree cameras at 30 fps, 0.9 or 1.8 m apart, calibrated with a moving light; flashes
detected by pixel-intensity thresholding and triangulated in 3D; analysis of flash counts, burst-relative timing
and streak velocities over nights 3-13 June 2020. Read via the PMC open-access version: abstract, results and
discussion; supplementary materials not read. Data or code availability not checked (the PMC page lists
supplementary material only).

## Limitations and open questions

- One species, one site and season; camera field of view captures a cone of the swarm, not the whole swarm.
- The line-of-sight network model is inferred, not directly tested by manipulation.
- Individual identities are not tracked across bursts, so individual phase-response curves are not measured.

## Relevance to us

A real biological dataset showing density-thresholded, burst-mode synchrony with local occluded coupling, which
is close to what an LED-flashing robot swarm with line-of-sight sensors would face. Gives target statistics
(0.55 s period, ~0.5 m/s propagation, density threshold) to compare simulations against. Pairs with
[[werner-allen-2005-firefly]] (engineering), [[okeeffe-2017-oscillators]] (sync plus motion) and the
criticality-measurement topic (density-driven order transition).

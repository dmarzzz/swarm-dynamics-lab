---
id: poissonnier-2019-experimental
type: paper
title: Experimental investigation of ant traffic under crowded conditions
authors:
- Laure-Anne Poissonnier
- Sebastien Motsch
- Jacques Gautrais
- Camille Buhl
- Audrey Dussutour
year: 2019
venue: eLife
url: https://pmc.ncbi.nlm.nih.gov/articles/PMC6805160/
doi: 10.7554/elife.48945
arxiv: null
cite: Poissonnier, L.-A., Motsch, S., Gautrais, J., Buhl, C., & Dussutour, A. (2019). Experimental investigation of ant traffic under crowded conditions. eLife, 8, e48945. https://doi.org/10.7554/elife.48945
topics:
- crowds-and-traffic
- collective-decision
- collective-motion
added_by: dmarz/crowds-and-traffic-audit
accessed: '2026-10-03'
read_depth: full
relevance: 4
citations: 16 (Crossref is-referenced-by-count, 2026-10-03, likely an undercount; OpenAlex budget exhausted)
code: []
---

## Summary

Measures the fundamental diagram of bidirectional ant traffic over the widest density range yet tested. Colonies of Argentine ants (Linepithema humile, 400 to 25,600 workers) were connected to sucrose by bridges 5, 10 or 20 mm wide, and flow and density were counted every second for an hour in 170 experiments (612,000 flow–density pairs). Densities reached 18 ants/cm^2 and occupancy 0.8, yet flow never decreased: it rose linearly up to about 8 ants/cm^2 and then plateaued. Individual tracking of about 7,900 ants shows why: contacts grow linearly with density and each costs a fixed time, but ants move faster at intermediate density (a likely pheromone effect) and refrain from entering crowded bridges.

## Contribution

Direct experimental evidence that a natural collective avoids congestion collapse at occupancies where human and vehicle traffic jam (flow typically falls beyond about 40% occupancy). It replaces the standard concave fundamental diagram (Greenshields, Pipes, Underwood) with a two-phase, jam-free diagram for ants and decomposes it into measurable individual rules. A biological counterpoint to [[sugiyama-2008-traffic]] and [[seyfried-2005-fundamental]].

## Key results

All measured:
- Flow q increases linearly with density k for k < 8 ants/cm^2 and stays constant (does not decline) for k > 8 up to 18 ants/cm^2; a two-phase piecewise-linear function q = k v (k ≤ k_j), q = k_j v (k > k_j) is preferred by Akaike weights over Greenshields, Pipes–Munjal and Underwood functions.
- Flow depends almost only on density, not on the asymmetry between outbound and nestbound streams (response-surface regression R^2 = 0.82, standardised β_density = 0.980, β_asymmetry = 0.026), unlike pedestrian counterflow. No clear lane formation was seen.
- Contacts per crossing C = 0.61 k (R^2 = 0.77); traveling time T = T0 + C ΔT with T0 = 0.95 s and ΔT = 0.24 s per contact (R^2 = 0.55), head-on and rear-end contacts costing the same.
- Contact-free speed v_f rises with density up to k ≈ 5 ants/cm^2 and then decays back, attributed (not shown) to trail pheromone reinforcement.
- A speed model v(k) = L / [T0 + ΔT C(k)] × (α + β k e^{−γk}) with α = 0.812 ± 0.009, β = 0.160 ± 0.010, γ = 0.156 ± 0.007 reproduces the linear-then-plateau flow.
- Observed: ants avoid entering an already crowded bridge, keeping density below the level at which flow would fall (behavioural regulation of inflow).

## Methods and models

35 colonies, starved five days, bridge to 1 M sucrose; one hour video per run; inbound and outbound ants counted in 1 s intervals; density estimated automatically and checked against manual counts. Individual-level data from manual event logging (entry, exit, contacts, U-turns) of ants crossing a 2 cm section 10 min into each experiment. Statistics with GLMMs, nonlinear least squares, Akaike weights, response-surface regression in R.

## Limitations and open questions

- One species with a strong pheromone trail and no competitive pressure; the authors cite other species (fire ants in tunnels) that do jam.
- The pheromone explanation for faster intermediate-density movement is inferred, not tested; inflow regulation is described qualitatively.
- Bridges are short (traffic over 2 cm sections), so long-range wave instabilities like those on a ring road cannot develop.

## Relevance to us

A concrete natural example of a swarm whose local rules prevent the jamming transition that humans and cars hit, with measured per-contact costs and a simple speed–density law we can put into a simulation. Suggests design rules for robot traffic (admission control at entry, constant-cost brief contacts, density-tuned speed) and a test: can a learned or designed swarm controller reproduce a non-decreasing fundamental diagram? Compare [[pastor-2015-experimental]] (sheep and humans that do clog), [[stern-2018-dissipation]] (engineered jam suppression) and [[helbing-2001-traffic]].

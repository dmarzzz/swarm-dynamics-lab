---
id: sridhar-2021-geometry
type: paper
title: "The geometry of decision-making in individuals and collectives"
authors: ["Vivek H. Sridhar", "Liang Li", "Dan Gorbonos", "Máté Nagy", "Bianca R. Schell", "Timothy Sorochkin", "Nir S. Gov", "Iain D. Couzin"]
year: 2021
venue: "Proceedings of the National Academy of Sciences"
url: "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC8685676/fullTextXML"
doi: "10.1073/pnas.2102157118"
arxiv: null
cite: "Sridhar, V. H., Li, L., Gorbonos, D., Nagy, M., Schell, B. R., Sorochkin, T., Gov, N. S., & Couzin, I. D. (2021). The geometry of decision-making in individuals and collectives. Proceedings of the National Academy of Sciences, 118(50), e2102157118. https://doi.org/10.1073/pnas.2102157118"
topics: ["collective-decision", "collective-motion", "criticality-measurement"]
added_by: dmarz/collective-decision
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: "132 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Combines a spin-system model of neural vector integration with virtual-reality experiments on fruit flies, desert locusts and larval zebrafish to study decisions among spatially separated targets made while moving. The model predicts that an animal first moves along the average direction and then, at a critical angular separation, abruptly commits to one target, so that multi-option choices are broken into a sequence of binary bifurcations; the experiments show these bifurcations, and a collective-motion model shows the same geometry at group level.

## Contribution

Shows that embodied movement plus local excitation and global inhibition produce sharp, critical-point-like decisions in space, linking neural ring-attractor dynamics to the compromise-versus-decision transitions known from animal groups ([[couzin-2005-effective]], [[leonard-2012-decision]], [[biro-2006-from]], [[strandburg-peshkin-2015-shared]]). It also shows that the uninformed-individual mechanism of [[couzin-2011-uninformed]] alone cannot reproduce three-option bifurcations.

## Key results

- Model: N spins with H = -(k/N) sum J_ij sigma_i sigma_j, J_ij = cos(pi (|theta_ij| / pi)^nu); velocity proportional to the sum of goal vectors of active spins; Metropolis dynamics. Below a critical neural noise T_c the mean-field model shows a phase transition from averaging to deciding, with a peak in susceptibility near the critical angle.
- Two-choice VR: flies and locusts move along the average direction and then bifurcate; randomisation test P < 0.01 for both. Three-choice: two sequential bifurcations, P < 10^-4 for both species.
- Observed bifurcation angles about 110 degrees (flies) and 90 degrees (locusts), far above visual resolution (about 8 and 2 degrees).
- About 30 per cent of flies and locusts moved directly to a target without the bifurcation pattern, which the authors attribute to individual tuning variation.
- Zebrafish following two or three virtual conspecifics show one and two bifurcations as lateral separation increases; with asymmetric spacing (0.09 m and 0.03 m) the fish treats the close pair as one target.
- Collective model: informed/uninformed mixing explains two-option bifurcations but sends groups to the central target with three options; adding decay of goal-orientedness when moving against one's preference restores sequential bifurcations.

## Methods and models

Neural model adapted from Pinkoviezky, Couzin and Gov (2018) with tuning nu, noise T and agent speed v0; mean-field analysis in SI. Experiments: 60 tethered Drosophila (30 per condition), 156 fifth-instar locusts (122 analysed), 440 zebrafish 24-26 dpf (198 two-target, 39 three-target, 50 asymmetric) in loopbio VR rigs. Bifurcations quantified by fitting y = A |x - x_c|^alpha beyond x_c. Data and code: https://github.com/vivekhsridhar/GODM and Zenodo 10.5281/zenodo.5599711.

## Limitations and open questions

The 'critical' language refers to quasi-phase transitions in finite systems; the fitted exponent alpha is descriptive, not a measured universal exponent. Neural mechanism is inferred from behaviour, not recorded. Collective-level claims rest on simulation, not on group experiments in this paper. Only identical targets are tested experimentally.

## Relevance to us

A direct template for a hackathon experiment on spatial multi-target choice in a moving swarm: the bifurcation geometry is easy to measure from trajectories and the GODM repository gives code and data. It connects collective decision to criticality measures (susceptibility peak) and to motion models. Related: [[leonard-2012-decision]], [[couzin-2005-effective]], [[hartnett-2016-heterogeneous]], [[leonard-2024-fast]].

## Notes from dmarz/collective-decision-audit

Audited 2026-10-03: opened the full text and checked title, authors, year, venue, volume/pages (against Crossref) and every number in Key results against the paper. No errors found; read_depth full is consistent with the methods detail.

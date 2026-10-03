---
id: couzin-2002-collective
type: paper
title: Collective Memory and Spatial Sorting in Animal Groups
authors: [Iain D. Couzin, Jens Krause, Richard James, Graeme D. Ruxton, Nigel R. Franks]
year: 2002
venue: Journal of Theoretical Biology
url: https://jmvidal.cse.sc.edu/library/couzin02a.pdf
doi: 10.1006/jtbi.2002.3065
arxiv: null
cite: Couzin, I. D., Krause, J., James, R., Ruxton, G. D., & Franks, N. R. (2002). Collective memory and spatial sorting in animal groups. Journal of Theoretical Biology, 218(1), 1–11.
topics: [collective-motion, collective-decision]
added_by: dmarz/collective-motion
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: "1902 (Crossref is-referenced-by-count, 2026-10-03); 2161 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

A 3D individual-based model in which each agent responds to neighbours in three nested zones: repulsion
(highest priority), orientation (alignment) and attraction, with a blind cone behind it, a maximum turning
rate and Gaussian angular noise. Varying only the widths of the orientation and attraction zones produces
four collective states: swarm, torus (milling), dynamic parallel group and highly parallel group, with sharp
transitions between them. Sweeping the orientation zone up and then down shows hysteresis ("collective
memory"): the group state depends on its history. Individual differences in speed, turning rate and zone
sizes sort individuals spatially (for example faster individuals move to the front). Read in full from a
PDF copy of the journal article.

## Contribution

The "Couzin zonal model", which made attraction/repulsion/alignment zones the standard biological model of
flocking and schooling (building on [[aoki-1982-simulation]], [[reynolds-1987-flocks]] and
Huth and Wissel (1992, J. Theor. Biol. 156:365-385; not catalogued, full text not reachable)). Unlike [[vicsek-1995-novel]] it produces self-bounded groups in open space and
shows multiple ordered states (including milling) and bistability, which later fish experiments confirmed
([[tunstrom-2013-collective]]).

## Key results

- Four states as functions of Delta r_o = r_o - r_r and Delta r_a = r_a - r_o: swarm (low polarization
  p_group, low angular momentum m_group), torus (low p, high m; appears for small Delta r_o and large
  Delta r_a), dynamic parallel (high p, low m; intermediate Delta r_o), highly parallel (very high p, large
  Delta r_o). Fragmentation region at small zone widths.
- Hysteresis: with r_a = 14, increasing r_o goes swarm -> torus (near r_o ~ 1.5) -> parallel (beyond ~2.5);
  decreasing r_o from the parallel state skips the torus and stays polarized until r_o < 1.5, then returns to
  swarm (15 replicates, 2000 steps per value).
- Torus region shrinks to a small range when the field of perception alpha = 360 deg and grows as alpha
  decreases; below about alpha = 230 deg groups fragment across parameter space.
- Spatial sorting (Spearman rho): speed positively correlated with being at the front; higher turning rate
  and higher error put individuals at the rear; smaller repulsion zone puts individuals nearer the centre
  and front; r_a variation has no effect. Correlations strengthen with inter-individual variance.

## Methods and models

N = 10-100 agents, time step tau = 0.1 s (fish response latency). Desired direction d_r = -sum r_ij/|r_ij|
over zor neighbours; otherwise d_o = sum v_j/|v_j| (zoo) and d_a = sum r_ij/|r_ij| (zoa), averaged if both
are non-empty. Rotate by noise from a spherically wrapped Gaussian (sigma up to 0.2 rad), then turn towards d
by at most theta * tau. Constant speed s (1-5 units/s), r_r = 1, Delta r_o and Delta r_a in 0-15, alpha in
200-360 deg, theta in 10-100 deg/s. Order parameters: polarization p_group = |(1/N) sum v_i| and normalized
angular momentum m_group about the centroid. States measured after convergence (within 5000 steps), 30
replicates per parameter pair.

## Limitations and open questions

- Discrete zones with hard priority (repulsion overrides everything) are a modelling convenience; fish data
  show smoothly varying, speed-mediated interactions and no explicit alignment ([[katz-2011-inferring]],
  [[herbert-read-2011-inferring]]); locusts show no explicit alignment at all ([[sayin-2025-behavioral]]).
- Metric zones, not topological ([[ballerini-2008-interaction]]).
- The authors could not explain a small negative correlation between r_o and frontal position at low
  variance.
- Collective memory was predicted, not observed; [[tunstrom-2013-collective]] later reported multistability
  between milling and polarized states in real fish schools.

## Relevance to us

The canonical model to reproduce for a swarm-dynamics hackathon: it is cheap, has interpretable parameters,
shows a phase diagram with milling and hysteresis, and is the comparison point for learned controllers and
LLM-agent swarms. Polarization and angular momentum are the two order parameters to log. Related:
[[calovi-2014-swarming]] (data-driven phase diagram), [[couzin-2005-effective]] (adds informed individuals).

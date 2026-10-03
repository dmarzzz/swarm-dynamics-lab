---
id: hegselmann-2002-opinion
type: paper
title: "Opinion dynamics and bounded confidence: models, analysis and simulation"
authors: [Rainer Hegselmann, Ulrich Krause]
year: 2002
venue: Journal of Artificial Societies and Social Simulation
url: https://www.jasss.org/5/3/2.html
doi: null
arxiv: null
cite: "Hegselmann, R., & Krause, U. (2002). Opinion dynamics and bounded confidence: Models, analysis and simulation. Journal of Artificial Societies and Social Simulation, 5(3), 2. https://www.jasss.org/5/3/2.html"
topics: [sync-consensus]
added_by: dmarz/sync-consensus-audit
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: null  # no DOI; OpenAlex search budget exhausted on 2026-10-03, count not retrieved
code: []
---

## Summary

Asks when opinion formation in a group ends in consensus, polarisation or fragmentation. The paper puts the
DeGroot averaging model, Friedkin-Johnsen's variant (stubborn agents with "positive degrees"), a time-varying
version and a nonlinear bounded-confidence version into one framework, states the known analytic results for
each, and then explores the bounded-confidence model by simulation. In the bounded-confidence (HK) model every
agent replaces its opinion by the mean of all opinions within distance epsilon of its own, synchronously. With
625 agents and uniform random initial opinions in [0,1], a small confidence level leaves many opinion clusters,
an intermediate one two camps, and a large one consensus.

## Contribution

Introduces what is now called the Hegselmann-Krause (HK) model, the synchronous, all-neighbours-within-epsilon
counterpart of the Deffuant-Weisbuch pairwise model. It turns linear consensus ([[degroot-1974-reaching]]) into
a state-dependent switching network, the same structural move that metric-neighbourhood flocking makes
([[jadbabaie-2003-coordination]], [[vicsek-1995-novel]]), and is the base model of the bounded-confidence
literature surveyed in [[bernardo-2024-bounded]] and [[proskurnikov-2017-tutorial]].

## Key results

- Analytic (Section 3, from Krause 2000 and the Appendix): the dynamics preserves the order of opinions; once two
  agents are split (|x_i - x_j| > epsilon) they stay split forever; consensus requires the profile to stay an
  "epsilon-profile" (adjacent sorted opinions within epsilon) at all times; for n = 2, 3, 4 the initial
  epsilon-profile condition is necessary and sufficient, but not for n = 5, and for n = 6 even an equidistant
  epsilon-profile fails. If consensus happens, it happens in finite time (Result 5); for any initial profile the
  agents split in finite time into subgroups that each reach internal consensus (Result 6).
- Simulated (Section 4.1, symmetric confidence, n = 625 random opinions, single runs): epsilon = 0.01 leaves 38
  opinions, epsilon = 0.15 gives two camps, epsilon = 0.25 gives consensus, all stabilising within 15 steps.
  Sweeping epsilon from 0.01 to 0.4 with 50 runs per value: plurality at small epsilon, polarisation in the
  middle, and an abrupt switch to a single central cluster near epsilon = 0.25; beyond 0.4 the outcome is always
  consensus.
- Regular (equally spaced) start profiles show the mechanism: agents near the edges of the opinion range have
  one-sided neighbourhoods and are pulled inward, which carves out clusters roughly 2 epsilon apart.
- Asymmetric confidence (Section 4.2): biased intervals drive the population toward the favoured side; the
  authors also study opinion-dependent asymmetry.

## Methods and models

x_i(t+1) = |I(i,x)|^(-1) sum_{j in I(i,x)} x_j(t), with I(i,x) = {j : |x_i - x_j| <= epsilon_i} (or the asymmetric
interval [-epsilon_l, +epsilon_r]); opinions scalar in [0,1]; synchronous update. Analytic results via products of
row-stochastic matrices (Appendix). Simulations: 625 agents, random uniform start, 50 repetitions per parameter
point, run until stable. Read: Sections 1-3 and 4.1 in full from the JASSS PDF; 4.2 skimmed.

## Limitations and open questions

- Mostly simulation; general-n convergence and the cluster count as a function of epsilon were open (later work
  proved finite-time convergence and studied the "2 epsilon" cluster rule).
- Synchronous updates, all agents mutually visible, no noise, no network structure beyond the confidence bound.
- Homogeneous epsilon in the main sweep; heterogeneous confidence changes outcomes qualitatively.

## Relevance to us

The cleanest model of state-dependent connectivity: agents only listen to agents "close" to them, exactly as a
robot or drone only hears neighbours within radio range. It is a one-dimensional sandbox for fragmentation
versus consensus thresholds that a hackathon could reproduce in minutes, and the bridge between opinion
dynamics ([[castellano-2009-statistical]], [[bizyaeva-2023-nonlinear]]) and metric-neighbourhood consensus
([[olfati-saber-2007-consensus]], [[motsch-2011-new]], whose heterophilious model generalises HK).

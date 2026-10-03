---
id: mora-2011-biological
type: paper
title: 'Are Biological Systems Poised at Criticality?'
authors: ['Thierry Mora', 'William Bialek']
year: 2011
venue: 'Journal of Statistical Physics'
url: https://arxiv.org/abs/1012.2242
doi: 10.1007/s10955-011-0229-4
arxiv: '1012.2242'
cite: 'Mora, T., & Bialek, W. (2011). Are Biological Systems Poised at Criticality? Journal of Statistical Physics, 144(2), 268–302.'
topics: [criticality-measurement, collective-motion]
added_by: dmarz/criticality-measurement
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: '801 (OpenAlex, 2026-10-03)'
code: []
---

## Summary

Mora and Bialek review the "inverse" statistical-mechanics programme: fit maximum entropy models
(Boltzmann distributions constrained by measured low-order statistics) directly to large biological data sets,
then study the fitted model's thermodynamics. They cover three systems: retinal ganglion cell populations
(pairwise Ising models, N up to 40, extrapolated to 120), protein families (Potts models of sequence
alignments, antibody D regions in zebrafish) and starling flocks. In every case the fitted model sits close
to a critical point: heat capacity peaks sharply at the operating temperature T=1 as N grows, rank-frequency
plots follow Zipf's law, and flock velocity fluctuations are scale-free. They also discuss dynamical
criticality (neuronal avalanches, Hopf bifurcation in hair cells) and argue that these hints point to a
general principle, while flagging that criticality remains a hypothesis.

## Contribution

The paper that framed the modern "criticality hypothesis" for living systems as a data-analysis
question, and that made Zipf's law a formal signature of criticality (entropy exactly linear in energy, S''(E)=0).
It sits between Bak-style self-organised criticality (models with little data) and the later critiques of
Schwab et al. and Morrell et al. that showed the same signatures arise without fine tuning.

## Key results

- Zipf's law P(sigma) ~ 1/rank is equivalent, for large N, to an entropy that is an exactly linear function of energy, S(E)=E/alpha; a heat-capacity divergence at the operating temperature follows (derivation, Sec. II).
- Retina: pairwise maximum entropy models capture about 90% of the multi-information I2/I in salamander retina for N <= 10; heat capacity C(T) peaks increasingly sharply near T=1 as N grows to 40 and in synthetic N=120 networks (re-analysis of earlier data, Fig. 2).
- Antibody repertoire of single zebrafish: a translation-invariant Potts model explains 70-90% of correlations, cuts entropy from about 15 to 9 bits, and predicts Zipf's law that the data then confirm (Fig. 8).
- Flocks: polarization 0.96 +/- 0.03; correlation length of velocity fluctuations scales with flock size and the decay exponent gamma is indistinguishable from zero, for both orientation and speed (reviewing [[cavagna-2010-scale]]).
- Avalanches in cortical cultures: size exponent near -3/2 and branching ratio near 1; the authors note the exponent was later shown to depend on measurement details.

## Methods and models

Maximum entropy: P_m(sigma) = Z^-1 exp(sum_a beta_a O_a(sigma)), with Lagrange multipliers fitted by
gradient ascent on likelihood (beta_a <- beta_a + eta(<O_a>_data - <O_a>_model)), Monte Carlo for the direct
problem. Pairwise constraints give disordered Ising (neurons) or Potts (sequences) models; for flocks, a
Heisenberg-like model of velocity directions. A fictitious temperature rescales all couplings to probe
thermodynamics. Dynamical part: branching process (critical at branching ratio 1) and the normal form of a
Hopf bifurcation dz/dt=(mu+i omega0)z-|z|^2 z+F e^{i omega t}, whose gain r/F ~ F^{-2/3} diverges at mu=0.

## Limitations and open questions

The authors list three challenges: statistical and dynamical notions of criticality use different
mathematics; the inverse problem is hard exactly near criticality; and data are limited (few independent
flock snapshots, unknown sampling biases in sequence databases, intrinsic vs stimulus-driven correlations
in the retina). They give no mechanism for how flocks would tune to criticality. Later work showed Zipf's law
and similar scalings arise generically from latent variables ([[schwab-2014-zipfs]], [[morrell-2021-latent]],
[[ngampruetikorn-2025-extrinsic]]), so the signatures reviewed here are necessary-but-not-sufficient.

## Relevance to us

Foundational review for any hackathon claim that a swarm is "near critical". It gives two
concrete, cheap diagnostics we can compute on simulated or tracked swarms: (1) fit a maximum entropy model and
sweep a fictitious temperature to see whether the heat capacity peaks at T=1; (2) rank-frequency plots of
discretised group states. Read alongside the empirical flock papers [[cavagna-2010-scale]],
[[bialek-2012-statistical]], [[bialek-2014-social]], the broader review [[munoz-2018-colloquium]], and the
skeptical line [[schwab-2014-zipfs]] and [[touboul-2017-power]].

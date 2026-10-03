---
id: ballerini-2008-interaction
type: paper
title: 'Interaction ruling animal collective behavior depends on topological rather than metric distance: Evidence from a field study'
authors: [M. Ballerini, N. Cabibbo, R. Candelier, A. Cavagna, E. Cisbani, I. Giardina, V. Lecomte, A. Orlandi, G. Parisi, A. Procaccini, M. Viale, V. Zdravkovic]
year: 2008
venue: Proceedings of the National Academy of Sciences
url: https://arxiv.org/abs/0709.1916
doi: 10.1073/pnas.0711437105
arxiv: '0709.1916'
cite: Ballerini, M., Cabibbo, N., Candelier, R., Cavagna, A., Cisbani, E., Giardina, I., Lecomte, V., Orlandi, A., Parisi, G., Procaccini, A., et al. (2008). Interaction ruling animal collective behavior depends on topological rather than metric distance - Evidence from a field study. Proceedings of the National Academy of Sciences, 105(4), 1232–1237.
topics: [collective-motion, criticality-measurement]
added_by: dmarz/collective-motion
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: "1860 (Crossref is-referenced-by-count, 2026-10-03); 2009 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

The STARFLAG group reconstructed 3D positions of individual starlings in ten flocks of up to about 2600 birds
over Rome using stereo photography plus a third camera and a trifocal matching algorithm. They measured how
the anisotropy of the n-th nearest neighbour's position decays with n and defined the interaction range as
the n at which the distribution becomes isotropic. Across flocks whose densities differ substantially, the
range is constant in number of neighbours (about 6.5) rather than in metres, so the interaction is
topological. A Vicsek-type simulation with a predator perturbation shows topological flocks stay cohesive
far more often than metric ones.

## Contribution

First large-N, 3D, field measurement that discriminates between metric and topological interaction rules,
and the empirical origin of the "fixed number of nearest neighbours" (k ~ 7) convention now used across
models, robotics and control. Earlier empirical studies covered tens of animals in loose groups; this one is
about two orders of magnitude larger.

## Key results

- Nearest neighbours are strongly depleted along the direction of motion (anisotropic structure); far
  neighbours are isotropic.
- Anisotropy index gamma(n) decays to the isotropic value 1/3 at n_c; average n_c = 6.5 +/- 0.9 (SE), i.e. 6-7
  neighbours.
- Test of metric vs topological: no correlation between n_c^(-1/3) and nearest-neighbour distance r_1
  (n = 10 flocks, R^2 = 0.00021, P = 0.97), but r_c is linear in r_1 (R^2 = 0.78, P = 0.00072). r_1 ranges
  from 0.68 m to 1.51 m across flocks.
- Simulation (2D self-propelled particles, metric vs topological, flat or 1/r vs 1/n weighting): after a
  predator-like perturbation metric flocks most often split into M = 5 pieces; topological flocks most often
  stay whole (M = 1). Weighting shape matters much less than metric vs topological.
- Interpretation (claimed, not measured): the 6-7 limit reflects a cognitive tracking/subitizing limit;
  vision is argued to be the only mechanism consistent with the data.

## Methods and models

Stereo pair with 25 m baseline plus a trifocal camera 2.5 m away, Canon EOS 1D Mk II, 10 fps by interlacing,
birds about 100 m away; nominal relative depth error 0.09 m. Matching on average 88% of birds (never below
80%). About 500 events recorded, about 50 usable, 10 analysed (sharp borders, > 400 birds). Border bias
handled with alpha-shapes and the Hanisch method. The numerical model is the Vicsek-style SPP model with
attraction/repulsion (from [[gregoire-2004-onset]]) modified to interact with a fixed number of neighbours.

## Limitations and open questions

- Only ten flocks; the inference is from static structure (anisotropy), not from dynamics. Later dynamic
  inference ([[bialek-2012-statistical]]) reached the same topological conclusion with n_c ~ 11-12 effective
  neighbours, so the exact number depends on method.
- Density range limited: the densest flocks were excluded because matching failed.
- The cohesion simulation is 2D and the predator is a crude perturbation.
- Topological vs metric is not universal: fish studies find mixed or visual-network rules
  ([[strandburg-peshkin-2013-visual]], [[rosenthal-2015-revealing]]), and [[pearce-2014-role]] proposes a
  projection-based (visual) alternative.

## Relevance to us

If we design neighbour selection for simulated or LLM agents, k-nearest (k ~ 6-7) is the empirically
grounded default and is robust to density swings. Pair with [[cavagna-2010-scale]] (correlations far exceed
the interaction range) and the review [[cavagna-2014-bird]].

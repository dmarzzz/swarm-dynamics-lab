---
id: chen-2025-inconvenient
type: paper
title: The inconvenient truth about flocks
authors: [Leiming Chen, Patrick Jentsch, Chiu Fan Lee, Ananyo Maitra, Sriram Ramaswamy, John Toner]
year: 2025
venue: arXiv preprint (cond-mat.soft)
url: https://arxiv.org/pdf/2503.17064
doi: null
arxiv: '2503.17064'
cite: 'Chen, L., Jentsch, P., Lee, C. F., Maitra, A., Ramaswamy, S., & Toner, J. (2025). The inconvenient truth about flocks. arXiv preprint arXiv:2503.17064.'
topics: [collective-motion, active-matter]
added_by: dmarz/collective-motion-audit
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: "0 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

A re-analysis of the hydrodynamic (Toner-Tu type) theory of two-dimensional polar flocks by six theorists,
including Toner, Ramaswamy and the authors of [[jentsch-2024-new]]. For "Malthusian" flocks (birth and death
make density a fast variable) they derive two exact scaling relations among the roughness, anisotropy and
dynamic exponents, chi - zeta + 1 = 0 and z - zeta - 2 chi - 1 = 0, but argue that no third exact relation
exists, so the exponents themselves cannot be computed exactly. For "immortal" (number-conserving) flocks,
the extra nonlinearities from the density field rule out any exact relation. They conclude that the
published claims of exact 2D exponents, chiefly [[chate-2024-dynamic]] and Ikeda (PRL 133, 258301, 2024),
are incorrect. Read: abstract, introduction, Section II and the summary of arXiv v2 (31 Mar 2025); the
renormalization-group derivations in Sections III-IV were skimmed only.

## Contribution

The main counter-argument in the 2024-2025 dispute over the universality class of the 2D ordered flocking
phase. It does not dispute the numerics of [[mahault-2019-quantitative]] or [[chate-2024-dynamic]]; it
disputes the claim that the exponents follow exactly from symmetry plus non-renormalization. Its central
technical objection is that [[chate-2024-dynamic]] assume the deterministic part of the Goldstone-mode
(angle) dynamics must be a total divergence; Chen et al. argue rotation invariance does not require this.

## Key results

- Malthusian flocks, d = 2: two exact relations, chi - zeta + 1 = 0 and z - zeta - 2chi - 1 = 0 (their
  Eqs. I.4-I.5). The first alone rules out the old Toner 2012 values z = 6/5, zeta = 3/5, chi = -1/5.
  Note (auditor's check): the Chaté-Solon Malthusian values chi = -1/4, zeta = 3/4, z = 5/4 satisfy both
  relations; the dispute is over the third relation that fixes them.
- They argue Malthusian flocks very likely have true long-range order in 2D (chi < 0), and that
  fluctuations along some wavevector directions are smaller than earlier predicted.
- Immortal (Vicsek-class) flocks: no exact scaling relation can be obtained; the evidence for long-range
  order there rests on numerics (they cite [[chate-2020-dry]]).
- The canonical Toner-Tu exponents z = 2(d+1)/5, zeta = (d+1)/5, chi = (3-2d)/5 are wrong in d = 2 but
  hold for incompressible flocks in d >= 3.
- All claims are analytical; the paper contains no new simulations.

## Methods and models

General hydrodynamic equations for polarization p(x,t) and density rho(x,t) built from symmetry
(their Eqs. II.1-II.2: advective lambda_a,b,c terms, U(rho,|p|) p, pressures P1, P2, anisotropic
diffusion mu_B,T,A, birth-death term h(rho,|p|), conserved and non-conserved Gaussian noises), expanded
around the ordered state for the Nambu-Goldstone mode, then dynamic renormalization-group recursion
relations and fixed-point analysis.

## Limitations and open questions

- Preprint (no journal version found on Crossref as of 2026-10-03). The dispute is live: Chaté and Solon
  replied (arXiv 2504.13683, "Comment on 'The inconvenient truth about flocks'"), Chen et al. responded
  (arXiv 2505.21602) and a further round followed (arXiv 2506.13437); none of these replies is catalogued.
- Neither side settles the exponents numerically beyond existing simulations, which agree with
  [[chate-2024-dynamic]] within error bars.

## Relevance to us

Low practical relevance for a hackathon, but essential context before quoting any "exact" 2D flocking
exponent: treat the Vicsek-phase exponents as numerically measured (about chi = -0.31, zeta = 0.95,
z = 1.33 from [[mahault-2019-quantitative]]) rather than theoretically settled. Related: [[toner-1998-flocks]],
[[toner-2005-hydrodynamics]], [[toner-2024-physics]], [[jentsch-2024-new]].

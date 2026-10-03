---
id: koss-2026-mean
type: paper
title: On the Mean-Field Limit of Consensus-Based Methods
authors: [Marvin Koß, Simon Weißmann, Jakob Zech]
year: 2026
venue: Mathematical Methods in the Applied Sciences
url: https://doi.org/10.1002/mma.70343
doi: 10.1002/mma.70343
arxiv: null
cite: Koß, M., Weißmann, S., & Zech, J. (2026). On the mean-field limit of consensus-based methods. Mathematical Methods in the Applied Sciences, 49(5), 4214–4240. https://doi.org/10.1002/mma.70343
topics: [swarm-intelligence, sync-consensus]
added_by: dmarz/swarm-intelligence-audit
accessed: 2026-10-03
read_depth: abstract
relevance: 2
citations: 0 (OpenAlex, 2026-10-03)
code: []
---

## Summary

Studies the mean-field limit of a class of consensus methods that includes both consensus-based optimisation (CBO)
and consensus-based sampling (CBS). Establishes existence of a unique strong solution of the finite-particle SDE
system, uniform-in-N moment estimates, convergence to a Fokker-Planck equation as the number of particles goes to
infinity, and existence and uniqueness of the limiting McKean-Vlasov SDE.

## Contribution

A unified, rigorous mean-field derivation covering CBO and CBS together, building on earlier particle-limit work for
other algorithms. Complements the quantitative rates of [[gerber-2025-mean]]; the abstract does not claim a rate.

## Key results

- Claimed (abstract): well-posedness (unique strong solution) of the finite-particle consensus SDEs; uniform moment
  estimates; mean-field Fokker-Planck limit; well-posedness of the limiting McKean-Vlasov SDE.

## Methods and models

Stochastic analysis of interacting SDEs with Gibbs-weighted mean (and covariance for CBS) coefficients; tightness and
moment arguments. Published online 2025, in the 2026 volume. The open-access PDF (Mannheim repository) was behind a
bot wall during this audit, so only the abstract was read.

## Limitations and open questions

Unread beyond the abstract. Appears qualitative (no convergence rate in the abstract).

## Relevance to us

Background theory only: confirms that the PDE view of CBO/CBS swarms is well founded. See [[gerber-2025-mean]],
[[carrillo-2022-consensus]], [[pinnau-2017-consensus]].

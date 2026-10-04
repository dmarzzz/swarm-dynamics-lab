---
id: ott-2008-low
type: paper
title: Low dimensional behavior of large systems of globally coupled oscillators
authors: [Edward Ott, Thomas M. Antonsen]
year: 2008
venue: "Chaos: An Interdisciplinary Journal of Nonlinear Science"
url: https://arxiv.org/abs/0806.0004
doi: 10.1063/1.2930766
arxiv: '0806.0004'
cite: "Ott, E., & Antonsen, T. M. (2008). Low dimensional behavior of large systems of globally coupled oscillators. Chaos: An Interdisciplinary Journal of Nonlinear Science, 18(3), 037113."
topics: [sync-consensus]
added_by: dmarz/sync-consensus
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "981 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Shows that in the infinite-N limit, certain systems of globally coupled phase oscillators have exactly
low-dimensional macroscopic dynamics: restricting the oscillator density to a special invariant manifold (a
Poisson-kernel form of the Fourier coefficients, now the "Ott-Antonsen ansatz") yields a finite set of ODEs for
the order parameter. For the Kuramoto model with Lorentzian frequencies this gives an exact closed-form solution
of the order parameter's nonlinear time evolution; the method also covers several extensions and time-delayed
coupling.

## Contribution

The main analytic tool of modern Kuramoto theory; it is what makes [[yoon-2022-sync]] and other "solvable
swarmalator" results possible.

## Key results

- Exact reduction of the infinite-dimensional Kuramoto dynamics (Lorentzian frequencies) to one complex ODE for
  the order parameter (abstract).
- Applies to several prototypical extensions and to delayed coupling (abstract).

## Methods and models

Continuum (kinetic) description with a Fourier expansion of the density; invariant-manifold ansatz. Abstract read
on arXiv.

## Limitations and open questions

Requires N to infinity, sinusoidal coupling and (for closed forms) Lorentzian frequency distributions;
attraction of the manifold was addressed in later work by the same authors (cited in [[yoon-2022-sync]] as
Ott and Antonsen 2009).

## Relevance to us

Lets us write down exact mean-field predictions to compare with finite-N swarm simulations; the reduced ODE is
also a cheap surrogate model for control design.

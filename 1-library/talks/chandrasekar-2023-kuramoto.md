---
id: chandrasekar-2023-kuramoto
type: talk
title: "Kuramoto model in the presence of additional asymmetric interactions (Lecture 89)"
authors: [V. K. Chandrasekar]
year: 2023
url: https://www.youtube.com/watch?v=Dv4CZgrqhVM
venue: "Lecture Series in Nonlinear Dynamics, Department of Nonlinear Dynamics, Bharathidasan University; uploaded 4 May 2023, 76 min including Q&A"
topics: [sync-consensus]
added_by: shadow/sol-w6
accessed: 2026-10-03
read_depth: skim
relevance: 2
---

## Summary

Research-seminar talk in two halves: a pedagogical derivation of the Kuramoto model from weakly coupled limit-cycle oscillators, then the speaker's own results on a Kuramoto variant with an added symmetry-breaking coupling term. Read from the auto-generated transcript, which garbles names and some equations (e.g. "Kuramoto" is rendered as "chromota"), so this is a skim and I only record what is unambiguous; no paper is named on the audio and I have not located it. The YouTube description abstract matches the second half. Timestamps approximate.

- 04:33 to 29:14: what phase is, then multiple-scale analysis of a weakly damped and then a weakly nonlinear (van der Pol type) oscillator, showing the slow amplitude and phase equations and the limit-cycle amplitude; a student question clarifies this is the ODE analogue of self-similar PDE analysis.
- 29:14 to 46:35: weakly coupled nonlinear oscillators reduce to phase equations because amplitude deviations are negligible at weak coupling, giving the Kuramoto model (he dates it to 1975 and mentions the 1984 book). Order parameter r, mean-field transformation, Lorentzian frequency distribution with critical coupling K_c = 2 / (pi g(0)), second-order transition with a synchronised cluster growing continuously (42:53). He then reviews explosive (first-order) synchronisation settings: frequency-degree correlated networks and adaptive coupling.
- 46:35 to 62:52: his model. Add to the Kuramoto coupling a second term with coupling constant epsilon_2 that is not invariant under the global phase shift theta_j -> theta_j + Omega t, which is what he means by "asymmetric interaction" breaking rotational symmetry; epsilon_1 is the usual symmetric coupling. Analysed via a mean-field reduction for a Lorentzian distribution (half-width gamma, centre omega_0) using a time-averaged order parameter R. Three states reported: incoherent (R = 0), a standing-wave state with an oscillating order parameter (synchronised cluster plus desynchronised oscillators), and stationary synchrony. Claims: for small epsilon_2 the incoherent-to-standing-wave transition is second order as in the plain model; above a critical epsilon_2 there are bistability regions, a first-order (explosive) transition, and, at larger epsilon_2, suppression of the standing-wave state (51:38 to 58:15). Results stated to hold also for Gaussian frequency distributions. He notes the model reduces to Kuramoto at epsilon_2 = 0 and resembles a Winfree-type model with two sensitivity functions in another limit (60:32).
- Q&A (62:52 onward): clarifications on coupling that depends on the state rather than time, whether a Lagrangian exists for the multistable system (no), and a useful aside that detecting anti-phase synchrony needs the second Daido order parameter mean exp(2 i theta) rather than r.

Measured versus speculated: the phase diagram is from their own analytical plus numerical study; I could not verify the specific critical values from the transcript.

## Relevance to us

Low. The take-away for agent swarms is the general one that breaking the symmetry of a consensus interaction (here, a term that singles out an absolute phase rather than phase differences) turns a smooth onset of coordination into a hysteretic, explosive one with coexisting states. In agent terms: a shared third-party reference (a global clock, a leader signal, a common prompt anchor) added on top of peer-to-peer alignment can make the collective snap between regimes and become path dependent. Background: [[kuramoto-1984-chemical]], [[strogatz-2000-kuramoto]], [[acebron-2005-kuramoto]]; the mean-field derivation here is the same one explained more clearly in [[strogatz-2011-coupled]]. No explosive-synchronisation paper is in the library yet.

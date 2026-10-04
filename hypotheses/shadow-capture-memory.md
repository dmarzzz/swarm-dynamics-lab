---
id: shadow-capture-memory
type: hypothesis
title: Memory length decides whether committed-minority capture reverses after the minority leaves
owner: shadow
agents: [shadow/sol-1]
status: proposed
created: 2026-10-03
surveys: [llm-agent-swarms]
closest_prior: [de-marzo-2026-conformity, magistrali-2026-aligned, hishiki-2026-how, yang-2026-when, flint-2026-group]
topics: [committed-minority, tipping, hysteresis, memory, reversibility]
---

<!-- PROPOSAL ONLY. Not accepted, not run. -->

## Claim

For an opinion pair that sits inside the mean-field metastable region (beta > 1, |h| < h_s) under local
pairwise interaction, the fraction of captured populations that return to the pre-attack state after the
committed minority is removed falls monotonically with agent memory length, from mostly recovering at
memory 1 to mostly persisting at memory 20 or full history.

## Grounding

- [[de-marzo-2026-conformity]]: whole-population observation, no memory. Fits P(m) = [tanh(beta(m + h)) + 1]/2
  per pair, predicts and shows both persistence (pairs inside the spinodal) and relaxation (outside), with
  hysteresis loops in the stubborn fraction.
- [[magistrali-2026-aligned]]: local pairwise encounters, five-slot FIFO memory, one scenario and one dose
  (k = 6 of 12), four seeds. After capture, recovery happens (4/4 replace, 1/4 remove), consistent with a
  single stable fixed point in its benign response curve.
- The two disagree on reversibility, and they differ in exactly two things at once: locality and memory.
  The survey's revised reading (Open problems) is that reversibility is regime-dependent and untested for a
  metastable pair under local, bounded-memory interaction.
- [[hishiki-2026-how]] (abstract): memory length alone moves a spatial LLM swarm between collective regimes,
  which makes memory the natural single manipulated variable.
- Mechanism: with memory L, an agent's effective input after removal is still dominated by remembered
  minority-era encounters for about L interactions; long memory extends the time the population spends past
  the tipping point, which inside the spinodal is enough to stay there.

## Novelty

- [[de-marzo-2026-conformity]]: reversibility vs (beta, h) for memoryless whole-population updates. We fix
  a pair inside their metastable region and vary memory under local interaction. They did not vary memory or
  locality.
- [[magistrali-2026-aligned]]: reversibility with fixed 5-slot memory, pairwise, one benign-regime scenario.
  We sweep memory length and choose a pair known to be metastable. Honest difference: same removal design,
  new manipulated variable and a different regime.
- [[hishiki-2026-how]]: memory as control parameter for cooperation in a spatial Prisoner's Dilemma, no
  committed minority and no removal. We use memory in a tipping and recovery protocol.
- [[yang-2026-when]]: diagnostic separating social coupling from numeric anchoring. Used as a control here;
  no paper in the library applies it to tipping (survey Gap 2), so the control is also a small contribution.
- [[flint-2026-group]]: committed minorities in the naming game, deterministic above N_c, no removal-by-memory
  sweep.

## Prediction

If true: recovery fraction (populations back within the benign band 50 rounds after removal) decreases
monotonically with memory L in {1, 5, 20, full}, with at least a 50-point drop from L = 1 to L = full, and
time-to-recovery among recovering runs grows with L. A pair outside the spinodal recovers at every L.

If false: recovery fraction is flat in L (within CIs), so the [[magistrali-2026-aligned]] versus
[[de-marzo-2026-conformity]] contrast is driven by locality or the coordination-game framing, not memory.
Or the inside-spinodal pair persists at every L, meaning local interaction alone does not rescue it.

## Minimal experiment

- Pre-step (half day): fit (beta, h) with the [[de-marzo-2026-conformity]] protocol for one open model on
  about 20 candidate pairs; pick one pair clearly inside the spinodal and one clearly outside.
- Population: N = 24, random pairwise encounters on a complete graph, each agent sees its last L encounter
  outcomes (L in {1, 5, 20, full}). One open model, fixed temperature.
- Phases: 20 rounds benign entrench; replace k agents with committed agents at k = 1.5 x the measured tipping
  dose; run to capture or 60 rounds; remove the committed agents; run 80 rounds.
- Controls: randomised initial conditions and label-swap of the two opinions ([[yang-2026-when]]); a
  no-attack arm at each L to measure intrinsic drift; the outside-spinodal pair as a regime control.
- Seeds: 10 per (pair, L), so 2 x 4 x 10 = 80 populations plus 8 no-attack arms. About 80 x 24 x 160
  encounters, roughly 300K short calls. A small open model on a hosted endpoint, about a day. Pilot at
  L in {1, full} with 3 seeds first.
- Endpoints fixed in advance: benign band = mean of no-attack runs +- 2 SD; recovery = inside band for
  10 consecutive rounds within 50 rounds of removal.

## Kill criteria

- Pre-step finds no pair inside the spinodal for the chosen model: park, or switch to a model where
  [[de-marzo-2026-conformity]] reports one (Gemma 3 27B).
- Capture does not occur at the chosen dose in at least 70% of attack runs: the removal question cannot be
  asked; re-dose once, then park.
- Recovery fraction flat in L (L = 1 and L = full CIs overlap with less than a 20-point gap): claim refuted.
- The randomised-initial-condition control shows the endpoint is set by the label prior rather than the
  minority: the result is a prior artefact; report it as such and drop the claim.

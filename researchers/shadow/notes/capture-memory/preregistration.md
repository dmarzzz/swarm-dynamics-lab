# Pre-registration draft: capture-memory (S0/S1 only)

This is the pre-registration that would be committed before an S2 if the hypothesis
[shadow-capture-memory (PR 82)](https://github.com/dmarzzz/swarm-lab/pull/82) is accepted. Until then it
documents what was fixed before the scripted S1 ran. There is no S2 in this coordinator. Sections follow
vishesh's design guide (`researchers/vishesh/notes/seo-poisoning/experimental-design.md`, Experimental design
sections 0 to 8) and the template in `templates/experiment-worker/preregistration.md`.

## 1. Hypotheses, with directions

- **H1 (capture check).** In W1_INSIDE at dose 0.42 the committed minority captures (honest fraction on the
  attack label at least 0.75 for 3 consecutive rounds) most populations at every bounded memory length.
- **H2 (primary).** Among populations captured at both memory lengths, the fraction of honest agents back on
  the original convention 50 rounds after perfect removal (`frac_original_T`) is LOWER at memory 20 than at
  memory 1, under A1_purge. Direction: memory 20 minus memory 1 is negative.
- **H3 (bridge).** A2_purge_wipe recovers more than A1_purge at every memory length, and the gap grows with
  memory. We report the size rather than predicting it.
- **H4 (regime control).** In W2_OUTSIDE, A1_purge recovers at every memory length.

Kill criterion for the hunch: if the memory 20 minus memory 1 difference under A1_purge in W1_INSIDE is zero
or positive with a CI excluding a 0.20 drop, memory length does not govern reversibility in this model, and
the de-marzo versus magistrali contrast must be explained by something else (locality, framing, or the
coordination payoff).

## 2. Contrasts declared in advance

- **Primary:** `design.yaml -> primary_contrast`. Stage S1, world W1_INSIDE, dose 0.42, arm A1_purge, metric
  `frac_original_T`, memory 20 minus memory 1, paired per task x seed, restricted to episodes captured under
  both memory lengths (capture is decided before removal, so this restriction cannot depend on the arm).
- **Secondary:** `recovered` (10 consecutive rounds at or above 0.75 within 50 rounds) and `half_time`
  (first round after removal at or above 0.5) in the same cell.
- **Bridge:** A2_purge_wipe minus A1_purge on `frac_original_T`, per memory length.
- Everything else (dose 0.5, memory 5 and full, W2_OUTSIDE, A0_no_purge) is exploratory and labelled so.

## 3. Minimum meaningful effect

- Minimum meaningful drop: memory 20 minus memory 1 at or below -0.20 on `frac_original_T`.
- Clean-world non-inferiority: in S0 (W0_CLEAN) every memory length keeps `frac_original_T` above 0.8 and
  the three arms are identical (nothing to remove).
- Capture floor: at least 70% of W1_INSIDE episodes captured at each bounded memory, else the removal question
  cannot be asked at that memory (same rule as the hypothesis file's kill criteria).

## 4. Sample size from S1

S1 (100 dev tasks x 2 seeds per cell) gives the per-task standard deviation of the paired difference. The
scripted S1 numbers are in `results/S1.md` after the run; the sample size for an S2 is written here only once a
model backend has been qualified, because the scripted policy's variance says nothing about an LLM's.

## 5. Units and metrics, with denominators

- **Unit of assignment:** the task x seed draw (matching schedule plus one uniform per agent per round).
  Every arm and every memory length run on the same draw.
- **Unit of analysis:** the episode (one arm, one memory, one draw). **Cluster:** the task. Seeds within a
  task share the task's word pair and parity.
- **Metrics** (per episode; honest agents only; rounds counted from the removal round):
  - `captured`: honest fraction on the attack label at least `capture_frac` = 0.75 for `capture_streak` = 3
    consecutive rounds during takeover (then takeover stops and removal happens).
  - `capture_latency`: rounds from the start of takeover to capture.
  - `frac_original_T`: honest fraction on the original convention at round `eval_round` = 50 after removal.
  - `recovered`: at or above `recover_frac` = 0.75 for `recover_streak` = 10 consecutive rounds within the
    first 50 rounds after removal.
  - `recovery_round`: first round of that streak. `half_time`: first round at or above 0.5.
  - `entrench_frac_original`, `frac_original_at_removal`, `frac_original_end`: diagnostics.
- Rates are over all valid episodes of the cell unless marked "captured", which restricts to captured episodes.

## 6. Failure and retry policy (identical across arms)

An episode whose policy raises is recorded with `validity.ok = false`, counted per arm (`invalid` in the CSV),
and never retried or dropped. A hub run that fails stays failed; its cells are re-queued only with a dated
amendment here.

## 7. Agent-population validity checks

The scripted policy is not an LLM, so the design guide's unawareness probe does not apply. For a model
backend the pre-step is: fit (beta, h) per word pair with the de-marzo-2026-conformity protocol, pick one pair
inside and one outside the spinodal, and record the randomised-label diagnostic (yang-2026-when): if recovery
depends on which word is the original (task parity) rather than on the arm, the result is a prior artefact.
In the scripted model h is set in cfg and parity only changes the word strings, so the diagnostic is trivially
flat; it is kept in the design so the model run inherits it.

## 8. Seeds and splits

- Dev tasks 0 to 199 (S0 uses 0 to 49, S1 uses 0 to 99). Holdout tasks 1000 to 1999, never touched before an
  accepted S2.
- Seeds: S0 [1], S1 [1, 2]. Fixed in `design.yaml` before any run.
- Fixed design constants: N = 24, beta = 2.5, h_inside = 0.1 (h_s(2.5) = 0.362, inside), h_outside = 0.5
  (outside), entrench 20 rounds, takeover cap 100 rounds, recovery 80 rounds. beta and h were chosen from the
  mean-field fixed-point map of the tanh rule over a binomial memory of length L (see README, "Why these
  constants") before any simulation of the removal phase was looked at per memory length. Dose 0.42 = 10 of 24
  is about 1.5x the mean-field tipping fraction at memory 1 for this pair; 0.5 = 12 of 24 is a second dose.

## 9. What we may claim

A scripted S1 result is a property of the tanh-over-memory rule, not a finding about LLM agents. What it can
show is whether, under the simplest model that has both the de-marzo response curve and the magistrali FIFO
memory, memory length alone moves a captured population between return and persistence after perfect
removal, and whether a memory wipe closes that gap. It says nothing about detection, quarantine, selective
repair, shared stores or returning children: those are vishesh's immune-response lane.

## Amendments

None.
